#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from channel_id.virtual_izu_abm import SCENARIOS, run_abm


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the minimal synthetic Izu plant ABM")
    parser.add_argument("--scenario", choices=sorted(SCENARIOS), required=True)
    parser.add_argument("--generations", type=int, default=80)
    parser.add_argument("--founders", type=int, default=180)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    result = run_abm(
        scenario=args.scenario,
        generations=args.generations,
        founders=args.founders,
        seed=args.seed,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
