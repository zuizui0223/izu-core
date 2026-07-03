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
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

HERE = Path(__file__).parent
QUEUE = HERE / "evidence_screening" / "known_source_upgrade_queue.csv"
OUT = HERE / "evidence_screening" / "openalex_source_access.csv"
DOI_PATTERN = re.compile(r"10\.\d{4,9}/[-._;()/:a-z0-9]+", flags=re.I)
FIELDS = (
    "source_id", "taxon", "doi", "query_url", "retrieved_at_utc", "retrieval_status",
    "http_status", "openalex_id", "display_name", "publication_year", "is_oa", "oa_status",
    "best_oa_pdf_url", "best_oa_landing_url", "host_venue", "source_queue_status", "boundary",
)
BOUNDARY = (
    "OpenAlex metadata is a discovery and access-routing record only. "
    "It does not verify article contents, sampling design, trait values or taxonomy."
)


def doi_from_reference(reference: str) -> str:
    match = DOI_PATTERN.search(reference or "")
    return match.group(0).lower().rstrip(".,;:)]}") if match else ""


def url_for_doi(doi: str) -> str:
    return "https://api.openalex.org/works/https://doi.org/" + doi


def fetch(url: str) -> tuple[dict, int]:
    request = Request(url, headers={"User-Agent": "izu-meta-analysis-source-recovery/1.1"})
    with urlopen(request, timeout=45) as response:  # nosec B310: fixed HTTPS API
        return json.load(response), int(response.status)


def blank(base: dict[str, str], status: str, http_status: object = "") -> dict[str, str]:
    return {
        **base, "retrieval_status": status, "http_status": str(http_status), "openalex_id": "",
        "display_name": "", "publication_year": "", "is_oa": "", "oa_status": "",
        "best_oa_pdf_url": "", "best_oa_landing_url": "", "host_venue": "",
    }


def main() -> None:
    rows: list[dict[str, str]] = []
    with QUEUE.open(encoding="utf-8", newline="") as handle:
        sources = list(csv.DictReader(handle))
    for source in sources:
        doi = doi_from_reference(source.get("source_reference", ""))
        url = url_for_doi(doi) if doi else ""
        timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        base = {
            "source_id": source["source_id"], "taxon": source["taxon"], "doi": doi,
            "query_url": url, "retrieved_at_utc": timestamp,
            "source_queue_status": source["status"], "boundary": BOUNDARY,
        }
        if not doi:
            rows.append(blank(base, "missing_doi"))
            continue
        try:
            record, status = fetch(url)
            oa = record.get("open_access") or {}
            location = record.get("best_oa_location") or {}
            source_info = (record.get("primary_location") or {}).get("source") or {}
            rows.append({
                **base, "retrieval_status": "retrieved", "http_status": str(status),
                "openalex_id": str(record.get("id", "")), "display_name": str(record.get("display_name", "")),
                "publication_year": str(record.get("publication_year", "")), "is_oa": str(oa.get("is_oa", "")),
                "oa_status": str(oa.get("oa_status", "")), "best_oa_pdf_url": str(location.get("pdf_url", "")),
                "best_oa_landing_url": str(location.get("landing_page_url", "")), "host_venue": str(source_info.get("display_name", "")),
            })
        except HTTPError as error:
            rows.append(blank(base, f"error:HTTPError:{error.code}", error.code))
        except URLError as error:
            rows.append(blank(base, f"error:URLError:{error.reason}"))
        time.sleep(0.5)
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(rows)
    print(f"wrote {len(rows)} source-access rows to {OUT}")


if __name__ == "__main__":
    main()
