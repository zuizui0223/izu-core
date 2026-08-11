#!/usr/bin/env python3
"""Apply the Southwest Pacific measurement-error admission gate to effect rows.

The source-native flower-size analysis intentionally emits descriptive numeric
candidate effects before all downstream robustness audits are known.  This gate
uses the checked classical measurement-error coupling sensitivity to decide
which candidates may enter the formal cross-system effect registry.

The starting-size slopes use log10(FI/FM) as the response and log10(FM) as the
predictor, so mainland flower size is shared between response and predictor.
When the coupling sensitivity remains unresolved, those slopes stay numeric and
reportable but are not model-eligible.  The animal floral-display mean log ratio
is a different response and is not blocked by this specific denominator-sharing
gate.
"""
from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping


STARTING_SIZE_EFFECT_IDS = {
    "southwest_pacific_animal_flower_size_starting_value_slope",
    "southwest_pacific_wind_flower_size_starting_value_slope",
}


def apply_admission_gate(
    effect_document: Mapping[str, Any],
    coupling_summary: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a gated copy of the Southwest Pacific effect document."""
    document = deepcopy(dict(effect_document))
    effects = document.get("effects")
    if not isinstance(effects, list):
        raise ValueError("effect document must contain an effects list")

    if coupling_summary.get("status") != (
        "classical_measurement_error_coupling_sensitivity_complete"
    ):
        raise ValueError("measurement-error coupling sensitivity is not complete")
    if coupling_summary.get("reliability_is_empirically_estimated_here") is not False:
        raise ValueError("unexpected reliability-estimation state")

    coupling_gate_open = bool(coupling_summary.get("effect_registry_eligible"))
    seen_starting_size_ids: set[str] = set()
    for effect in effects:
        if not isinstance(effect, dict):
            raise ValueError("each effect row must be an object")
        effect_id = str(effect.get("effect_id", ""))
        if effect_id not in STARTING_SIZE_EFFECT_IDS:
            continue
        seen_starting_size_ids.add(effect_id)
        if coupling_gate_open:
            continue
        effect["cross_system_model_eligible"] = False
        effect["admission_status"] = (
            "blocked_measurement_error_denominator_coupling_unresolved"
        )
        effect["notes"] = (
            "Numeric source-native morphology effect retained for description, "
            "but excluded from formal cross-system fitting because log10(FM) "
            "is shared between predictor and log10(FI/FM) response and the "
            "source does not empirically identify mainland-size reliability."
        )

    if seen_starting_size_ids != STARTING_SIZE_EFFECT_IDS:
        missing = sorted(STARTING_SIZE_EFFECT_IDS - seen_starting_size_ids)
        raise ValueError(f"missing expected starting-size effects: {missing}")

    document["status"] = "effect_rows_ready_with_measurement_error_admission_gate"
    document["admission_gate"] = {
        "gate": "southwest_pacific_measurement_error_denominator_coupling",
        "coupling_summary_status": coupling_summary["status"],
        "reliability_is_empirically_estimated_here": False,
        "starting_size_effects_model_eligible": coupling_gate_open,
        "animal_point_negative_reliability_threshold": coupling_summary.get(
            "animal_point_negative_reliability_threshold"
        ),
        "animal_ci_negative_reliability_threshold": coupling_summary.get(
            "animal_ci_negative_reliability_threshold"
        ),
        "claim_boundary": coupling_summary.get("claim_boundary", ""),
    }
    document["formal_cross_system_fit_ready"] = False
    return document


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--effect-rows", type=Path, required=True)
    parser.add_argument("--coupling-summary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    effect_document = json.loads(args.effect_rows.read_text(encoding="utf-8"))
    coupling_summary = json.loads(
        args.coupling_summary.read_text(encoding="utf-8")
    )
    gated = apply_admission_gate(effect_document, coupling_summary)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(gated, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(args.output)


if __name__ == "__main__":
    main()
