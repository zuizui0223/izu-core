"""Read-only audit of apparent counterintuitive assurance effects in Model 3.

This intentionally does NOT start a new biological history, alter the original
four-setting experiment, or declare new evolutionary confirmation. It distinguishes
terminal intervention contrasts from static, source-native rare-mutant selection.
The high-pollen grid is a post-outcome *mathematical sensitivity* on ONE artificial
four-visitor community, not a new mainland simulation or saturation calibration.
"""
from __future__ import annotations

from dataclasses import replace
import argparse
import json
from pathlib import Path

import numpy as np

from scripts.model3_island.types import VisitorState
from scripts.model3_island.selection import investment_invasion_terms
from scripts.audit_model3_joint_syndrome_vector import invasion_gradient
from scripts.run_chapter2_assurance_generality import config, load_design

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_assurance_generality_20261006.json"
GENERALITY = ROOT / "data/results/chapter2_assurance_generality_20261006.json"
ARMS = ROOT / "data/results/chapter2_assurance_attenuation_decomposition_20261006.json"
GRADIENT = ROOT / "data/results/chapter2_assurance_gradient_components_20261006.json"
SETTINGS = ("delayed_control", "prior_selfing", "pollen_discount", "assurance_cost")
# Deliberately chosen synthetic functional optima; NOT the original near/far visitor states.
SCALES = (0.0, 0.25, 1.0, 2.0, 4.0, 8.0, 16.0, 64.0)
A_LEVELS = (0.25, 0.75)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def artificial_visitors(cfg):
    optima = np.asarray((0.35, 0.45, 0.55, 0.65), dtype=float)
    return VisitorState(
        np.arange(4, dtype=np.int64),
        optima,
        np.full(4, cfg.visitor_breadth, dtype=float),
        np.full(4, cfg.visitor_effectiveness, dtype=float),
    )


def source_static_grid(design):
    rows = []
    for setting in SETTINGS:
        cfg = config(design, setting, 0.01, "evolving")
        visitors = artificial_visitors(cfg)
        for scale in SCALES:
            c = replace(cfg, pollen_budget=cfg.pollen_budget * scale)
            results = []
            for a in A_LEVELS:
                resident = np.array([0.5, 0.5, a], dtype=float)
                native = investment_invasion_terms(resident, visitors, c)
                beta = float(native["gradient"])
                q = float(native["outcross_fraction"])
                independent = float(invasion_gradient(
                    resident, visitors, c, trait_index=1, step=1e-5,
                ))
                if not (np.isfinite(beta) and np.isfinite(independent)
                        and np.isfinite(q) and 0.0 <= q <= 1.0):
                    raise AssertionError("nonfinite mathematical source diagnostic")
                if abs(beta - independent) > 2e-6:
                    raise AssertionError(
                        f"rare-mutant native versus independent finite difference: "
                        f"{setting}, pollen scale {scale}, A {a}: {beta} != {independent}"
                    )
                results.append({
                    "assurance": a,
                    "outcross_fraction": q,
                    "investment_invasion_gradient": beta,
                    "independent_finite_difference": independent,
                })
            rows.append({
                "setting": setting,
                "pollen_budget_multiplier": scale,
                "artificial_visitor_optima": [0.35, 0.45, 0.55, 0.65],
                "A_low": results[0],
                "A_high": results[1],
                "A_high_minus_low_investment_gradient": (
                    results[1]["investment_invasion_gradient"]
                    - results[0]["investment_invasion_gradient"]
                ),
            })
    return rows


