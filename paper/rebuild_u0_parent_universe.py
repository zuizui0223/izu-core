"""Rebuild the U0 mainland-plus-island candidate universe from GBIF facets.

This script makes the parent universe auditable. It never silently treats a
failed island query as absence. Results are written as a dated artifact, together
with the exact generated query URLs and retrieval outcomes.

The spatial footprint is an explicit proxy profile (mainland Izu-peninsula
reference plus six island circles). It is reproducible, but not assumed to be
identical to any earlier undocumented 319-species snapshot. Compare the output
against that legacy count rather than overwriting it.

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
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API = "https://api.gbif.org/v1"
PROFILE = "izu_proxy_circles_v1"
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
USER_AGENT = "izu-core-u0-rebuild/1.0"


def circle_wkt(lat: float, lon: float, radius_km: float, vertices: int = 32) -> str:
    """Return a deterministic local-circle approximation as WKT lon-lat polygon."""
    points: list[tuple[float, float]] = []
    lat_scale = 111.32
    lon_scale = 111.32 * math.cos(math.radians(lat))
    for index in range(vertices):
        angle = 2 * math.pi * index / vertices
        y = lat + (radius_km * math.sin(angle) / lat_scale)
        x = lon + (radius_km * math.cos(angle) / lon_scale)
        points.append((x, y))
    points.append(points[0])
    return "POLYGON((" + ",".join(f"{x:.6f} {y:.6f}" for x, y in points) + "))"


def request_json(url: str, *, attempts: int = 4) -> tuple[dict, int]:
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


def facet_url(geometry: str) -> str:
    params = {
        "kingdom": "Plantae",
        "hasCoordinate": "true",
        "hasGeospatialIssue": "false",
        "geometry": geometry,
        "facet": "speciesKey",
        "facetLimit": 1000,
        "limit": 0,
    }
    return API + "/occurrence/search?" + urlencode(params)


def species_url(key: str) -> str:
    return f"{API}/species/{key}"


def species_facets(payload: dict) -> dict[str, int]:
    facets = payload.get("facets") or []
    for facet in facets:
        if facet.get("field") == "SPECIES_KEY" or facet.get("field") == "speciesKey":
            return {str(entry["name"]): int(entry["count"]) for entry in facet.get("counts", [])}
    raise RuntimeError("GBIF response did not include speciesKey facet")


def resolve_taxon(key: str, cache: dict[str, dict]) -> dict:
    if key not in cache:
        cache[key] = request_json(species_url(key))[0]
    first = cache[key]
    accepted_key = str(first.get("acceptedKey") or first.get("key") or key)
    if accepted_key not in cache:
        cache[accepted_key] = request_json(species_url(accepted_key))[0]
    return cache[accepted_key]


def accepted_name(record: dict) -> str:
    return str(record.get("canonicalName") or record.get("scientificName") or "")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", default="artifacts/u0_snapshot", help="directory for CSV and JSON artifacts")
    args = parser.parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    retrieved_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    query_log: list[dict[str, object]] = []
    raw_counts: dict[str, dict[str, int]] = {}
    for region, (lat, lon, radius) in REGIONS.items():
        geometry = circle_wkt(lat, lon, radius)
        url = facet_url(geometry)
        try:
            payload, http_status = request_json(url)
            raw_counts[region] = species_facets(payload)
            query_log.append({
                "profile": PROFILE, "region": region, "lat": lat, "lon": lon,
                "radius_km": radius, "geometry_wkt": geometry, "query_url": url,
                "retrieved_at_utc": retrieved_at, "http_status": http_status,
                "retrieval_status": "retrieved", "facet_species_count": len(raw_counts[region]),
                "gbif_total_occurrences": payload.get("count", ""),
            })
        except HTTPError as error:
            query_log.append({"profile": PROFILE, "region": region, "lat": lat, "lon": lon, "radius_km": radius, "geometry_wkt": geometry, "query_url": url, "retrieved_at_utc": retrieved_at, "http_status": error.code, "retrieval_status": f"error:HTTPError:{error.code}", "facet_species_count": "", "gbif_total_occurrences": ""})
            raise RuntimeError(f"GBIF region query failed for {region}: HTTP {error.code}") from error
        except URLError as error:
            query_log.append({"profile": PROFILE, "region": region, "lat": lat, "lon": lon, "radius_km": radius, "geometry_wkt": geometry, "query_url": url, "retrieved_at_utc": retrieved_at, "http_status": "", "retrieval_status": f"error:URLError:{error.reason}", "facet_species_count": "", "gbif_total_occurrences": ""})
            raise RuntimeError(f"GBIF region query failed for {region}: {error.reason}") from error
        time.sleep(0.4)

    taxon_cache: dict[str, dict] = {}
    counts_by_accepted: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    raw_keys_by_accepted: dict[str, set[str]] = defaultdict(set)
    metadata: dict[str, dict] = {}
    for region, counts in raw_counts.items():
        for raw_key, count in counts.items():
            record = resolve_taxon(raw_key, taxon_cache)
            accepted_key = str(record.get("key") or raw_key)
            rank = str(record.get("rank") or "")
            if rank != "SPECIES":
                continue
            counts_by_accepted[accepted_key][region] += count
            raw_keys_by_accepted[accepted_key].add(raw_key)
            metadata[accepted_key] = record
            time.sleep(0.08)

    rows: list[dict[str, object]] = []
    for key, by_region in counts_by_accepted.items():
        if by_region.get("MAINLAND", 0) <= 0:
            continue
        n_islands = sum(by_region.get(island, 0) > 0 for island in ISLANDS)
        if n_islands < 2:
            continue
        record = metadata[key]
        row: dict[str, object] = {
            "profile": PROFILE,
            "accepted_key": key,
            "accepted_name": accepted_name(record),
            "scientific_name": record.get("scientificName", ""),
            "family": record.get("family", ""),
            "order": record.get("order", ""),
            "class": record.get("class", ""),
            "taxonomic_status": record.get("taxonomicStatus", ""),
            "taxon_rank": record.get("rank", ""),
            "raw_species_keys_merged": "|".join(sorted(raw_keys_by_accepted[key])),
            "mainland_present": "yes",
            "n_islands": n_islands,
            "total_occ": sum(by_region.values()),
            "retrieved_at_utc": retrieved_at,
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
    log_fields = ["profile", "region", "lat", "lon", "radius_km", "geometry_wkt", "query_url", "retrieved_at_utc", "http_status", "retrieval_status", "facet_species_count", "gbif_total_occurrences"]
    with (out_dir / "u0_gbif_query_log.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=log_fields)
        writer.writeheader(); writer.writerows(query_log)
    summary = {
        "profile": PROFILE,
        "retrieved_at_utc": retrieved_at,
        "region_count": len(REGIONS),
        "u0_species_mainland_plus_two_islands": len(rows),
        "u0_species_mainland_plus_three_islands": sum(int(row["n_islands"]) >= 3 for row in rows),
        "u0_species_mainland_plus_five_islands": sum(int(row["n_islands"]) >= 5 for row in rows),
        "legacy_reference_not_asserted_equal": {"mainland_plus_two_islands": 319, "mainland_plus_three_islands": 289, "mainland_plus_five_islands": 113},
    }
    (out_dir / "u0_snapshot_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
