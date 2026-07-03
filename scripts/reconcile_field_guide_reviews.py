"""Reconcile completed first-party field guide-photo reviews."""

from __future__ import annotations

import argparse
from pathlib import Path

from channel_id.field_guide_reconcile import reconcile_field_reviews, write_field_reconciliation
from channel_id.guide_photo_review import read_completed_reviews


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
        geographic, review_a, review_b, key = read_completed_reviews(
            args.geographic_review, args.trait_review_a, args.trait_review_b, args.blind_key
        )
        eligible, summaries, drafts = reconcile_field_reviews(
            geographic, review_a, review_b, key,
            min_units_per_island=args.min_units_per_island,
            maximum_reviewer_score_difference=args.maximum_reviewer_score_difference,
        )
        write_field_reconciliation(args.output_dir, eligible, summaries, drafts)
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
