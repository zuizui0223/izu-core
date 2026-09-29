"""Retrieve candidate geometries for literature-named study localities.

This script deliberately performs *candidate retrieval*, not automatic spatial
assignment. Nominatim results are retained verbatim with the query and response
metadata. A returned geometry must be reviewed against the cited source locality
before it can become an island reference point, a barrier distance endpoint, or
a climate-extraction location.

Island-proxy searches are recorded separately from literature-locality searches.
A proxy can support sensitivity analysis of geography only after review; it never
silently replaces the actual plant sampling locality.
"""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_ROOT = "https://nominatim.openstreetmap.org/search"
CSV_COLUMNS = (
    "target_id",
    "reference_role",
    "island_id",
    "source_id",
    "source_locality",
    "candidate_rank",
    "osm_type",
    "osm_id",
    "display_name",
    "class",
    "type",
    "lat",
    "lon",
    "boundingbox",
    "importance",
    "source_url",
    "review_status",
    "notes",
)


def query_url(locality: str, limit: int) -> str:
    params = {
        "q": locality,
        "format": "jsonv2",
        "addressdetails": 1,
        "polygon_geojson": 1,
        "limit": limit,
    }
    return f"{API_ROOT}?{urlencode(params)}"


def fetch_json(url: str) -> list[dict[str, Any]]:
    request = Request(
        url,
        headers={
            "User-Agent": "campanula-channel-identification/1.0 (research evidence audit; contact: repository maintainer)",
            "Accept": "application/json",
        },
    )
    with urlopen(request, timeout=90) as response:  # nosec B310 - fixed HTTPS endpoint
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, list):
        raise ValueError("Nominatim response is not a result list")
    if not all(isinstance(item, dict) for item in payload):
        raise ValueError("Nominatim result list contains a non-object value")
    return payload


def normalize_candidate(target: dict[str, str], candidate: dict[str, Any], rank: int) -> dict[str, str]:
    role = target.get("reference_role", "literature_locality")
    note = (
        "Raw island-proxy geocoding candidate; use only for geography sensitivity after review. "
        "It is not a plant sampling locality."
        if role == "island_proxy"
        else "Raw literature-locality geocoding candidate; do not use for climate or barrier analysis until locality review."
    )
    return {
        "target_id": target["target_id"],
        "reference_role": role,
        "island_id": target["island_id"],
        "source_id": target["source_id"],
        "source_locality": target["source_locality"],
        "candidate_rank": str(rank),
        "osm_type": str(candidate.get("osm_type") or ""),
        "osm_id": str(candidate.get("osm_id") or ""),
        "display_name": str(candidate.get("display_name") or ""),
        "class": str(candidate.get("class") or ""),
        "type": str(candidate.get("type") or ""),
        "lat": str(candidate.get("lat") or ""),
        "lon": str(candidate.get("lon") or ""),
        "boundingbox": json.dumps(candidate.get("boundingbox"), ensure_ascii=False),
        "importance": str(candidate.get("importance") or ""),
        "source_url": f"https://www.openstreetmap.org/{candidate.get('osm_type', '')}/{candidate.get('osm_id', '')}",
        "review_status": "candidate",
        "notes": note,
    }


def fetch_targets(config: dict[str, Any], limit: int, delay_seconds: float) -> tuple[list[dict[str, Any]], list[dict[str, str]], list[dict[str, str]]]:
    raw: list[dict[str, Any]] = []
    rows: list[dict[str, str]] = []
    failures: list[dict[str, str]] = []
    targets = config.get("targets")
    if not isinstance(targets, list):
        raise ValueError("config targets must be a list")
    for index, target in enumerate(targets):
        if not isinstance(target, dict):
            failures.append({"target_id": "unknown", "error": "Target is not an object"})
            continue
        target_id = str(target.get("target_id") or "")
        locality = str(target.get("source_locality") or "")
        if not target_id or not locality:
            failures.append({"target_id": target_id or "unknown", "error": "Missing target_id or source_locality"})
            continue
        url = query_url(locality, limit)
        try:
            candidates = fetch_json(url)
            raw.append({"target": target, "query_url": url, "results": candidates})
            rows.extend(normalize_candidate(target, result, rank + 1) for rank, result in enumerate(candidates))
        except (OSError, ValueError, json.JSONDecodeError) as error:
            failures.append({"target_id": target_id, "error": str(error)})
        if index < len(targets) - 1:
            time.sleep(delay_seconds)
    return raw, rows, failures


def write_snapshot(config_path: Path, output_dir: Path, limit: int, delay_seconds: float) -> int:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    raw, rows, failures = fetch_targets(config, limit, delay_seconds)
    output_dir.mkdir(parents=True, exist_ok=True)
    metadata = {
        "source": "OpenStreetMap Nominatim search API",
        "fetched_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "config_path": str(config_path),
        "candidate_limit_per_locality": limit,
        "minimum_delay_seconds": delay_seconds,
        "source_context": config.get("source_context"),
        "boundary": "Candidates preserve place-name search results only. None is a reviewed sampling locality, island centroid, island polygon, or climate/barrier endpoint until separately accepted.",
    }
    (output_dir / "manifest.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output_dir / "raw_responses.json").write_text(json.dumps(raw, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with (output_dir / "geocoding_candidates.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "failures.json").write_text(json.dumps(failures, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 1 if failures else 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--delay-seconds", type=float, default=1.1)
    args = parser.parse_args()
    if args.limit <= 0:
        raise SystemExit("--limit must be positive")
    if args.delay_seconds < 1.0:
        raise SystemExit("--delay-seconds must be at least 1.0 to respect the public API rate limit")
    try:
        status = write_snapshot(args.config, args.output_dir, args.limit, args.delay_seconds)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(str(error)) from error
    if status:
        raise SystemExit("One or more locality queries failed; inspect the retained artifact.")


if __name__ == "__main__":
    main()
