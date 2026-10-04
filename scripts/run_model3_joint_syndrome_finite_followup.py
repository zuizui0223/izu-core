"""Finite two-trait joint-syndrome follow-up under frozen decision rules.

Runs all four assurance settings on the exact 128 frozen near/far visitor
histories, three prespecified initial investment-assurance states, and four new
finite demographic repeats.  All settings run regardless of rare-mutant
outcome; promotion is adjudicated separately from the frozen selection gate.

The trait endpoint is far-minus-near terminal mean investment and assurance.
A history receives a trait class only when all four paired demographic repeats
are occupied in both arms.
"""
from __future__ import annotations

from dataclasses import replace
import argparse
import json
from pathlib import Path

import numpy as np

from scripts.model3_island.density import make_grid
from scripts.model3_island.run import founders_from_spec
from scripts.model3_island.simulate import simulate
from scripts.model3_island.types import Config
from scripts.model3_island_bridge_ops import prepare_arms

ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "data/design/model3_ch2_bridge_20260927.json"
JOINT = ROOT / "data/design/model3_joint_syndrome_rare_mutant_20261004.json"
DESIGN = ROOT / "data/design/model3_joint_syndrome_finite_followup_20261004.json"


def _settings(base, decision):
    return {
        name: {
            "assurance_timing": patch["assurance_timing"],
            "pollen_discount": float(patch["pollen_discount"]),
            "assurance_cost": float(patch["assurance_cost"]),
        }
        for name, patch in decision["settings"].items()
    }


def _classify(di, da, deadband=0.05):
    if di <= -deadband and da >= deadband:
        return "syndrome"
    if di >= deadband and da <= -deadband:
        return "outcross"
    return "intermediate"


def _summarize_start(records, split_halves):
    eligible = [r for r in records if r["eligible"]]
    classes = [r["class"] for r in eligible]
    counts = {k: classes.count(k) for k in ("syndrome", "outcross", "intermediate")}
    n = len(eligible)
    freqs = {k: (counts[k] / n if n else None) for k in counts}
    branching = bool(
        n
        and freqs["syndrome"] is not None
        and freqs["outcross"] is not None
        and freqs["syndrome"] >= 0.10
        and freqs["outcross"] >= 0.10
    )

    split_classes = []
    for rec in records:
        per = rec["per_repeat"]
        row = []
        for half in split_halves:
            chosen = [x for x in per if x["demographic_seed"] in half]
            if len(chosen) != len(half) or not all(x["paired_occupied"] for x in chosen):
                row.append(None)
                continue
            di = float(np.mean([x["far_investment"] - x["near_investment"] for x in chosen]))
            da = float(np.mean([x["far_assurance"] - x["near_assurance"] for x in chosen]))
            row.append(_classify(di, da))
        split_classes.append(row)

    both = [x for x in split_classes if x[0] is not None and x[1] is not None]
    agreement = (
        float(np.mean([x[0] == x[1] for x in both]))
        if both else None
    )

    return {
        "histories_total": len(records),
        "histories_eligible": n,
        "class_counts": counts,
        "class_frequencies": freqs,
        "history_branching": branching,
        "split_half_classifiable_histories": len(both),
        "split_half_class_agreement": agreement,
        "split_half_agreement_gate_pass": bool(
            agreement is not None and agreement >= 0.70
        ),
    }


