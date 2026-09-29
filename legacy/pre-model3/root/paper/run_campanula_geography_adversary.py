#!/usr/bin/env python3
"""Run the Campanula area/connectivity geography adversary audit."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from channel_id.campanula_geography_adversary import run_audit, write_outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--traits", type=Path, default=ROOT / "data" / "inoue_literature_island_traits.csv")
    parser.add_argument("--scaffold", type=Path, default=ROOT / "data" / "design" / "izu_regime_scaffold.csv")
    parser.add_argument("--geography", type=Path, default=ROOT / "data" / "design" / "izu_geography_covariates.csv")
    parser.add_argument("--out-dir", type=Path, default=ROOT / "artifacts" / "campanula_geography_adversary")
    args = parser.parse_args()
    result = run_audit(args.traits, args.scaffold, args.geography)
    write_outputs(args.out_dir, result)
    print(f"best composite: {result['best_composite']}")
    print(args.out_dir / "summary.json")


if __name__ == "__main__":
    main()
