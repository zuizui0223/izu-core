"""Generate a next-action and island-readiness report for guide-photo reviews."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from channel_id.guide_photo_review import read_completed_reviews
from channel_id.guide_review_audit import audit_completed_reviews
from channel_id.guide_review_progress import (
    ISLAND_PROGRESS_COLUMNS,
    UNIT_PROGRESS_COLUMNS,
    build_guide_review_progress,
)


def _write(path: Path, fields: tuple[str, ...], rows: tuple[dict[str, str], ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--geographic-review", type=Path, required=True)
    parser.add_argument("--trait-review-a", type=Path, required=True)
    parser.add_argument("--trait-review-b", type=Path, required=True)
    parser.add_argument("--blind-key", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--min-units-per-island", type=int, default=3)
    parser.add_argument("--maximum-reviewer-score-difference", type=int, default=1)
    args = parser.parse_args()
    try:
        geographic, a, b, key = read_completed_reviews(
            args.geographic_review, args.trait_review_a, args.trait_review_b, args.blind_key
        )
        audit = audit_completed_reviews(
            geographic, a, b, key,
            maximum_reviewer_score_difference=args.maximum_reviewer_score_difference,
        )
        progress = build_guide_review_progress(audit, min_units_per_island=args.min_units_per_island)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        _write(args.output_dir / "guide_review_next_actions.csv", UNIT_PROGRESS_COLUMNS, progress.unit_rows)
        _write(args.output_dir / "guide_review_island_readiness.csv", ISLAND_PROGRESS_COLUMNS, progress.island_rows)
        lines = [
            "# Blinded guide-photo review progress", "",
            "Island counts start only after accepted geographic and taxonomic review. Proxy candidates are not counted.",
            "",
            "| island | verified units | awaiting trait review | eligible units | eligible shortfall | potential shortfall | readiness |",
            "|---|---:|---:|---:|---:|---:|---|",
        ]
        for row in progress.island_rows:
            lines.append(
                f"| {row['island_id']} | {row['verified_geographic_taxon_units']} | "
                f"{row['awaiting_trait_review_units']} | {row['eligible_for_manual_constraint_review_units']} | "
                f"{row['eligible_shortfall']} | {row['potential_shortfall_if_all_pending_pass']} | {row['readiness_status']} |"
            )
        lines.extend((
            "", "No row here updates guide constraints. `ready_for_manual_pairwise_direction_check` means only that one island has reached the review-unit threshold; pairwise biological confirmation remains separate.",
        ))
        (args.output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