def run_setting(setting_name: str) -> dict:
    bridge = json.loads(BRIDGE.read_text(encoding="utf-8"))
    joint = json.loads(JOINT.read_text(encoding="utf-8"))
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    if setting_name not in design["settings_to_run"]:
        raise ValueError("setting not frozen for execution")

    base = Config.from_dict(bridge["base_config"])
    patch = _settings(base, joint)[setting_name]
    grid = make_grid(tuple(design["grid_axes"]))
    split_halves = design["branching"]["split_halves"]

    starts_out = []
    all_occupancy = []
    for start in design["initial_states"]:
        founders = founders_from_spec(
            {
                "count": int(design["founders"]["count"]),
                "draw_count": int(design["founders"]["draw_count"]),
                "means": [
                    float(start["access"]),
                    float(start["investment"]),
                    float(start["assurance"]),
                ],
                "sd": float(design["founders"]["sd"]),
                "birth_year": int(design["founders"]["birth_year"]),
            },
            bridge["founder_seed"],
        )
        histories = []
        for history_seed in bridge["history_seeds"]:
            arms = prepare_arms(
                base,
                seed=int(history_seed),
                pool_size=int(bridge["pool_size"]),
            )
            arm_results = {}
            for arm_name in design["arms"]:
                arm_config, history = arms[arm_name]
                config = replace(
                    arm_config,
                    assurance_mode="evolving",
                    assurance_timing=patch["assurance_timing"],
                    pollen_discount=patch["pollen_discount"],
                    assurance_cost=patch["assurance_cost"],
                    mutation_rate=float(design["mutation_rate"]),
                    seed_arrival=replace(
                        arm_config.seed_arrival,
                        supply=float(design["seed_arrival_supply"]),
                    ),
                    years=int(design["years"]),
                )
                per_rep = {}
                for ds in design["demographic_seeds"]:
                    replicate = int(
                        np.random.SeedSequence([int(history_seed), int(ds)]).generate_state(1)[0]
                    )
                    result = simulate(
                        config,
                        history,
                        founders,
                        replicate=replicate,
                        grid=grid,
                        projection_mode=design["projection_mode"],
                        immigration_mode="source",
                    )
                    occupied = bool(result["population"][-1] > 0)
                    all_occupancy.append(occupied)
                    per_rep[int(ds)] = {
                        "occupied": occupied,
                        "investment": (
                            float(result["trait_mean"][-1, 1]) if occupied else None
                        ),
                        "assurance": (
                            float(result["trait_mean"][-1, 2]) if occupied else None
                        ),
                    }
                arm_results[arm_name] = per_rep

            paired = []
            for ds in design["demographic_seeds"]:
                near = arm_results["near"][int(ds)]
                far = arm_results["far"][int(ds)]
                paired_occupied = bool(near["occupied"] and far["occupied"])
                paired.append({
                    "demographic_seed": int(ds),
                    "paired_occupied": paired_occupied,
                    "near_investment": near["investment"],
                    "far_investment": far["investment"],
                    "near_assurance": near["assurance"],
                    "far_assurance": far["assurance"],
                })

            eligible = all(x["paired_occupied"] for x in paired)
            if eligible:
                di = float(np.mean([
                    x["far_investment"] - x["near_investment"] for x in paired
                ]))
                da = float(np.mean([
                    x["far_assurance"] - x["near_assurance"] for x in paired
                ]))
                klass = _classify(di, da)
            else:
                di = da = None
                klass = None

            histories.append({
                "history_seed": int(history_seed),
                "eligible": eligible,
                "far_minus_near_investment": di,
                "far_minus_near_assurance": da,
                "class": klass,
                "per_repeat": paired,
            })

        starts_out.append({
            "initial_state": start,
            "summary": _summarize_start(histories, split_halves),
            "histories": histories,
        })

    summary = {
        row["initial_state"]["id"]: row["summary"] for row in starts_out
    }
    any_branching = any(x["history_branching"] for x in summary.values())
    any_reproducible_branching = any(
        x["history_branching"] and x["split_half_agreement_gate_pass"]
        for x in summary.values()
    )
    return {
        "status": "finite_joint_syndrome_followup_complete",
        "setting": setting_name,
        "cases": (
            len(bridge["history_seeds"])
            * len(design["initial_states"])
            * len(design["demographic_seeds"])
            * len(design["arms"])
        ),
        "terminal_occupancy_fraction_all_trajectories": float(np.mean(all_occupancy)),
        "summary_by_initial_state": summary,
        "any_history_branching": any_branching,
        "any_reproducible_history_branching": any_reproducible_branching,
        "records": starts_out,
        "claim_boundary": [
            "all settings were executed independent of rare-mutant outcome",
            "trait classes require all four paired repeats occupied in both arms",
            "delta fixed; no purging feedback",
            "endpoint classes are synthetic trait differences, not natural prevalence",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--setting", required=True)
    parser.add_argument("--out")
    args = parser.parse_args()
    result = run_setting(args.setting)
    rendered = json.dumps(result, indent=2, sort_keys=True)
    print(rendered)
    if args.out:
        Path(args.out).write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
