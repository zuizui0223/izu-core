"""Fork only verified inherited t400 states into all 28 future conditions.

No new founders are created at the future boundary. Every assigned expression
history enters the identical canonical no-offset, evolving-A future biology.
No analysis is run until every full-case receipt has been independently audited.
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

from scripts.plan_chapter2_order_expression_identification import (
    SPEC, load_protocol, prehistories,
)
from scripts.chapter2_order_prehistory_runner import (
    STATE_FIELDS, case_key, source_hashes, _atomic_bytes,
)
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config,
    load_design as source_biology, founders as source_founders,
)
from scripts.run_model3_persistent_isolation import exposure
from scripts.model3_island.population import subset, advance
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.types import PlantState
from scripts.model3_island.randomness import stream, STREAM_IDS


def restore_prehistory(root: Path, task, d: dict, hashes: dict):
    """Reject a receipt that fails task/biological-source/entire-genotype checks."""
    key = case_key(task)
    npz = Path(root) / f"{key}.npz"
    js = Path(root) / f"{key}.json"
    if not npz.is_file() or not js.is_file():
        raise FileNotFoundError("missing t400 diploid source " + key)
    raw = json.loads(js.read_text(encoding="utf-8"))
    digest = hashlib.sha256(npz.read_bytes()).hexdigest()
    if (raw["status"] != "raw_prehistory_unadjudicated"
            or raw["task"] != asdict(task)
            or raw["completed_updates"] != 400
            or raw["source_hashes"] != hashes
            or raw["protocol_sha256"] != hashlib.sha256(SPEC.read_bytes()).hexdigest()
            or raw["state_sha256"] != digest
            or raw["no_future_outcomes_exposed"] is not True):
        raise AssertionError("prehistory source receipt does not match protocol")
    with np.load(npz, allow_pickle=False) as archive:
        state = PlantState(**{field: archive[field] for field in STATE_FIELDS})
        parentage = archive["parentage_edges"]
    # Independently reject impossible or silently dropped parent–offspring
    # relationships; checksums alone only prove byte integrity.
    if (parentage.ndim != 2 or parentage.shape[1] != 4
            or parentage.dtype.kind not in "iu"
            or raw["parentage_link_count"] != len(parentage)
            or raw["parentage_sha256"] != hashlib.sha256(
                parentage.tobytes()).hexdigest()):
        raise AssertionError("invalid full-source parentage archive")
    initial = raw["founder_ids"]
    if (len(set(initial)) != len(initial)
            or len(initial) != 48
            or not all(isinstance(i, int) for i in initial)):
        raise AssertionError("invalid original founder IDs")
    # The source founders must agree with the deterministic frozen biological
    # starting state, not merely with a caller-controlled receipt.
    expected_founders = source_founders(source_biology(DEFAULT_DESIGN))
    if (initial != [int(x) for x in expected_founders.ids]
            or raw["founder_allele_sha256"] != hashlib.sha256(
                expected_founders.alleles.tobytes()).hexdigest()):
        raise AssertionError("founder genotype differs from frozen source biology")
    birth_year = {int(i): 0 for i in initial}
    last_year = 0
    for year, child, mother, father in parentage:
        year, child, mother, father = map(int, (year,child,mother,father))
        if (not last_year <= year <= 400 or year < 1
                or not 48*year <= child < 48*(year+1)
                or child in birth_year
                or mother not in birth_year or father not in birth_year
                or birth_year[mother] >= year or birth_year[father] >= year):
            raise AssertionError("chronologically impossible parentage")
        birth_year[child] = year
        last_year = year
    if any(int(i) not in birth_year for i in state.ids):
        raise AssertionError("untracked genotype appeared after reproduction")
    if (len(parentage) and raw["parentage_year_bounds"]
            != [int(parentage[:,0].min()),int(parentage[:,0].max())]):
        raise AssertionError("inconsistent pedigree year bounds")
    if not len(parentage) and raw["parentage_year_bounds"] is not None:
        raise AssertionError("false pedigree times for empty genealogy")
    if (len(raw["annual_inherited_censuses"]) != 401
            or raw["annual_inherited_censuses"][-1]["n"] != len(state.ids)
            or raw["annual_inherited_censuses"][-1]["year"] != 400):
        raise AssertionError("annual final source state inconsistent")
    traits = state.alleles.mean(axis=2)
    expected = traits.mean(axis=0).tolist() if len(state.ids) else None
    if expected is None and raw["annual_inherited_censuses"][-1]["inherited_means"] is not None:
        raise AssertionError("invented source phenotype after extinction")
    if expected is not None and not np.allclose(
        expected, raw["annual_inherited_censuses"][-1]["inherited_means"],
        atol=1e-12, rtol=0
    ):
        raise AssertionError("source inherited means differ from full alleles")
    return state, digest


def sampled_eight(task, state: PlantState, d: dict) -> PlantState:
    if not len(state.ids):
        return state
    s = d["reproductive_settings"].index(task.setting)
    seed = int(np.random.SeedSequence([
        task.visitor_history, task.demographic_repeat,
        s, 3711082026,
    ]).generate_state(1)[0])
    positions = np.random.default_rng(seed).choice(
        len(state.ids), size=min(8, len(state.ids)), replace=False,
    )
    return subset(state, positions)


def paired_streams(task, d: dict, regime: str, future: str, budget: float):
    """Never use assigned order or historical near/far in post RNG seed."""
    seed = int(np.random.SeedSequence([
        task.visitor_history, task.demographic_repeat,
        d["reproductive_settings"].index(task.setting),
        d["postshock"]["arms"].index(regime),
        d["postshock"]["future_environments"].index(future),
        d["postshock"]["budgets"].index(budget),
        3711082048,
    ]).generate_state(1)[0])
    return {name: stream(seed, name, 0) for name in STREAM_IDS}


def one_future(task, state, selected_eight, d, biology,
               regime: str, future: str, budget: float):
    cap = 48 if regime == "unbottlenecked_capacity48" else 8
    initial = state if cap == 48 else selected_eight
    if len(initial.ids) > cap:
        raise AssertionError("wrong bottleneck count/capacity")
    cfg = replace(
        source_config(biology, task.setting,
                      d["postshock"]["post_mutation_rate"], "evolving"),
        capacity=cap, ovule_budget=float(budget), assurance_mode="evolving",
    )
    if cfg.seed_arrival.supply != 0:
        raise AssertionError("unexpected plant immigration")
    visitors = exposure(
        task.visitor_history + d["postshock"]["future_visitor_seed_offset"],
        future,
    )
    streams = paired_streams(task, d, regime, future, budget)
    if len(initial.ids):
        ledger0 = reproduce(initial, visitors.visitors[0], cfg)
        direct_payoff = {
            "maternal_viable_per_plant": float(ledger0.maternal.mean()),
            "female_outcross_per_plant": float(ledger0.outcross.sum()/len(initial.ids)),
            "paternal_export_per_plant": float(ledger0.exported.mean()),
            "viable_selfed_per_plant": float(ledger0.self_viable.mean()),
        }
    else:
        direct_payoff = None
    current = initial
    first_extinction = 0 if not len(current.ids) else None
    recruits_self = recruits_outcross = 0
    for year in range(d["postshock"]["updates"]):
        if not len(current.ids):
            break
        candidate = visitors.seed_candidates[year]
        if len(candidate.ids):
            raise AssertionError("nonzero plant immigrant candidates")
        ledger = reproduce(current, visitors.visitors[year], cfg)
        current, info = advance(
            current, ledger, candidate, cfg, streams,
            year=d["prehistory"]["updates"] + year,
            mutation_traits=(True, True, True),
        )
        recruits_self += info["resident_selfed_recruits"]
        recruits_outcross += info["resident_outcross_recruits"]
        if first_extinction is None and not len(current.ids):
            first_extinction = year + 1
    if len(current.ids):
        means = current.alleles.mean(axis=2)
        endpoint = {
            "means": means.mean(axis=0).tolist(),
            "variances": means.var(axis=0).tolist(),
        }
    else:
        endpoint = None
    return {
        "regime": regime,
        "future_visitor": future,
        "budget": float(budget),
        "t0_population": int(len(initial.ids)),
        "end_population": int(len(current.ids)),
        "occupied": int(bool(len(current.ids))),
        "first_extinction": first_extinction,
        "immediate_reproductive_payoff": direct_payoff,
        "surviving_genetic_endpoint": endpoint,
        "selfed_recruits": int(recruits_self),
        "outcross_recruits": int(recruits_outcross),
        "future_assurance_mode": "evolving",
        "future_expression_offsets": [0, 0],
    }


def persist_one(out: Path, pre_dir: Path, task, d: dict, biology: dict, hashes):
    out = Path(out)
    name = case_key(task)
    target = out / f"{name}.json"
    digest_path = out / f"{name}.sha256"
    proto_sha = hashlib.sha256(SPEC.read_bytes()).hexdigest()
    if target.exists() or digest_path.exists():
        if not target.is_file() or not digest_path.is_file():
            raise AssertionError("partial future receipt")
        row = json.loads(target.read_text())
        if (hashlib.sha256(target.read_bytes()).hexdigest()
                != digest_path.read_text().strip()
                or row["task"] != asdict(task)
                or row["source_hashes"] != hashes
                or row["protocol_sha256"] != proto_sha
                or len(row["postshock"]) != 28):
            raise AssertionError("different or unverified future case")
        return name
    state, state_sha = restore_prehistory(pre_dir, task, d, hashes)
    bottleneck = sampled_eight(task, state, d)
    result = [
        one_future(task, state, bottleneck, d, biology, regime, future, budget)
        for regime, budget, future in product(
            d["postshock"]["arms"],
            d["postshock"]["budgets"],
            d["postshock"]["future_environments"],
        )
    ]
    grid = {(r["regime"], r["budget"], r["future_visitor"]) for r in result}
    if len(result) != 28 or len(grid) != 28:
        raise AssertionError("incomplete/duplicate future grid")
    payload = {
        "task": asdict(task),
        "status": "raw_postshock_unadjudicated",
        "source_hashes": hashes,
        "protocol_sha256": proto_sha,
        "prehistory_state_sha256": state_sha,
        "sampled_eight_allele_sha256": hashlib.sha256(
            bottleneck.alleles.tobytes()).hexdigest(),
        "postshock": result,
    }
    raw = (json.dumps(payload, sort_keys=True, indent=2,
                      allow_nan=False) + "\n").encode()
    _atomic_bytes(target, raw)
    _atomic_bytes(digest_path, (hashlib.sha256(raw).hexdigest()+"\n").encode())
    return name


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--prehistory", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--shard-index", type=int, required=True)
    p.add_argument("--shard-count", type=int, default=64)
    p.add_argument("--workers", type=int, default=2)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--execute-frozen-cohort", action="store_true")
    args = p.parse_args()
    d = load_protocol()
    if not 0 <= args.shard_index < args.shard_count:
        raise ValueError("invalid shard")
    tasks = [task for i, task in enumerate(prehistories(d))
             if i % args.shard_count == args.shard_index]
    if args.dry_run:
        print(json.dumps({
            "prehistories": len(tasks), "postshock_cases": 28 * len(tasks),
            "biological_outcomes_generated": False,
        }))
        return
    if not args.execute_frozen_cohort:
        raise PermissionError("production run requires explicit --execute-frozen-cohort")
    args.out.mkdir(parents=True, exist_ok=True)
    biology = source_biology(DEFAULT_DESIGN)
    hashes = source_hashes()
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        completed = sorted(f.result() for f in as_completed([
            pool.submit(persist_one, args.out, args.prehistory, task,
                        d, biology, hashes)
            for task in tasks
        ]))
    if len(completed) != len(tasks):
        raise AssertionError("incomplete future shard")
    _atomic_bytes(args.out / f"postshock_shard_{args.shard_index:02d}.json",
        (json.dumps({
            "status": "raw_postshock_complete_unadjudicated",
            "case_keys": completed,
            "source_hashes": hashes,
            "protocol_sha256": hashlib.sha256(SPEC.read_bytes()).hexdigest(),
        }, indent=2)+"\n").encode())
    print(json.dumps({"postshock_cases": len(completed)*28, "status": "raw_only"}))


if __name__ == "__main__":
    main()
