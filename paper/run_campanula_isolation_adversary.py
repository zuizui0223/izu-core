#!/usr/bin/env python3
"""Run the Campanula mainland-isolation adversary audit."""
from __future__ import annotations

import argparse
from pathlib import Path

from channel_id.campanula_isolation_adversary import run_audit, write_outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--traits",
        type=Path,
        default=Path("data/inoue_literature_island_traits.csv"),
        help="Source-locked Campanula island trait table.",
    )
    parser.add_argument(
        "--scaffold",
        type=Path,
        default=Path("data/design/izu_regime_scaffold.csv"),
        help="Frozen Izu geographic/regime scaffold.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("artifacts/campanula_isolation_adversary"),
    )
    args = parser.parse_args()
    result = run_audit(args.traits, args.scaffold)
    write_outputs(args.out_dir, result)
    print(f"best composite: {result['best_composite']}")
    print(args.out_dir / "summary.json")


if __name__ == "__main__":
    main()
