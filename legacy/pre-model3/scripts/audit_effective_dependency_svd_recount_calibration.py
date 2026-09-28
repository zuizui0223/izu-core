#!/usr/bin/env python3
"""Audit blinded technical recount repeatability for SVD pollen counts."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from channel_id.effective_dependency_measurement_calibration import build_svd_recount_calibration


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recounts", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        with args.recounts.open(newline="", encoding="utf-8") as handle:
            rows = tuple(csv.DictReader(handle))
        result = build_svd_recount_calibration(rows)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
