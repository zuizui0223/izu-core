"""Audit OA access routes for DOI-tagged Izu evidence-recovery targets.

This is an access-discovery step. An OA link is not treated as a verified source
transcription until the original article, its taxonomic units and its tables or
figures are reviewed.
"""
from __future__ import annotations

import csv
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

HERE = Path(__file__).parent
QUEUE = HERE / "evidence_screening" / "known_source_upgrade_queue.csv"
OUT = HERE / "evidence_screening" / "openalex_source_access.csv"
DOI_PATTERN = re.compile(r"10\.\d{4,9}/[-._;()/:a-z0-9]+", flags=re.I)
FIELDS = (
    "source_id", "taxon", "doi", "retrieved_at_utc", "retrieval_status",
    "openalex_id", "display_name", "publication_year", "is_oa", "oa_status",
    "best_oa_pdf_url", "best_oa_landing_url", "host_venue", "source_queue_status",
    "boundary",
)
BOUNDARY = (
    "OpenAlex metadata is a discovery and access-routing record only. "
    "It does not verify article contents, sampling design, trait values or taxonomy."
)


def doi_from_reference(reference: str) -> str:
    match = DOI_PATTERN.search(reference or "")
    return match.group(0).lower() if match else ""


def fetch(doi: str) -> dict:
    url = "https://api.openalex.org/works/https://doi.org/" + quote(doi, safe="")
    request = Request(url, headers={"User-Agent": "izu-meta-analysis-source-recovery/1.0"})
    with urlopen(request, timeout=45) as response:  # nosec B310: fixed HTTPS API
        return json.load(response)


def main() -> None:
    rows: list[dict[str, str]] = []
    with QUEUE.open(encoding="utf-8", newline="") as handle:
        sources = list(csv.DictReader(handle))
    for source in sources:
        doi = doi_from_reference(source.get("source_reference", ""))
        timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        base = {
            "source_id": source["source_id"], "taxon": source["taxon"], "doi": doi,
            "retrieved_at_utc": timestamp, "source_queue_status": source["status"],
            "boundary": BOUNDARY,
        }
        if not doi:
            rows.append({**base, "retrieval_status": "missing_doi", "openalex_id": "", "display_name": "", "publication_year": "", "is_oa": "", "oa_status": "", "best_oa_pdf_url": "", "best_oa_landing_url": "", "host_venue": ""})
            continue
        try:
            record = fetch(doi)
            oa = record.get("open_access") or {}
            location = record.get("best_oa_location") or {}
            source_info = (record.get("primary_location") or {}).get("source") or {}
            rows.append({
                **base,
                "retrieval_status": "retrieved",
                "openalex_id": record.get("id", ""),
                "display_name": record.get("display_name", ""),
                "publication_year": record.get("publication_year", ""),
                "is_oa": oa.get("is_oa", ""),
                "oa_status": oa.get("oa_status", ""),
                "best_oa_pdf_url": location.get("pdf_url", ""),
                "best_oa_landing_url": location.get("landing_page_url", ""),
                "host_venue": source_info.get("display_name", ""),
            })
        except Exception as error:
            rows.append({**base, "retrieval_status": f"error:{type(error).__name__}", "openalex_id": "", "display_name": "", "publication_year": "", "is_oa": "", "oa_status": "", "best_oa_pdf_url": "", "best_oa_landing_url": "", "host_venue": ""})
        time.sleep(0.4)
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(rows)
    print(f"wrote {len(rows)} source-access rows to {OUT}")


if __name__ == "__main__":
    main()
