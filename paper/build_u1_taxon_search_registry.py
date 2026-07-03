"""Expand all U1 taxa into an auditable synonym and vernacular-name registry.

The registry is deliberately built from U1, not the entomophilous pilot. Names
are search leads, not taxonomic decisions. Each row records its GBIF endpoint,
retrieval time and review status before Japanese or English literature searching.

Usage:
    python paper/build_u1_taxon_search_registry.py \
        --u1 artifacts/u0_snapshot/u1_screening_queue.csv \
        --out artifacts/u0_snapshot/u1_taxon_name_registry.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API = "https://api.gbif.org/v1"
USER_AGENT = "izu-core-u1-name-registry/1.0"
FIELDS = (
    "u0_accepted_key", "accepted_name", "queue_rank", "name_type", "search_name",
    "language", "source_endpoint", "retrieved_at_utc", "retrieval_status", "review_status", "notes",
)


def request_json(url: str, attempts: int = 4) -> tuple[dict, int]:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        request = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(request, timeout=60) as response:  # nosec B310 fixed HTTPS GBIF endpoint
                return json.load(response), int(response.status)
        except HTTPError as error:
            last_error = error
            if error.code not in (429, 500, 502, 503, 504) or attempt == attempts:
                raise
        except URLError as error:
            last_error = error
            if attempt == attempts:
                raise
        time.sleep(1.25 * attempt)
    assert last_error is not None
    raise last_error


def unique_names(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str, str, str]] = set()
    output = []
    for row in rows:
        key = (row["u0_accepted_key"], row["name_type"], row["search_name"].casefold(), row["language"])
        if row["search_name"] and key not in seen:
            seen.add(key)
            output.append(row)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--u1", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    with args.u1.open(encoding="utf-8", newline="") as handle:
        queue = list(csv.DictReader(handle))
    rows: list[dict[str, str]] = []
    for taxon in queue:
        key = taxon["u0_accepted_key"]
        accepted = taxon["accepted_name"]
        rank = taxon["queue_rank"]
        stamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        rows.append({
            "u0_accepted_key": key, "accepted_name": accepted, "queue_rank": rank,
            "name_type": "accepted_input", "search_name": accepted, "language": "",
            "source_endpoint": "U1 queue", "retrieved_at_utc": stamp,
            "retrieval_status": "input", "review_status": "input", "notes": "Accepted U0 name; verify taxonomic concept when retaining a source.",
        })
        synonym_url = f"{API}/species/{key}/synonyms"
        vernacular_url = f"{API}/species/{key}/vernacularNames"
        try:
            payload, _ = request_json(synonym_url)
            for record in payload.get("results", []):
                name = str(record.get("scientificName") or record.get("canonicalName") or "").strip()
                if name:
                    rows.append({
                        "u0_accepted_key": key, "accepted_name": accepted, "queue_rank": rank,
                        "name_type": "gbif_synonym", "search_name": name, "language": "",
                        "source_endpoint": synonym_url, "retrieved_at_utc": stamp,
                        "retrieval_status": "retrieved", "review_status": "unreviewed",
                        "notes": str(record.get("taxonomicStatus") or "synonym lead"),
                    })
        except HTTPError as error:
            rows.append({"u0_accepted_key": key, "accepted_name": accepted, "queue_rank": rank, "name_type": "synonym_error", "search_name": "", "language": "", "source_endpoint": synonym_url, "retrieved_at_utc": stamp, "retrieval_status": f"error:HTTPError:{error.code}", "review_status": "error", "notes": "Retry before declaring no synonyms."})
        except URLError as error:
            rows.append({"u0_accepted_key": key, "accepted_name": accepted, "queue_rank": rank, "name_type": "synonym_error", "search_name": "", "language": "", "source_endpoint": synonym_url, "retrieved_at_utc": stamp, "retrieval_status": f"error:URLError:{error.reason}", "review_status": "error", "notes": "Retry before declaring no synonyms."})
        try:
            payload, _ = request_json(vernacular_url)
            for record in payload.get("results", []):
                name = str(record.get("vernacularName") or "").strip()
                if name:
                    rows.append({
                        "u0_accepted_key": key, "accepted_name": accepted, "queue_rank": rank,
                        "name_type": "gbif_vernacular", "search_name": name,
                        "language": str(record.get("language") or ""), "source_endpoint": vernacular_url,
                        "retrieved_at_utc": stamp, "retrieval_status": "retrieved", "review_status": "unreviewed",
                        "notes": "Search lead only; confirm Japanese script and taxonomic concept against authority.",
                    })
        except HTTPError as error:
            rows.append({"u0_accepted_key": key, "accepted_name": accepted, "queue_rank": rank, "name_type": "vernacular_error", "search_name": "", "language": "", "source_endpoint": vernacular_url, "retrieved_at_utc": stamp, "retrieval_status": f"error:HTTPError:{error.code}", "review_status": "error", "notes": "Retry before declaring no vernacular names."})
        except URLError as error:
            rows.append({"u0_accepted_key": key, "accepted_name": accepted, "queue_rank": rank, "name_type": "vernacular_error", "search_name": "", "language": "", "source_endpoint": vernacular_url, "retrieved_at_utc": stamp, "retrieval_status": f"error:URLError:{error.reason}", "review_status": "error", "notes": "Retry before declaring no vernacular names."})
        time.sleep(0.25)

    deduplicated = unique_names(rows)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(deduplicated)
    summary = {
        "u1_taxa": len(queue),
        "name_registry_rows": len(deduplicated),
        "scientific_synonym_rows": sum(row["name_type"] == "gbif_synonym" for row in deduplicated),
        "vernacular_rows": sum(row["name_type"] == "gbif_vernacular" for row in deduplicated),
        "errors": sum(row["review_status"] == "error" for row in deduplicated),
        "boundary": "Names are discovery leads and require source-level taxonomic review before evidence extraction.",
    }
    args.out.with_suffix(".summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
