from __future__ import annotations

import json
import re
from pathlib import Path

import acquire_audit_martinique_2025_v9_source as source_gate

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/results/martinique_2025_author_r_reconstruction_semantics.json"
R_SOURCES = {
    "Motifs.R": "https://search-data.ubfc.fr/dl_data.php?file=594",
    "Interaction_turnover.R": "https://search-data.ubfc.fr/dl_data.php?file=589",
}
TOKENS = (
    "num_sp",
    "insects_plants",
    "insects-plants",
    "plant_best_id",
    "insect_best_id",
    "group_by",
    "summarise",
    "summarize",
    "count(",
    "xtabs",
    "table(",
    "pivot_wider",
    "spread(",
    "interaction",
    "period",
    "site",
)


def decode(payload: bytes) -> tuple[str, str]:
    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return payload.decode(encoding), encoding
        except UnicodeDecodeError:
            pass
    raise RuntimeError("R source could not be decoded")


def structural_matches(text: str) -> list[dict]:
    lines = text.splitlines()
    hit_indices = set()
    for index, line in enumerate(lines):
        lower = line.lower()
        if any(token in lower for token in TOKENS):
            for j in range(max(0, index - 2), min(len(lines), index + 3)):
                hit_indices.add(j)
    return [
        {"line": index + 1, "text": lines[index][:1000]}
        for index in sorted(hit_indices)
    ]


def num_sp_use_class(matches: list[dict]) -> dict:
    num_lines = [row for row in matches if "num_sp" in row["text"].lower()]
    assignment_like = []
    aggregation_like = []
    filter_like = []
    for row in num_lines:
        lower = row["text"].lower()
        if any(token in lower for token in ("sum(", "summarise", "summarize", "weight", "freq", "abundance", "count")):
            aggregation_like.append(row)
        if any(token in lower for token in ("filter(", "subset(", "[", "==", "!=", "%in%")):
            filter_like.append(row)
        if "<-" in row["text"] or "=" in row["text"]:
            assignment_like.append(row)
    return {
        "num_sp_reference_count": len(num_lines),
        "num_sp_reference_lines": num_lines,
        "aggregation_like_num_sp_lines": aggregation_like,
        "filter_like_num_sp_lines": filter_like,
        "assignment_like_num_sp_lines": assignment_like,
        "interpretation_boundary": (
            "This is lexical source-code structure only. A Num_sp weight rule is not inferred unless author code explicitly uses Num_sp in aggregation."
        ),
    }


def main() -> None:
    files = []
    blocked = []
    for name, url in R_SOURCES.items():
        status, payload, error = source_gate.fetch(url)
        row = {"name": name, "url": url, "http_status": status, "error": error}
        if status != 200 or payload is None:
            blocked.append(name)
            files.append(row)
            continue
        text, encoding = decode(payload)
        matches = structural_matches(text)
        row.update({
            "bytes": len(payload),
            "sha256": source_gate.sha256(payload),
            "encoding": encoding,
            "line_count": len(text.splitlines()),
            "structural_matches": matches,
            "num_sp_use": num_sp_use_class(matches),
        })
        files.append(row)

    output = {
        "schema_version": "1.0",
        "analysis": "martinique_2025_author_r_reconstruction_semantics_audit",
        "files": files,
        "blocked_files": blocked,
        "all_r_sources_recovered": not blocked,
        "target_metrics_calculated": False,
        "network_outcomes_inspected": False,
        "claim_boundary": (
            "Only author R source lines relevant to raw interaction reconstruction are inventoried. No ecological network result, target value, model coefficient, or v9 prediction is calculated or interpreted."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({
        "blocked_files": blocked,
        "files": [
            {
                "name": row["name"],
                "http_status": row.get("http_status"),
                "sha256": row.get("sha256"),
                "num_sp_use": row.get("num_sp_use"),
                "structural_matches": row.get("structural_matches", []),
            }
            for row in files
        ],
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
