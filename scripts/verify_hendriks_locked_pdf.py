#!/usr/bin/env python3
"""Verify the Hendriks 35-pair reconstruction against exact locked PDF bytes.

The verifier uses text extracted from the acquired institutional PDF.  It is
strict: every reconstructed Table B9 row must find both taxa and both displayed
numeric values within the Table B9 region, and every island species must occur in
its declared Appendix-A source-table region.  Incomplete extraction or any
unmatched row keeps provenance admission closed rather than guessing.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path
from typing import Iterable

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PDF = ROOT / "artifacts/hendriks_2019/source_lock/hendriks_2019_vuw_thesis.pdf"
DEFAULT_LOCK = ROOT / "artifacts/hendriks_2019/source_lock/source_lock.json"
DEFAULT_PAIRS = ROOT / "data/source_tables/hendriks_2019_flower_area_table_b9_reconstructed.csv"
DEFAULT_MAPPING = ROOT / "data/source_tables/hendriks_2019_flower_area_island_mapping.csv"
DEFAULT_OUTPUT = ROOT / "artifacts/hendriks_2019/source_lock/pdf_reverification.json"
EXPECTED_N = 35


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = value.replace("\u00ad", "").replace("–", "-").replace("—", "-")
    # pypdf can retain a visual line-break as "novae- zelandiae".  Treat only
    # whitespace immediately adjacent to an existing hyphen as layout noise;
    # this does not alter ordinary taxon spelling.
    value = re.sub(r"-\s+", "-", value)
    value = re.sub(r"\s+-", "-", value)
    value = re.sub(r"\s+", " ", value)
    return value.casefold().strip()


def numeric_variants(value: str) -> set[str]:
    number = float(value)
    variants = {value.strip(), f"{number:g}"}
    variants.add(f"{number:.10f}".rstrip("0").rstrip("."))
    return {item for item in variants if item}


def extract_pdf_text(path: Path) -> tuple[str, int]:
    reader = PdfReader(str(path))
    pages = [(page.extract_text() or "") for page in reader.pages]
    return "\n".join(pages), len(pages)


def table_header_positions(normalized: str, label: str) -> list[int]:
    """Return all explicit table-header positions, including possible TOC copies."""
    patterns = [
        # Appendix A is extracted as both "Table A4" and "TableA4" depending
        # on page/layout, so the inter-token whitespace must be optional.
        rf"\btable\s*{re.escape(label.casefold())}\b",
        rf"\b{re.escape(label.casefold())}\s*:\s*",
    ]
    return sorted({match.start() for pattern in patterns for match in re.finditer(pattern, normalized)})


def table_region(text: str, label: str, next_label: str | None = None) -> str:
    normalized = normalize_text(text)
    starts = table_header_positions(normalized, label)
    if not starts:
        return ""

    # Thesis tables are named once in the table of contents and again at the
    # actual appendix/table.  The last explicit occurrence is therefore the
    # data-bearing occurrence; using the first occurrence silently selects TOC
    # text for Appendix A tables.
    start = starts[-1]
    if next_label:
        later_next = [
            position
            for position in table_header_positions(normalized, next_label)
            if position > start
        ]
        if later_next:
            return normalized[start : later_next[0]]

    return normalized[start : start + 50000]


def contains_taxon(region: str, taxon: str) -> bool:
    normalized_taxon = normalize_text(taxon)
    if normalized_taxon in region:
        return True
    tokens = [re.escape(token) for token in normalized_taxon.split()]
    if not tokens:
        return False
    return re.search(r"\s+".join(tokens), region) is not None


def contains_numeric(region: str, value: str) -> bool:
    for variant in numeric_variants(value):
        if re.search(rf"(?<![0-9.]){re.escape(variant)}(?![0-9.])", region):
            return True
    return False


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def verify_b9(text: str, rows: Iterable[dict[str, str]]) -> dict[str, object]:
    region = table_region(text, "B9", "B10")
    results = []
    for row in rows:
        checks = {
            "island_species": contains_taxon(region, row["island_species"]),
            "island_flower_area_cm2": contains_numeric(region, row["island_flower_area_cm2"]),
            "mainland_relative": contains_taxon(region, row["mainland_relative"]),
            "mainland_flower_area_cm2": contains_numeric(region, row["mainland_flower_area_cm2"]),
        }
        results.append(
            {
                "pair_id": int(row["pair_id"]),
                "checks": checks,
                "verified": all(checks.values()),
            }
        )
    return {
        "table_region_found": bool(region),
        "n_rows": len(results),
        "n_verified": sum(bool(row["verified"]) for row in results),
        "all_rows_verified": len(results) == EXPECTED_N and all(bool(row["verified"]) for row in results),
        "rows": results,
    }


def appendix_next_label(label: str) -> str | None:
    match = re.fullmatch(r"A(\d+)", label.upper())
    if not match:
        return None
    return f"A{int(match.group(1)) + 1}"


def verify_appendix_mapping(text: str, rows: Iterable[dict[str, str]]) -> dict[str, object]:
    cache: dict[str, str] = {}
    results = []
    for row in rows:
        label = row["appendix_source_table"].upper().strip()
        if label not in cache:
            cache[label] = table_region(text, label, appendix_next_label(label))
        region = cache[label]
        found = bool(region) and contains_taxon(region, row["island_species"])
        results.append(
            {
                "pair_id": int(row["pair_id"]),
                "island_species": row["island_species"],
                "island_group": row["island_group"],
                "appendix_source_table": label,
                "table_region_found": bool(region),
                "species_verified_in_declared_table": found,
            }
        )
    return {
        "n_rows": len(results),
        "n_verified": sum(bool(row["species_verified_in_declared_table"]) for row in results),
        "all_rows_verified": len(results) == EXPECTED_N
        and all(bool(row["species_verified_in_declared_table"]) for row in results),
        "rows": results,
    }


def verify_lock(pdf_path: Path, lock_path: Path) -> dict[str, object]:
    data = pdf_path.read_bytes()
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    sha256 = hashlib.sha256(data).hexdigest()
    expected = str(lock.get("checksums", {}).get("sha256") or "")
    return {
        "pdf_magic_valid": data.startswith(b"%PDF-"),
        "sha256": sha256,
        "matches_source_lock_sha256": bool(expected) and sha256 == expected,
        "source_lock_status": lock.get("status"),
    }


def build_report(pdf_path: Path, lock_path: Path, pairs_path: Path, mapping_path: Path) -> dict[str, object]:
    pair_rows = read_csv(pairs_path)
    mapping_rows = read_csv(mapping_path)
    if len(pair_rows) != EXPECTED_N or len(mapping_rows) != EXPECTED_N:
        raise ValueError("checked pair and mapping tables must each contain 35 rows")

    text, n_pages = extract_pdf_text(pdf_path)
    identity_text = normalize_text(text[:30000])
    identity = {
        "title_found": "the island rule and its application to multiple plant traits" in identity_text,
        "author_found": "annemieke" in identity_text and "hendriks" in identity_text,
        "n_pdf_pages": n_pages,
    }
    lock = verify_lock(pdf_path, lock_path)
    b9 = verify_b9(text, pair_rows)
    appendix = verify_appendix_mapping(text, mapping_rows)
    complete = (
        identity["title_found"]
        and identity["author_found"]
        and lock["pdf_magic_valid"]
        and lock["matches_source_lock_sha256"]
        and b9["all_rows_verified"]
        and appendix["all_rows_verified"]
    )
    return {
        "schema_version": "1.0",
        "status": "locked_pdf_reverification_complete" if complete else "locked_pdf_reverification_incomplete",
        "identity": identity,
        "source_lock": lock,
        "table_b9": b9,
        "appendix_a_mapping": appendix,
        "all_35_pairs_verified_against_locked_bytes": b9["all_rows_verified"],
        "all_35_island_assignments_verified_against_locked_bytes": appendix["all_rows_verified"],
        "provenance_gate_opened": complete,
        "eiv_gate_opened": False,
        "formal_cross_system_admission_opened": False,
        "claim_boundary": (
            "A complete result verifies provenance/transcription only. It does not estimate measurement reliability, "
            "resolve EIV, or by itself admit Hendriks to a formal cross-system model."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--lock", type=Path, default=DEFAULT_LOCK)
    parser.add_argument("--pairs", type=Path, default=DEFAULT_PAIRS)
    parser.add_argument("--mapping", type=Path, default=DEFAULT_MAPPING)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    report = build_report(args.pdf, args.lock, args.pairs, args.mapping)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(args.output)
    if not report["provenance_gate_opened"]:
        raise SystemExit("locked PDF recovered but strict 35-pair/island re-verification is incomplete")


if __name__ == "__main__":
    main()
