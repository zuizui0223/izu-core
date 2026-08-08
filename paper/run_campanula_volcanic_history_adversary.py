#!/usr/bin/env python3
"""Run the pre-1986 Campanula volcanic-history adversary."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from channel_id.campanula_volcanic_history_adversary import run_audit, write_outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--traits", type=Path, default=ROOT / "data" / "inoue_literature_island_traits.csv")
    parser.add_argument("--history", type=Path, default=ROOT / "data" / "design" / "izu_volcanic_history_pre1986.csv")
    parser.add_argument("--out-dir", type=Path, default=ROOT / "artifacts" / "campanula_volcanic_history_adversary")
    args = parser.parse_args()
    result = run_audit(args.traits, args.history)
    write_outputs(args.out_dir, result)
    for case, payload in result["cases"].items():
        print(f"{case}: best composite={payload['best_composite']}")
    print(args.out_dir / "summary.json")


if __name__ == "__main__":
    main()
