"""Build blinded scoring sheets from GBIF herbarium-image candidates.

This is intentionally downstream of `audit_gbif_herbarium_media.py`. The input
still contains region and regime proxy labels; this script separates them into
protected keys and creates per-taxon sheets whose scorer sees only taxon,
image URL and stage-0 visibility fields. No record becomes a morphology value
until a human scores it while the key remains unopened.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

BLIND_FIELDS = (
    "card_id", "taxon", "analysis_group", "trait_candidate", "trait_family", "image_url",
    "source_type", "flowering_state_open_closed_fruit_vegetative_unclear",
    "focal_structure_visible_yes_no_unclear", "scale_or_reference_present_yes_no_unclear",
    "comparable_for_predeclared_trait_yes_no", "trait_score_if_eligible", "reviewer_notes",
)
KEY_FIELDS = (
    "card_id", "taxon", "candidate_id", "gbif_occurrence_key", "region_proxy", "regime_proxy",
    "distance_to_proxy_km", "decimal_latitude", "decimal_longitude", "event_date", "recorded_by",
    "institution_code", "collection_code", "catalog_number", "locality", "source_url",
)
SUMMARY_FIELDS = (
    "taxon", "analysis_group", "trait_candidate", "candidate_large_bombus", "candidate_ardens",
    "candidate_no_bombus", "selected_large_bombus", "selected_ardens", "selected_no_bombus",
    "min_per_regime", "max_per_regime", "sheet_created", "reason",
)
REGIMES = ("large_bombus_proxy", "ardens_proxy", "no_bombus_proxy")


def clean(value: object) -> str:
    return str(value or "").strip()


def read_candidates(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {
        "candidate_id", "taxon", "analysis_group", "trait_candidate", "trait_family", "media_url",
        "gbif_occurrence_key", "region_proxy", "regime_proxy", "source_url",
    }
    if not rows or not required.issubset(rows[0]):
        raise ValueError("candidate table is empty or missing required columns")
    ids = [clean(row["candidate_id"]) for row in rows]
    if any(not value for value in ids) or len(set(ids)) != len(ids):
        raise ValueError("candidate_id must be nonempty and unique")
    return rows


def choose_cards(rows: list[dict[str, str]], min_per_regime: int, max_per_regime: int, seed: int) -> tuple[list[dict[str, str]], list[dict[str, object]]]:
    by_taxon: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if clean(row["regime_proxy"]) in REGIMES and clean(row["media_url"]):
            by_taxon[clean(row["taxon"])].append(row)
    sheets: list[dict[str, str]] = []
    summary: list[dict[str, object]] = []
    card_serial = 1
    for taxon in sorted(by_taxon):
        pool = by_taxon[taxon]
        regime_counts = Counter(clean(row["regime_proxy"]) for row in pool)
        eligible = all(regime_counts[regime] >= min_per_regime for regime in REGIMES)
        if not eligible:
            summary.append({
                "taxon": taxon, "analysis_group": clean(pool[0]["analysis_group"]),
                "trait_candidate": clean(pool[0]["trait_candidate"]),
                "candidate_large_bombus": regime_counts[REGIMES[0]], "candidate_ardens": regime_counts[REGIMES[1]],
                "candidate_no_bombus": regime_counts[REGIMES[2]], "selected_large_bombus": 0,
                "selected_ardens": 0, "selected_no_bombus": 0, "min_per_regime": min_per_regime,
                "max_per_regime": max_per_regime, "sheet_created": "no",
                "reason": "insufficient candidate media in one or more proxy regimes",
            })
            continue
        selected: list[dict[str, str]] = []
        for regime_index, regime in enumerate(REGIMES):
            choices = [row for row in pool if clean(row["regime_proxy"]) == regime]
            choices.sort(key=lambda row: clean(row["candidate_id"]))
            rng = random.Random(seed + regime_index + sum(ord(char) for char in taxon))
            rng.shuffle(choices)
            selected.extend(choices[:max_per_regime])
        for row in selected:
            row = dict(row)
            row["card_id"] = f"herbarium-{card_serial:04d}"
            card_serial += 1
            sheets.append(row)
        selected_counts = Counter(clean(row["regime_proxy"]) for row in selected)
        summary.append({
            "taxon": taxon, "analysis_group": clean(pool[0]["analysis_group"]),
            "trait_candidate": clean(pool[0]["trait_candidate"]),
            "candidate_large_bombus": regime_counts[REGIMES[0]], "candidate_ardens": regime_counts[REGIMES[1]],
            "candidate_no_bombus": regime_counts[REGIMES[2]], "selected_large_bombus": selected_counts[REGIMES[0]],
            "selected_ardens": selected_counts[REGIMES[1]], "selected_no_bombus": selected_counts[REGIMES[2]],
            "min_per_regime": min_per_regime, "max_per_regime": max_per_regime, "sheet_created": "yes",
            "reason": "eligible candidate pool; key must remain unopened during scoring",
        })
    return sheets, summary


def write_taxon_sheets(output_dir: Path, selected: list[dict[str, str]]) -> None:
    by_taxon: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in selected:
        by_taxon[clean(row["taxon"])].append(row)
    for taxon, rows in by_taxon.items():
        slug = "_".join(taxon.lower().split())
        blind_path = output_dir / f"{slug}_herbarium_blind.csv"
        key_path = output_dir / f"{slug}_herbarium_key.csv"
        with blind_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=BLIND_FIELDS)
            writer.writeheader()
            for row in rows:
                writer.writerow({
                    "card_id": row["card_id"], "taxon": row["taxon"], "analysis_group": row["analysis_group"],
                    "trait_candidate": row["trait_candidate"], "trait_family": row["trait_family"],
                    "image_url": row["media_url"], "source_type": "GBIF_preserved_specimen",
                    "flowering_state_open_closed_fruit_vegetative_unclear": "",
                    "focal_structure_visible_yes_no_unclear": "",
                    "scale_or_reference_present_yes_no_unclear": "",
                    "comparable_for_predeclared_trait_yes_no": "",
                    "trait_score_if_eligible": "", "reviewer_notes": "",
                })
        with key_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=KEY_FIELDS)
            writer.writeheader()
            for row in rows:
                writer.writerow({field: row.get(field, "") for field in KEY_FIELDS})


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--min-per-regime", type=int, default=2)
    parser.add_argument("--max-per-regime", type=int, default=6)
    parser.add_argument("--seed", type=int, default=20260704)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.min_per_regime <= 0 or args.max_per_regime < args.min_per_regime:
        raise SystemExit("max-per-regime must be at least min-per-regime and both must be positive")
    try:
        candidates = read_candidates(args.candidates)
        selected, summary = choose_cards(candidates, args.min_per_regime, args.max_per_regime, args.seed)
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_taxon_sheets(args.output_dir, selected)
    with (args.output_dir / "herbarium_blind_sheet_summary.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SUMMARY_FIELDS)
        writer.writeheader(); writer.writerows(summary)
    (args.output_dir / "HERBARIUM_BLIND_SCORING_INSTRUCTIONS.txt").write_text(
        "Score only *_herbarium_blind.csv files. Do not open the matching *_herbarium_key.csv until all stage-0 fields and trait scores are complete. "
        "An image must show an open flower, the predeclared focal structure, and a usable scale/reference before it can receive a trait score. Missing visibility is not score zero.\n",
        encoding="utf-8",
    )
    print(json.dumps({"selected_cards": len(selected), "taxa_with_sheets": sum(row["sheet_created"] == "yes" for row in summary)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
