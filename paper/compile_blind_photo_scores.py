"""Join a completed blinded photo sheet to its hidden regional key.

This is deliberately a one-way compilation step. The scorer works from the
blind sheet only; after human scoring is complete, this script joins card IDs to
the protected key and writes C-rank ordinal observations in the common
prediction-meta schema. It refuses missing stage-0 eligibility fields and
never interprets an unscored card as zero.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


REGIME_BY_REGION = {
    "MAINLAND": "large_bombus",
    "Oshima": "ardens",
    "Toshima": "no_bombus",
    "Niijima": "no_bombus",
    "Kozushima": "no_bombus",
    "Miyake": "no_bombus",
    "Hachijo": "no_bombus",
}
OUTPUT_FIELDS = (
    "observation_id", "analysis_partition", "lineage_id", "taxon", "analysis_group",
    "group_confidence", "trait_id", "trait_family", "pollinator_regime", "value",
    "value_unit", "evidence_tier", "source_locator", "review_status", "weight", "notes",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def require_columns(rows: list[dict[str, str]], columns: set[str], label: str) -> None:
    if not rows:
        raise ValueError(f"{label} is empty")
    missing = sorted(columns - set(rows[0]))
    if missing:
        raise ValueError(f"{label} is missing columns: {', '.join(missing)}")


def clean(value: object) -> str:
    return str(value or "").strip()


def manifest_row(path: Path, taxon: str) -> dict[str, str]:
    rows = read_csv(path)
    require_columns(rows, {
        "taxon", "analysis_group", "group_confidence", "trait_id", "trait_family",
        "trait_definition_id", "trait_definition", "requires_interior_visible",
        "minimum_score", "maximum_score", "analysis_partition",
    }, "photo cohort manifest")
    matches = [row for row in rows if clean(row["taxon"]) == taxon]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one manifest row for {taxon!r}, found {len(matches)}")
    return matches[0]


def compile_sheet(
    blind_path: Path,
    key_path: Path,
    manifest_path: Path,
    taxon: str,
) -> tuple[list[dict[str, str]], dict[str, int]]:
    spec = manifest_row(manifest_path, taxon)
    blind_rows = read_csv(blind_path)
    key_rows = read_csv(key_path)
    require_columns(blind_rows, {
        "card_id", "image_url", "flowering_state_open_closed_fruit_vegetative_unclear",
        "focal_flower_visible_yes_no_unclear", "interior_visible_yes_no_na",
        "comparable_for_predeclared_trait_yes_no", "trait_definition_id",
        "trait_score_if_eligible", "reviewer_notes",
    }, "blind scoring sheet")
    require_columns(key_rows, {"card_id", "region", "obs_id"}, "hidden key")
    key_by_card = {clean(row["card_id"]): row for row in key_rows}
    if len(key_by_card) != len(key_rows):
        raise ValueError("hidden key contains duplicate card_id")

    lower = float(clean(spec["minimum_score"]))
    upper = float(clean(spec["maximum_score"]))
    requires_interior = clean(spec["requires_interior_visible"]).lower() == "yes"
    output: list[dict[str, str]] = []
    counts = {"cards_total": len(blind_rows), "eligible": 0, "scored": 0, "excluded": 0}
    for row in blind_rows:
        card_id = clean(row["card_id"])
        if card_id not in key_by_card:
            raise ValueError(f"blind card has no hidden key row: {card_id}")
        region = clean(key_by_card[card_id]["region"])
        if region not in REGIME_BY_REGION:
            raise ValueError(f"unknown region in key: {region!r}")
        comparable = clean(row["comparable_for_predeclared_trait_yes_no"]).lower()
        focal = clean(row["focal_flower_visible_yes_no_unclear"]).lower()
        flowering = clean(row["flowering_state_open_closed_fruit_vegetative_unclear"]).lower()
        interior = clean(row["interior_visible_yes_no_na"]).lower()
        eligible = comparable == "yes" and focal == "yes" and flowering == "open" and (not requires_interior or interior == "yes")
        score_text = clean(row["trait_score_if_eligible"])
        recorded_definition = clean(row["trait_definition_id"])
        if recorded_definition and recorded_definition != clean(spec["trait_definition_id"]):
            raise ValueError(f"{card_id}: trait_definition_id does not match manifest")
        if not eligible:
            counts["excluded"] += 1
            if score_text:
                raise ValueError(f"{card_id}: an ineligible card must not have a trait score")
            continue
        counts["eligible"] += 1
        if not score_text:
            continue
        try:
            score = float(score_text)
        except ValueError as error:
            raise ValueError(f"{card_id}: trait score must be numeric") from error
        if not lower <= score <= upper:
            raise ValueError(f"{card_id}: score {score} outside declared range [{lower}, {upper}]")
        counts["scored"] += 1
        lineage = taxon.lower().replace(" ", "_")
        output.append({
            "observation_id": f"photo-{lineage}-{card_id}",
            "analysis_partition": clean(spec["analysis_partition"]),
            "lineage_id": lineage,
            "taxon": taxon,
            "analysis_group": clean(spec["analysis_group"]),
            "group_confidence": clean(spec["group_confidence"]),
            "trait_id": clean(spec["trait_id"]),
            "trait_family": clean(spec["trait_family"]),
            "pollinator_regime": REGIME_BY_REGION[region],
            "value": f"{score:.12g}",
            "value_unit": "ordinal_score",
            "evidence_tier": "ordinal_blind_photo",
            "source_locator": f"{blind_path.name}:{card_id}; {key_path.name}:{card_id}",
            "review_status": "blinded_score_joined_pending_audit",
            "weight": "1",
            "notes": "Trait was scored before region key join. " + clean(row["reviewer_notes"]),
        })
    return output, counts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blind", required=True, type=Path)
    parser.add_argument("--key", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--taxon", required=True)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--audit-out", type=Path, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        rows, counts = compile_sheet(args.blind, args.key, args.manifest, args.taxon)
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader(); writer.writerows(rows)
    audit = {"taxon": args.taxon, **counts, "output_rows": len(rows)}
    if args.audit_out is not None:
        args.audit_out.parent.mkdir(parents=True, exist_ok=True)
        args.audit_out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(audit, ensure_ascii=False))


if __name__ == "__main__":
    main()
