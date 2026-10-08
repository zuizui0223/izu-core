"""Conditional demographic RNG repeatability for assurance donor versus mean targeting.

Four previously observed history seeds; 8 NEW postshock demographic RNG streams
per matched genotype pair. The histories are NOT new independent ecology samples.
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

from scripts.run_chapter2_assurance_generality import config
from scripts.run_chapter2_island_genetic_state_transplant import history_state
from scripts.run_chapter2_island_assurance_donor_mean_distribution import (
    load_protocol as load_original_protocol, state_variant
)
from scripts.run_model3_persistent_isolation import exposure
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import stream, STREAM_IDS

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_island_assurance_postshock_rng_repeatability_20261008.json"


def load_design():
    d = json.loads(DESIGN.read_text(encoding="utf-8"))
    parent, biology, source = load_original_protocol()
    if d["status"] != "explanatory_demographic_rng_repeatability_protocol_declared_before_new_repeats":
        raise ValueError("not a declared diagnostic")
    if d["historical_demographic_repeat_seed"] != parent["demographic_repeat_seed"]:
        raise ValueError("historical repeat must be the original independent16")
    if d["settings"] != parent["settings"]:
        raise ValueError("reproductive setting mismatch")
    if not set(d["historical_visitor_seeds"]).issubset(
        range(parent["visitor_history_range"][0],
              parent["visitor_history_range"][1] + 1)
    ):
        raise ValueError("historical seeds absent from parent campaign")
    assert d["n_postshock_trajectories"] == 2048
    return d, parent, biology, source


def declared_groups(d):
    return list(product(d["settings"], d["historical_visitor_seeds"]))


def simulate_pair(group, d, parent, biology, source):
    setting, h = group
    states = {
        bg: history_state(biology, source, setting, h, bg)
        for bg in d["backgrounds"]
    }
    original = config(source, setting, .01, "evolving")
    rows = []
    for bg, variant, post, budget in product(
        d["backgrounds"], d["treatments"],
        d["future_visitor_environments"], d["post_ovule_budgets"],
    ):
        state = state_variant(states, bg, variant)
        cfg = replace(original, capacity=d["post_capacity"],
                      ovule_budget=float(budget))
        future = exposure(h + biology["post_visitor_seed_offset"], post)
        viable = float(reproduce(state, future.visitors[0], cfg).maternal.sum()
                       / d["post_capacity"])
        for repeat_id in d["new_postshock_demographic_repeat_ids"]:
            seed = int(np.random.SeedSequence([
                h, parent["demographic_repeat_seed"],
                d["settings"].index(setting),
                d["future_visitor_environments"].index(post),
                d["post_ovule_budgets"].index(budget),
                713, repeat_id, 20261008
            ]).generate_state(1)[0])
            streams = {name: stream(seed, name, 0) for name in STREAM_IDS}
            resident = state
            first_extinction = None
            for t in range(d["post_updates"]):
                ledger = reproduce(resident, future.visitors[t], cfg)
                resident, _ = advance(
                    resident, ledger, future.seed_candidates[t], cfg, streams,
                    year=parent["pre_updates"] + t,
                    mutation_traits=(True, True, True),
                )
                if not len(resident.ids) and first_extinction is None:
                    first_extinction = t + 1
            rows.append({
                "setting": setting, "history": h,
                "background": bg, "variant": variant,
                "post": post, "budget": float(budget),
                "repeat": repeat_id,
                "occupied": int(bool(len(resident.ids))),
                "end_n": int(len(resident.ids)),
                "first_extinction": first_extinction,
                "viable_maternal": viable,
                "assurance_mean": float(state.alleles[:, 2, :].mean()),
                "assurance_variance": float(state.alleles[:, 2, :].var()),
            })
    if len(rows) != 128:
        raise RuntimeError("incomplete technical repeat grid")
    return rows


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--shard-index", type=int, default=0)
    p.add_argument("--shard-count", type=int, default=4)
    p.add_argument("--workers", type=int, default=2)
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    d, parent, biology, source = load_design()
    groups = declared_groups(d)
    if len(groups) != d["n_historical_pairs"] or not 0 <= a.shard_index < a.shard_count:
        raise ValueError("invalid declared group/shard")
    chosen = [g for i, g in enumerate(groups) if i % a.shard_count == a.shard_index]
    if a.dry_run:
        print(json.dumps({"historical_pairs": len(chosen),
                          "postshock_trajectories": len(chosen) * 128}))
        return
    a.out.mkdir(parents=True, exist_ok=True)
    with ProcessPoolExecutor(max_workers=a.workers) as executor:
        tasks = [executor.submit(simulate_pair, g, d, parent, biology, source)
                 for g in chosen]
        rows = [item for future in as_completed(tasks) for item in future.result()]
    rows.sort(key=lambda r: (
        d["settings"].index(r["setting"]), r["history"], r["background"],
        r["variant"], r["post"], r["budget"], r["repeat"]
    ))
    if len(rows) != len(chosen) * 128:
        raise RuntimeError("postshock cases missing")
    raw = (json.dumps(rows, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()
    output = a.out / f"assurance_rng_repeatability_shard_{a.shard_index:02d}.json"
    temp = output.with_suffix(".tmp")
    temp.write_bytes(raw)
    os.replace(temp, output)
    print(json.dumps({"cases": len(rows),
                      "sha256": hashlib.sha256(raw).hexdigest()}))


if __name__ == "__main__":
    main()
