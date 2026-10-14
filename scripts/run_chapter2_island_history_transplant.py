"""Exploratory island-history reciprocal pollinator-community transplant.

A paired finite population is evolved once under the pre-switch environment,
then forked into post-switch environments and post-switch mutation treatments.
This is deliberately not a direct temporal-order manipulation or an island
colonization simulation.
"""
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import deepcopy
from dataclasses import replace
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import os

import numpy as np

from scripts.model3_island.population import advance
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.model3_island.reproduction import reproduce
from scripts.run_chapter2_assurance_generality import (
    config as generality_config,
    founders as generality_founders,
    load_design as generality_load,
)
from scripts.run_model3_persistent_isolation import exposure

ROOT = Path(__file__).resolve().parents[1]
DESIGN_PATH = ROOT / "data/design/chapter2_island_history_transplant_20261008.json"


def load_design(path=DESIGN_PATH):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    if d["status"] != "exploratory_pilot_protocol_locked_before_execution":
        raise ValueError("unexpected pilot protocol status")
    if d["pre_periods"] != 400 or d["post_periods"] != 400:
        raise ValueError("unexpected time horizon")
    if sorted(d["post_mutation_probabilities"]) != [0, 0.01]:
        raise ValueError("unexpected mutation treatments")
    source = generality_load(ROOT / d["source_design"])
    if set(d["settings"]) != set(source["settings"]):
        raise ValueError("source setting mismatch")
    if (len(d["visitor_history_seeds"]) != 4
            or len(d["demographic_repeat_seeds"]) != 2):
        raise ValueError("wrong independent sample size")
    if d["campaign"]["total_cases"] != 512:
        raise ValueError("wrong case count")
    return d, source


def declared_groups(d):
    result = list(product(
        d["settings"],
        d["visitor_history_seeds"],
        d["demographic_repeat_seeds"],
        d["modes"],
        d["pre_environments"],
    ))
    if len(result) * len(d["post_environments"]) * len(d["post_mutation_probabilities"]) != d["campaign"]["total_cases"]:
        raise ValueError("pilot task count mismatch")
    return result


def census(state):
    count = len(state.ids)
    if not count:
        return {"count": 0, "traits": None, "trait_variances": None,
                "allele_variances": None}
    traits = state.alleles.mean(axis=2)
    return {
        "count": count,
        "traits": traits.mean(axis=0).tolist(),
        "trait_variances": traits.var(axis=0).tolist(),
        "allele_variances": state.alleles.var(axis=(0, 2)).tolist(),
    }


def snapshot_digest(state):
    return hashlib.sha256(state.alleles.tobytes() + state.ids.tobytes()).hexdigest()


def immediate_reproduction(state, visitors, cfg):
    if not len(state.ids):
        return {"maternal_viable_per_plant": None,
                "outcross_female_per_plant": None,
                "pollen_export_per_plant": None}
    ledger = reproduce(state, visitors, cfg)
    n = len(state.ids)
    return {
        "maternal_viable_per_plant": float(ledger.maternal.sum() / n),
        "outcross_female_per_plant": float(ledger.outcross.sum() / n),
        "pollen_export_per_plant": float(ledger.exported.sum() / n),
    }


def case_id(group, post, post_mutation):
    setting, history, repeat, mode, pre = group
    return (
        f"{setting}_h{history}_r{repeat}_{mode}_{pre}-to-{post}_"
        f"postmu{post_mutation:.2f}"
    )


def atomic_json(path, data):
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, sort_keys=True, indent=2, allow_nan=False) + "\n",
                   encoding="utf-8")
    os.replace(tmp, path)


