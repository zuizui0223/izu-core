#!/usr/bin/env python3
"""Screen a recovered Hetherington-Rauth thesis for source-table/data routes.

The screen is discovery-only. It extracts searchable PDF text page by page and
reports pages containing prespecified appendix/data/pair-table vocabulary plus
URLs/DOIs. It never infers or transcribes a numeric 136-pair effect.
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


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.casefold()).strip()


def extract_links(text: str) -> list[str]:
    links = set(re.findall(r"https?://[^\s<>\]\)]+", text))
    dois = set(re.findall(r"10\.\d{4,9}/[-._;()/:a-z0-9]+", text, flags=re.I))
    return sorted(links | {"https://doi.org/" + doi.rstrip(".,;:") for doi in dois})


def screen_pages(pdf_path: Path) -> dict[str, object]:
    reader = PdfReader(str(pdf_path))
    hits = []
    all_links: set[str] = set()
    for page_number, page in enumerate(reader.pages, start=1):
        raw = page.extract_text() or ""
        text = normalize(raw)
        matched = [term for term in TERMS if term in text]
        links = extract_links(raw)
        all_links.update(links)
        # Preserve only pages with multiple relevant signals, or explicit data/appendix wording.
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
    return {
        "schema_version": "1.0",
        "status": "thesis_source_table_screen_complete",
        "n_pages": len(reader.pages),
        "candidate_pages": hits,
        "all_extracted_links": sorted(all_links),
        "source_native_136_pair_table_verified": False,
        "third_response_shape_admitted": False,
        "claim_boundary": (
            "Keyword/page screening identifies where source-native data may reside. It does not establish that a 136-pair "
            "table exists, verify trait columns/units, or authorize numeric effect reconstruction."
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
