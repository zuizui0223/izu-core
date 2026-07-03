"""Rebuild the U0 mainland-plus-island candidate universe from GBIF facets.

The script distinguishes occurrence retrieval from taxonomic normalization. It
fails closed on missing facet pages or unresolved taxon records, and writes both
query and name-resolution logs. Spatial circles are a reproducible proxy profile,
not a silent replacement for an earlier undocumented species count.

Usage:
    python paper/rebuild_u0_parent_universe.py --out-dir artifacts/u0_snapshot
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API = "https://api.gbif.org/v1"
PROFILE = "izu_proxy_circles_v1"
FACET_PAGE_SIZE = 1_000
REGIONS = {
    "MAINLAND": (34.7500, 138.9500, 25.0),
    "Oshima": (34.7385, 139.4024, 8.0),
    "Toshima": (34.5230, 139.2800, 5.0),
    "Niijima": (34.3813, 139.2654, 6.0),
    "Kozushima": (34.2142, 139.1523, 6.0),
    "Miyake": (34.0854, 139.5213, 8.0),
    "Hachijo": (33.1025, 139.8077, 8.0),
}
ISLANDS = tuple(region for region in REGIONS if region != "MAINLAND")
USER_AGENT = "izu-core-u0-rebuild/1.2"


def circle_wkt(lat: float, lon: float, radius_km: float, vertices: int = 32) -> str:
    """Return a deterministic local-circle approximation as WKT lon-lat polygon."""
    lat_scale = 111.32
    lon_scale = 111.32 * math.cos(math.radians(lat))
    points = []
    for index in range(vertices):
        angle = 2 * math.pi * index / vertices
        points.append((lon + radius_km * math.cos(angle) / lon_scale, lat + radius_km * math.sin(angle) / lat_scale))
    points.append(points[0])
    return "POLYGON((" + ",".join(f"{x:.6f} {y:.6f}" for x, y in points) + "))"


def request_json(url: str, *, attempts: int = 5) -> tuple[dict, int]:
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
        time.sleep(1.2 * attempt)
    assert last_error is not None
    raise last_error


def facet_url(geometry: str, offset: int) -> str:
    return API + "/occurrence/search?" + urlencode({
        "kingdom": "Plantae", "hasCoordinate": "true", "hasGeospatialIssue": "false",
        "geometry": geometry, "facet": "speciesKey", "facetLimit": FACET_PAGE_SIZE,
        "facetOffset": offset, "limit": 0,
    })


def species_url(key: str) -> str:
    return f"{API}/species/{key}"


def facet_entries(payload: dict) -> list[dict]:
    for facet in payload.get("facets") or []:
        if facet.get("field") in {"SPECIES_KEY", "speciesKey"}:
            return list(facet.get("counts", []))
    raise RuntimeError("GBIF response did not include speciesKey facet")


def fetch_all_species_facets(region: str, geometry: str, retrieved_at: str) -> tuple[dict[str, int], list[dict[str, object]], int]:
    """Page through every GBIF species facet; fail closed on any missing page."""
    result: dict[str, int] = {}
    pages: list[dict[str, object]] = []
    offset = 0
    total_occurrences: int | None = None
    while True:
        url = facet_url(geometry, offset)
        payload, http_status = request_json(url)
        entries = facet_entries(payload)
        if total_occurrences is None:
            total_occurrences = int(payload.get("count") or 0)
        pages.append({
            "profile": PROFILE, "region": region, "facet_offset": offset, "query_url": url,
            "retrieved_at_utc": retrieved_at, "http_status": http_status,
            "retrieval_status": "retrieved", "facet_entries": len(entries),
            "gbif_total_occurrences": total_occurrences,
        })
        for entry in entries:
            raw_key = str(entry["name"])
            result[raw_key] = result.get(raw_key, 0) + int(entry["count"])
        if len(entries) < FACET_PAGE_SIZE:
            break
        offset += FACET_PAGE_SIZE
        time.sleep(0.25)
    return result, pages, int(total_occurrences or 0)


def fetch_species_record(key: str) -> tuple[str, dict, int]:
    record, status = request_json(species_url(key))
    return key, record, status


def fetch_records_parallel(keys: list[str], workers: int) -> tuple[dict[str, dict], dict[str, int]]:
    """Fetch distinct GBIF taxon records concurrently, failing closed on error."""
    records: dict[str, dict] = {}
    status_codes: dict[str, int] = {}
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(fetch_species_record, key): key for key in keys}
        for future in as_completed(futures):
            key = futures[future]
            try:
                result_key, record, status = future.result()
            except Exception as error:  # preserve key in fatal error
                raise RuntimeError(f"GBIF taxon normalization failed for speciesKey={key}") from error
            records[result_key] = record
            status_codes[result_key] = status
    return records, status_codes


def accepted_name(record: dict) -> str:
    return str(record.get("canonicalName") or record.get("scientificName") or "")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", default="artifacts/u0_snapshot", help="directory for CSV and JSON artifacts")
    parser.add_argument("--taxon-workers", type=int, default=6, help="concurrent GBIF taxon requests (1-12)")
    args = parser.parse_args()
    if not 1 <= args.taxon_workers <= 12:
        raise ValueError("--taxon-workers must be between 1 and 12")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    retrieved_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    region_log: list[dict[str, object]] = []
    page_log: list[dict[str, object]] = []
    raw_counts: dict[str, dict[str, int]] = {}
    for region, (lat, lon, radius) in REGIONS.items():
        geometry = circle_wkt(lat, lon, radius)
        try:
            counts, pages, total_occurrences = fetch_all_species_facets(region, geometry, retrieved_at)
        except HTTPError as error:
            raise RuntimeError(f"GBIF region query failed for {region}: HTTP {error.code}") from error
        except URLError as error:
            raise RuntimeError(f"GBIF region query failed for {region}: {error.reason}") from error
        raw_counts[region] = counts
        page_log.extend(pages)
        region_log.append({
            "profile": PROFILE, "region": region, "lat": lat, "lon": lon, "radius_km": radius,
            "geometry_wkt": geometry, "retrieved_at_utc": retrieved_at, "retrieval_status": "retrieved",
            "facet_pages": len(pages), "facet_species_count": len(counts),
            "gbif_total_occurrences": total_occurrences,
        })
        time.sleep(0.25)

    # Resolve every distinct facet key. This retains synonym-split records that would
    # be missed by filtering raw keys before their accepted concepts are known.
    raw_keys = sorted({raw_key for counts in raw_counts.values() for raw_key in counts})
    raw_records, raw_status = fetch_records_parallel(raw_keys, args.taxon_workers)
    accepted_keys = sorted({str(record.get("acceptedKey") or record.get("key") or key) for key, record in raw_records.items()})
    missing_accepted = [key for key in accepted_keys if key not in raw_records]
    accepted_extra, accepted_extra_status = fetch_records_parallel(missing_accepted, args.taxon_workers)
    all_records = {**raw_records, **accepted_extra}
    all_status = {**raw_status, **accepted_extra_status}

    resolution_rows: list[dict[str, object]] = []
    counts_by_accepted: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    raw_keys_by_accepted: dict[str, set[str]] = defaultdict(set)
    metadata: dict[str, dict] = {}
    for region, counts in raw_counts.items():
        for raw_key, count in counts.items():
            raw_record = raw_records[raw_key]
            accepted_key = str(raw_record.get("acceptedKey") or raw_record.get("key") or raw_key)
            accepted_record = all_records[accepted_key]
            resolution_rows.append({
                "raw_species_key": raw_key, "accepted_key": accepted_key,
                "raw_scientific_name": raw_record.get("scientificName", ""),
                "raw_taxonomic_status": raw_record.get("taxonomicStatus", ""),
                "accepted_name": accepted_name(accepted_record), "accepted_rank": accepted_record.get("rank", ""),
                "region": region, "occurrence_count": count, "retrieved_at_utc": retrieved_at,
                "raw_http_status": raw_status.get(raw_key, ""), "accepted_http_status": all_status.get(accepted_key, ""),
            })
            if str(accepted_record.get("rank") or "") != "SPECIES":
                continue
            counts_by_accepted[accepted_key][region] += count
            raw_keys_by_accepted[accepted_key].add(raw_key)
            metadata[accepted_key] = accepted_record

    rows: list[dict[str, object]] = []
    for key, by_region in counts_by_accepted.items():
        if by_region.get("MAINLAND", 0) <= 0:
            continue
        n_islands = sum(by_region.get(island, 0) > 0 for island in ISLANDS)
        if n_islands < 2:
            continue
        record = metadata[key]
        row: dict[str, object] = {
            "profile": PROFILE, "accepted_key": key, "accepted_name": accepted_name(record),
            "scientific_name": record.get("scientificName", ""), "family": record.get("family", ""),
            "order": record.get("order", ""), "class": record.get("class", ""),
            "taxonomic_status": record.get("taxonomicStatus", ""), "taxon_rank": record.get("rank", ""),
            "raw_species_keys_merged": "|".join(sorted(raw_keys_by_accepted[key])),
            "mainland_present": "yes", "n_islands": n_islands,
            "total_occ": sum(by_region.values()), "retrieved_at_utc": retrieved_at,
        }
        for region in REGIONS:
            row[f"{region}_occ"] = by_region.get(region, 0)
            row[f"{region}_present"] = "yes" if by_region.get(region, 0) > 0 else "no"
        rows.append(row)
    rows.sort(key=lambda row: (-int(row["n_islands"]), -int(row["total_occ"]), str(row["accepted_name"])))

    regions = list(REGIONS)
    parent_fields = [
        "profile", "accepted_key", "accepted_name", "scientific_name", "family", "order", "class",
        "taxonomic_status", "taxon_rank", "raw_species_keys_merged", "mainland_present", "n_islands",
        "total_occ", "retrieved_at_utc",
    ] + [field for region in regions for field in (f"{region}_occ", f"{region}_present")]
    with (out_dir / "u0_parent_universe.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=parent_fields)
        writer.writeheader(); writer.writerows(rows)
    region_fields = ["profile", "region", "lat", "lon", "radius_km", "geometry_wkt", "retrieved_at_utc", "retrieval_status", "facet_pages", "facet_species_count", "gbif_total_occurrences"]
    with (out_dir / "u0_gbif_region_log.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=region_fields)
        writer.writeheader(); writer.writerows(region_log)
    page_fields = ["profile", "region", "facet_offset", "query_url", "retrieved_at_utc", "http_status", "retrieval_status", "facet_entries", "gbif_total_occurrences"]
    with (out_dir / "u0_gbif_query_pages.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=page_fields)
        writer.writeheader(); writer.writerows(page_log)
    resolution_fields = ["raw_species_key", "accepted_key", "raw_scientific_name", "raw_taxonomic_status", "accepted_name", "accepted_rank", "region", "occurrence_count", "retrieved_at_utc", "raw_http_status", "accepted_http_status"]
    with (out_dir / "u0_gbif_taxon_resolution.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=resolution_fields)
        writer.writeheader(); writer.writerows(resolution_rows)
    summary = {
        "profile": PROFILE, "retrieved_at_utc": retrieved_at, "region_count": len(REGIONS),
        "raw_species_keys_normalized": len(raw_keys), "accepted_species_records": len({row["accepted_key"] for row in resolution_rows}),
        "u0_species_mainland_plus_two_islands": len(rows),
        "u0_species_mainland_plus_three_islands": sum(int(row["n_islands"]) >= 3 for row in rows),
        "u0_species_mainland_plus_five_islands": sum(int(row["n_islands"]) >= 5 for row in rows),
        "legacy_reference_not_asserted_equal": {"mainland_plus_two_islands": 319, "mainland_plus_three_islands": 289, "mainland_plus_five_islands": 113},
    }
    (out_dir / "u0_snapshot_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
