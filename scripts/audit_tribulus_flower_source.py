#!/usr/bin/env python3
"""Audit the source-native Tribulus flower CSV before quantitative analysis.

The audit is deliberately source descriptive. It records headers, row counts,
missingness, distinct low-cardinality values, numeric ranges, and candidate
columns suggested only by their literal source names. It does not decide that a
column means island/continent, population, petal length, or environmental
exposure unless the source header itself supports that reading.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


ROLE_PATTERNS = {
    "island_continent": ("island", "continent", "insular", "habitat", "origin", "region"),
    "petal_length": ("petal", "flower", "corolla"),
    "population": ("population", "locality", "location", "site", "island_name", "country"),
    "specimen": ("specimen", "catalog", "barcode", "individual", "plant", "record"),
    "latitude": ("lat", "latitude"),
    "longitude": ("lon", "long", "longitude"),
    "environment": ("bio", "temp", "precip", "clim", "elev", "aridity", "rain"),
}


def norm(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value or "").strip().casefold()).strip("_")


def finite(value: object) -> float | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def load_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = list(reader.fieldnames or [])
        rows = [dict(row) for row in reader]
    if not headers:
        raise ValueError("Tribulus flower CSV has no header")
    if not rows:
        raise ValueError("Tribulus flower CSV has no data rows")
    return headers, rows


def role_matches(headers: Iterable[str]) -> dict[str, list[str]]:
    output: dict[str, list[str]] = {}
    normalized = [(header, norm(header)) for header in headers]
    for role, patterns in ROLE_PATTERNS.items():
        output[role] = [
            header
            for header, key in normalized
            if any(pattern in key for pattern in patterns)
        ]
    return output


def column_summary(header: str, rows: list[dict[str, str]]) -> dict[str, Any]:
    values = [str(row.get(header) or "").strip() for row in rows]
    present = [value for value in values if value]
    numeric = [number for value in present if (number := finite(value)) is not None]
    counts = Counter(present)
    distinct = len(counts)
    record: dict[str, Any] = {
        "header": header,
        "normalized_header": norm(header),
        "n_rows": len(rows),
        "n_present": len(present),
        "n_missing": len(rows) - len(present),
        "n_distinct": distinct,
        "numeric_fraction_present": len(numeric) / len(present) if present else 0.0,
    }
    if numeric:
        record.update(
            {
                "numeric_min": min(numeric),
                "numeric_max": max(numeric),
                "numeric_mean": sum(numeric) / len(numeric),
            }
        )
    if distinct <= 30:
        record["distinct_value_counts"] = dict(
            sorted(counts.items(), key=lambda item: (-item[1], item[0].casefold()))
        )
    else:
        record["top_value_counts"] = dict(counts.most_common(20))
    return record


def find_source_file(input_dir: Path, filename: str) -> Path:
    candidates = sorted(input_dir.rglob(filename))
    if len(candidates) != 1:
        raise ValueError(
            f"expected exactly one {filename!r} under {input_dir}, found {len(candidates)}"
        )
    return candidates[0]


def audit(path: Path) -> dict[str, Any]:
    headers, rows = load_rows(path)
    summaries = [column_summary(header, rows) for header in headers]
    roles = role_matches(headers)
    return {
        "schema_version": "1.0",
        "status": "tribulus_flower_source_schema_audited",
        "source_filename": path.name,
        "n_rows": len(rows),
        "n_columns": len(headers),
        "headers": headers,
        "literal_header_role_candidates": roles,
        "columns": summaries,
        "analysis_admitted": False,
        "next_gate": (
            "Inspect README and source headers together, then write an explicit source-specific mapping for "
            "island/continent status, petal-length response, geographic grouping, independent specimen or plant unit, "
            "and any environmental covariates. Do not choose columns from statistical convenience."
        ),
        "claim_boundary": (
            "This schema audit is not a biological effect. Low-cardinality strings are not automatically island/continent labels, "
            "numeric columns are not automatically traits, and repeated flowers/specimens cannot be treated as independent populations."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=Path("artifacts/tribulus_dryad"))
    parser.add_argument(
        "--filename", default="Tribulus_flower_data_clean.csv"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/tribulus_dryad/flower_schema_audit.json"),
    )
    args = parser.parse_args()
    source = find_source_file(args.input_dir, args.filename)
    result = audit(source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"rows={result['n_rows']} columns={result['n_columns']}")
    print(args.output)


if __name__ == "__main__":
    main()
