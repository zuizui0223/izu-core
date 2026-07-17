#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from channel_id.threshold_identifiability import load_regimes, run_recovery_audit


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--regimes", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--replicates", type=int, default=5000)
    parser.add_argument("--effect-size", type=float, default=1.0)
    parser.add_argument("--noise-sd", type=float, default=0.6)
    parser.add_argument("--samples-per-regime", type=int, default=20)
    parser.add_argument("--seed", type=int, default=20260717)
    args = parser.parse_args()
    result = run_recovery_audit(load_regimes(args.regimes), replicates=args.replicates, effect_size=args.effect_size, noise_sd=args.noise_sd, samples_per_regime=args.samples_per_regime, seed=args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
