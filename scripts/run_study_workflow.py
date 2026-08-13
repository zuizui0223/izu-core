#!/usr/bin/env python3
from __future__ import annotations

import argparse

from channel_id.study_workflow import run_workflow


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and analyse small-regime summary data.")
    parser.add_argument("input", help="CSV containing channel-level summary statistics")
    parser.add_argument("--output", default="results/study_workflow.json")
    parser.add_argument("--replicates", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=20260717)
    args = parser.parse_args()
    result = run_workflow(args.input, args.output, replicates=args.replicates, seed=args.seed)
    if result["status"] != "ok":
        for error in result["errors"]:
            print(f"ERROR: {error}")
        raise SystemExit(2)
    print(f"wrote {args.output}")
    for channel, payload in result["channels"].items():
        print(f"{channel}: {payload['selected_shape']}")


if __name__ == "__main__":
    main()
