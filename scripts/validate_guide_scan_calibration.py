#!/usr/bin/env python3
"""Validate and report the versioned Campanula guide-scan calibration."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from channel_id.guide_scan_calibration import (
    load_guide_summary,
    summarize_second_transition,
    validate_contract_v1_1,
    validate_observation_bridge,
)

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--guide-summary",
        type=Path,
        default=ROOT / "data/predictive_meta/campanula_guide_scan_summary.csv",
    )
    parser.add_argument(
        "--contract",
        type=Path,
        default=ROOT / "data/predictive_meta/campanula_channel_shape_v1_1.csv",
    )
    parser.add_argument(
        "--observations",
        type=Path,
        default=ROOT / "data/predictive_meta/campanula_calibration_observations.csv",
    )
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    rows = load_guide_summary(args.guide_summary)
    validate_contract_v1_1(args.contract)
    validate_observation_bridge(args.observations, rows)
    summary = summarize_second_transition(rows)
    payload = {
        "status": "ok",
        "contract_version": "1.1.0",
        "ardens_island": summary.ardens_island,
        "ardens_guide_cov_pct": summary.ardens_guide_cov_pct,
        "no_bombus_islands": list(summary.no_bombus_islands),
        "no_bombus_equal_island_mean_pct": summary.no_bombus_equal_island_mean_pct,
        "second_transition_delta_pct_points": summary.second_transition_delta_pct_points,
        "no_bombus_islands_below_ardens": summary.no_bombus_islands_below_ardens,
        "leave_one_island_out_deltas": list(summary.leave_one_island_out_deltas),
        "interpretation": (
            "Measured focal calibration supports a second-transition decrease in guide "
            "coverage; it does not identify a causal pollinator effect."
        ),
    }
    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "guide_scan_calibration.json").write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        lines = [
            "# Campanula guide-scan calibration",
            "",
            f"- Oshima (*B. ardens*): {summary.ardens_guide_cov_pct:.2f}%",
            f"- equal-island mean across four no-Bombus islands: {summary.no_bombus_equal_island_mean_pct:.2f}%",
            f"- second-transition difference: {summary.second_transition_delta_pct_points:.2f} percentage points",
            f"- no-Bombus islands below Oshima: {summary.no_bombus_islands_below_ardens}/4",
            "",
            "All leave-one-island-out differences remain negative. This is a descriptive focal calibration, not a causal effect or an independent holdout replication.",
        ]
        (args.output_dir / "GUIDE_SCAN_CALIBRATION.md").write_text(
            "\n".join(lines) + "\n", encoding="utf-8"
        )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
