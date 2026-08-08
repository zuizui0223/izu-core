#!/usr/bin/env python3
"""Run the B-grade source-native directional evidence audit."""
from __future__ import annotations

import argparse
from pathlib import Path

from channel_id.source_native_directional_holdout import run_audit, write_report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--directional",
        type=Path,
        default=Path("data/predictive_meta/source_native_directional_holdout.csv"),
    )
    parser.add_argument(
        "--native",
        type=Path,
        default=Path("data/predictive_meta/primary_source_native_evidence.csv"),
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("artifacts/source_native_directional_holdout/report.json"),
    )
    args = parser.parse_args()
    report = run_audit(args.directional, args.native)
    write_report(args.out, report)
    summary = report["summary"]
    print(f"directional lineages: {summary['n_lineages']}")
    print(f"shared-step support: {len(summary['shared_second_step_support_lineages'])}")
    print(f"status: {summary['universal_shared_second_step_status']}")
    print(args.out)


if __name__ == "__main__":
    main()
