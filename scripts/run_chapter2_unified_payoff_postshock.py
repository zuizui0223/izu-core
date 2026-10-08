"""Fork a verified t400 diploid population into all 42 declared postshock arms.

No new source founders are sampled. Historical fixed/evolving A treatments
share the identical FUTURE evolving-A policy, visitor realizations and paired
demographic streams. Readout is handled separately, only after all 86,016
outcomes and upstream state receipts have been admitted.
"""
from __future__ import annotations
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict, replace
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import os
import numpy as np

from scripts.plan_chapter2_unified_payoff_evolution_persistence import (
    DESIGN, load_design, prehistory_tasks
)
from scripts.run_chapter2_unified_payoff_prehistories import (
    SOURCE, FIELDS, key, source_hashes
)
from scripts.run_chapter2_assurance_generality import (
    config as base_config,
    load_design as load_biology,
)
from scripts.run_model3_persistent_isolation import exposure
from scripts.model3_island.types import PlantState
from scripts.model3_island.population import subset, advance
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.randomness import stream, STREAM_IDS

ROOT = Path(__file__).resolve().parents[1]


def recover_state(root, task, d, hashes):
    name = key(task)
    receipt_path = Path(root) / f"{name}.json"
    state_path = Path(root) / f"{name}.npz"
    if not receipt_path.exists() or not state_path.exists():
        raise FileNotFoundError(f"missing verified prehistory state {name}")
    receipt = json.loads(receipt_path.read_text())
    if (receipt["task"] != asdict(task)
            or receipt["status"] != "complete_prehistory_unadjudicated"
            or receipt["design_sha256"] != hashlib.sha256(DESIGN.read_bytes()).hexdigest()
            or receipt["source_hashes"] != hashes
            or hashlib.sha256(state_path.read_bytes()).hexdigest()
                != receipt["state_sha256"]):
        raise AssertionError("prehistory receipt, source or genotype hash mismatch")
    with np.load(state_path, allow_pickle=False) as archive:
        state = PlantState(**{name: archive[name] for name in FIELDS})
    if state.alleles.shape[1:] != (3, 2):
        raise AssertionError("not the recorded diploid three-trait state")
    if task.mode == "fixed" and len(state.ids):
        if not np.all(state.alleles[:, 2, :] == d["fixed_assurance_allele_value"]):
            raise AssertionError("fixed historical assurance state was altered")
    return state, receipt["state_sha256"]


def shock_ancestors(task, state, n_limit=8):
    if not len(state.ids):
        return state
    n = min(n_limit, len(state.ids))
    seed = int(np.random.SeedSequence(
        [task.history, task.repeat, 117]).generate_state(1)[0])
    positions = np.random.default_rng(seed).choice(len(state.ids), size=n,
                                                    replace=False)
    return subset(state, positions)


def common_streams(task, setting_index, regime_index, future_index,
                   budget_index):
    # MUST not include historical near/far or past fixed/evolving mode.
    seed = int(np.random.SeedSequence([
        task.history, task.repeat, setting_index, regime_index,
        future_index, budget_index, 3611082026
    ]).generate_state(1)[0])
    return {k: stream(seed, k, 0) for k in STREAM_IDS}


def one_future(task, state, d, biology, regime, budget, future, bottleneck):
    setting_idx = d["reproductive_settings"].index(task.setting)
    regime_idx = [r["id"] for r in d["postshock"]["regimes"]].index(regime)
    future_idx = d["postshock"]["visitor_environments"].index(future)
    budget_idx = d["postshock"]["budgets"].index(budget)
    cap = next(r["capacity"] for r in d["postshock"]["regimes"]
               if r["id"] == regime)
    initial = state if regime == "fecundity_only" else bottleneck
    if len(initial.ids) > cap:
        raise AssertionError("postshock population exceeds declared capacity")
    cfg = replace(
        base_config(biology, task.setting, d["prehistory"]["mutation_rate"],
                    task.mode),
        assurance_mode="evolving", capacity=cap,
        mutation_rate=d["postshock"]["post_mutation_rate"],
        ovule_budget=float(budget),
    )
    if cfg.seed_arrival.supply != 0:
        raise AssertionError("postshock immigrant seeds not declared")
    visitors = exposure(task.history + d["postshock"]["future_visitor_seed_offset"], future)
    rng = common_streams(task, setting_idx, regime_idx,
                         future_idx, budget_idx)
    first_output = None
    if len(initial.ids):
        expected = reproduce(initial, visitors.visitors[0], cfg)
        first_output = {
            "maternal_viable_per_plant": float(expected.maternal.sum() / len(initial.ids)),
            "female_outcross_per_plant": float(expected.outcross.sum() / len(initial.ids)),
            "pollen_export_per_plant": float(expected.exported.sum() / len(initial.ids)),
            "viable_selfed_per_plant": float(expected.self_viable.sum() / len(initial.ids)),
        }
    current = initial
    first_extinct = 0 if not len(initial.ids) else None
    total_selfed = total_outcross = 0
    for t in range(d["postshock"]["updates"]):
        if not len(current.ids):
            break
        ledger = reproduce(current, visitors.visitors[t], cfg)
        candidate = visitors.seed_candidates[t]
        if len(candidate.ids):
            raise AssertionError("unexpected external seed arrival in zero-migration design")
        current, info = advance(
            current, ledger, candidate, cfg, rng,
            year=d["prehistory"]["updates"] + t,
            mutation_traits=(True, True, True),
        )
        total_selfed += info["resident_selfed_recruits"]
        total_outcross += info["resident_outcross_recruits"]
        if not len(current.ids) and first_extinct is None:
            first_extinct = t + 1
    if current.ids.size:
        traits = current.alleles.mean(axis=2)
        endpoint = {
            "means": traits.mean(axis=0).tolist(),
            "variances": traits.var(axis=0).tolist(),
        }
    else:
        endpoint = None
    return {
        "regime": regime, "future_environment": future,
        "ovule_budget": float(budget),
        "t0_population": len(initial.ids),
        "occupied": int(bool(len(current.ids))),
        "end_population": len(current.ids),
        "first_extinction": first_extinct,
        "t0_reproductive_output": first_output,
        "post_genetic_outcome": endpoint,
        "realized_selfed_recruits": total_selfed,
        "realized_outcross_recruits": total_outcross,
        "future_assurance_mode": cfg.assurance_mode,
    }


