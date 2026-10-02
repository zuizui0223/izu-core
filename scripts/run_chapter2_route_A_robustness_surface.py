"""Prospective robustness surface for the Route A assurance-by-cost mechanism."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from scripts.model3_island.assays import investment_assay
from scripts.model3_island.density import make_grid
from scripts.model3_island.simulate import simulate
from scripts.model3_island.types import ArrivalConfig, Config, EVENT_ORDER
from scripts.run_chapter2_syndrome_causal_knockout import _founders, _history, _visitors

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "data/design/chapter2_route_A_robustness_surface_20261002.json"


def _config(*, years, capacity, survival, ovule_budget, pollen_budget,
            activity, assurance, investment_cost, depression):
    zero_seed = ArrivalConfig(0.0, 0.0, 1.0, "exponential", 0.0, 0.0)
    zero_visitor = ArrivalConfig(0.0, 0.0, 1.0, "exponential", 0.0, 0.0)
    return Config(
        schema_version=1,
        event_order=EVENT_ORDER,
        time_unit="reproductive_year",
        capacity=int(capacity),
        years=int(years),
        survival=float(survival),
        ovule_budget=float(ovule_budget),
        pollen_budget=float(pollen_budget),
        investment_cost=float(investment_cost),
        pollen_scale=1.0,
        depression=float(depression),
        mutation_rate=0.0,
        mutation_sd=0.025,
        assurance_mode="fixed",
        fixed_assurance=float(assurance),
        assurance_timing="delayed",
        pollen_discount=0.0,
        assurance_cost=0.0,
        activity=float(activity),
        activity_mode="fixed",
        reference_visitor_count=4.0,
        background_ratio=1.0,
        background_resources=1.0,
        seed_arrival=zero_seed,
        visitor_arrival=zero_visitor,
        island_history="founding",
        initial_visitors=0,
        visitor_breadth=0.18,
        visitor_effectiveness=1.0,
        source_allele_means=(0.5, 0.5, 0.5),
        source_allele_sd=0.15,
    )


def _mean_or_none(values):
    x = np.asarray(values, dtype=float)
    x = x[np.isfinite(x)]
    return None if not len(x) else float(x.mean())


def _adjacent_negative(activities, values, *, ceiling=0.1):
    pairs = [(float(a), float(v)) for a, v in zip(activities, values) if float(a) <= ceiling]
    neg = [v < 0 for _, v in pairs]
    return any(neg[i] and neg[i + 1] for i in range(len(neg) - 1))


def _crossing_estimate(activities, values):
    x = np.asarray(activities, dtype=float)
    y = np.asarray(values, dtype=float)
    hits = []
    for i in range(len(x) - 1):
        if y[i] == 0:
            hits.append(float(x[i]))
        elif y[i] * y[i + 1] < 0:
            hits.append(float(x[i] + (0 - y[i]) * (x[i + 1] - x[i]) / (y[i + 1] - y[i])))
    return hits


def run(design: dict) -> dict:
    if design["status"] != "prospective_frozen_before_execution":
        raise ValueError("design must be frozen before execution")

    surface = design["fixed_surface"]
    visitors = _visitors(surface["visitor_composition"])
    founders = _founders(float(surface["starting_access"]), [[0.4, 0.4], [0.4, 0.6], [0.6, 0.6]])

    surface_rows = []
    for depression in surface["inbreeding_depression"]:
        for assurance in surface["fixed_assurance"]:
            for cost in surface["investment_cost"]:
                for activity in surface["activities"]:
                    cfg = _config(
                        years=80,
                        capacity=48,
                        survival=0.0,
                        ovule_budget=8.0,
                        pollen_budget=20.0,
                        activity=activity,
                        assurance=assurance,
                        investment_cost=cost,
                        depression=depression,
                    )
                    assay = investment_assay(founders, visitors, cfg, step=0.05)
                    surface_rows.append({
                        "activity": float(activity),
                        "assurance": float(assurance),
                        "investment_cost": float(cost),
                        "depression": float(depression),
                        "total_gradient": float(np.mean(assay["total_gradient"])),
                        "outcross_gradient": float(np.mean(assay["outcross_gradient"])),
                    })

    low = [
        r for r in surface_rows
        if r["activity"] <= 0.1 and r["assurance"] >= 0.5 and r["investment_cost"] >= 0.5
    ]
    overall_negative_fraction = float(np.mean([r["total_gradient"] < 0 for r in low]))
    negative_fraction_by_depression = {
        str(d): float(np.mean([
            r["total_gradient"] < 0 for r in low if r["depression"] == float(d)
        ]))
        for d in surface["inbreeding_depression"]
    }
    surface_nonisolated = bool(
        overall_negative_fraction >= 0.5
        and all(v >= 0.25 for v in negative_fraction_by_depression.values())
    )

    central_profiles = {}
    contiguous_by_depression = {}
    crossings_by_depression = {}
    for depression in surface["inbreeding_depression"]:
        rows = sorted([
            r for r in surface_rows
            if r["depression"] == float(depression)
            and r["assurance"] == 0.5
            and r["investment_cost"] == 0.5
        ], key=lambda r: r["activity"])
        acts = [r["activity"] for r in rows]
        vals = [r["total_gradient"] for r in rows]
        central_profiles[str(depression)] = [
            {"activity": a, "total_gradient": v} for a, v in zip(acts, vals)
        ]
        contiguous_by_depression[str(depression)] = _adjacent_negative(acts, vals)
        crossings_by_depression[str(depression)] = _crossing_estimate(acts, vals)
    central_contiguous = bool(all(contiguous_by_depression.values()))

    traj = design["trajectory_check"]
    trajectory_rows = []
    grid = make_grid(([0.5], [0.4, 0.5, 0.6], [0.5]))
    for life_name, life in traj["life_histories"].items():
        for depression in traj["inbreeding_depression"]:
            for activity in traj["activities"]:
                cfg = _config(
                    years=traj["years"],
                    capacity=traj["capacity"],
                    survival=life["survival"],
                    ovule_budget=life["ovule_budget"],
                    pollen_budget=life["pollen_budget"],
                    activity=activity,
                    assurance=traj["fixed_assurance"],
                    investment_cost=traj["investment_cost"],
                    depression=depression,
                )
                history = _history(_visitors(traj["visitor_composition"]), cfg.years)
                founders_t = _founders(float(traj["starting_access"]), [[0.4, 0.4], [0.4, 0.6], [0.6, 0.6]])
                initial = float(founders_t.alleles[:, 1].mean())
                density_change = None
                abm_changes = []
                occupancy = []
                for rep in traj["demographic_replicates"]:
                    result = simulate(
                        cfg, history, founders_t, replicate=int(rep), grid=grid,
                        projection_mode="grid", immigration_mode="source",
                    )
                    if density_change is None:
                        x = result["density_traits"][-1, 1]
                        density_change = float(x - initial) if np.isfinite(x) else None
                    x = result["trait_mean"][-1, 1]
                    abm_changes.append(float(x - initial) if np.isfinite(x) else np.nan)
                    occupancy.append(bool(result["population"][-1] > 0))
                trajectory_rows.append({
                    "life_history": life_name,
                    "activity": float(activity),
                    "depression": float(depression),
                    "density_investment_change": density_change,
                    "abm_mean_investment_change": _mean_or_none(abm_changes),
                    "abm_terminal_occupancy": float(np.mean(occupancy)),
                })

    target_rows = [
        r for r in trajectory_rows if r["activity"] == 0.05
    ]
    life_history_details = []
    for r in target_rows:
        ok = (
            r["density_investment_change"] is not None
            and r["density_investment_change"] < 0
            and r["abm_mean_investment_change"] is not None
            and r["abm_mean_investment_change"] < 0
            and r["abm_terminal_occupancy"] > 0
        )
        life_history_details.append({**r, "passes": bool(ok)})
    life_history_propagation = bool(all(r["passes"] for r in life_history_details))

    route_A_robust = bool(surface_nonisolated and central_contiguous and life_history_propagation)
    return {
        "status": "complete_route_A_robustness_surface",
        "surface_rows": surface_rows,
        "surface_diagnostics": {
            "low_region_negative_fraction": overall_negative_fraction,
            "negative_fraction_by_depression": negative_fraction_by_depression,
            "surface_nonisolated": surface_nonisolated,
            "central_contiguous_by_depression": contiguous_by_depression,
            "central_contiguous": central_contiguous,
            "central_crossings_by_depression": crossings_by_depression,
            "central_profiles": central_profiles,
        },
        "trajectory_rows": trajectory_rows,
        "life_history_activity_0_05": life_history_details,
        "life_history_propagation": life_history_propagation,
        "route_A_robust": route_A_robust,
        "headline_decision": (
            "retain_route_A_as_headline_model_mechanism"
            if route_A_robust
            else "drop_route_A_from_headline_retain_as_model_conditional_SI"
        ),
        "claim_boundary": design["claim_boundary"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--design", default=str(DEFAULT_DESIGN))
    parser.add_argument("--out")
    args = parser.parse_args()
    design = json.loads(Path(args.design).read_text(encoding="utf-8"))
    result = run(design)
    encoded = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(encoded, encoding="utf-8")
    print(encoded)


if __name__ == "__main__":
    main()
