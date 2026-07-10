"""Route the predeclared priority source queue through all OpenAlex locations."""
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

from channel_id.priority_source_access import summarize_openalex

API = "https://api.openalex.org/works/https://doi.org/"
USER_AGENT = "izu-core-priority-source-routing/1.0 (systematic evidence synthesis)"
FIELDS = (
    "priority", "source_id", "doi", "taxon", "current_status", "blocking_item",
    "retrieved_at_utc", "retrieval_status", "openalex_lookup_url", "openalex_id",
    "title", "publication_year", "is_oa", "oa_status", "best_oa_pdf_url",
    "best_oa_landing_url", "best_oa_source", "access_class", "next_action",
    "location_count", "oa_pdf_location_count", "oa_landing_location_count",
    "all_locations_json", "boundary",
)


def request_json(url: str, attempts: int = 4) -> dict:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        request = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(request, timeout=60) as response:  # nosec B310 fixed HTTPS API
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--sleep-seconds", type=float, default=0.2)
    args = parser.parse_args()
    if args.sleep_seconds < 0:
        raise SystemExit("sleep-seconds must be nonnegative")

    with args.queue.open(encoding="utf-8", newline="") as handle:
        queue = [row for row in csv.DictReader(handle) if str(row.get("doi") or "").strip()]
    output: list[dict[str, str]] = []
    for candidate in queue:
        doi = str(candidate["doi"]).strip().lower()
        lookup = API + quote(doi, safe="")
        stamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        row = {field: "" for field in FIELDS}
        for field in ("priority", "source_id", "doi", "taxon", "current_status", "blocking_item"):
            row[field] = str(candidate.get(field) or "").strip()
        row.update({
            "retrieved_at_utc": stamp,
            "retrieval_status": "",
            "openalex_lookup_url": lookup,
            "boundary": "Access metadata is not source content, study eligibility, or a trait effect.",
        })
        try:
            payload = request_json(lookup)
            row.update(summarize_openalex(payload))
            row["retrieval_status"] = "retrieved"
        except HTTPError as error:
            row.update({
                "retrieval_status": f"error:HTTPError:{error.code}",
                "access_class": "lookup_error",
                "next_action": "retry_or_verify_DOI",
            })
        except URLError:
            row.update({
                "retrieval_status": "error:URLError",
                "access_class": "lookup_error",
                "next_action": "retry_OpenAlex_lookup",
            })
        output.append(row)
        time.sleep(args.sleep_seconds)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(output)
    summary = {
        "sources": len(output),
        "retrieved": sum(row["retrieval_status"] == "retrieved" for row in output),
        "oa_pdf": sum(row["access_class"] == "oa_pdf" for row in output),
        "oa_landing": sum(row["access_class"] == "oa_landing" for row in output),
        "library_or_author": sum(row["access_class"] == "library_or_author" for row in output),
        "lookup_errors": sum(row["access_class"] == "lookup_error" for row in output),
        "boundary": "No source is promoted until original pages, tables or figures are inspected.",
    }
    args.out.with_suffix(".summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
