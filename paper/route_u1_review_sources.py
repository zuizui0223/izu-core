"""Route DOI-bearing U1 source-review candidates through OpenAlex access metadata.

This script does not download manuscripts. It records only source-level access
routes so that original tables/figures can be inspected through legal OA,
repository, author, or institutional-library channels. A missing OA route is
not evidence that a work is unavailable elsewhere.

Usage:
    python paper/route_u1_review_sources.py \
        --queue artifacts/u0_snapshot/crossref_batch_001/u1_crossref_review_queue.csv \
        --out artifacts/u0_snapshot/crossref_batch_001/u1_source_access_routes.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

API = "https://api.openalex.org/works/https://doi.org/"
USER_AGENT = "izu-core-source-routing/1.0 (systematic evidence screening)"
FIELDS = (
    "review_rank", "review_priority", "recommended_synthesis_role", "u0_accepted_key", "accepted_name",
    "title", "year", "doi", "source_url", "retrieved_at_utc", "openalex_lookup_url", "retrieval_status",
    "is_oa", "oa_status", "best_oa_pdf_url", "best_oa_landing_url", "primary_location_landing_url",
    "repository_or_host", "next_action", "notes",
)


def request_json(url: str, attempts: int = 4) -> dict:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        request = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(request, timeout=45) as response:  # nosec B310 fixed HTTPS OpenAlex endpoint
                return json.load(response)
        except HTTPError as error:
            last_error = error
            if error.code not in (429, 500, 502, 503, 504) or attempt == attempts:
                raise
        except URLError as error:
            last_error = error
            if attempt == attempts:
                raise
        time.sleep(attempt)
    assert last_error is not None
    raise last_error


def openalex_url(doi: str) -> str:
    return API + quote(doi, safe="")


def route(payload: dict) -> dict[str, str]:
    open_access = payload.get("open_access") or {}
    best = payload.get("best_oa_location") or {}
    primary = payload.get("primary_location") or {}
    source = best.get("source") or primary.get("source") or {}
    is_oa = bool(open_access.get("is_oa"))
    pdf = str(best.get("pdf_url") or "")
    landing = str(best.get("landing_page_url") or "")
    primary_landing = str(primary.get("landing_page_url") or "")
    host = str(source.get("display_name") or "")
    if pdf:
        action = "inspect_OA_PDF_for_population_units_and_extractable_tables"
    elif landing:
        action = "inspect_OA_landing_or_repository_for_full_text"
    elif is_oa:
        action = "inspect_OpenAlex_locations_for_OA_copy"
    else:
        action = "library_or_author_route; retain DOI and do_not_infer_unavailability"
    return {
        "is_oa": "yes" if is_oa else "no",
        "oa_status": str(open_access.get("oa_status") or ""),
        "best_oa_pdf_url": pdf, "best_oa_landing_url": landing,
        "primary_location_landing_url": primary_landing, "repository_or_host": host,
        "next_action": action,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--max-sources", type=int, default=120)
    parser.add_argument("--sleep-seconds", type=float, default=0.15)
    args = parser.parse_args()

    with args.queue.open(encoding="utf-8", newline="") as handle:
        queue = [row for row in csv.DictReader(handle) if row.get("doi")][: args.max_sources]
    rows: list[dict[str, str]] = []
    for candidate in queue:
        doi = candidate["doi"].strip().lower()
        stamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        url = openalex_url(doi)
        row = {field: candidate.get(field, "") for field in FIELDS if field in candidate}
        row.update({
            "retrieved_at_utc": stamp, "openalex_lookup_url": url, "retrieval_status": "",
            "is_oa": "", "oa_status": "", "best_oa_pdf_url": "", "best_oa_landing_url": "",
            "primary_location_landing_url": "", "repository_or_host": "", "next_action": "", "notes": "",
        })
        try:
            payload = request_json(url)
            row.update(route(payload))
            row["retrieval_status"] = "retrieved"
        except HTTPError as error:
            row.update({"retrieval_status": f"error:HTTPError:{error.code}", "next_action": "retry_or_check_DOI_format", "notes": "No access inference from failed lookup."})
        except URLError as error:
            row.update({"retrieval_status": "error:URLError", "next_action": "retry_lookup", "notes": str(error.reason)})
        rows.append(row)
        time.sleep(args.sleep_seconds)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(rows)
    summary = {
        "sources_routed": len(rows), "lookup_errors": sum(row["retrieval_status"].startswith("error:") for row in rows),
        "oa_pdf_routes": sum(bool(row["best_oa_pdf_url"]) for row in rows),
        "oa_landing_routes": sum(bool(row["best_oa_landing_url"]) for row in rows),
        "library_or_author_routes": sum(row["next_action"].startswith("library_or_author") for row in rows),
        "boundary": "Access routing does not establish content, study eligibility, or a numeric effect size.",
    }
    args.out.with_suffix(".summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
