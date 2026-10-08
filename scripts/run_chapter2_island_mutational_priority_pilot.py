"""Explore how the order of mutational access to floral investment and assurance affects persistence.

This manipulates mutation supply, NOT trait-expression order or equal-duration
evolutionary opportunity. The source model and earlier confirmed results remain
unchanged. Four visitor histories with nested repeats: exploratory only.
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
from scripts.run_chapter2_assurance_generality import config, founders, load_design as load_source
from scripts.run_model3_persistent_isolation import exposure
from scripts.model3_island.population import advance, subset
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.randomness import stream, STREAM_IDS

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_island_mutational_priority_pilot_20261008.json"


def load_pilot(path=DESIGN):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    assert d["status"] == "exploratory_mutational_access_order_protocol_preoutcome"
    assert d["total_prehistory_groups"] == 256
    assert d["total_post_stress_trajectories"] == 2048
    source = load_source(ROOT / d["source_biology"])
    assert set(d["settings"]) == set(source["settings"])
    return d, source


def groups(d):
    return list(product(d["settings"], d["new_visitor_history_seeds"],
        d["nested_demographic_repeat_seeds"], d["pre_visitor_environments"],
        d["schedules"]))


def founders_zero_standing(source):
    state = founders(source)
    alleles = state.alleles.copy()
    alleles[:, 1:3, :] = 0.5
    return replace(state, alleles=alleles)


def census(state):
    if len(state.ids) == 0:
        return None
    traits = state.alleles.mean(axis=2)
    return {
        "n": len(state.ids),
        "means": traits.mean(axis=0).tolist(),
        "variance": traits.var(axis=0).tolist(),
        "allele_variance": state.alleles.var(axis=(0, 2)).tolist(),
    }


def simulate_group(group, d, source):
    setting, h, repeat, pre, schedule = group
    cfg = config(source, setting, d["mutation_rate"], "evolving")
    history = exposure(h, pre)
    resident = founders_zero_standing(source)
    master = int(np.random.SeedSequence([h, repeat]).generate_state(1)[0])
    streams = {name: stream(master, name, 0) for name in STREAM_IDS}
    first_threshold_crossing = {"investment": None, "assurance": None}
    midpoint = None

    for t in range(d["total_prehistory_generations"]):
        if t == d["initial_phase_generations"]:
            midpoint = census(resident)
            early_mask = d["schedules"][schedule]["phase1_mutation_mask"]
            for k in (1, 2):
                if not early_mask[k] and not np.array_equal(
                    resident.alleles[:, k, :],
                    np.full_like(resident.alleles[:, k, :], 0.5)
                ):
                    raise AssertionError("locked locus acquired mutations: " + str(group))
        mask = (d["schedules"][schedule]["phase1_mutation_mask"]
                if t < d["initial_phase_generations"]
                else d["schedules"][schedule]["phase2_mutation_mask"])
        ledger = reproduce(resident, history.visitors[t], cfg)
        resident, _ = advance(
            resident, ledger, history.seed_candidates[t], cfg, streams, year=t,
            mutation_traits=tuple(mask)
        )
        if len(resident.ids):
            current = resident.alleles.mean(axis=(0, 2))
            for k, name in ((1, "investment"), (2, "assurance")):
                if first_threshold_crossing[name] is None and abs(current[k] - 0.5) >= 0.05:
                    first_threshold_crossing[name] = t + 1

    end_pre = census(resident)
    n = d["post_bottleneck_n"]
    if len(resident.ids) < n:
        return {"group": group, "mid": midpoint, "end_pre": end_pre,
                "first_hit": first_threshold_crossing, "post_cases": None}

    bottleneck_seed = int(np.random.SeedSequence([h, repeat, 117]).generate_state(1)[0])
    selected = np.random.default_rng(bottleneck_seed).choice(
        len(resident.ids), size=n, replace=False
    )
    bottleneck = subset(resident, selected)
    post_cases = []
    for post, budget in product(d["post_visitor_environments"], d["post_ovule_budgets"]):
        post_cfg = replace(cfg, capacity=d["post_bottleneck_capacity"],
                           ovule_budget=float(budget))
        # Neither historical pre-environment nor schedule enters this RNG.
        common_seed = int(np.random.SeedSequence([
            h, repeat, d["settings"].index(setting),
            d["post_visitor_environments"].index(post),
            d["post_ovule_budgets"].index(budget), 713
        ]).generate_state(1)[0])
        rng = {name: stream(common_seed, name, 0) for name in STREAM_IDS}
        future = exposure(h + d["post_visitor_seed_offset"], post)
        current = bottleneck
        initial_viable = float(
            reproduce(current, future.visitors[0], post_cfg).maternal.sum() / n
        )
        first_extinction = None
        for j in range(d["post_stress_generations"]):
            ledger = reproduce(current, future.visitors[j], post_cfg)
            current, _ = advance(
                current, ledger, future.seed_candidates[j], post_cfg, rng,
                year=d["total_prehistory_generations"] + j,
                mutation_traits=(True, True, True),
            )
            if not len(current.ids) and first_extinction is None:
                first_extinction = j + 1
        post_cases.append({
            "post": post, "budget": float(budget),
            "occupied": int(bool(len(current.ids))),
            "end_n": len(current.ids), "first_extinction": first_extinction,
            "initial_viable": initial_viable,
            "end_traits": census(current),
        })
    return {
        "group": group, "mid": midpoint, "end_pre": end_pre,
        "first_hit": first_threshold_crossing,
        "bottleneck_hash": hashlib.sha256(bottleneck.alleles.tobytes()).hexdigest(),
        "post_cases": post_cases,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--shard-count", type=int, default=4)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    d, source = load_pilot()
    declared = groups(d)
    if len(declared) != 256 or not 0 <= args.shard_index < args.shard_count:
        raise ValueError("invalid task count or shard choice")
    chosen = [g for i, g in enumerate(declared) if i % args.shard_count == args.shard_index]
    if args.dry_run:
        print(json.dumps({"groups": len(chosen), "post_stress_cases": 8 * len(chosen)}))
        return
    args.out.mkdir(parents=True, exist_ok=True)
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        rows = [f.result() for f in as_completed(
            pool.submit(simulate_group, g, d, source) for g in chosen
        )]
    rows.sort(key=lambda r: tuple(r["group"]))
    if len(rows) != len(chosen) or any(
        r["post_cases"] is None or len(r["post_cases"]) != 8 for r in rows
    ):
        raise RuntimeError("pilot incomplete or prehistory group unoccupied")
    path = args.out / f"priority_shard_{args.shard_index:02d}.json"
    raw = (json.dumps(rows, sort_keys=True, allow_nan=False) + "\n").encode()
    temp = path.with_suffix(".tmp")
    temp.write_bytes(raw)
    os.replace(temp, path)
    print(json.dumps({
        "groups": len(rows), "post_trajectories": 8 * len(rows),
        "raw_sha256": hashlib.sha256(raw).hexdigest(),
    }))


if __name__ == "__main__":
    main()
