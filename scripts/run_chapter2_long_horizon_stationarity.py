"""Prospective fixed-horizon stationarity extension for Chapter 2 EL framing.

The design is frozen before execution. This runner does not adapt the horizon
or thresholds to observed outcomes.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.model3_island.density import density_step, make_grid, project_state
from scripts.model3_island.run import founders_from_spec, history_from_spec
from scripts.model3_island.types import Config
from scripts.run_chapter2_mutation_input_calibration_sensitivity import (
    _founders as mutation_founders,
    _simulate as mutation_simulate,
    _visitors as mutation_visitors,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "data/design/chapter2_long_horizon_stationarity_20261003.json"
DEFAULT_BRIDGE = ROOT / "data/design/model3_ch2_bridge_20260927.json"
DEFAULT_MUTATION = ROOT / "data/design/chapter2_mutation_input_calibration_sensitivity_20261002.json"


def _investment(counts, traits):
    mass = float(counts.sum())
    if mass <= 0:
        return None
    return float(counts @ traits[:, 1] / mass)


def _density_checkpoints(cfg, history, founders, grid, checkpoints):
    _, counts = project_state(founders, grid)
    traits = grid.genotypes.mean(axis=2)
    initial = _investment(counts, traits)
    if initial is None:
        raise ValueError("empty initial density")
    wanted = set(int(x) for x in checkpoints)
    reports = {
        0: {
            "investment": initial,
            "investment_change": 0.0,
            "density_mass": float(counts.sum()),
        }
    }
    for year in range(cfg.years):
        counts, _ = density_step(
            counts,
            grid,
            history.visitors[year],
            history.seed_candidates[year],
            cfg,
            immigration_mode="source",
        )
        y = year + 1
        if y in wanted:
            investment = _investment(counts, traits)
            reports[y] = {
                "investment": investment,
                "investment_change": None if investment is None else float(investment - initial),
                "density_mass": float(counts.sum()),
            }
    missing = sorted(wanted - set(reports))
    if missing:
        raise ValueError(f"missing checkpoint reports: {missing}")
    return reports


def run_backbone_shard(design, parent, shard_index, shard_count):
    if design["status"] != "prospective_frozen_before_execution":
        raise ValueError("prospective frozen design required")
    if parent["status"] != "frozen":
        raise ValueError("frozen bridge parent required")
    checkpoints = [int(x) for x in design["checkpoints"]]
    horizon = int(design["max_horizon"])
    if horizon != max(checkpoints):
        raise ValueError("max horizon must equal final checkpoint")
    all_histories = [int(x) for x in parent["history_seeds"]]
    histories = [h for i, h in enumerate(all_histories) if i % shard_count == shard_index]
    if not histories:
        raise ValueError("empty backbone shard")

    base = Config.from_dict(parent["base_config"])
    base = replace(
        base,
        years=horizon,
        depression=float(design["backbone"]["depression"]),
    )
    grid = make_grid(parent["grid_axes"])
    starts = [float(x) for x in design["backbone"]["starts"]]
    rows = []
    for hs in histories:
        near_cfg = replace(base, visitor_arrival=replace(base.visitor_arrival, distance=0.0))
        far_cfg = replace(base, visitor_arrival=replace(base.visitor_arrival, distance=3.0))
        # These are exactly the first near/far assembly histories used by the
        # frozen bridge; matched, pooled and large-population arms are not
        # generated because they are outside this prospective long-horizon test.
        near_history = history_from_spec(near_cfg, {"kind": "assembly"}, hs)
        far_history = history_from_spec(far_cfg, {"kind": "assembly"}, hs)
        for start in starts:
            spec = {
                "count": base.capacity,
                "draw_count": 48,
                "means": [0.5, start, 0.5],
                "sd": 0.15,
                "birth_year": 0,
            }
            founders = founders_from_spec(spec, int(parent["founder_seed"]))
            near = _density_checkpoints(near_cfg, near_history, founders, grid, checkpoints)
            far = _density_checkpoints(far_cfg, far_history, founders, grid, checkpoints)
            for year in checkpoints:
                nc = near[year]["investment_change"]
                fc = far[year]["investment_change"]
                rows.append({
                    "history_seed": hs,
                    "start_investment": start,
                    "year": year,
                    "near_change": nc,
                    "far_change": fc,
                    "effect_far_minus_near": None if nc is None or fc is None else float(fc - nc),
                    "near_density_mass": near[year]["density_mass"],
                    "far_density_mass": far[year]["density_mass"],
                })
    return {
        "status": "complete_long_horizon_backbone_shard",
        "shard_index": int(shard_index),
        "shard_count": int(shard_count),
        "histories": histories,
        "rows": rows,
    }


def _mutation_parent_with_horizon(parent, design):
    out = json.loads(json.dumps(parent))
    out["baseline"]["years"] = int(design["max_horizon"])
    out["baseline"]["report_years"] = [0] + [int(x) for x in design["checkpoints"]]
    return out


def run_mutation_shard(design, parent, shard_index, shard_count):
    if design["status"] != "prospective_frozen_before_execution":
        raise ValueError("prospective frozen design required")
    if parent["status"] != "prospective_frozen_before_execution":
        raise ValueError("frozen mutation parent required")
    p = _mutation_parent_with_horizon(parent, design)
    comparisons = design["mutation_accessibility"]["comparison"]
    combos = []
    for comp in comparisons:
        for capacity in design["mutation_accessibility"]["capacities"]:
            for founder_seed in design["mutation_accessibility"]["founder_seeds"]:
                for demographic_seed in design["mutation_accessibility"]["demographic_seeds"]:
                    for history_name in design["mutation_accessibility"]["visitor_histories"]:
                        combos.append((comp, int(capacity), int(founder_seed), int(demographic_seed), history_name))
    selected = [x for i, x in enumerate(combos) if i % shard_count == shard_index]
    if not selected:
        raise ValueError("empty mutation shard")

    rows = []
    for comp, capacity, founder_seed, demographic_seed, history_name in selected:
        standing_sd = float(comp["standing_sd_investment"])
        ratio = float(comp["VM_over_VG0"])
        founders = mutation_founders(
            p,
            capacity=capacity,
            founder_seed=founder_seed,
            investment_sd=standing_sd,
        )
        optima = p["baseline"]["visitor_histories"][history_name]
        visitors = mutation_visitors(optima)
        result = mutation_simulate(
            p,
            capacity=capacity,
            founders=founders,
            visitors=visitors,
            founder_seed=founder_seed,
            demographic_seed=demographic_seed,
            ratio=ratio,
        )
        initial_mean = next(r["investment_mean"] for r in result["reports"] if r["year"] == 0)
        reports = []
        for report in result["reports"]:
            if report["year"] not in design["checkpoints"]:
                continue
            response = (
                None
                if report["investment_mean"] is None or initial_mean is None
                else float(report["investment_mean"] - initial_mean)
            )
            reports.append({
                "year": int(report["year"]),
                "population": int(report["population"]),
                "investment_mean": report["investment_mean"],
                "investment_response": response,
                "investment_va_proxy": report["investment_va_proxy"],
            })
        rows.append({
            "standing_regime": comp["standing_regime"],
            "standing_sd_investment": standing_sd,
            "target_VM_over_VG0": ratio,
            "capacity": capacity,
            "founder_seed": founder_seed,
            "demographic_seed": demographic_seed,
            "visitor_history": history_name,
            "initial_va_proxy": result["initial_va_proxy"],
            "mutation_sd": result["mutation_sd"],
            "reports": reports,
        })
    return {
        "status": "complete_long_horizon_mutation_shard",
        "shard_index": int(shard_index),
        "shard_count": int(shard_count),
        "n_trajectories": len(rows),
        "rows": rows,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--component", choices=("backbone", "mutation"), required=True)
    parser.add_argument("--design", default=str(DEFAULT_DESIGN))
    parser.add_argument("--parent")
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--shard-count", type=int, default=1)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    if args.shard_count < 1 or not 0 <= args.shard_index < args.shard_count:
        raise ValueError("invalid shard specification")
    design = json.loads(Path(args.design).read_text(encoding="utf-8"))
    if args.component == "backbone":
        parent_path = Path(args.parent) if args.parent else DEFAULT_BRIDGE
        parent = json.loads(parent_path.read_text(encoding="utf-8"))
        result = run_backbone_shard(design, parent, args.shard_index, args.shard_count)
    else:
        parent_path = Path(args.parent) if args.parent else DEFAULT_MUTATION
        parent = json.loads(parent_path.read_text(encoding="utf-8"))
        result = run_mutation_shard(design, parent, args.shard_index, args.shard_count)
    encoded = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(encoded, encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "component": args.component,
        "shard_index": args.shard_index,
        "shard_count": args.shard_count,
        "rows": len(result["rows"]),
    }, indent=2))


if __name__ == "__main__":
    main()
