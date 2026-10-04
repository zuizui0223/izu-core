"""Adjudicate the frozen Model 3 joint-syndrome extension.

This script contains no simulation. It combines:
1) the committed rare-mutant/Price/G-beta result summary, and
2) the four finite follow-up setting JSONs produced by the frozen workflow.

Promotion rules are read from the pre-outcome design files.  Missing settings
fail closed.
"""
from __future__ import annotations

import argparse
import json
import hashlib
from scripts.model3_joint_result_validation import validate_selection, validate_finite
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELECTION = ROOT / "data/results/model3_joint_syndrome_rare_mutant_frozen_20261004.json"
FINITE_DESIGN = ROOT / "data/design/model3_joint_syndrome_finite_followup_20261004.json"
PROVENANCE = ROOT / "data/results/model3_repair_input_provenance_20261004.json"
GATE = ROOT / "data/design/model3_joint_syndrome_rare_mutant_gate_addendum_20261004.json"


def adjudicate(finite_paths):
    selection = json.loads(SELECTION.read_text(encoding="utf-8"))
    finite_design = json.loads(FINITE_DESIGN.read_text(encoding="utf-8"))
    gate = json.loads(GATE.read_text(encoding="utf-8"))

    response_supported = validate_selection(selection)
    input_hashes = {}
    trusted = {x["setting"]: x["sha256"] for x in json.loads(PROVENANCE.read_text(encoding="utf-8"))["inputs"]}
    finite = {}
    for path in finite_paths:
        x = json.loads(Path(path).read_text(encoding="utf-8"))
        if x.get("status") != "finite_joint_syndrome_followup_complete":
            raise ValueError(f"incomplete finite result: {path}")
        setting = x["setting"]
        if setting in finite:
            raise ValueError(f"duplicate finite setting: {setting}")
        validate_finite(x, finite_design)
        input_hashes[setting] = hashlib.sha256(Path(path).read_bytes()).hexdigest()
        if input_hashes[setting] != trusted.get(setting):
            raise ValueError("finite source identity differs from reviewed provenance")
        finite[setting] = x

    expected = set(finite_design["settings_to_run"])
    if set(finite) != expected:
        raise ValueError(
            f"finite setting set differs: got={sorted(finite)} expected={sorted(expected)}"
        )

    selection_settings = selection["rare_mutant_selection"]["settings"]
    rows = {}
    tradeoffs = {"prior_selfing", "pollen_discount", "assurance_cost"}
    for setting in sorted(expected):
        sel = selection_settings[setting]
        beta_eligible = (
            sel["joint_shift_gate_pass_states"] == 45  # includes required central state
        )
        f = finite[setting]
        start_summaries = f["summary_by_initial_state"]
        syndrome_endpoint = any(
            (x["class_frequencies"]["syndrome"] or 0.0) >= 0.10
            for x in start_summaries.values()
        )
        reproducible_branching = bool(f["any_reproducible_history_branching"])
        sign_reversal = sel["maximum_classic_sign_reversal_fraction"] >= 0.50

        if setting == "delayed_control":
            promotion = "control_only"
        elif not beta_eligible:
            promotion = "no_promotion"
        elif not response_supported:
            promotion = "si_only_response_gate_incomplete"
        elif reproducible_branching:
            promotion = "repeatability_core_or_next_paper"
        elif syndrome_endpoint or sign_reversal:
            promotion = "mechanistic_core"
        else:
            promotion = "si_only"

        rows[setting] = {
            "beta_shift_eligible": beta_eligible,
            "classic_sign_reversal_supported": sign_reversal,
            "finite_syndrome_endpoint_at_least_10pct_any_start": syndrome_endpoint,
            "finite_reproducible_history_branching": reproducible_branching,
            "terminal_occupancy_fraction": f["terminal_occupancy_fraction_all_trajectories"],
            "promotion": promotion,
            "summary_by_initial_state": start_summaries,
        }

    overall = "si_only"
    if any(rows[s]["promotion"] == "repeatability_core_or_next_paper" for s in tradeoffs):
        overall = "repeatability_core_or_next_paper"
    elif any(rows[s]["promotion"] == "mechanistic_core" for s in tradeoffs):
        overall = "mechanistic_core"
    elif not any(rows[s]["beta_shift_eligible"] for s in tradeoffs):
        overall = "no_promotion"

    return {
        "status": "joint_syndrome_extension_adjudicated",
        "overall_promotion": overall,
        "settings": rows,
        "selection_provenance": selection["provenance"],
        "finite_input_sha256": input_hashes,
        "response_gate_all_cells_pass": response_supported,
        "response_boundary": "46/48 is not silently promoted to complete response support",
        "promotion_rule_text": gate["promotion_rules"],
        "claim_boundary": [
            "delayed control never counts as independent assurance-evolution evidence",
            "absolute sign reversal and directional shift remain distinct",
            "fixed delta; no purging feedback",
            "a next-paper label requires reproducible endpoint branching under the frozen finite criteria",
        ],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("finite", nargs=4)
    p.add_argument("--out")
    a = p.parse_args()
    result = adjudicate(a.finite)
    rendered = json.dumps(result, indent=2, sort_keys=True)
    print(rendered)
    if a.out:
        Path(a.out).write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
