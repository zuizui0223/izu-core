#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from channel_id.seychelles_joint_linkage import build_report, load_joint_rows

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Seychelles individual-level exposure/dependency overlap.")
    parser.add_argument(
        "--input",
        type=Path,
        default=ROOT / "data/predictive_meta/seychelles_thespesia_joint_plant.csv",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "data/results/seychelles_individual_joint_audit.json",
    )
    args = parser.parse_args()
    report = build_report(load_joint_rows(args.input))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report["decision"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
