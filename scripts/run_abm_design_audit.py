#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from channel_id.abm_design_audit import run_design_audit


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank synthetic Izu observation designs")
    parser.add_argument("--target-accuracy", type=float, default=0.70)
    parser.add_argument("--reference-replicates", type=int, default=8)
    parser.add_argument("--test-replicates", type=int, default=10)
    parser.add_argument("--generations", type=int, default=45)
    parser.add_argument("--founders", type=int, default=120)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run_design_audit(
        target_accuracy=args.target_accuracy,
        reference_replicates=args.reference_replicates,
        test_replicates=args.test_replicates,
        generations=args.generations,
        founders=args.founders,
        seed=args.seed,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")


if __name__ == "__main__":
    main()
