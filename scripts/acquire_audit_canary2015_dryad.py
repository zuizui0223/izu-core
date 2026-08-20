from __future__ import annotations

import csv
import hashlib
import html
import json
import math
import re
import urllib.error
import urllib.request
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/abm_v6_canary_site_source_gate_v1.json"
OUT = ROOT / "data/results/canary2015_dryad_site_source_audit.json"
RAW_DIR = ROOT / "data/external/canary2015"
LANDING = "https://datadryad.org/dataset/doi%3A10.5061/dryad.76173"
USER_AGENT = "izu-core-source-audit/1.0"
EXPECTED_SITE_FILES = [
    "Site1_WesternSahara1.csv",
    "Site2_WesternSahara2.csv",
    "Site3_Fuerteventura1.csv",
    "Site4_Fuerteventura2.csv",
    "Site5_GranCanaria1.csv",
    "Site6_GranCanaria2.csv",
    "Site7_TenerifeSouth1.csv",
    "Site8_TenerifeSouth2.csv",
    "Site9_TenerifeTeno1.csv",
    "Site10_TenerifeTeno2.csv",
    "Site11_Gomera1.csv",
    "Site12_Gomera2.csv",
    "Site13_Hierro1.csv",
    "Site14_Hierro2.csv",
]
DISTANCE_FILE = "Distance_between_sites_Dryad.csv"


def fetch_bytes(url: str) -> tuple[int | None, bytes | None, str | None]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            return int(response.status), response.read(), None
    except urllib.error.HTTPError as exc:
        return int(exc.code), None, str(exc)
    except Exception as exc:  # network layer must be recorded, not converted to biology
        return None, None, f"{type(exc).__name__}: {exc}"


def extract_file_links(page: str) -> dict[str, str]:
    anchors = re.findall(
        r'href=["\']([^"\']*/downloads/file_stream/\d+)["\'][^>]*>(.*?)</a>',
        page,
        flags=re.IGNORECASE | re.DOTALL,
    )
    links: dict[str, str] = {}
    for href, label_html in anchors:
        label = re.sub(r"<[^>]+>", "", label_html)
        label = " ".join(html.unescape(label).split())
        if href.startswith("/"):
            href = "https://datadryad.org" + href
        links[label] = href
    return links


def decode_csv(payload: bytes, filename: str) -> str:
    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return payload.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"could not decode {filename}")


def audit_matrix(payload: bytes, filename: str) -> dict:
    text = decode_csv(payload, filename)
    rows = list(csv.reader(StringIO(text)))
    if len(rows) < 2 or len(rows[0]) < 2:
        raise RuntimeError(f"{filename}: matrix too small")
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise RuntimeError(f"{filename}: ragged CSV")

    numeric_cells = 0
    negative_cells = 0
    nonfinite_cells = 0
    for row_index, row in enumerate(rows[1:], start=2):
        if not str(row[0]).strip():
            raise RuntimeError(f"{filename}: blank pollinator identity at row {row_index}")
        for column_index, raw in enumerate(row[1:], start=2):
            cell = str(raw).strip()
            if cell == "":
                raise RuntimeError(f"{filename}: blank matrix value at row {row_index}, column {column_index}")
            try:
                value = float(cell)
            except ValueError as exc:
                raise RuntimeError(
                    f"{filename}: non-numeric matrix value at row {row_index}, column {column_index}"
                ) from exc
            numeric_cells += 1
            if not math.isfinite(value):
                nonfinite_cells += 1
            if value < 0:
                negative_cells += 1
    if numeric_cells == 0 or negative_cells or nonfinite_cells:
        raise RuntimeError(
            f"{filename}: invalid quantitative matrix; numeric={numeric_cells}, negative={negative_cells}, nonfinite={nonfinite_cells}"
        )
    if any(not str(name).strip() for name in rows[0][1:]):
        raise RuntimeError(f"{filename}: blank plant identity in header")

    return {
        "matrix_rows_including_header": len(rows),
        "matrix_columns_including_row_label": width,
        "pollinator_rows": len(rows) - 1,
        "plant_columns": width - 1,
        "numeric_cells": numeric_cells,
        "quantitative_nonnegative_schema": True,
        "target_metrics_calculated": False,
    }


