"""Create a blinded stage-zero audit sheet from public-image feature rows.

This consumes only the feature table with image IDs, taxon labels and image
URLs. It deliberately does not read the separate geographic key. The sheet
records whether an image is an open-flower display that is comparable for the
visual-signature layer; excluded images are not score zero.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

FIELDS = (
    "image_id", "taxon", "analysis_group", "image_url", "feature_status",
    "flowering_state_open_closed_fruit_vegetative_unclear",
    "focal_flower_visible_yes_no_unclear",
    "floral_display_dominance_low_medium_high_unclear",
    "comparable_for_visual_signature_yes_no",
    "reviewer_notes",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--features", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    rows = read_csv(args.features)
    needed = {"image_id", "taxon", "analysis_group", "image_url", "feature_status"}
    if not rows or not needed.issubset(rows[0]):
        raise SystemExit("feature table missing required columns")
    output = []
    for row in rows:
        output.append({
            "image_id": row["image_id"], "taxon": row["taxon"], "analysis_group": row["analysis_group"],
            "image_url": row["image_url"], "feature_status": row["feature_status"],
            "flowering_state_open_closed_fruit_vegetative_unclear": "",
            "focal_flower_visible_yes_no_unclear": "",
            "floral_display_dominance_low_medium_high_unclear": "",
            "comparable_for_visual_signature_yes_no": "",
            "reviewer_notes": "",
        })
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(output)
    print(f"wrote {len(output)} blinded stage-zero rows to {args.out}")


if __name__ == "__main__":
    main()
