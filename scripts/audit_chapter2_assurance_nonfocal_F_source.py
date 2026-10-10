"""Read-only assurance -> conspecific outcross pathway check on original Model3.

Post-discovery source-model mechanistic check only; 4 reproductive settings
at one preselected 8-genotype resident fixture, NOT a trajectory-level
mediation estimate or a new confirmatory ecological history.
"""
from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path

from scripts.audit_chapter2_beta_gamma_seed_map import (
    load_contract, state_of_clones, changed_state, visitors_for,
)
from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, load_design, config as source_config,
)

SETTINGS = ("delayed_control", "prior_selfing", "pollen_discount", "assurance_cost")
ROOT = Path(__file__).resolve().parents[1]


def source_outcross_to_other_mothers(state, visitors, cfg):
    ledger = reproduce_kb(state, visitors, cfg, background_denominator_capacity=48)
    female_outcross = ledger.outcross.sum(axis=0)
    return float(female_outcross[1:].sum())


def assay():
    grid, _ = load_contract()
    initial = state_of_clones((.2, .35, .35), 8)
    visitors = visitors_for("matched4", grid)
    source_design = load_design(DEFAULT_DESIGN)
    rows = []
    for setting in SETTINGS:
        cfg = replace(
            source_config(source_design, setting, 0.0, "evolving"),
            capacity=8, ovule_budget=8.0,
        )
        # Manipulate focal mother's/father's assurance separately from
        # her investment; 7 neighbours have identical source genotypes.
        low_a = changed_state(initial, 2, -0.1, whole=False)
        high_a = changed_state(initial, 2, +0.1, whole=False)
        # Second intervention, decreasing only the focal investment by 0.1.
        high_a_low_i = changed_state(high_a, 1, -0.1, whole=False)
        f00 = source_outcross_to_other_mothers(low_a, visitors, cfg)
        f10 = source_outcross_to_other_mothers(high_a, visitors, cfg)
        f11 = source_outcross_to_other_mothers(high_a_low_i, visitors, cfg)
        direct = f10-f00
        via_investment = f11-f10
        total = f11-f00
        if abs(total-(direct+via_investment))>1e-12:
            raise AssertionError("pathwise source response decomposition failed")
        rows.append({
            "setting": setting,
            "pollen_discount": cfg.pollen_discount,
            "focal_assurance_low_high": [0.25,0.45],
            "focal_investment_high_low": [0.35,0.25],
            "other_mothers_outcross_low_assurance": f00,
            "other_mothers_outcross_high_assurance_same_investment": f10,
            "other_mothers_outcross_high_assurance_low_investment": f11,
            "direct_assurance_delta_at_fixed_investment": direct,
            "investment_response_delta_at_high_assurance": via_investment,
            "combined_finite_contrast": total,
        })
    return {
        "status": "MODEL3_FIXED_STATE_POSTDISCOVERY_ASSURANCE_PATH_DIAGNOSTIC",
        "rows": rows,
        "n_natural_systems": 0,
        "n_new_visitor_histories": 0,
        "no_dynamic_evolution_test": True,
        "note": (
            "The direct term is zero for unchanged pollen-export settings. "
            "Pollen discount permits an immediate negative externality. "
            "The investment-response term imposes a counterfactual reduction "
            "in investment; it does not estimate that such a change was "
            "caused by assurance evolution in #411 histories. "
            "Neither term is an evolutionary persistence or selection estimate."
        ),
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    output = assay()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, sort_keys=True, allow_nan=False)+"\n")
    print(json.dumps({"status": output["status"],
                      "rows": output["rows"]}, sort_keys=True))


if __name__ == "__main__":
    main()