def write_case(directory, payload):
    path = directory / (payload["case_id"] + ".json")
    receipt = directory / (payload["case_id"] + ".sha256")
    serialized = (json.dumps(payload, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()
    digest = hashlib.sha256(serialized).hexdigest()
    if path.exists():
        if path.read_bytes() != serialized or receipt.read_text().strip() != digest:
            raise ValueError("existing pilot case differs: " + str(path))
        return
    tmp = path.with_suffix(".tmp")
    tmp.write_bytes(serialized)
    os.replace(tmp, path)
    receipt.write_text(digest + "\n", encoding="utf-8")


def run_group(d, source, group, out):
    setting, history, repeat, mode, pre = group
    c_pre = generality_config(source, setting, d["pre_mutation_probability"], mode)
    if c_pre.seed_arrival.supply != 0:
        raise ValueError("the transplant currently requires no plant immigration")
    state = generality_founders(source)
    starting = census(state)
    visitor_pre = exposure(history, pre)
    master = int(np.random.SeedSequence([history, repeat]).generate_state(1)[0])
    streams = {name: stream(master, name, 0) for name in STREAM_IDS}
    pre_occupied = 1 if len(state.ids) else 0

    for year in range(d["pre_periods"]):
        ledger = reproduce(state, visitor_pre.visitors[year], c_pre)
        state, _ = advance(state, ledger, visitor_pre.seed_candidates[year],
                           c_pre, streams, year=year,
                           mutation_traits=(True, True, mode == "evolving"))
        pre_occupied += int(bool(len(state.ids)))

    switch = census(state)
    genetic_snapshot_sha256 = snapshot_digest(state)
    future_history = history + d["post_visitor_seed_offset"]

    for post, post_mu in product(d["post_environments"], d["post_mutation_probabilities"]):
        h = exposure(future_history, post)
        c_post = replace(c_pre, mutation_rate=float(post_mu))
        # Each future intervention begins with the same exact realised finite
        # population and the same RNG state, not a fresh founder sample.
        rng = deepcopy(streams)
        resident = state
        immediate = immediate_reproduction(resident, h.visitors[0], c_post)
        post_occupied = int(bool(len(resident.ids)))
        min_n = len(resident.ids)
        for j in range(d["post_periods"]):
            year = d["pre_periods"] + j
            ledger = reproduce(resident, h.visitors[j], c_post)
            resident, _ = advance(
                resident, ledger, h.seed_candidates[j], c_post, rng,
                year=year, mutation_traits=(True, True, mode == "evolving")
            )
            post_occupied += int(bool(len(resident.ids)))
            min_n = min(min_n, len(resident.ids))
        payload = {
            "status": "exploratory_pilot_case",
            "case_id": case_id(group, post, post_mu),
            "setting": setting, "visitor_history_seed": history,
            "demographic_repeat_seed": repeat, "assurance_mode": mode,
            "pre_environment": pre, "post_environment": post,
            "post_mutation_probability": post_mu,
            "pre_periods": d["pre_periods"], "post_periods": d["post_periods"],
            "start": starting, "switch": switch, "end": census(resident),
            "switch_genetic_snapshot_sha256": genetic_snapshot_sha256,
            "immediate_post_switch_reproduction": immediate,
            "pre_occupied_censuses": pre_occupied,
            "post_occupied_censuses": post_occupied,
            "min_post_population": min_n,
            "ever_extinct_in_post": min_n == 0,
        }
        write_case(out, payload)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--shard-index", type=int, default=0)
    p.add_argument("--shard-count", type=int, default=1)
    p.add_argument("--workers", type=int, default=2)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    d, source = load_design()
    groups = declared_groups(d)
    if args.shard_count < 1 or not 0 <= args.shard_index < args.shard_count:
        raise ValueError("invalid shard choice")
    tasks = [g for i, g in enumerate(groups)
             if i % args.shard_count == args.shard_index]
    print(json.dumps({"groups": len(tasks),
                      "cases": len(tasks) * 4,
                      "shard": args.shard_index}))
    if args.dry_run:
        return
    args.out.mkdir(parents=True, exist_ok=True)
    design_hash = hashlib.sha256(DESIGN_PATH.read_bytes()).hexdigest()
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run_group, d, source, group, args.out)
                   for group in tasks]
        for future in as_completed(futures):
            future.result()
    cases = sorted(args.out.glob("*_postmu*.json"))
    if len(cases) != 4 * len(tasks):
        raise RuntimeError("pilot shard incomplete")
    atomic_json(args.out / f"shard_{args.shard_index:02d}_complete.json", {
        "status": "pilot_shard_complete",
        "design_sha256": design_hash, "groups": len(tasks),
        "cases": len(cases), "case_files": [p.name for p in cases],
    })


if __name__ == "__main__":
    main()
