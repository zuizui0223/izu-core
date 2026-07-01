"""Fetch spatially scoped iNaturalist candidate observations for the Izu study.

The script preserves raw API pages and a normalized candidate table. It does not
identify pollination interactions, assign records to individual islands, or infer
absence from missing observations. Photograph metadata are retained so that
eligible flower images can later enter an independently reviewed trait layer.
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


API_ROOT = "https://api.inaturalist.org/v1/observations"
PAGE_SIZE = 200
CSV_COLUMNS = (
    "record_id",
    "target_id",
    "query_taxon_name",
    "observed_taxon_name",
    "observed_on",
    "latitude",
    "longitude",
    "positional_accuracy_m",
    "quality_grade",
    "captive_or_cultivated",
    "photo_count",
    "source_url",
    "review_status",
    "notes",
)


def fetch_json(url: str) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": "campanula-channel-identification/1.0"})
    with urlopen(request, timeout=90) as response:  # nosec B310 - fixed HTTPS source
        return json.loads(response.read().decode("utf-8"))


def observation_url(target: dict[str, str], region: dict[str, Any], page: int, per_page: int) -> str:
    query: dict[str, Any] = {
        "taxon_name": target["taxon_name"],
        "swlat": region["swlat"],
        "swlng": region["swlng"],
        "nelat": region["nelat"],
        "nelng": region["nelng"],
        "per_page": per_page,
        "page": page,
        "order": "asc",
        "order_by": "observed_on",
    }
    return f"{API_ROOT}?{urlencode(query)}"


def _coordinates(record: dict[str, Any]) -> tuple[str, str]:
    geojson = record.get("geojson")
    if not isinstance(geojson, dict):
        return "", ""
    coordinates = geojson.get("coordinates")
    if not isinstance(coordinates, list) or len(coordinates) < 2:
        return "", ""
    return str(coordinates[1]), str(coordinates[0])


def _taxon_name(record: dict[str, Any]) -> str:
    taxon = record.get("taxon")
    if not isinstance(taxon, dict):
        return ""
    return str(taxon.get("name") or "")


def normalize_record(record: dict[str, Any], target: dict[str, str]) -> dict[str, str]:
    latitude, longitude = _coordinates(record)
    observation_id = str(record.get("id") or "").strip()
    photos = record.get("photos")
    photo_count = len(photos) if isinstance(photos, list) else 0
    return {
        "record_id": observation_id,
        "target_id": target["target_id"],
        "query_taxon_name": target["taxon_name"],
        "observed_taxon_name": _taxon_name(record),
        "observed_on": str(record.get("observed_on") or ""),
        "latitude": latitude,
        "longitude": longitude,
        "positional_accuracy_m": str(record.get("positional_accuracy") or ""),
        "quality_grade": str(record.get("quality_grade") or ""),
        "captive_or_cultivated": str(record.get("captive") if record.get("captive") is not None else ""),
        "photo_count": str(photo_count),
        "source_url": str(record.get("uri") or ""),
        "review_status": "candidate",
        "notes": "Spatially scoped raw iNaturalist candidate; review required before any island, trait, or interaction use.",
    }


def fetch_target(target: dict[str, str], region: dict[str, Any], max_records: int) -> dict[str, Any]:
    if max_records <= 0:
        raise ValueError("max_records must be positive")
    pages: list[dict[str, Any]] = []
    urls: list[str] = []
    records: list[dict[str, str]] = []
    total_results: int | None = None
    page_number = 1
    while len(records) < max_records:
        per_page = min(PAGE_SIZE, max_records - len(records))
        url = observation_url(target, region, page_number, per_page)
        urls.append(url)
        page = fetch_json(url)
        pages.append(page)
        count = page.get("total_results")
        if total_results is None and isinstance(count, int) and count >= 0:
            total_results = count
        results = page.get("results", [])
        if not isinstance(results, list):
            raise ValueError(f"{target['target_id']}: iNaturalist response lacks a results list")
        records.extend(normalize_record(record, target) for record in results)
        if not results or len(records) >= max_records or (total_results is not None and len(records) >= total_results):
            break
        page_number += 1
    return {
        "target": target,
        "query_urls": urls,
        "pages": pages,
        "records": records,
        "reported_total_results": total_results,
        "retrieved_candidate_records": len(records),
        "truncated_by_max_records": total_results is not None and len(records) < total_results and len(records) >= max_records,
    }


def write_snapshot(root: Path, result: dict[str, Any], region: dict[str, Any], max_records: int) -> None:
    target = result["target"]
    destination = root / target["target_id"]
    destination.mkdir(parents=True, exist_ok=True)
    manifest = {
        "source": "iNaturalist observations API",
        "fetched_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "target": target,
        "study_region": region,
        "max_records": max_records,
        "page_size": PAGE_SIZE,
        "reported_total_results": result["reported_total_results"],
        "retrieved_candidate_records": result["retrieved_candidate_records"],
        "truncated_by_max_records": result["truncated_by_max_records"],
        "query_urls": result["query_urls"],
        "boundary": "Candidate observations can document public records and photo leads only. They do not establish island assignment, floral visitation, pollination effectiveness, historical presence, or absence.",
    }
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (destination / "observation_pages.json").write_text(json.dumps(result["pages"], indent=2) + "\n", encoding="utf-8")
    with (destination / "observations_candidate.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(result["records"])


def write_inventory(root: Path, results: list[dict[str, Any]], failures: list[dict[str, str]]) -> None:
    lines = [
        "# Izu-scoped iNaturalist candidate snapshot inventory",
        "",
        "These are raw public observations within a broad rectangle. A record is not an island-level observation until record-level geometry and taxonomy review are complete.",
        "",
        "| target | reported regional results | retrieved candidates | truncated | status |",
        "|---|---:|---:|---|---|",
    ]
    for result in results:
        lines.append(
            f"| {result['target']['target_id']} | {result['reported_total_results']} | {result['retrieved_candidate_records']} | {str(result['truncated_by_max_records']).lower()} | success |"
        )
    for failure in failures:
        lines.append(f"| {failure['target_id']} |  |  |  | failure |")
    lines.extend((
        "",
        "## Boundary",
        "",
        "A zero result is a result of this named taxon + bounding-box query, not evidence of taxon absence. A record with a photo is a candidate for independent floral-trait review, not a random sample of a population.",
    ))
    (root / "INVENTORY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (root / "FAILURES.json").write_text(json.dumps(failures, indent=2) + "\n", encoding="utf-8")


def run(config_path: Path, output_dir: Path, max_records: int) -> int:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    region = config["study_region"]
    required = {"swlat", "swlng", "nelat", "nelng"}
    if not required.issubset(region):
        raise ValueError("study_region lacks one or more bounding coordinates")
    output_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    for target in config["targets"]:
        try:
            result = fetch_target(target, region, max_records)
            write_snapshot(output_dir, result, region, max_records)
            results.append(result)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            failures.append({"target_id": str(target.get("target_id", "unknown")), "error": str(error)})
    write_inventory(output_dir, results, failures)
    return 1 if failures or any(row["truncated_by_max_records"] for row in results) else 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--max-records", type=int, default=5000)
    args = parser.parse_args()
    try:
        status = run(args.config, args.output_dir, args.max_records)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(str(error)) from error
    if status:
        raise SystemExit("One or more iNaturalist targets failed or reached the record ceiling; inspect the retained artifact.")


if __name__ == "__main__":
    main()