def audit() -> dict:
    design = load_design(DESIGN)
    original = load_json(GENERALITY)
    arm_data = load_json(ARMS)
    gradient = load_json(GRADIENT)
    if (original["adjudication"]["n_passed"] != 4
            or original["declared_cases"] != 8448
            or original["structural_control"]["status"] != "passed"
            or original["structural_control"]["matched_pairs_checked"] != 128
            or arm_data["source_cases_verified"] != 8448
            or original["independent_visitor_histories"] != 64
            or arm_data["independent_visitor_histories"] != 64
            or gradient["independent_visitor_histories"] != 64):
        raise AssertionError("historical source/control admission has changed")
    if (original["design_sha256"] != arm_data["source_design_sha256"]
            or original["design_sha256"] != gradient["source_design_sha256"]):
        raise AssertionError("mismatched historical experiment source")
    if original["structural_control"]["mismatches"]:
        raise AssertionError("zero-mutation structural null failed")

    g400 = {r["setting"]: r for r in gradient["rows"] if r["snapshot"] == 400}
    arms = {r["setting"]: r for r in arm_data["settings"]}
    evolution = {r["setting"]: r for r in original["settings"]}
    if not (set(g400) == set(arms) == set(evolution) == set(SETTINGS)):
        raise AssertionError("four-setting comparison incomplete")

    recorded = []
    for setting in SETTINGS:
        a = arms[setting]["estimates"]
        n = a["evolution_effect_near"]["mean"]
        f = a["evolution_effect_far"]["mean"]
        interaction = a["attenuation"]["mean"]
        local_n = g400[setting]["assurance_effect_high_minus_low"]["near"]["gradient"]["mean"]
        local_f = g400[setting]["assurance_effect_high_minus_low"]["far"]["gradient"]["mean"]
        if (not (n < 0 < f and local_n < local_f < 0)
                or not a["evolving_far_assurance_change"]["mean"] >
                       a["evolving_near_assurance_change"]["mean"]
                or not abs((f - n) - interaction) < 1e-11
                or not abs(interaction
                           - evolution[setting]["attenuation_evolving_minus_fixed"]["mean"]) < 1e-11
                or not all(evolution[setting]["occupancy"][mode][arm] == 1.0
                           for mode in ("fixed", "evolving") for arm in ("near", "far"))):
            raise AssertionError(f"historical four-arm/source-gradient crosswalk: {setting}")
        recorded.append({
            "setting": setting,
            "near_evolving_minus_fixed_investment": n,
            "far_evolving_minus_fixed_investment": f,
            "far_minus_near_interaction": interaction,
            "near_change_in_A": a["evolving_near_assurance_change"]["mean"],
            "far_change_in_A": a["evolving_far_assurance_change"]["mean"],
            "near_fixed_resident_A_effect_on_I_gradient": local_n,
            "far_fixed_resident_A_effect_on_I_gradient": local_f,
            "interpretation": (
                "The positive far terminal effect is opposite to the sign of "
                "the local fixed-resident high-minus-low-A investment gradient. "
                "It cannot be assigned to that local direct gradient alone. "
                "Neither genetic covariance nor demographic mediation is uniquely identified."
            ),
        })

    synthetic = source_static_grid(design)
    for setting in SETTINGS:
        zero = next(x for x in synthetic
                    if x["setting"] == setting and x["pollen_budget_multiplier"] == 0)
        if abs(zero["A_high_minus_low_investment_gradient"]) > 1e-11:
            raise AssertionError("source no-pollen coupling should vanish")
    return {
        "status": "SOURCE_ONLY_DIAGNOSTIC_NO_NEW_BIOLOGICAL_TRAJECTORIES",
        "frozen_primary_retained": True,
        "source_original_trajectories": 8448,
        "source_independent_visitor_histories": 64,
        "new_evolutionary_trajectories": 0,
        "original_four_setting_endpoints": recorded,
        "mathematical_synthetic_visitor_grid": synthetic,
        "limitations": [
            "The observed far-side positive endpoint cannot be causally decomposed from means.",
            "Static monomorphic rare-mutant gradients are not finite inherited trajectories.",
            "The artificial pollen-budget grid cannot establish saturation of original near histories.",
            "At zero pollen the assurance-to-investment gradient effect is exactly zero in this source model.",
            "The behaviour at near-complete fertilization is mating-system-dependent; no universal hump is claimed.",
            "Do not treat four reproductive settings as four independent ecological systems.",
        ],
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, default=None)
    args = p.parse_args()
    result = audit()
    if args.out is not None:
        if args.out.exists():
            raise ValueError("refuse to overwrite prior audit")
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n",
                            encoding="utf-8")
    compact = {
        "status": result["status"],
        "settings": result["original_four_setting_endpoints"],
        "synthetic_grid": [
            {"setting": x["setting"], "scale": x["pollen_budget_multiplier"],
             "q_low": x["A_low"]["outcross_fraction"],
             "q_high": x["A_high"]["outcross_fraction"],
             "delta_gradient": x["A_high_minus_low_investment_gradient"]}
            for x in result["mathematical_synthetic_visitor_grid"]
        ],
    }
    print(json.dumps(compact, allow_nan=False))


if __name__ == "__main__":
    main()
