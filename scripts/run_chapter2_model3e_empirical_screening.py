"""Prospective Model 3E screening against Chapter 1 H1 + H3 only.

Held-out H2/H4 targets are deliberately not calculated in this module.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.stats import qmc
from threadpoolctl import threadpool_limits

from scripts.model3_island.density import make_grid, project_state
from scripts.model3e_empirical import (
    Model3EParams,
    density_step_model3e,
    make_founders,
    make_history,
    make_stratum_context,
    weighted_trait_means,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "data/design/chapter2_model3e_empirical_screening_20261003.json"
DEFAULT_TARGETS = ROOT / "data/design/chapter2_model3e_chapter1_empirical_targets_20261003.json"


def _standardized_log_distance(distances) -> dict[float, float]:
    d = np.asarray(distances, dtype=float)
    x = np.log1p(d)
    x = (x - x.mean()) / x.std(ddof=0)
    return {float(dd): float(xx) for dd, xx in zip(d, x)}


def _slope(y, x):
    y = np.asarray(y, dtype=float)
    x = np.asarray(x, dtype=float)
    if len(y) != len(x) or len(y) < 3 or not np.isfinite(y).all():
        return None
    X = np.column_stack([np.ones(len(x)), x])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return float(beta[1])


def _pooled_stratum_adjusted_slope(rows, response: str) -> float | None:
    strata = sorted({r["stratum"] for r in rows})
    if len(strata) < 2:
        return None
    y = np.asarray([r[response] for r in rows], dtype=float)
    if not np.isfinite(y).all():
        return None
    x = np.asarray([r["x_distance"] for r in rows], dtype=float)
    dummies = np.column_stack([
        np.asarray([1.0 if r["stratum"] == s else 0.0 for r in rows])
        for s in strata[1:]
    ])
    X = np.column_stack([np.ones(len(rows)), x, dummies])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return float(beta[1])


def _positive_scale(model, target) -> float:
    m = np.asarray(model, dtype=float)
    t = np.asarray(target, dtype=float)
    denom = float(m @ m)
    if denom <= 0:
        return 0.0
    return max(0.0, float((m @ t) / denom))


def _nrmse(model, target, scale) -> float:
    m = np.asarray(model, dtype=float) * float(scale)
    t = np.asarray(target, dtype=float)
    denom = float(np.sqrt(np.mean(t * t)))
    if denom <= 0:
        return float("inf")
    return float(np.sqrt(np.mean((m - t) ** 2)) / denom)


def _lhs_parameter_sets(design: dict) -> list[dict]:
    spec = design["search"]
    names = list(spec["parameters"])
    ranges = np.asarray([spec["parameters"][k] for k in names], dtype=float)
    sampler = qmc.LatinHypercube(d=len(names), seed=int(spec["seed"]))
    u = sampler.random(n=int(spec["n_parameter_sets"]))
    values = qmc.scale(u, ranges[:, 0], ranges[:, 1])
    out = []
    for i, row in enumerate(values):
        params = {k: float(v) for k, v in zip(names, row)}
        out.append({"parameter_id": f"p{i:03d}", "params": params})
    return out


def _to_params(p: dict) -> Model3EParams:
    return Model3EParams(
        visitor_reach_scale=p["visitor_reach_scale"],
        seed_reach_scale=p["seed_reach_scale"],
        visitor_supply=p["visitor_supply"],
        visitor_loss_hazard=p["visitor_loss_hazard"],
        activity=p["activity"],
        visitor_breadth=p["visitor_breadth"],
        generalization_span=p["generalization_span"],
        generalization_cost=p["generalization_cost"],
        investment_cost=p["investment_cost"],
        assurance_cost=p["assurance_cost"],
        inbreeding_depression=p["inbreeding_depression"],
        seed_supply=p["seed_supply"],
    )


def _run_pseudo_island(
    design: dict,
    params: Model3EParams,
    context: dict,
    *,
    stratum: str,
    distance: float,
    history_seed: int,
    x_distance: float,
    grid,
) -> dict:
    founders = make_founders(
        design,
        context,
        seed=int(design["pseudo_islands"]["stratum_context_seeds"][stratum]),
    )
    _, counts = project_state(founders, grid)
    visitors, immigrants = make_history(
        design,
        params,
        context,
        distance=float(distance),
        seed=int(history_seed),
    )
    window = int(design["pseudo_islands"]["terminal_window_years"])
    trait_window = []
    pl_window = []
    visitor_window = []
    years = int(design["common_operator"]["years"])

    for year in range(years):
        counts, ledger = density_step_model3e(
            counts,
            grid,
            visitors[year],
            immigrants[year],
            design,
            params,
        )
        if year >= years - window:
            tm = weighted_trait_means(counts, grid)
            if tm is None or ledger["pollen_limitation"] is None:
                return {
                    "defined": False,
                    "stratum": stratum,
                    "distance": float(distance),
                    "history_seed": int(history_seed),
                    "x_distance": float(x_distance),
                }
            trait_window.append(tm)
            pl_window.append(float(ledger["pollen_limitation"]))
            visitor_window.append(float(ledger["visitor_count"]))

    traits = np.mean(np.asarray(trait_window, dtype=float), axis=0)
    return {
        "defined": True,
        "stratum": stratum,
        "distance": float(distance),
        "history_seed": int(history_seed),
        "x_distance": float(x_distance),
        "accessibility": float(traits[0]),
        "display_investment": float(traits[1]),
        "display_dulling": float(1.0 - traits[1]),
        "assurance": float(traits[2]),
        "pollen_limitation": float(np.mean(pl_window)),
        "visitor_count": float(np.mean(visitor_window)),
    }


def _fit_one(design: dict, targets: dict, parameter_set: dict, contexts: dict, grid) -> dict:
    params = _to_params(parameter_set["params"])
    xmap = _standardized_log_distance(design["pseudo_islands"]["distances"])
    rows = []
    for stratum in design["pseudo_islands"]["strata"]:
        for distance in design["pseudo_islands"]["distances"]:
            for history_seed in design["pseudo_islands"]["history_seeds"]:
                rows.append(
                    _run_pseudo_island(
                        design,
                        params,
                        contexts[stratum],
                        stratum=stratum,
                        distance=float(distance),
                        history_seed=int(history_seed),
                        x_distance=xmap[float(distance)],
                        grid=grid,
                    )
                )

    defined = all(r["defined"] for r in rows)
    if not defined:
        return {
            **parameter_set,
            "defined": False,
            "eligible": False,
            "score": None,
            "reason": "at_least_one_terminal_window_undefined",
        }

    strata = list(design["pseudo_islands"]["strata"])
    model_slopes = {"assurance": [], "accessibility": [], "display_dulling": []}
    per_stratum = {}
    for stratum in strata:
        rr = [r for r in rows if r["stratum"] == stratum]
        x = [r["x_distance"] for r in rr]
        ss = {
            "assurance": _slope([r["assurance"] for r in rr], x),
            "accessibility": _slope([r["accessibility"] for r in rr], x),
            "display_dulling": _slope([r["display_dulling"] for r in rr], x),
        }
        per_stratum[stratum] = ss
        for key in model_slopes:
            model_slopes[key].append(ss[key])

    h3 = _pooled_stratum_adjusted_slope(rows, "pollen_limitation")
    if h3 is None or any(v is None for vals in model_slopes.values() for v in vals):
        return {
            **parameter_set,
            "defined": True,
            "eligible": False,
            "score": None,
            "reason": "regression_undefined",
        }

    target_h1 = targets["fit_targets"]["H1_all_analysis_domain_slopes"]
    target_vectors = {
        key: [float(target_h1[s][key]) for s in strata]
        for key in model_slopes
    }
    scales = {}
    nrmse = {}
    for key in model_slopes:
        scales[key] = _positive_scale(model_slopes[key], target_vectors[key])
        nrmse[key] = _nrmse(model_slopes[key], target_vectors[key], scales[key])

    h3_target = float(targets["fit_targets"]["H3_global_pollen_limitation_slope"]["estimate"])
    h3_se = float(targets["fit_targets"]["H3_global_pollen_limitation_slope"]["se"])
    h3_z = float((h3 - h3_target) / h3_se)

    sign_gate = bool(
        all(v > 0 for v in model_slopes["assurance"])
        and all(v > 0 for v in model_slopes["accessibility"])
        and h3 > 0
    )
    score = float(
        nrmse["assurance"]
        + nrmse["accessibility"]
        + nrmse["display_dulling"]
        + h3_z * h3_z
    )
    eligible = bool(sign_gate and score <= 4.0)
    return {
        **parameter_set,
        "defined": True,
        "eligible": eligible,
        "score": score,
        "sign_gate": sign_gate,
        "domain_scales": scales,
        "domain_nrmse": nrmse,
        "h3_model_slope": h3,
        "h3_z_error": h3_z,
        "model_h1_slopes": per_stratum,
        "mean_terminal_visitor_count": float(np.mean([r["visitor_count"] for r in rows])),
    }


def run(design: dict, targets: dict) -> dict:
    if design["status"] != "prospective_frozen_before_model3e_screening":
        raise ValueError("Model 3E screening design must be prospectively frozen")
    if targets["status"] != "frozen_empirical_targets_before_model3e_execution":
        raise ValueError("Chapter 1 empirical targets must be frozen before execution")

    contexts = {
        s: make_stratum_context(design, s)
        for s in design["pseudo_islands"]["strata"]
    }
    grid = make_grid(design["common_operator"]["grid_axes"])
    parameter_sets = _lhs_parameter_sets(design)
    results = []

    with threadpool_limits(limits=1):
        for p in parameter_sets:
            results.append(_fit_one(design, targets, p, contexts, grid))

    eligible = sorted(
        [r for r in results if r["eligible"]],
        key=lambda r: r["score"],
    )
    best = eligible[:5]
    return {
        "status": "complete_model3e_h1_h3_screening",
        "held_out_H2_H4_opened": False,
        "n_parameter_sets": len(results),
        "n_eligible": len(eligible),
        "contexts": contexts,
        "accepted_parameter_ids": [r["parameter_id"] for r in best],
        "accepted_parameter_sets": best,
        "all_parameter_summaries": results,
        "fit_success": len(best) > 0,
        "claim_boundary": design["claim_boundary"],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--design", default=str(DEFAULT_DESIGN))
    p.add_argument("--targets", default=str(DEFAULT_TARGETS))
    p.add_argument("--out")
    a = p.parse_args()
    design = json.loads(Path(a.design).read_text(encoding="utf-8"))
    targets = json.loads(Path(a.targets).read_text(encoding="utf-8"))
    result = run(design, targets)
    encoded = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if a.out:
        out = Path(a.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(encoded, encoding="utf-8")
    print(encoded)


if __name__ == "__main__":
    main()
