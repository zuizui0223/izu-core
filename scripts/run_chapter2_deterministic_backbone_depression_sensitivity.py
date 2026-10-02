"""Prospective inbreeding-depression sensitivity of the natural deterministic bridge backbone.

Uses the frozen Model 3 Chapter 2 bridge visitor histories and founder/grid
construction, but advances only the deterministic genotype-density counterpart.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.model3_island.density import density_step, make_grid, project_state
from scripts.model3_island.run import founders_from_spec
from scripts.model3_island.types import Config
from scripts.model3_island_bridge_ops import prepare_arms

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "data/design/chapter2_deterministic_backbone_depression_sensitivity_20261002.json"


def _terminal_investment(cfg, history, founders, grid):
    _, counts = project_state(founders, grid)
    initial_mass = float(counts.sum())
    if initial_mass <= 0:
        raise ValueError("empty initial density")
    traits = grid.genotypes.mean(axis=2)
    initial = float(counts @ traits[:, 1] / initial_mass)

    for year in range(cfg.years):
        counts, _ = density_step(
            counts,
            grid,
            history.visitors[year],
            history.seed_candidates[year],
            cfg,
            immigration_mode="source",
        )
    mass = float(counts.sum())
    terminal = None if mass <= 0 else float(counts @ traits[:, 1] / mass)
    change = None if terminal is None else float(terminal - initial)
    return {
        "initial_investment": initial,
        "terminal_investment": terminal,
        "investment_change": change,
        "terminal_density_mass": mass,
    }


def _sign(x, eps=1e-12):
    if x is None or not np.isfinite(x):
        return None
    if x > eps:
        return 1
    if x < -eps:
        return -1
    return 0


def run(design: dict, parent: dict) -> dict:
    if design["status"] != "prospective_frozen_before_execution":
        raise ValueError("design must be frozen before execution")
    if parent["status"] != "frozen":
        raise ValueError("parent bridge must remain frozen")

    starts = [float(x) for x in parent["starts"]]
    history_seeds = [int(x) for x in parent["history_seeds"]]
    grid = make_grid(parent["grid_axes"])
    rows = []

    for depression in design["intervention"]["depression"]:
        base = Config.from_dict(parent["base_config"])
        base = replace(base, depression=float(depression))
        for hs in history_seeds:
            arms = prepare_arms(base, seed=hs, pool_size=int(parent["pool_size"]))
            for start in starts:
                spec = {
                    "count": base.capacity,
                    "draw_count": 48,
                    "means": [0.5, start, 0.5],
                    "sd": 0.15,
                    "birth_year": 0,
                }
                founders = founders_from_spec(spec, int(parent["founder_seed"]))
                near_cfg, near_history = arms["near"]
                far_cfg, far_history = arms["far"]
                near = _terminal_investment(near_cfg, near_history, founders, grid)
                far = _terminal_investment(far_cfg, far_history, founders, grid)
                effect = (
                    None
                    if near["investment_change"] is None or far["investment_change"] is None
                    else float(far["investment_change"] - near["investment_change"])
                )
                rows.append({
                    "depression": float(depression),
                    "history_seed": hs,
                    "start_investment": start,
                    "near_change": near["investment_change"],
                    "far_change": far["investment_change"],
                    "effect_far_minus_near": effect,
                    "near_terminal_mass": near["terminal_density_mass"],
                    "far_terminal_mass": far["terminal_density_mass"],
                })

    reports = []
    for depression in design["intervention"]["depression"]:
        drows = [r for r in rows if r["depression"] == float(depression)]
        effects = np.asarray(
            [r["effect_far_minus_near"] for r in drows if r["effect_far_minus_near"] is not None],
            dtype=float,
        )
        overall_mean = None if not len(effects) else float(effects.mean())

        mean_by_start = {}
        for start in starts:
            x = [
                r["effect_far_minus_near"]
                for r in drows
                if r["start_investment"] == start and r["effect_far_minus_near"] is not None
            ]
            mean_by_start[str(start)] = None if not x else float(np.mean(x))

        mixed = 0
        positive_only = 0
        negative_only = 0
        zero_or_undefined = 0
        history_labels = []
        for hs in history_seeds:
            vals = [
                r["effect_far_minus_near"]
                for r in drows
                if r["history_seed"] == hs
            ]
            signs = {_sign(v) for v in vals}
            signs.discard(None)
            nonzero = {s for s in signs if s != 0}
            if 1 in nonzero and -1 in nonzero:
                label = "mixed"
                mixed += 1
            elif nonzero == {1}:
                label = "positive_only"
                positive_only += 1
            elif nonzero == {-1}:
                label = "negative_only"
                negative_only += 1
            else:
                label = "zero_or_undefined"
                zero_or_undefined += 1
            history_labels.append({"history_seed": hs, "label": label, "effects": vals})

        uniform_negative = bool(
            overall_mean is not None
            and overall_mean < 0
            and all(v is not None and v < 0 for v in mean_by_start.values())
            and mixed == 0
            and positive_only == 0
            and zero_or_undefined == 0
            and negative_only == len(history_seeds)
        )
        reports.append({
            "depression": float(depression),
            "overall_mean_effect": overall_mean,
            "mean_effect_by_start": mean_by_start,
            "mixed_histories_eps0": mixed,
            "positive_only_histories_eps0": positive_only,
            "negative_only_histories_eps0": negative_only,
            "zero_or_undefined_histories_eps0": zero_or_undefined,
            "uniform_negative_backbone": uniform_negative,
            "history_labels": history_labels,
        })

    by_dep = {r["depression"]: r for r in reports}
    dep075 = by_dep[0.75]
    sign_reversal = bool(
        dep075["overall_mean_effect"] is not None
        and dep075["overall_mean_effect"] >= 0
    )
    conditional_uniformity = bool(
        not sign_reversal and not dep075["uniform_negative_backbone"]
    )
    robust = bool(all(r["uniform_negative_backbone"] for r in reports))

    if robust:
        action = "retain_uniform_negative_backbone_within_tested_depression_envelope"
    elif sign_reversal:
        action = "qualify_backbone_direction_as_inbreeding_depression_dependent"
    else:
        action = "retain_negative_mean_but_drop_uniform_one_directional_backbone_claim"

    return {
        "status": "complete_deterministic_backbone_depression_sensitivity",
        "n_density_trajectories": len(rows) * 2,
        "reports": reports,
        "backbone_robust": robust,
        "sign_reversal_at_depression_0_75": sign_reversal,
        "conditional_uniformity_at_depression_0_75": conditional_uniformity,
        "reporting_action": action,
        "rows": rows,
        "claim_boundary": design["claim_boundary"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--design", default=str(DEFAULT_DESIGN))
    parser.add_argument("--parent", default=str(ROOT / "data/design/model3_ch2_bridge_20260927.json"))
    parser.add_argument("--out")
    args = parser.parse_args()
    design = json.loads(Path(args.design).read_text(encoding="utf-8"))
    parent = json.loads(Path(args.parent).read_text(encoding="utf-8"))
    result = run(design, parent)
    encoded = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(encoded, encoding="utf-8")
    print(encoded)


if __name__ == "__main__":
    main()
