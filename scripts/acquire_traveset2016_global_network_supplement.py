from __future__ import annotations

import argparse
import json
import re
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

DOI = "10.1111/geb.12362"
SUPPLEMENT_URL = (
    "https://onlinelibrary.wiley.com/action/downloadSupplement?"
    "doi=10.1111%2Fgeb.12362&file=geb12362-sup-0001-si.docx"
)
WEB_OF_LIFE_METADATA_URL = "https://www.web-of-life.es/get_network_info.php"

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def clean_text(x: str) -> str:
    return re.sub(r"\s+", " ", x).strip()


def cell_text(cell: ET.Element) -> str:
    return clean_text(" ".join(t.text or "" for t in cell.findall(".//w:t", NS)))


def parse_docx_tables(path: Path) -> list[list[list[str]]]:
    with zipfile.ZipFile(path) as zf:
        xml = zf.read("word/document.xml")
    root = ET.fromstring(xml)
    tables: list[list[list[str]]] = []
    for table in root.findall(".//w:tbl", NS):
        rows: list[list[str]] = []
        for tr in table.findall("./w:tr", NS):
            rows.append([cell_text(tc) for tc in tr.findall("./w:tc", NS)])
        if rows:
            tables.append(rows)
    return tables


def score_table(rows: list[list[str]], keywords: tuple[str, ...]) -> int:
    text = " ".join(" ".join(row) for row in rows[:5]).lower()
    return sum(k.lower() in text for k in keywords)


def classify_tables(tables: list[list[list[str]]]) -> dict:
    specs = {
        "network_inventory": ("location", "archipelago", "latitude", "sampling"),
        "oceanic_island_traits": ("area", "age", "elevation", "isolation"),
        "network_metrics": ("species", "interaction", "connectance", "nested"),
    }
    out: dict[str, dict] = {}
    used: set[int] = set()
    for name, keys in specs.items():
        ranked = sorted(
            ((score_table(rows, keys), i, rows) for i, rows in enumerate(tables) if i not in used),
            reverse=True,
            key=lambda x: x[0],
        )
        if ranked and ranked[0][0] >= 2:
            score, i, rows = ranked[0]
            used.add(i)
            out[name] = {"table_index": i, "keyword_score": score, "rows": rows}
    return out


def retrieve(url: str, out: Path, timeout: int = 45) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "izu-core-source-audit/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
            content_type = r.headers.get("Content-Type", "")
            final_url = r.geturl()
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {"status": "blocked_source_retrieval", "error": repr(exc), "url": url}

    if not data.startswith(b"PK"):
        return {
            "status": "invalid_payload",
            "url": url,
            "final_url": final_url,
            "content_type": content_type,
            "bytes": len(data),
        }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    return {
        "status": "retrieved",
        "url": url,
        "final_url": final_url,
        "content_type": content_type,
        "bytes": len(data),
        "path": str(out),
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--url", default=SUPPLEMENT_URL)
    p.add_argument("--raw", type=Path, default=Path("data/external/traveset2016/geb12362-sup-0001-si.docx"))
    p.add_argument("--out", type=Path, default=Path("data/results/traveset2016_global_network_supplement_gate.json"))
    args = p.parse_args()

    gate = {
        "source": "Traveset et al. 2016",
        "doi": DOI,
        "supplement_url": args.url,
        "purpose": "recover Tables S1-S3 for island-level held-out ABM reconstruction",
        "fallback_registry": {
            "web_of_life_metadata_api": WEB_OF_LIFE_METADATA_URL,
            "status": "candidate_source_for_original_network_matrices_and_metadata_only",
            "non_substitution_rule": "Do not choose a new set of 18 oceanic islands from Web of Life. Traveset Table S1 membership must be source-locked before exact 2016 reconstruction; otherwise build a separately preregistered new global sample."
        }
    }
    retrieval = retrieve(args.url, args.raw)
    gate["retrieval"] = retrieval

    if retrieval["status"] == "retrieved":
        try:
            tables = parse_docx_tables(args.raw)
            classified = classify_tables(tables)
            gate["parse"] = {
                "status": "parsed",
                "n_tables": len(tables),
                "classified": classified,
                "full_tables": tables,
            }
            required = {"network_inventory", "oceanic_island_traits", "network_metrics"}
            gate["admission"] = {
                "required_tables_found": required.issubset(classified),
                "status": "ready_for_schema_mapping" if required.issubset(classified) else "manual_table_mapping_required",
            }
        except Exception as exc:
            gate["parse"] = {"status": "parse_failed", "error": repr(exc)}
            gate["admission"] = {"required_tables_found": False, "status": "blocked_parse"}
    else:
        gate["admission"] = {
            "required_tables_found": False,
            "status": "blocked_source_retrieval",
            "next_route": "search source-locked mirrors / author repositories for Table S1-S3 membership; use Web of Life only after network IDs are linked, or preregister a new global sample rather than back-selecting 18 networks"
        }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(gate, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
