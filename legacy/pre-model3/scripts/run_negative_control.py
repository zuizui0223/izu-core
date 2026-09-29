#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from channel_id.negative_control import (
    analyse_negative_control,
    leave_one_lineage_out,
    load_contrasts,
    precision_multiplier_audit,
    simulate_refutation_power,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyse specialist-generalist island negative controls")
    parser.add_argument("input")
    parser.add_argument("--output", required=True)
    parser.add_argument("--equivalence-margin", type=float, required=True)
    parser.add_argument("--specialist-effect", type=float, default=-1.0)
    parser.add_argument("--generalist-effect", type=float, default=0.0)
    parser.add_argument("--replicates", type=int, default=2000)
    args = parser.parse_args()

    contrasts = load_contrasts(args.input)
    result = analyse_negative_control(contrasts, equivalence_margin=args.equivalence_margin)
    result["leave_one_lineage_out"] = leave_one_lineage_out(
        contrasts, equivalence_margin=args.equivalence_margin,
    )
    result["refutation_power"] = simulate_refutation_power(
        contrasts,
        equivalence_margin=args.equivalence_margin,
        specialist_effect=args.specialist_effect,
        generalist_effect=args.generalist_effect,
        replicates=args.replicates,
    )
    result["precision_audit"] = precision_multiplier_audit(
        contrasts,
        equivalence_margin=args.equivalence_margin,
        specialist_effect=args.specialist_effect,
        generalist_effect=args.generalist_effect,
        replicates=args.replicates,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
