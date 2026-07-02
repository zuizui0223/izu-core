"""Audit how Inoue 1986 visitor-rate evidence supports model regime inputs."""

from __future__ import annotations

import argparse
from pathlib import Path

from channel_id.pollinator_regime_evidence_audit import (
    build_audit,
    load_effort_rows,
    load_model_indicators,
    load_rate_rows,
    write_audit,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-indicators", type=Path, default=Path("data/inoue_literature_island_traits.csv"))
    parser.add_argument("--pollinator-rates", type=Path, default=Path("data/two_breakpoint_evidence/inoue1986_pollinator_rates.csv"))
    parser.add_argument("--observation-effort", type=Path, default=Path("data/two_breakpoint_evidence/inoue1986_observation_effort.csv"))
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()
    try:
        audit = build_audit(
            load_model_indicators(args.model_indicators),
            load_rate_rows(args.pollinator_rates),
            load_effort_rows(args.observation_effort),
        )
        write_audit(args.output_csv, args.output_md, audit)
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