def write(payload: dict) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def main() -> None:
    design = json.loads(DESIGN.read_text())
    status, page_bytes, page_error = fetch_bytes(LANDING)
    if status != 200 or page_bytes is None:
        write({
            "schema_version": "1.0",
            "analysis": "canary2015_dryad_site_source_audit",
            "status": "blocked_dryad_landing_page_not_recovered",
            "landing_http_status": status,
            "landing_error": page_error,
            "source_admission_succeeds": False,
            "target_metrics_calculated": False,
            "claim_boundary": "Source transport failure is not biological evidence.",
        })
        return

    page_text = page_bytes.decode("utf-8", errors="replace")
    links = extract_file_links(page_text)
    required = EXPECTED_SITE_FILES + [DISTANCE_FILE]
    missing_links = [name for name in required if name not in links]
    if missing_links:
        write({
            "schema_version": "1.0",
            "analysis": "canary2015_dryad_site_source_audit",
            "status": "blocked_exact_dryad_file_links_not_resolved",
            "landing_http_status": status,
            "landing_bytes": len(page_bytes),
            "landing_sha256": hashlib.sha256(page_bytes).hexdigest(),
            "resolved_labels": sorted(links),
            "missing_required_files": missing_links,
            "source_admission_succeeds": False,
            "target_metrics_calculated": False,
            "claim_boundary": "No filename substitution or inferred Dryad path is allowed.",
        })
        return

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    records = []
    blocked = []
    for filename in required:
        file_status, payload, error = fetch_bytes(links[filename])
        record = {
            "name": filename,
            "download_url": links[filename],
            "http_status": file_status,
            "error": error,
        }
        if file_status != 200 or payload is None:
            blocked.append(filename)
            records.append(record)
            continue
        path = RAW_DIR / filename
        path.write_bytes(payload)
        record.update({
            "bytes": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
        })
        if filename in EXPECTED_SITE_FILES:
            try:
                record["schema_audit"] = audit_matrix(payload, filename)
            except Exception as exc:
                record["schema_error"] = f"{type(exc).__name__}: {exc}"
                blocked.append(filename)
        else:
            record["role"] = "source distance audit only; not a target or network selection input"
            record["target_metrics_calculated"] = False
        records.append(record)

    admitted_site_records = [
        row for row in records
        if row["name"] in EXPECTED_SITE_FILES
        and row.get("http_status") == 200
        and row.get("schema_audit", {}).get("quantitative_nonnegative_schema") is True
    ]
    admission = len(admitted_site_records) == 14 and not blocked
    write({
        "schema_version": "1.0",
        "analysis": "canary2015_dryad_site_source_audit",
        "status": (
            "source_admitted_fourteen_site_level_quantitative_matrices"
            if admission else "blocked_canary_site_source_bytes_or_schema_incomplete"
        ),
        "dryad_doi": design["candidate_system"]["dryad_doi"],
        "landing_url": LANDING,
        "landing_bytes": len(page_bytes),
        "landing_sha256": hashlib.sha256(page_bytes).hexdigest(),
        "expected_site_network_count": 14,
        "admitted_site_network_count": len(admitted_site_records),
        "expected_site_files": EXPECTED_SITE_FILES,
        "blocked_files": sorted(set(blocked)),
        "files": records,
        "source_admission_succeeds": admission,
        "target_metrics_calculated": False,
        "independence_boundary": design["independence_boundary"],
        "claim_boundary": "This audit establishes source bytes and matrix schema only. It does not validate or falsify ABM v6 and does not calculate Shannon or plant niche overlap.",
    })


if __name__ == "__main__":
    main()
