"""Run the Izu-only interval-aware joint channel profile diagnostic."""
from __future__ import annotations

import argparse
from pathlib import Path

from channel_id.joint_interval_channel_profile import (
    load_izu_records,
    profile_cases,
    render_markdown,
    summarize,
    write_outputs,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("data/inoue_literature_island_traits.csv"))
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        records = load_izu_records(args.input)
        cases, loadings, reference_fits = profile_cases(records)
        report = summarize(cases, loadings, records)
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error
    write_outputs(args.output_dir, records, cases, report, reference_fits)
    (args.output_dir / "JOINT_INTERVAL_CHANNEL_PROFILE.md").write_text(
        render_markdown(report, cases) + "\n", encoding="utf-8"
    )
    print(f"profile cases={len(cases)}; two_stage_hybrid wins={report['profile_wins']['two_stage_hybrid']}")


if __name__ == "__main__":
    main()
