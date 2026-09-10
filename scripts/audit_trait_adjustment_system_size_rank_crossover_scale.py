from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.audit_trait_adjustment_system_size_rank_crossover import DESIGN, summarize_scale

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--copies", type=int, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    copies_values = [int(v) for v in design["system_size_multipliers"]]
    if args.copies not in copies_values:
        raise ValueError(f"copies={args.copies} not in frozen design")
    seeds = [int(v) for v in design["matching_seeds"]]
    replicates = int(design["realizations_per_seed"])
    rows = [summarize_scale(copies=args.copies, seed=seed, replicates=replicates) for seed in seeds]
    payload = {
        "schema_version": "2.0-scale",
        "design": DESIGN.relative_to(ROOT).as_posix(),
        "copies": args.copies,
        "rows": rows,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
