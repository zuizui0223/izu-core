#!/usr/bin/env python3
"""Validate the frozen Campanula channel-shape and prospective contracts."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from channel_id.prediction_contract_lock import validate_contract_bundle

ROOT = Path(__file__).resolve().parent.parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--shape",
        type=Path,
        default=ROOT / "data/predictive_meta/campanula_channel_shape_v1.csv",
    )
    parser.add_argument(
        "--scenario",
        type=Path,
        default=ROOT / "data/predictive_meta/two_breakpoint_prediction_contract.csv",
    )
    parser.add_argument(
        "--image",
        type=Path,
        default=ROOT / "data/predictive_meta/public_visual_signature_contract.csv",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = validate_contract_bundle(args.shape, args.scenario, args.image)
    print(json.dumps({
        "status": "ok",
        "contract_version": result.version,
        "shape_rows": result.shape_rows,
        "scenario_rows_checked": result.scenario_rows_checked,
        "image_rows_checked": result.image_rows_checked,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
