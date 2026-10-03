"""Prospective finite-population long-horizon persistence diagnostic.

Designed after the deterministic-density long-horizon diagnostic revealed
sub-individual density masses. This runner uses the same Model 3 finite
reproduction/inheritance/demography operator and records compact checkpoints.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.model3_island.density import make_grid, project_state
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.run import founders_from_spec, history_from_spec
from scripts.model3_island.types import Config

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "data/design/chapter2_finite_long_horizon_persistence_20261003.json"
DEFAULT_PARENT = ROOT / "data/design/model3_ch2_bridge_20260927.json"


def _trait_mean(state):
    if not len(state.ids):
        return None
    return float(state.alleles[:, 1, :].mean())


def _simulate_compact(cfg, history, founders, *, replicate, grid, checkpoints):
    # Match the frozen bridge: founder support is projected once even in
    # continuous projection mode; offspring thereafter remain continuous.
    state, _ = project_state(founders, grid)
    initial = _trait_mean(state)
    if initial is None:
        raise ValueError("empty founder state")
    streams = {name: stream(replicate, name, 0) for name in STREAM_IDS}
    wanted = set(int(x) for x in checkpoints)
    reports = {}
    extinction_year = None

    for year in range(cfg.years):
        if len(state.ids):
            ledger = reproduce(state, history.visitors[year], cfg)
            state, _ = advance(
                state,
                ledger,
                history.seed_candidates[year],
                cfg,
                streams,
                year=year,
            )
            if not len(state.ids) and extinction_year is None:
                extinction_year = year + 1
        # With zero seed supply extinction is absorbing, but keep checkpoint
        # accounting explicit without inventing post-extinction traits.
        y = year + 1
        if y in wanted:
            mean = _trait_mean(state)
            reports[y] = {
                "population": int(len(state.ids)),
                "occupied": bool(len(state.ids)),
                "investment_mean": mean,
                "investment_change": None if mean is None else float(mean - initial),
            }
        if extinction_year is not None and y >= max(wanted):
            break

    # Fill later checkpoints after absorbing extinction.
    if extinction_year is not None:
        for y in sorted(wanted):
            if y >= extinction_year and y not in reports:
                reports[y] = {
                    "population": 0,
                    "occupied": False,
                    "investment_mean": None,
                    "investment_change": None,
                }
    missing = sorted(wanted - set(reports))
    if missing:
        raise ValueError(f"missing checkpoints: {missing}")
    return {
        "initial_investment": initial,
        "extinction_year": extinction_year,
        "reports": [dict(year=y, **reports[y]) for y in sorted(wanted)],
    }


def run_shard(design, parent, shard_index, shard_count):
    if design["status"] != "prospective_frozen_after_density_stationarity_diagnostic_before_finite_execution":
        raise ValueError("frozen finite diagnostic design required")
    if parent["status"] != "frozen":
        raise ValueError("frozen bridge parent required")
    checkpoints = [int(x) for x in design["horizons"]]
    if max(checkpoints) != int(design["max_horizon"]):
        raise ValueError("checkpoint/horizon mismatch")

    histories_all = [int(x) for x in parent["history_seeds"]]
    histories = [h for i, h in enumerate(histories_all) if i % shard_count == shard_index]
    if not histories:
        raise ValueError("empty shard")

    grid = make_grid(parent["grid_axes"])
    starts = [float(x) for x in design["starts"]]
    demos = [int(x) for x in design["demographic_seeds"]]
    rows = []

    for depression in design["depressions"]:
        base = Config.from_dict(parent["base_config"])
        base = replace(
            base,
            years=int(design["max_horizon"]),
            depression=float(depression),
        )
        if base.seed_arrival.supply != 0:
            raise ValueError("finite persistence diagnostic requires zero seed supply")
        near_cfg = replace(base, visitor_arrival=replace(base.visitor_arrival, distance=0.0))
        far_cfg = replace(base, visitor_arrival=replace(base.visitor_arrival, distance=3.0))

        for hs in histories:
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

                for ds in demos:
                    replicate = int(np.random.SeedSequence([hs, ds]).generate_state(1)[0])
                    for arm, cfg, history in (
                        ("near", near_cfg, near_history),
                        ("far", far_cfg, far_history),
                    ):
                        result = _simulate_compact(
                            cfg, history, founders,
                            replicate=replicate,
                            grid=grid,
                            checkpoints=checkpoints,
                        )
                        rows.append({
                            "depression": float(depression),
                            "history_seed": hs,
                            "start_investment": start,
                            "demographic_seed": ds,
                            "arm": arm,
                            **result,
                        })

    return {
        "status": "complete_finite_long_horizon_persistence_shard",
        "shard_index": int(shard_index),
        "shard_count": int(shard_count),
        "histories": histories,
        "n_trajectories": len(rows),
        "rows": rows,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--design", default=str(DEFAULT_DESIGN))
    p.add_argument("--parent", default=str(DEFAULT_PARENT))
    p.add_argument("--shard-index", type=int, required=True)
    p.add_argument("--shard-count", type=int, required=True)
    p.add_argument("--out", required=True)
    a = p.parse_args()
    if a.shard_count < 1 or not 0 <= a.shard_index < a.shard_count:
        raise ValueError("invalid shard specification")
    design = json.loads(Path(a.design).read_text(encoding="utf-8"))
    parent = json.loads(Path(a.parent).read_text(encoding="utf-8"))
    result = run_shard(design, parent, a.shard_index, a.shard_count)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "shard": a.shard_index,
        "n_trajectories": result["n_trajectories"],
    }, indent=2))


if __name__ == "__main__":
    main()
