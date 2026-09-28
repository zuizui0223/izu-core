"""Build blinded photo sheets for all predeclared prediction-test cohorts.

This runner is a data-acquisition helper, not a scoring or inference step. It
uses the existing `build_photo_scoring_sheet.py` script and retains the hidden
key separately from the blind sheet. The manifest fixes each taxon's analysis
group and trait definition before any regional scores are joined.
"""
from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--per-region", type=int, default=6)
    parser.add_argument("--seed", type=int, default=20260704)
    parser.add_argument("--output-dir", type=Path, default=HERE / "photo_sheets")
    parser.add_argument("--taxon", action="append", default=[], help="Optional exact taxon filter; repeatable.")
    return parser.parse_args()


def load_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"taxon", "trait_definition_id", "analysis_group", "trait_family"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError("manifest is empty or missing required columns")
    if len({row["taxon"] for row in rows}) != len(rows):
        raise ValueError("manifest has duplicate taxon rows")
    return rows


def main() -> None:
    args = parse_args()
    if args.per_region <= 0:
        raise SystemExit("--per-region must be positive")
    try:
        rows = load_manifest(args.manifest)
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error
    selected = [row for row in rows if not args.taxon or row["taxon"] in set(args.taxon)]
    missing = sorted(set(args.taxon) - {row["taxon"] for row in selected})
    if missing:
        raise SystemExit("unknown --taxon: " + ", ".join(missing))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for index, row in enumerate(selected):
        command = [
            sys.executable, str(HERE / "build_photo_scoring_sheet.py"), row["taxon"],
            "--per-region", str(args.per_region),
            "--seed", str(args.seed + index),
        ]
        print("running:", " ".join(command))
        subprocess.run(command, check=True)
    shutil.copyfile(args.manifest, args.output_dir / "photo_cohort_manifest.csv")
    (args.output_dir / "PREDICTIVE_META_REVIEW.txt").write_text(
        "Score blind sheets without opening *_key.csv. Use the matching manifest row "
        "to predeclare the trait definition. Join only after scoring with "
        "paper/compile_blind_photo_scores.py.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
