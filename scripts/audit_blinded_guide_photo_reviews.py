"""Create an audit ledger for completed blinded guide-photo reviews.

The ledger is an unblinded administrative record. It explains every exclusion,
reports descriptive agreement, and lists units eligible only for later manual
biological confirmation. It never edits model constraints.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from channel_id.guide_photo_review import read_completed_reviews
from channel_id.guide_review_audit import AGREEMENT_COLUMNS, UNIT_AUDIT_COLUMNS, audit_completed_reviews


def _write_csv(path: Path, fields: tuple[str, ...], rows: tuple[dict[str, str], ...]) -> None:
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
    parser.add_argument("--maximum-reviewer-score-difference", type=int, default=1)
    args = parser.parse_args()
    try:
        geographic, review_a, review_b, key = read_completed_reviews(
            args.geographic_review,
            args.trait_review_a,
            args.trait_review_b,
            args.blind_key,
        )
        audit = audit_completed_reviews(
            geographic,
            review_a,
            review_b,
            key,
            maximum_reviewer_score_difference=args.maximum_reviewer_score_difference,
        )
        args.output_dir.mkdir(parents=True, exist_ok=True)
        _write_csv(args.output_dir / "review_unit_decision_ledger.csv", UNIT_AUDIT_COLUMNS, audit.unit_rows)
        _write_csv(args.output_dir / "review_agreement_and_exclusion_summary.csv", AGREEMENT_COLUMNS, audit.agreement_rows)
        lines = [
            "# Blinded guide-photo review audit",
            "",
            f"Keyed source-record units: {len(audit.unit_rows)}",
            f"Eligible only for manual constraint review: {len(audit.eligible_observation_unit_ids)}",
            "",
            "The decision ledger is unblinded and documents geographic/taxon gates, reviewer-ID independence, trait scoring gates, score differences, and exclusion codes.",
            "",
            "No file in this directory changes `data/guide_direction_constraints.csv`. A unit marked eligible remains a public-photo observation that needs source-unit and biological confirmation before any manual model update.",
        ]
        (args.output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
