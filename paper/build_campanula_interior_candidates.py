"""Build an expanded blind Campanula inner-corolla calibration cohort.

The live acquisition queries research-grade iNaturalist observations separately
for Oshima and no-Bombus islands. Every attached photo is considered; four
previously reviewed, interior-ineligible photo IDs are excluded. Blind cards and
the regional key are written to separate directories.
"""
from __future__ import annotations

import argparse
import csv
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from channel_id.campanula_interior_candidates import (
    KNOWN_INELIGIBLE_PHOTO_IDS,
    REGIONS,
    flatten_observations,
    select_and_blind,
)

BLIND_FIELDS = (
    "card_id", "image_url", "flowering_state", "focal_flower_visible",
    "interior_visible", "comparable_for_guide_score", "trait_definition_id",
    "guide_score_0_3", "reviewer_notes",
)
KEY_FIELDS = (
    "card_id", "region", "pollinator_regime", "obs_id", "photo_id", "photo_index",
)
AUDIT_FIELDS = (
    "region", "pollinator_regime", "query_url", "retrieved_at_utc",
    "observations_returned", "photos_recovered_before_exclusion", "candidate_photos_after_exclusion",
    "status", "error",
)


def fetch_region(region: str, config: dict[str, object], per_page: int) -> tuple[list[dict[str, object]], str]:
    params = {
        "taxon_name": "Campanula microdonta",
        "lat": config["lat"],
        "lng": config["lng"],
        "radius": config["radius"],
        "quality_grade": "research",
        "photos": "true",
        "per_page": per_page,
        "order_by": "created_at",
        "order": "desc",
    }
    url = "https://api.inaturalist.org/v1/observations?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"User-Agent": "izu-core-campanula-interior/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:  # nosec B310 fixed HTTPS API
        payload = json.load(response)
    return list(payload.get("results") or []), url


def write_csv(path: Path, fields: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blind-dir", type=Path, required=True)
    parser.add_argument("--key-dir", type=Path, required=True)
    parser.add_argument("--per-page", type=int, default=100)
    parser.add_argument("--per-region", type=int, default=24)
    parser.add_argument("--seed", type=int, default=20260710)
    parser.add_argument("--sleep-seconds", type=float, default=0.4)
    args = parser.parse_args()
    if not 1 <= args.per_page <= 200:
        raise SystemExit("--per-page must be between 1 and 200")
    if args.per_region <= 0 or args.sleep_seconds < 0:
        raise SystemExit("invalid per-region or sleep-seconds")

    all_rows: list[dict[str, str]] = []
    audit: list[dict[str, str]] = []
    for region, config in REGIONS.items():
        timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        try:
            observations, url = fetch_region(region, config, args.per_page)
            raw_photo_count = sum(len(row.get("photos") or []) for row in observations)
            candidates = flatten_observations(
                observations, region=region, regime=str(config["regime"])
            )
            all_rows.extend(candidates)
            audit.append({
                "region": region,
                "pollinator_regime": str(config["regime"]),
                "query_url": url,
                "retrieved_at_utc": timestamp,
                "observations_returned": str(len(observations)),
                "photos_recovered_before_exclusion": str(raw_photo_count),
                "candidate_photos_after_exclusion": str(len(candidates)),
                "status": "ok",
                "error": "",
            })
        except Exception as error:
            audit.append({
                "region": region,
                "pollinator_regime": str(config["regime"]),
                "query_url": "",
                "retrieved_at_utc": timestamp,
                "observations_returned": "0",
                "photos_recovered_before_exclusion": "0",
                "candidate_photos_after_exclusion": "0",
                "status": "error",
                "error": type(error).__name__,
            })
        time.sleep(args.sleep_seconds)

    blind, key = select_and_blind(all_rows, per_region=args.per_region, seed=args.seed)
    write_csv(args.blind_dir / "campanula_interior_candidates_blind.csv", BLIND_FIELDS, blind)
    write_csv(args.blind_dir / "query_audit.csv", AUDIT_FIELDS, audit)
    write_csv(args.key_dir / "campanula_interior_candidates_key.csv", KEY_FIELDS, key)
    (args.blind_dir / "candidate_summary.json").write_text(json.dumps({
        "cards": len(blind),
        "regions_queried": len(REGIONS),
        "known_ineligible_photo_ids_excluded": sorted(KNOWN_INELIGIBLE_PHOTO_IDS),
        "boundary": "Blind cards contain no geography. The separate key must not be opened before stage-0 and guide scores are frozen.",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"cards": len(blind), "queries_ok": sum(row["status"] == "ok" for row in audit)}))


if __name__ == "__main__":
    main()
