#!/usr/bin/env python3
"""Run the prospective dependency x FDQ design simulation."""

from __future__ import annotations

import argparse
from pathlib import Path

from channel_id.dependency_fdq_design_simulation import (
    load_design_config,
    run_design_simulation,
    write_report,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("data/design/dependency_fdq_design_scenarios.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/dependency_fdq_design_simulation/summary.json"),
    )
    args = parser.parse_args()
    config = load_design_config(args.config)
    write_report(args.output, run_design_simulation(config))


if __name__ == "__main__":
    main()