def run_one(task, d, biology, prepath, postpath, hashes):
    out = Path(postpath)
    name = key(task)
    path = out / f"{name}.json"
    receipt_path = out / f"{name}.sha256"
    if path.exists():
        if (not receipt_path.exists() or
                hashlib.sha256(path.read_bytes()).hexdigest() !=
                receipt_path.read_text().strip()):
            raise ValueError("postshock case receipt missing or invalid: " + name)
        row = json.loads(path.read_text())
        if (row["task"] != asdict(task)
                or row["source_hashes"] != hashes
                or row["design_sha256"] != hashlib.sha256(DESIGN.read_bytes()).hexdigest()
                or len(row["postshock"]) != 42):
            raise ValueError("different existing postshock case: " + name)
        return name
    state, initial_sha = recover_state(prepath, task, d, hashes)
    bottleneck = shock_ancestors(task, state)
    all_results = []
    for regime, future, budget in product(
        [r["id"] for r in d["postshock"]["regimes"]],
        d["postshock"]["visitor_environments"],
        d["postshock"]["budgets"],
    ):
        all_results.append(one_future(
            task, state, d, biology, regime, budget, future, bottleneck,
        ))
    if len(all_results) != 42 or any(
        x["future_assurance_mode"] != "evolving" for x in all_results
    ):
        raise AssertionError("future-evolution equalization failed")
    payload = {
        "task": asdict(task), "status": "complete_postshock_raw_not_adjudicated",
        "source_hashes": hashes,
        "design_sha256": hashlib.sha256(DESIGN.read_bytes()).hexdigest(),
        "prehistory_state_sha256": initial_sha,
        "bottleneck_state_sha256": hashlib.sha256(
            bottleneck.alleles.tobytes()).hexdigest(),
        "postshock": all_results,
    }
    raw = (json.dumps(payload, indent=2, sort_keys=True,
                      allow_nan=False) + "\n").encode()
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(raw)
    os.replace(tmp, path)
    # Independent raw-content checksum for the entire 42-cell postshock fork.
    checksum = hashlib.sha256(raw).hexdigest() + "\n"
    receipt_tmp = receipt_path.with_suffix(".sha256.tmp")
    receipt_tmp.write_text(checksum)
    os.replace(receipt_tmp, receipt_path)
    return name


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--prehistory", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--shard-index", type=int, required=True)
    p.add_argument("--shard-count", type=int, default=64)
    p.add_argument("--workers", type=int, default=2)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    d = load_design()
    biology = load_biology(SOURCE)
    all_tasks = prehistory_tasks(d)
    if not 0 <= args.shard_index < args.shard_count or args.shard_count <= 0:
        raise ValueError("invalid shard index")
    tasks = [t for i, t in enumerate(all_tasks)
             if i % args.shard_count == args.shard_index]
    if args.dry_run:
        print(json.dumps({"prehistories": len(tasks),
                          "postshock_cases": len(tasks) * 42}))
        return
    args.out.mkdir(parents=True, exist_ok=True)
    hashes = source_hashes()
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run_one, t, d, biology,
                               args.prehistory, args.out, hashes)
                   for t in tasks]
        names = sorted(f.result() for f in as_completed(futures))
    if len(names) != len(tasks):
        raise AssertionError("not all 42-condition postshock forks complete")
    path = args.out / f"postshock_shard_{args.shard_index:02d}.json"
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps({
        "status": "raw_postshock_complete_not_adjudicated",
        "case_keys": names,
        "design_sha256": hashlib.sha256(DESIGN.read_bytes()).hexdigest(),
        "source_hashes": hashes,
    }, indent=2) + "\n")
    os.replace(tmp, path)
    print(json.dumps({"prehistories": len(names),
                      "postshock_cases": len(names) * 42,
                      "status": "raw_only"}))


if __name__ == "__main__":
    main()
