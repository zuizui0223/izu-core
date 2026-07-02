"""Build a non-duplicative GBIF blinded flower-trait review bundle.

Rows with an explicit iNaturalist-republication hint are retained in the GBIF
candidate inventory but excluded from the GBIF review bundle, because a separate
iNaturalist source lane already indexes them. Unflagged does not prove
independence; provenance review remains mandatory.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from channel_id.gbif_photo_review_filter import split_gbif_review_rows
from channel_id.guide_photo_review import ReviewBundleConfig, build_review_bundle, read_proxy_queue, write_review_bundle


def _write_csv(path: Path, rows: list[dict[str, str]], fieldnames: tuple[str, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--proxy-queue", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--target-id", default="campanula_microdonta")
    parser.add_argument("--max-positional-accuracy-m", type=float, default=100.0)
    parser.add_argument("--min-proxy-gap-km", type=float, default=20.0)
    parser.add_argument("--seed", type=int, default=20260702)
    args = parser.parse_args()
    try:
        rows, fieldnames = read_proxy_queue(args.proxy_queue)
        retained, excluded, counts = split_gbif_review_rows(rows)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        _write_csv(args.output_dir / "excluded_iNaturalist_republication_rows.csv", excluded, fieldnames)
        config = ReviewBundleConfig(
            target_id=args.target_id,
            max_positional_accuracy_m=args.max_positional_accuracy_m,
            min_proxy_gap_km=args.min_proxy_gap_km,
            allowed_quality_grades=("HUMAN_OBSERVATION",),
            seed=args.seed,
        )
        geographic, trait_a, trait_b, key = build_review_bundle(retained, config)
        write_review_bundle(args.output_dir, geographic, trait_a, trait_b, key, config)
        lines = [
            "# GBIF source-provenance review audit",
            "",
            f"Input media rows: {counts['input_media_rows']}",
            f"Input unique GBIF records: {counts['input_unique_gbif_records']}",
            f"Excluded obvious iNaturalist republication rows: {counts['excluded_obvious_iNaturalist_republication_rows']}",
            f"Excluded obvious iNaturalist republication records: {counts['excluded_unique_gbif_records']}",
            f"Retained unflagged media rows: {counts['retained_not_flagged_media_rows']}",
            f"Retained unflagged GBIF records: {counts['retained_unique_gbif_records']}",
            "",
            "A row is excluded only when media identifier or reference explicitly names iNaturalist. A retained row is not proven independent; the geographic/taxonomic reviewer must still inspect source provenance and possible overlap before any cross-source evidence is combined.",
        ]
        (args.output_dir / "SOURCE_PROVENANCE_AUDIT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
