#!/usr/bin/env python3
"""Screen a recovered Hetherington-Rauth thesis for source-table/data routes.

The screen is discovery-only. It extracts searchable PDF text page by page,
identifies Supplemental Table A.2 explicitly, and distinguishes the pair-identity
table from a source-native numeric floral-measurement table. It never infers or
transcribes a numeric 136-pair effect.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PDF = ROOT / "artifacts/hetherington_2019/source_lock/hetherington_rauth_2019_thesis.pdf"
DEFAULT_OUTPUT = ROOT / "artifacts/hetherington_2019/source_lock/source_table_screen.json"
TERMS = (
    "136",
    "appendix",
    "supplementary",
    "data availability",
    "data are available",
    "island-mainland",
    "island mainland",
    "sister",
    "flower size",
    "floral trait",
    "corolla",
    "petal",
    "table",
)
A2_START_PATTERNS = (
    "supplemental table a.2",
    "supplemental table a. 2",
    "table a. 2 island-mainland pairs of taxa",
    "table a.2 island-mainland pairs of taxa",
)
A2_END_PATTERNS = (
    "literature cited in table a.2",
    "literature cited in table a. 2",
)
A2_EXPECTED_COLUMNS = (
    "family",
    "endemic island taxa",
    "mainland sister taxa",
    "data source",
    "reference",
)
NUMERIC_TRAIT_COLUMN_TERMS = (
    "flower size",
    "floral size",
    "trait value",
    "island flower",
    "mainland flower",
    "radius (mm",
    "tube length",
    "diameter (mm",
    "log ratio",
)
A2_HEADER_WINDOW_CHARS = 1800


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.casefold()).strip()


def extract_links(text: str) -> list[str]:
    links = set(re.findall(r"https?://[^\s<>\]\)]+", text))
    dois = set(re.findall(r"10\.\d{4,9}/[-._;()/:a-z0-9]+", text, flags=re.I))
    return sorted(links | {"https://doi.org/" + doi.rstrip(".,;:") for doi in dois})


def audit_supplemental_a2(page_texts: list[str]) -> dict[str, object]:
    normalized = [normalize(text) for text in page_texts]
    start = next(
        (
            index
            for index, text in enumerate(normalized)
            if any(pattern in text for pattern in A2_START_PATTERNS)
        ),
        None,
    )
    if start is None:
        return {
            "found": False,
            "pair_identity_table_verified": False,
            "numeric_flower_size_columns_found": False,
        }
    end = next(
        (
            index
            for index in range(start + 1, len(normalized))
            if any(pattern in normalized[index] for pattern in A2_END_PATTERNS)
        ),
        len(normalized),
    )
    region = " ".join(normalized[start:end])
    # Column identity is read from the opening table page/header only. Searching
    # the whole A.2 region for terms such as "flower size" can match cited paper
    # titles and falsely promote a reference phrase into a numeric source column.
    header_region = normalized[start][:A2_HEADER_WINDOW_CHARS]
    columns = {column: column in header_region for column in A2_EXPECTED_COLUMNS}
    numeric_terms = [
        term for term in NUMERIC_TRAIT_COLUMN_TERMS if term in header_region
    ]
    return {
        "found": True,
        "pdf_page_start": start + 1,
        "pdf_page_end_exclusive": end + 1,
        "declared_title": "Island-mainland pairs of taxa",
        "declared_sorting": "island, family, genus",
        "expected_identity_columns": columns,
        "pair_identity_table_verified": all(columns.values()),
        "numeric_column_detection_scope": "opening A.2 table header page/window only; reference titles excluded",
        "numeric_trait_column_terms_checked": list(NUMERIC_TRAIT_COLUMN_TERMS),
        "numeric_trait_column_terms_found": numeric_terms,
        "numeric_flower_size_columns_found": bool(numeric_terms),
        "interpretation": (
            "Supplemental Table A.2 is a pair-identity/provenance table. Its declared columns identify family, endemic island taxa, mainland sister taxa, data source, and reference. "
            "No source-native flower-size/log-ratio measurement column is verified in this table."
        ),
    }


def screen_pages(pdf_path: Path) -> dict[str, object]:
    reader = PdfReader(str(pdf_path))
    page_texts = [(page.extract_text() or "") for page in reader.pages]
    hits = []
    all_links: set[str] = set()
    for page_number, raw in enumerate(page_texts, start=1):
        text = normalize(raw)
        matched = [term for term in TERMS if term in text]
        links = extract_links(raw)
        all_links.update(links)
        keep = (
            len(matched) >= 2
            or "data availability" in matched
            or "data are available" in matched
            or "appendix" in matched
        )
        if keep:
            hits.append(
                {
                    "page": page_number,
                    "matched_terms": matched,
                    "links": links,
                    "text_excerpt": re.sub(r"\s+", " ", raw).strip()[:1800],
                }
            )
    a2 = audit_supplemental_a2(page_texts)
    return {
        "schema_version": "1.2",
        "status": "thesis_source_table_screen_complete",
        "n_pages": len(reader.pages),
        "candidate_pages": hits,
        "all_extracted_links": sorted(all_links),
        "supplemental_table_a2": a2,
        "source_native_pair_identity_table_verified": bool(a2.get("pair_identity_table_verified")),
        "source_native_136_pair_numeric_flower_size_table_verified": False,
        "third_response_shape_admitted": False,
        "claim_boundary": (
            "The thesis verifies a source-native island-mainland pair-identity table, but that table does not expose a verified numeric flower-size/log-ratio column. Keyword/page screening and pair identities do not authorize numeric effect reconstruction."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = screen_pages(args.pdf)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
