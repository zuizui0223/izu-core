"""Run negative and technical-positive calibration for public-image ROI proposals.

This runner reuses the manually flat Ajania cards.  It evaluates regional false
positives on the original crops and sensitivity on deterministic paired
attenuations of those same crops.  It does not claim a biological positive
control and therefore never releases an operator to the broad specialist
holdout.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError

from channel_id.roi_dual_control import (
    calibrate_technical_positive,
    combine_control_gates,
    technical_positive_rows,
)
from channel_id.roi_observation_calibration import (
    calibrate_against_ajania,
    crop_feature_rows,
    render_contact_page,
)
from paper.roi_metrics import (
    CANDIDATE_FIELDS,
    accepted_ajania,
    download,
    image_url_for_observation,
    read_csv,
    render_pages,
    write_csv,
)

POSITIVE_FIELDS = (
    "pair_id", "card_id", "taxon", "proposal", "control_variant", "image_url",
    "feature_status", "source_width_px", "source_height_px", "processed_width_px",
    "processed_height_px", "mean_brightness", "mean_saturation", "colourfulness",
    "radial_chroma_contrast", "hue_entropy", "edge_density",
)
NEGATIVE_FIELDS = (
    "proposal", "accepted_cards", "large_to_ardens_delta", "ardens_to_no_bombus_delta",
    "absolute_delta_sum", "max_abs_delta", "passes_flat_negative_control", "calibration_boundary",
)
SENSITIVITY_FIELDS = (
    "proposal", "paired_cards", "median_attenuated_minus_original", "negative_pair_fraction",
    "minimum_abs_median_delta", "minimum_negative_fraction", "passes_technical_positive_control",
    "positive_control_boundary",
)
GATE_FIELDS = (
    "proposal", "passes_flat_negative_control", "passes_technical_positive_control",
    "passes_dual_technical_gate", "biological_positive_control_status",
    "eligible_for_broad_specialist_holdout", "gate_boundary",
)
AUDIT_FIELDS = ("card_id", "obs_id", "status", "retrieved_at_utc", "error")


def _fmt(value: object) -> str:
    if value == "" or value is None:
        return "NA"
    number = float(value)
    return "NA" if not math.isfinite(number) else f"{number:.3f}"


def render_dual_report(
    negative: list[dict[str, object]],
    sensitivity: list[dict[str, object]],
    gates: list[dict[str, object]],
) -> str:
    negative_by = {str(row["proposal"]): row for row in negative}
    sensitivity_by = {str(row["proposal"]): row for row in sensitivity}
    gate_by = {str(row["proposal"]): row for row in gates}
    lines = [
        "# Dual-control ROI observation-model calibration",
        "",
        "The flat Ajania comparison tests false regional thresholds. A paired deterministic attenuation tests whether the same crop representation still responds to a known loss of colour and local contrast.",
        "",
        "| proposal | flat-control max | attenuation median delta | negative-pair fraction | dual technical pass | broad specialist holdout |",
        "|---|---:|---:|---:|---|---|",
    ]
    for proposal in negative_by:
        neg = negative_by[proposal]
        pos = sensitivity_by[proposal]
        gate = gate_by[proposal]
        lines.append(
            f"| {proposal} | {_fmt(neg['max_abs_delta'])} | "
            f"{_fmt(pos['median_attenuated_minus_original'])} | "
            f"{_fmt(pos['negative_pair_fraction'])} | "
            f"{gate['passes_dual_technical_gate']} | "
            f"{gate['eligible_for_broad_specialist_holdout']} |"
        )
    lines.extend((
        "",
        "## Interpretation boundary",
        "",
        "The attenuation comparison is a technical sensitivity control, not a biological positive control. No proposal is released to the broad specialist holdout until an independent source-native or blinded-human positive-control lineage is registered and passed.",
    ))
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--sleep-seconds", type=float, default=0.2)
    parser.add_argument("--minimum-pairs", type=int, default=6)
    parser.add_argument("--minimum-attenuation-delta", type=float, default=0.50)
    parser.add_argument("--minimum-negative-fraction", type=float, default=0.80)
    args = parser.parse_args()
    if args.sleep_seconds < 0:
        raise SystemExit("sleep-seconds must be nonnegative")

    manual_rows = accepted_ajania(read_csv(args.ledger))
    original_rows: list[dict[str, object]] = []
    paired_rows: list[dict[str, object]] = []
    audit: list[dict[str, str]] = []
    panels: list[tuple[str, object]] = []

    for row in manual_rows:
        timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        card_id, obs_id = row["card_id"], row["obs_id"]
        try:
            image_url = image_url_for_observation(obs_id)
            image_bytes = download(image_url)
            original_rows.extend(crop_feature_rows(image_bytes, "Ajania pacifica", card_id, image_url))
            paired_rows.extend(technical_positive_rows(image_bytes, "Ajania pacifica", card_id, image_url))
            panels.append((card_id, render_contact_page(image_bytes, card_id)))
            audit.append({
                "card_id": card_id,
                "obs_id": obs_id,
                "status": "ok",
                "retrieved_at_utc": timestamp,
                "error": "",
            })
        except (HTTPError, URLError, OSError, ValueError, RuntimeError) as error:
            audit.append({
                "card_id": card_id,
                "obs_id": obs_id,
                "status": "error",
                "retrieved_at_utc": timestamp,
                "error": type(error).__name__,
            })
        time.sleep(args.sleep_seconds)

    output = args.output_dir
    output.mkdir(parents=True, exist_ok=True)
    write_csv(output / "ajania_roi_candidates_blind.csv", CANDIDATE_FIELDS, original_rows)
    write_csv(output / "ajania_roi_technical_positive_pairs_blind.csv", POSITIVE_FIELDS, paired_rows)
    write_csv(output / "ajania_roi_download_audit.csv", AUDIT_FIELDS, audit)
    render_pages(panels, output / "blinded_contact_sheets")

    negative = calibrate_against_ajania(original_rows, manual_rows)
    sensitivity = calibrate_technical_positive(
        paired_rows,
        minimum_pairs=args.minimum_pairs,
        minimum_abs_median_delta=args.minimum_attenuation_delta,
        minimum_negative_fraction=args.minimum_negative_fraction,
    )
    gates = combine_control_gates(negative, sensitivity)
    write_csv(output / "ajania_roi_flat_negative_control.csv", NEGATIVE_FIELDS, negative)
    write_csv(output / "ajania_roi_technical_positive_control.csv", SENSITIVITY_FIELDS, sensitivity)
    write_csv(output / "roi_dual_control_gate.csv", GATE_FIELDS, gates)
    (output / "ROI_DUAL_CONTROL_REPORT.md").write_text(
        render_dual_report(negative, sensitivity, gates), encoding="utf-8"
    )

    summary = {
        "manually_accepted_ajania_cards": len(manual_rows),
        "images_recovered": sum(row["status"] == "ok" for row in audit),
        "proposals_passing_flat_control": sum(
            row["passes_flat_negative_control"] == "yes" for row in negative
        ),
        "proposals_passing_technical_positive_control": sum(
            row["passes_technical_positive_control"] == "yes" for row in sensitivity
        ),
        "proposals_passing_dual_technical_gate": sum(
            row["passes_dual_technical_gate"] == "yes" for row in gates
        ),
        "proposals_released_to_broad_specialist_holdout": 0,
        "blocking_reason": "independent biological positive control is missing",
    }
    (output / "roi_dual_control.summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
