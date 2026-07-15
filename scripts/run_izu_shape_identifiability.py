#!/usr/bin/env python3
"""Run the Izu cline/threshold design-power audit."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from channel_id.regime_shape_identifiability import (
    load_effort,
    load_scaffold,
    run_identifiability_audit,
    write_report,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scaffold",
        type=Path,
        default=Path("data/design/izu_regime_scaffold.csv"),
    )
    parser.add_argument(
        "--effort",
        type=Path,
        default=Path("data/public/izu_occurrence_audit/izu_island_effort.csv"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/izu_shape_identifiability"),
    )
    parser.add_argument("--replicates", type=int, default=300)
    parser.add_argument("--lineages", type=int, default=20)
    parser.add_argument("--seed", type=int, default=20260715)
    args = parser.parse_args()

    report = run_identifiability_audit(
        load_scaffold(args.scaffold),
        load_effort(args.effort),
        replicates=args.replicates,
        lineages=args.lineages,
        seed=args.seed,
    )
    write_report(report, args.output_dir)
    print(json.dumps(report.focus, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
