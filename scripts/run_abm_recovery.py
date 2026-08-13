#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
from pathlib import Path

from channel_id.abm_recovery import ObservationDesign, run_recovery_benchmark


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark recovery of synthetic Izu ABM worlds.")
    parser.add_argument("--output", required=True)
    parser.add_argument("--reference-replicates", type=int, default=8)
    parser.add_argument("--test-replicates", type=int, default=10)
    parser.add_argument("--generations", type=int, default=50)
    parser.add_argument("--founders", type=int, default=120)
    parser.add_argument("--island-fraction", type=float, default=1.0)
    parser.add_argument("--missing-rate", type=float, default=0.0)
    parser.add_argument("--measurement-sd", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()

    result = run_recovery_benchmark(
        reference_replicates=args.reference_replicates,
        test_replicates=args.test_replicates,
        generations=args.generations,
        founders=args.founders,
        design=ObservationDesign(
            island_fraction=args.island_fraction,
            missing_rate=args.missing_rate,
            measurement_sd=args.measurement_sd,
        ),
        seed=args.seed,
    )
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "output": str(path),
        "overall_accuracy": result["overall_accuracy"],
        "dominant_confusions": result["dominant_confusions"][:3],
    }, indent=2))


if __name__ == "__main__":
    main()
