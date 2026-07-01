"""Fetch auditable, spatially scoped GBIF candidate snapshots for the Izu study.

The targets and broad WKT retrieval envelope are declared in a JSON config.
For every target, the script validates the saved GBIF taxon key against the
live taxon record, then retrieves all pages up to a declared ceiling.

Outputs are candidate availability evidence only. They do not assign records to
islands, infer absence, establish visitation, or measure pollination efficacy.
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_ROOT = "https://api.gbif.org/v1"
PAGE_SIZE = 300
CSV_COLUMNS = (
    "record_id",
    "target_id",
    "scientific_name",
    "event_date",
    "decimal_latitude",
    "decimal_longitude",
    "coordinate_uncertainty_m",
    "basis_of_record",
    "dataset_key",
    "source_url",
    "identification_status",
    "review_status",
    "notes",
)


def fetch_json(url: str) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": "campanula-channel-identification/1.0"})
    with urlopen(request, timeout=90) as response:  # nosec B310 - fixed HTTPS source
        return json.loads(response.read().decode("utf-8"))


def taxon_url(taxon_key: int) -> str:
    return f"{API_ROOT}/species/{taxon_key}"


def occurrence_url(taxon_key: int, geometry_wkt: str, max_page: int, offset: int) -> str:
    query: dict[str, str | int] = {
        "taxon_key": taxon_key,
        "country": "JP",
        "has_coordinate": "true",
        "geometry": geometry_wkt,
        "limit": max_page,
        "offset": offset,
    }
    return f"{API_ROOT}/occurrence/search?{urlencode(query)}"


def normalized(value: object) -> str:
    return " ".join(str(value or "").casefold().split())


def validate_target(target: dict[str, Any], taxon: dict[str, Any]) -> None:
    if taxon.get("key") != target["taxon_key"]:
        raise ValueError(f"{target['target_id']}: GBIF returned a different taxon key")
    if str(taxon.get("taxonomicStatus", "")).upper() != "ACCEPTED":
        raise ValueError(f"{target['target_id']}: taxon is not accepted")
    if taxon.get("rank") != target["expected_rank"]:
        raise ValueError(f"{target['target_id']}: unexpected GBIF rank {taxon.get('rank')!r}")
    if normalized(taxon.get("canonicalName")) != normalized(target["expected_canonical_name"]):
        raise ValueError(f"{target['target_id']}: canonical name does not match declared target")


def normalize_record(record: dict[str, Any], target_id: str) -> dict[str, str]:
    key = str(record.get("key", "")).strip()
    return {
        "record_id": key,
        "target_id": target_id,
        "scientific_name": str(record.get("scientificName") or record.get("species") or "").strip(),
        "event_date": str(record.get("eventDate") or record.get("year") or "").strip(),
        "decimal_latitude": str(record.get("decimalLatitude") or "").strip(),
        "decimal_longitude": str(record.get("decimalLongitude") or "").strip(),
        "coordinate_uncertainty_m": str(record.get("coordinateUncertaintyInMeters") or "").strip(),
        "basis_of_record": str(record.get("basisOfRecord") or "").strip(),
        "dataset_key": str(record.get("datasetKey") or "").strip(),
        "source_url": f"https://www.gbif.org/occurrence/{key}" if key else "",
        "identification_status": str(record.get("taxonomicStatus") or "not_reviewed").strip(),
        "review_status": "candidate",
        "notes": "Spatially scoped raw GBIF candidate; review required before analysis.",
    }


def fetch_target(target: dict[str, Any], geometry_wkt: str, max_records: int) -> dict[str, Any]:
    if max_records <= 0:
        raise ValueError("max_records must be positive")
    taxon_query_url = taxon_url(target["taxon_key"])
    taxon = fetch_json(taxon_query_url)
    validate_target(target, taxon)
    raw_pages: list[dict[str, Any]] = []
    records: list[dict[str, str]] = []
    query_urls = [taxon_query_url]
    reported_total: int | None = None
    offset = 0
    while len(records) < max_records:
        limit = min(PAGE_SIZE, max_records - len(records))
        url = occurrence_url(target["taxon_key"], geometry_wkt, limit, offset)
        query_urls.append(url)
        page = fetch_json(url)
        raw_pages.append(page)
        count = page.get("count")
        if reported_total is None and isinstance(count, int) and count >= 0:
            reported_total = count
        results = page.get("results", [])
        if not isinstance(results, list):
            raise ValueError(f"{target['target_id']}: occurrence response lacks results list")
        records.extend(normalize_record(row, target["target_id"]) for row in results)
        if page.get("endOfRecords", True) or not results:
            break
        offset += len(results)
    return {
        "target": target,
        "taxon": taxon,
        "query_urls": query_urls,
        "raw_pages": raw_pages,
        "records": records,
        "reported_total_records": reported_total,
        "retrieved_candidate_records": len(records),
        "truncated_by_max_records": (
            reported_total is not None and len(records) < reported_total and len(records) >= max_records
        ),
    }


def write_target_snapshot(root: Path, result: dict[str, Any], region: dict[str, Any], max_records: int) -> None:
    target = result["target"]
    destination = root / target["target_id"]
    destination.mkdir(parents=True, exist_ok=True)
    manifest = {
        "source": "GBIF API",
        "fetched_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "scientific_name_requested": target["scientific_name"],
        "target_id": target["target_id"],
        "taxon_key": target["taxon_key"],
        "study_region": region,
        "country": "JP",
        "max_records": max_records,
        "page_size": PAGE_SIZE,
        "reported_total_records": result["reported_total_records"],
        "retrieved_candidate_records": result["retrieved_candidate_records"],
        "truncated_by_max_records": result["truncated_by_max_records"],
        "query_urls": result["query_urls"],
        "boundary": "Records are geographically scoped availability evidence only; no record is an island assignment, interaction observation, effectiveness measurement, or absence result.",
    }
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (destination / "selected_taxon.json").write_text(json.dumps(result["taxon"], indent=2) + "\n", encoding="utf-8")
    (destination / "occurrence_pages.json").write_text(json.dumps(result["raw_pages"], indent=2) + "\n", encoding="utf-8")
    with (destination / "occurrences_candidate.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(result["records"])


def write_inventory(root: Path, results: list[dict[str, Any]], failures: list[dict[str, str]]) -> None:
    lines = [
        "# Izu-scoped GBIF candidate snapshot inventory",
        "",
        "The WKT is a broad retrieval envelope, not an island assignment. Candidate records require record-level review before any scenario use.",
        "",
        "| target | GBIF taxon key | reported regional records | retrieved candidates | truncated | status |",
        "|---|---:|---:|---:|---|---|",
    ]
    for result in results:
        target = result["target"]
        lines.append(
            f"| {target['target_id']} | {target['taxon_key']} | {result['reported_total_records']} | {result['retrieved_candidate_records']} | {str(result['truncated_by_max_records']).lower()} | success |"
        )
    for failure in failures:
        lines.append(f"| {failure['target_id']} |  |  |  |  | failure |")
    lines.extend((
        "",
        "## Interpretation boundary",
        "",
        "A zero regional candidate count is a result of this declared query, not evidence of taxon absence. A truncated response is not eligible for a full regional coverage claim.",
    ))
    (root / "INVENTORY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (root / "FAILURES.json").write_text(json.dumps(failures, indent=2) + "\n", encoding="utf-8")


def run(config_path: Path, output_dir: Path, max_records: int) -> int:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    region = config["study_region"]
    geometry_wkt = str(region["geometry_wkt"])
    if not geometry_wkt.upper().startswith("POLYGON("):
        raise ValueError("study_region.geometry_wkt must be a POLYGON")
    output_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    for target in config["targets"]:
        try:
            result = fetch_target(target, geometry_wkt, max_records)
            write_target_snapshot(output_dir, result, region, max_records)
            results.append(result)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            failures.append({"target_id": str(target.get("target_id", "unknown")), "error": str(error)})
    write_inventory(output_dir, results, failures)
    has_truncation = any(row["truncated_by_max_records"] for row in results)
    return 1 if failures or has_truncation else 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--max-records", type=int, default=5000)
    args = parser.parse_args()
    try:
        code = run(args.config, args.output_dir, args.max_records)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(str(error)) from error
    if code:
        raise SystemExit("One or more targets failed or reached the configured record ceiling; inspect the retained artifact.")


if __name__ == "__main__":
    main()
