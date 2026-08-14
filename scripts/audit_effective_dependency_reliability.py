#!/usr/bin/env python3
"""Audit repeated final dependency estimates for calibration-scope reliability."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from channel_id.effective_dependency_reliability import build_dependency_reliability_audit


def read_rows(path: Path) -> tuple[dict[str, str], ...]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return tuple(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Audit independent repeat blocks of the final direct reproductive-dependency estimand. "
            "Technical SVD recounts and within-plant repeats are not accepted substitutes."
        )
    )
    parser.add_argument("input", type=Path, help="Repeated final-dependency calibration CSV")
    parser.add_argument("--output", type=Path, default=Path("effective_dependency_reliability_audit.json"))
    args = parser.parse_args()

    result = build_dependency_reliability_audit(read_rows(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
