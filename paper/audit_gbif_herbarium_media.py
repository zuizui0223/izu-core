"""Audit GBIF preserved-specimen media for Izu comparative cohorts.

This acquisition step asks a narrow question: do digitized, georeferenced
Japanese herbarium records with image media exist in each fixed regional proxy
bin for a predeclared set of taxa?  The result is a candidate pool, not a trait
dataset. A sheet enters later blind scoring only after a human confirms an open
flower, the predeclared visible structure, and an adequate scale/reference.

Boundaries:
* GBIF coordinate records are not treated as verified island assignments.
* Presence of an image is not evidence that a flower is visible.
* Preserved-specimen images may support morphology but cannot estimate
  pollinator assemblages, realised outcrossing, or historical causality.
* Region labels are kept in the audit/key; blind scoring sheets omit them.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

GBIF_API = "https://api.gbif.org/v1"
USER_AGENT = "izu-core-herbarium-media-audit/1.0"
RETRYABLE_HTTP = {429, 500, 502, 503, 504}
MAX_ATTEMPTS = 4
BASE_SLEEP_SECONDS = 0.8

# Keep the geographic proxy system exactly aligned with the earlier photo work.
# MAINLAND is a conservative Izu-peninsula reference proxy, not all of Honshu.
REGIONS = {
    "MAINLAND": (34.7500, 138.9500, 25.0),
    "Oshima": (34.7385, 139.4024, 8.0),
    "Toshima": (34.5230, 139.2800, 5.0),
    "Niijima": (34.3813, 139.2654, 6.0),
    "Kozushima": (34.2142, 139.1523, 6.0),
    "Miyake": (34.0854, 139.5213, 8.0),
    "Hachijo": (33.1025, 139.8077, 8.0),
}
REGIME_BY_REGION = {
    "MAINLAND": "large_bombus_proxy",
    "Oshima": "ardens_proxy",
    "Toshima": "no_bombus_proxy",
    "Niijima": "no_bombus_proxy",
    "Kozushima": "no_bombus_proxy",
    "Miyake": "no_bombus_proxy",
    "Hachijo": "no_bombus_proxy",
}

QUERY_FIELDS = (
    "taxon", "analysis_group", "group_confidence", "role", "taxon_key", "match_status",
    "total_reported", "records_requested", "records_retrieved", "retrieval_status",
    "http_status", "retrieved_at_utc", "query_url", "boundary",
)
CANDIDATE_FIELDS = (
    "candidate_id", "taxon", "analysis_group", "group_confidence", "role", "trait_candidate",
    "trait_family", "priority", "gbif_occurrence_key", "media_index", "media_url", "media_type",
    "region_proxy", "regime_proxy", "distance_to_proxy_km", "decimal_latitude",
    "decimal_longitude", "event_date", "recorded_by", "institution_code", "collection_code",
    "catalog_number", "locality", "basis_of_record", "source_url", "retrieved_at_utc", "boundary",
)
SUMMARY_FIELDS = (
    "taxon", "analysis_group", "role", "total_gbif_records_retrieved", "records_with_media",
    "media_candidates_in_region_proxies", "large_bombus_proxy_media", "ardens_proxy_media",
    "no_bombus_proxy_media", "three_regime_candidate_eligible", "minimum_candidates_per_regime",
    "next_action", "boundary",
)
BOUNDARY = (
    "GBIF PRESERVED_SPECIMEN records with StillImage media, country=JP, and fixed regional-proxy circles. "
    "This is candidate availability only; it is not an island assignment, an open-flower confirmation, "
    "a morphological measurement, a pollination observation, or evidence of absence."
)


def clean(value: object) -> str:
    return str(value or "").strip()


def load_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"taxon", "analysis_group", "group_confidence", "role", "trait_candidate", "trait_family", "priority"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError("herbarium cohort manifest is empty or missing required columns")
    names = [clean(row["taxon"]) for row in rows]
    if any(not name for name in names) or len(set(names)) != len(names):
        raise ValueError("manifest taxa must be nonempty and unique")
    return rows


def request_json(url: str) -> tuple[dict[str, object], int]:
    last_error: Exception | None = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
        try:
            with urlopen(request, timeout=60) as response:  # nosec B310 fixed HTTPS API
                return json.load(response), int(response.status)
        except HTTPError as error:
            last_error = error
            if error.code not in RETRYABLE_HTTP or attempt == MAX_ATTEMPTS:
                raise
            retry_after = error.headers.get("Retry-After") if error.headers else None
            delay = float(retry_after) if retry_after and retry_after.replace(".", "", 1).isdigit() else BASE_SLEEP_SECONDS * attempt
            time.sleep(delay)
        except URLError as error:
            last_error = error
            if attempt == MAX_ATTEMPTS:
                raise
            time.sleep(BASE_SLEEP_SECONDS * attempt)
    assert last_error is not None
    raise last_error


def species_match_url(taxon: str) -> str:
    return f"{GBIF_API}/species/match?" + urlencode({"name": taxon, "rank": "SPECIES"})


def occurrence_url(taxon_key: int, offset: int, limit: int) -> str:
    params = {
        "taxon_key": taxon_key,
        "basis_of_record": "PRESERVED_SPECIMEN",
        "media_type": "StillImage",
        "country": "JP",
        "has_coordinate": "true",
        "limit": limit,
        "offset": offset,
    }
    return f"{GBIF_API}/occurrence/search?" + urlencode(params)


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius = 6371.0088
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi, dlambda = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    value = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * radius * math.asin(math.sqrt(value))


def assign_region(latitude: object, longitude: object) -> tuple[str, str, float | None]:
    try:
        lat, lon = float(latitude), float(longitude)
    except (TypeError, ValueError):
        return "", "", None
    matches: list[tuple[float, str]] = []
    for name, (center_lat, center_lon, radius_km) in REGIONS.items():
        distance = haversine_km(lat, lon, center_lat, center_lon)
        if distance <= radius_km:
            matches.append((distance, name))
    if not matches:
        return "", "", None
    distance, name = sorted(matches)[0]
    return name, REGIME_BY_REGION[name], distance


def media_rows(record: dict[str, object]) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    media = record.get("media", [])
    if not isinstance(media, list):
        return output
    for index, item in enumerate(media):
        if not isinstance(item, dict):
            continue
        identifier = clean(item.get("identifier"))
        if not identifier:
            continue
        media_type = clean(item.get("type")) or "StillImage"
        if media_type not in {"StillImage", ""}:
            continue
        output.append({"media_index": str(index), "media_url": identifier, "media_type": media_type})
    return output


def taxon_key_for(name: str) -> tuple[int | None, str, str]:
    url = species_match_url(name)
    data, _ = request_json(url)
    key = data.get("usageKey") or data.get("speciesKey")
    match_type = clean(data.get("matchType"))
    if key is None:
        return None, match_type or "no_key", url
    return int(key), match_type or "matched", url


def fetch_occurrences(taxon_key: int, max_records: int, page_size: int, sleep_seconds: float) -> tuple[list[dict[str, object]], int, int, str]:
    records: list[dict[str, object]] = []
    offset = 0
    total_reported = 0
    last_url = occurrence_url(taxon_key, offset, page_size)
    while len(records) < max_records:
        url = occurrence_url(taxon_key, offset, min(page_size, max_records - len(records)))
        last_url = url
        payload, _ = request_json(url)
        total_reported = int(payload.get("count", 0) or 0)
        results = payload.get("results", [])
        if not isinstance(results, list) or not results:
            break
        records.extend(row for row in results if isinstance(row, dict))
        offset += len(results)
        if offset >= total_reported or len(results) < page_size:
            break
        time.sleep(sleep_seconds)
    return records, total_reported, offset, last_url


def audit(manifest: list[dict[str, str]], max_records: int, page_size: int, max_media_per_record: int, sleep_seconds: float) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    queries: list[dict[str, object]] = []
    candidates: list[dict[str, object]] = []
    summaries: list[dict[str, object]] = []
    for spec in manifest:
        taxon = clean(spec["taxon"])
        timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        try:
            taxon_key, match_status, match_url = taxon_key_for(taxon)
            if taxon_key is None:
                queries.append({
                    **spec, "taxon_key": "", "match_status": match_status, "total_reported": "",
                    "records_requested": max_records, "records_retrieved": 0, "retrieval_status": "no_taxon_key",
                    "http_status": "", "retrieved_at_utc": timestamp, "query_url": match_url, "boundary": BOUNDARY,
                })
                summaries.append({
                    "taxon": taxon, "analysis_group": spec["analysis_group"], "role": spec["role"],
                    "total_gbif_records_retrieved": 0, "records_with_media": 0, "media_candidates_in_region_proxies": 0,
                    "large_bombus_proxy_media": 0, "ardens_proxy_media": 0, "no_bombus_proxy_media": 0,
                    "three_regime_candidate_eligible": "no", "minimum_candidates_per_regime": 2,
                    "next_action": "check_taxon_name_or_synonym", "boundary": BOUNDARY,
                })
                continue
            records, total, retrieved, query_url = fetch_occurrences(taxon_key, max_records, page_size, sleep_seconds)
            queries.append({
                **spec, "taxon_key": taxon_key, "match_status": match_status, "total_reported": total,
                "records_requested": max_records, "records_retrieved": retrieved, "retrieval_status": "retrieved",
                "http_status": 200, "retrieved_at_utc": timestamp, "query_url": query_url, "boundary": BOUNDARY,
            })
        except HTTPError as error:
            records = []
            queries.append({
                **spec, "taxon_key": "", "match_status": "error", "total_reported": "",
                "records_requested": max_records, "records_retrieved": 0, "retrieval_status": f"error:HTTPError:{error.code}",
                "http_status": error.code, "retrieved_at_utc": timestamp, "query_url": "", "boundary": BOUNDARY,
            })
        except (URLError, ValueError, json.JSONDecodeError) as error:
            records = []
            queries.append({
                **spec, "taxon_key": "", "match_status": "error", "total_reported": "",
                "records_requested": max_records, "records_retrieved": 0, "retrieval_status": f"error:{type(error).__name__}",
                "http_status": "", "retrieved_at_utc": timestamp, "query_url": "", "boundary": BOUNDARY,
            })
        media_record_count = 0
        local_candidates: list[dict[str, object]] = []
        for record in records:
            images = media_rows(record)
            if images:
                media_record_count += 1
            region, regime, distance = assign_region(record.get("decimalLatitude"), record.get("decimalLongitude"))
            if not region:
                continue
            for image in images[:max_media_per_record]:
                occurrence_key = clean(record.get("key"))
                local_candidates.append({
                    "candidate_id": f"gbif-{occurrence_key}-{image['media_index']}", "taxon": taxon,
                    "analysis_group": spec["analysis_group"], "group_confidence": spec["group_confidence"],
                    "role": spec["role"], "trait_candidate": spec["trait_candidate"], "trait_family": spec["trait_family"],
                    "priority": spec["priority"], "gbif_occurrence_key": occurrence_key, **image,
                    "region_proxy": region, "regime_proxy": regime,
                    "distance_to_proxy_km": "" if distance is None else f"{distance:.6f}",
                    "decimal_latitude": clean(record.get("decimalLatitude")), "decimal_longitude": clean(record.get("decimalLongitude")),
                    "event_date": clean(record.get("eventDate")), "recorded_by": clean(record.get("recordedBy")),
                    "institution_code": clean(record.get("institutionCode")), "collection_code": clean(record.get("collectionCode")),
                    "catalog_number": clean(record.get("catalogNumber")), "locality": clean(record.get("locality")),
                    "basis_of_record": clean(record.get("basisOfRecord")),
                    "source_url": f"https://www.gbif.org/occurrence/{occurrence_key}", "retrieved_at_utc": timestamp,
                    "boundary": BOUNDARY,
                })
        candidates.extend(local_candidates)
        by_regime = Counter(row["regime_proxy"] for row in local_candidates)
        eligible = all(by_regime[regime] >= 2 for regime in ("large_bombus_proxy", "ardens_proxy", "no_bombus_proxy"))
        summaries.append({
            "taxon": taxon, "analysis_group": spec["analysis_group"], "role": spec["role"],
            "total_gbif_records_retrieved": len(records), "records_with_media": media_record_count,
            "media_candidates_in_region_proxies": len(local_candidates),
            "large_bombus_proxy_media": by_regime["large_bombus_proxy"], "ardens_proxy_media": by_regime["ardens_proxy"],
            "no_bombus_proxy_media": by_regime["no_bombus_proxy"], "three_regime_candidate_eligible": "yes" if eligible else "no",
            "minimum_candidates_per_regime": 2,
            "next_action": "build_blind_sheet_then_human_visibility_audit" if eligible else "retain_as_source_or_specimen_recovery_candidate",
            "boundary": BOUNDARY,
        })
        time.sleep(sleep_seconds)
    return queries, candidates, summaries


def write_csv(path: Path, fields: tuple[str, ...], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--max-records-per-taxon", type=int, default=300)
    parser.add_argument("--page-size", type=int, default=100)
    parser.add_argument("--max-media-per-record", type=int, default=1)
    parser.add_argument("--sleep-seconds", type=float, default=0.25)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.max_records_per_taxon <= 0 or args.page_size <= 0 or args.max_media_per_record <= 0:
        raise SystemExit("record/page/media limits must be positive")
    try:
        manifest = load_manifest(args.manifest)
        queries, candidates, summaries = audit(
            manifest, args.max_records_per_taxon, args.page_size, args.max_media_per_record, args.sleep_seconds
        )
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.output_dir / "gbif_herbarium_queries.csv", QUERY_FIELDS, queries)
    write_csv(args.output_dir / "gbif_herbarium_media_candidates.csv", CANDIDATE_FIELDS, candidates)
    write_csv(args.output_dir / "gbif_herbarium_media_summary.csv", SUMMARY_FIELDS, summaries)
    report = {
        "taxa_audited": len(manifest), "candidate_media_rows": len(candidates),
        "three_regime_candidate_eligible_taxa": sum(row["three_regime_candidate_eligible"] == "yes" for row in summaries),
        "boundary": BOUNDARY,
    }
    (args.output_dir / "gbif_herbarium_media.summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
