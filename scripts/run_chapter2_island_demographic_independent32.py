"""Frozen independent island-history demographic persistence assay (32 histories).

This file reproduces the exact biological event sequence of the independent
2026-10-08 offline study. Historical founders and visitors come from the
previously frozen source model; the demographic shock is fully declared in
data/design/chapter2_island_demographic_independent32_20261008.json.

Important: a 32-history bootstrap is not 4096 independent observations.
"""
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import replace
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import os

import numpy as np

from scripts.run_chapter2_assurance_generality import (
    config, founders, load_design as load_generality,
)
from scripts.run_model3_persistent_isolation import exposure
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.population import advance, subset
from scripts.model3_island.randomness import stream, STREAM_IDS

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_island_demographic_independent32_20261008.json"


def load_frozen():
    d = json.loads(DESIGN.read_text(encoding="utf-8"))
    if d["status"] != "frozen_before_new_history_demographic_confirmation":
        raise ValueError("unexpected design status")
    if d["total_groups"] != 512 or d["total_post_trajectories"] != 4096:
        raise ValueError("unexpected independent design counts")
    if d["stress_ovule_budgets"] != [2, 3, 4, 5]:
        raise ValueError("unexpected stress conditions")
    source = load_generality(ROOT / d["source_biology"])
    return d, source


def tasks(d):
    return list(product(
        d["settings"],
        d["modes"],
        range(
            d["independent_visitor_histories"]["first"],
            d["independent_visitor_histories"]["last"] + 1,
        ),
        d["demographic_repeat_seeds"],
        d["pre_environments"],
    ))


def census(state):
    if not len(state.ids):
        return None
    return state.alleles.mean(axis=(0, 2)).tolist()


def run_group(g, d, source):
    setting, mode, h, rep, pre = g
    cfg = config(source, setting, d["pre_mutation_rate"], mode)
    pre_history = exposure(h, pre)
    resident = founders(source)
    master = int(np.random.SeedSequence([h, rep]).generate_state(1)[0])
    streams = {name: stream(master, name, 0) for name in STREAM_IDS}
    for year in range(d["prehistories"]):
        ledger = reproduce(resident, pre_history.visitors[year], cfg)
        resident, _ = advance(
            resident, ledger, pre_history.seed_candidates[year], cfg, streams,
            year=year, mutation_traits=(True, True, mode == "evolving"),
        )

    n = d["source_bottleneck_n"]
    if len(resident.ids) < n:
        return {"group": g, "pre_survivors": len(resident.ids),
                "post_cases": None}
    sample_seed = int(np.random.SeedSequence([h, rep, 117]).generate_state(1)[0])
    indices = np.random.default_rng(sample_seed).choice(
        len(resident.ids), size=n, replace=False
    )
    shock_founders = subset(resident, indices)
    cases = []

    for post, budget in product(
        d["post_environments"], d["stress_ovule_budgets"]
    ):
        post_cfg = replace(
            cfg, capacity=d["post_capacity"], ovule_budget=float(budget),
        )
        # Critically, pre is NOT part of this seed. Counterfactual historical
        # populations thus receive common post-event demographic random draws.
        common_seed = int(np.random.SeedSequence([
            h, rep, d["settings"].index(setting), d["modes"].index(mode),
            d["post_environments"].index(post),
            d["stress_ovule_budgets"].index(budget), 713
        ]).generate_state(1)[0])
        rng = {name: stream(common_seed, name, 0) for name in STREAM_IDS}
        history = exposure(h + d["post_seed_offset"], post)
        current = shock_founders
        first = reproduce(current, history.visitors[0], post_cfg)
        immediate = float(first.maternal.sum() / n)
        first_extinction = None
        minimum = n

        for j in range(d["post_updates"]):
            ledger = reproduce(current, history.visitors[j], post_cfg)
            current, _ = advance(
                current, ledger, history.seed_candidates[j], post_cfg, rng,
                year=d["prehistories"] + j,
                mutation_traits=(True, True, mode == "evolving"),
            )
            if len(current.ids) == 0 and first_extinction is None:
                first_extinction = j + 1
            minimum = min(minimum, len(current.ids))

        cases.append({
            "post": post, "ovule_budget": float(budget),
            "occupied": int(len(current.ids) > 0),
            "terminal_N": len(current.ids),
            "first_extinction": first_extinction,
            "min_N": minimum,
            "initial_viable_maternal_per_capita": immediate,
            "end_traits": census(current),
        })

    return {
        "group": g,
        "pre_survivors": len(resident.ids),
        "start_traits": census(resident),
        "bottleneck_traits": census(shock_founders),
        "bottleneck_sha256": hashlib.sha256(
            shock_founders.alleles.tobytes()
        ).hexdigest(),
        "post_cases": cases,
    }


def save(path, payload):
    raw = (json.dumps(payload, sort_keys=True, allow_nan=False) + "\n").encode()
    temporary = path.with_suffix(".tmp")
    temporary.write_bytes(raw)
    os.replace(temporary, path)
    return hashlib.sha256(raw).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--shard-index", type=int, required=True)
    p.add_argument("--shard-count", type=int, default=8)
    p.add_argument("--workers", type=int, default=2)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    d, source = load_frozen()
    declared = tasks(d)
    if len(declared) != 512 or not 0 <= args.shard_index < args.shard_count:
        raise ValueError("invalid task count or shard selection")
    selected = [
        g for i, g in enumerate(declared)
        if i % args.shard_count == args.shard_index
    ]
    if args.dry_run:
        print(json.dumps({"groups": len(selected),
                          "post_trajectories": 8 * len(selected)}))
        return
    args.out.mkdir(parents=True, exist_ok=True)
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run_group, g, d, source) for g in selected]
        results = [f.result() for f in as_completed(futures)]
    results.sort(key=lambda r: tuple(r["group"]))
    if len(results) != len(selected):
        raise RuntimeError("missing historical group")
    name = f"demographic_independent32_shard_{args.shard_index:02d}.json"
    digest = save(args.out / name, results)
    print(json.dumps({"groups": len(results), "cases": sum(
        len(r["post_cases"]) for r in results if r["post_cases"] is not None
    ), "sha256": digest}))


if __name__ == "__main__":
    main()
