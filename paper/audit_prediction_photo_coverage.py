"""Screen public photo availability for the prediction-meta specialist holdout.

This is an acquisition audit, not a trait analysis. It queries iNaturalist
research-grade observations with photographs under the same fixed regional
proxies as the blinded-card builder, then asks which *preclassified*
specialist-bee candidate taxa have at least a declared minimum number of
available public photos in all three regime bins:

``MAINLAND`` (large Bombus proxy), ``Oshima`` (ardens proxy), and the pooled
remaining Izu islands (no-Bombus proxy).

Counts are availability metadata only. They are not occurrences, flowering
records, pollinator interactions, or trait scores.
"""
from __future__ import annotations

import argparse
import csv
import json
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REGIONS = {
    "MAINLAND": (34.75, 138.95, 25),
    "Oshima": (34.7385, 139.4024, 8),
    "Toshima": (34.5230, 139.2800, 5),
    "Niijima": (34.3813, 139.2654, 6),
    "Kozushima": (34.2142, 139.1523, 6),
    "Miyake": (34.0854, 139.5213, 8),
    "Hachijo": (33.1025, 139.8077, 8),
}
NO_BOMBUS_REGIONS = frozenset(REGIONS) - {"MAINLAND", "Oshima"}
RAW_FIELDS = (
    "taxon", "functional_group", "confidence", "n_islands", "total_occ", "region",
    "photo_count", "retrieval_status", "http_status", "retrieved_at_utc", "query_url", "boundary",
)
SUMMARY_FIELDS = (
    "taxon", "functional_group", "confidence", "n_islands", "total_occ", "mainland_photo_count",
    "ardens_photo_count", "no_bombus_photo_count", "all_regions_retrieved", "minimum_per_bin",
    "three_regime_photo_eligible", "next_action", "boundary",
)
BOUNDARY = (
    "iNaturalist research-grade photo availability under fixed geographic proxy radii; "
    "not island assignment, flowering confirmation, trait data, pollinator interaction, or absence evidence."
)


def api_url(taxon: str, lat: float, lng: float, radius: float) -> str:
    params = {
        "taxon_name": taxon, "lat": lat, "lng": lng, "radius": radius,
        "quality_grade": "research", "photos": "true", "per_page": 1,
    }
    return "https://api.inaturalist.org/v1/observations?" + urllib.parse.urlencode(params)


def fetch_count(url: str) -> tuple[int, int]:
    request = urllib.request.Request(url, headers={"User-Agent": "izu-predictive-meta-photo-audit/1.0"})
    with urllib.request.urlopen(request, timeout=45) as response:  # nosec B310 fixed HTTPS endpoint
        return int(json.load(response).get("total_results", 0)), int(response.status)


def select_candidates(path: Path, min_islands: int, min_total_occ: int, max_candidates: int) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"name", "functional_group", "confidence", "n_islands", "total_occ"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError("classification table is empty or missing required columns")
    candidates = [
        row for row in rows
        if row["functional_group"] == "specialist_bee"
        and row["confidence"] in {"high", "medium"}
        and int(row["n_islands"]) >= min_islands
        and int(row["total_occ"]) >= min_total_occ
    ]
    candidates.sort(key=lambda row: (-int(row["n_islands"]), -int(row["total_occ"]), row["name"]))
    return candidates[:max_candidates]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--classification", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--min-islands", type=int, default=3)
    parser.add_argument("--min-total-occ", type=int, default=10)
    parser.add_argument("--max-candidates", type=int, default=20)
    parser.add_argument("--minimum-per-bin", type=int, default=2)
    parser.add_argument("--sleep-seconds", type=float, default=0.25)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.minimum_per_bin <= 0 or args.max_candidates <= 0:
        raise SystemExit("minimum-per-bin and max-candidates must be positive")
    try:
        candidates = select_candidates(args.classification, args.min_islands, args.min_total_occ, args.max_candidates)
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error
    raw: list[dict[str, object]] = []
    by_taxon: dict[str, dict[str, object]] = defaultdict(dict)
    for candidate in candidates:
        taxon = candidate["name"]
        for region, (lat, lng, radius) in REGIONS.items():
            url = api_url(taxon, lat, lng, radius)
            timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
            try:
                count, status = fetch_count(url)
                state = "retrieved"
            except Exception as error:  # Record error rather than treating it as zero.
                count, status, state = "", "", f"error:{type(error).__name__}"
            raw.append({
                "taxon": taxon, "functional_group": candidate["functional_group"], "confidence": candidate["confidence"],
                "n_islands": candidate["n_islands"], "total_occ": candidate["total_occ"], "region": region,
                "photo_count": count, "retrieval_status": state, "http_status": status,
                "retrieved_at_utc": timestamp, "query_url": url, "boundary": BOUNDARY,
            })
            by_taxon[taxon][region] = count
            time.sleep(args.sleep_seconds)
    summary: list[dict[str, object]] = []
    for candidate in candidates:
        taxon = candidate["name"]
        counts = by_taxon[taxon]
        retrieved = all(isinstance(counts.get(region), int) for region in REGIONS)
        mainland = counts.get("MAINLAND", "")
        ardens = counts.get("Oshima", "")
        no_bombus = "" if not retrieved else sum(counts[region] for region in NO_BOMBUS_REGIONS)
        eligible = (
            retrieved and mainland >= args.minimum_per_bin and ardens >= args.minimum_per_bin
            and no_bombus >= args.minimum_per_bin
        )
        summary.append({
            "taxon": taxon, "functional_group": candidate["functional_group"], "confidence": candidate["confidence"],
            "n_islands": candidate["n_islands"], "total_occ": candidate["total_occ"],
            "mainland_photo_count": mainland, "ardens_photo_count": ardens, "no_bombus_photo_count": no_bombus,
            "all_regions_retrieved": "yes" if retrieved else "no", "minimum_per_bin": args.minimum_per_bin,
            "three_regime_photo_eligible": "yes" if eligible else "no",
            "next_action": "build_blind_sheet" if eligible else "keep_as_source_recovery_or_replace_photo_cohort",
            "boundary": BOUNDARY,
        })
    args.out_dir.mkdir(parents=True, exist_ok=True)
    raw_path = args.out_dir / "specialist_photo_coverage_raw.csv"
    summary_path = args.out_dir / "specialist_photo_coverage_summary.csv"
    with raw_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=RAW_FIELDS)
        writer.writeheader(); writer.writerows(raw)
    with summary_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SUMMARY_FIELDS)
        writer.writeheader(); writer.writerows(summary)
    report = {
        "candidate_taxa": len(candidates),
        "minimum_per_bin": args.minimum_per_bin,
        "three_regime_photo_eligible": sum(row["three_regime_photo_eligible"] == "yes" for row in summary),
        "boundary": BOUNDARY,
    }
    (args.out_dir / "specialist_photo_coverage.summary.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
