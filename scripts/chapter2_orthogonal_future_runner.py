"""Production-only Chapter 2 orthogonal capacity x self-viability futures.

No biological outcomes on import, plan, or CI. Only explicitly approved
production can advance plant states. All future conditions are kept, including
early-extinct histories, without selection based on outcomes.
"""
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict, replace
from itertools import product
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from scripts.chapter2_orthogonal_cohort_manifest import compile_manifest, tasks
from scripts.chapter2_orthogonal_prehistory_source_runner import prospective_biological_design
from scripts.chapter2_orthogonal_capacity_pairing import (
    select_fixed_eight, prepare_arms, common_future_streams, state_fingerprint,
)
from scripts.chapter2_postzygotic_viability_gate import gate_postzygotic_seed_viability
from scripts.chapter2_order_prehistory_runner import (
    case_key, _atomic_bytes, source_hashes,
)
from scripts.chapter2_order_postshock_runner import restore_prehistory
from scripts.model3_island.population import advance
from scripts.model3_island.reproduction import reproduce
from scripts.run_model3_persistent_isolation import exposure
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config,
    load_design as source_biology,
)

ARM_NAMES = ("eight_founders_capacity8", "eight_founders_capacity48",
             "all_available_founders_capacity48")
GATES = ("baseline", "self_half")
STATUS = "ORTHOGONAL_84_RAW_FUTURES_UNADJUDICATED"


def future_one(task, full, selected, d, biology, *,
               regime: str, gate: str, future: str, budget: float) -> dict:
    if regime not in ARM_NAMES or gate not in GATES:
        raise ValueError("Nonprospective capacity or viability arm")
    if budget not in tuple(d["postshock"]["budgets"]) or future not in (
            "near", "far"):
        raise ValueError("Nonprospective future condition")
    prepared = prepare_arms(full, selected)
    population, capacity = prepared[regime]
    if len(population.ids) > capacity:
        raise AssertionError("Initial population exceeds assigned capacity")
    cfg = replace(source_config(
        biology, task.setting, d["postshock"]["post_mutation_rate"], "evolving"
    ), capacity=capacity, ovule_budget=float(budget), assurance_mode="evolving")
    if cfg.seed_arrival.supply != 0:
        raise AssertionError("Unexpected external plant seed immigration")

    visitor = exposure(
        task.visitor_history + d["postshock"]["future_visitor_seed_offset"],
        future,
    )
    streams = common_future_streams(
        visitor_history=task.visitor_history,
        demographic_repeat=task.demographic_repeat,
        setting=task.setting,
        future_visitor=future,
        budget=float(budget),
    )
    current = population
    first_extinction = 0 if not len(current.ids) else None
    self_recruits = other_recruits = 0
    start_payoff = None
    for y in range(d["postshock"]["updates"]):
        if not len(current.ids):
            break
        candidate = visitor.seed_candidates[y]
        if len(candidate.ids):
            raise AssertionError("Immigrating plant candidates forbidden")
        ledger = reproduce(current, visitor.visitors[y], cfg)
        if gate == "self_half":
            original_export = ledger.exported.copy()
            ledger = gate_postzygotic_seed_viability(
                ledger, selfed_fraction=0.5, outcross_fraction=1.0
            )
            if not np.array_equal(ledger.exported, original_export):
                raise AssertionError("Postzygotic manipulation changed pollen export")
        if y == 0:
            start_payoff = {
                "viable_selfed": float(ledger.self_viable.sum()),
                "viable_outcross": float(ledger.outcross.sum()),
                "expected_pollen_export": float(ledger.exported.sum()),
            }
        current, info = advance(
            current, ledger, candidate, cfg, streams,
            year=d["prehistory"]["updates"] + y,
            mutation_traits=(True, True, True),
        )
        self_recruits += info["resident_selfed_recruits"]
        other_recruits += info["resident_outcross_recruits"]
        if first_extinction is None and not len(current.ids):
            first_extinction = y + 1
    return {
        "regime": regime, "gate": gate, "budget": float(budget),
        "future_visitor": future,
        "t0_population": int(len(population.ids)),
        "t0_full_source_population": int(len(full.ids)),
        "t0_selected_eight_fingerprint": state_fingerprint(selected),
        "t0_payoff": start_payoff,
        "terminal_occupancy": int(bool(len(current.ids))),
        "terminal_population": int(len(current.ids)),
        "first_extinction": first_extinction,
        "selfed_recruits": self_recruits,
        "outcrossed_recruits": other_recruits,
        "assigned_postshock_offsets": [0, 0],
        "future_assurance_mode": "evolving",
    }


def one_source(out: Path, pre: Path, task, d, biology, manifest) -> str:
    key = case_key(task)
    target = out / f"orthogonal_{key}.json"
    check = out / f"orthogonal_{key}.sha256"
    biohash = source_hashes()
    if manifest["source_code_sha256"] != biohash:
        raise AssertionError("Changed frozen biological source during production")
    full, digest = restore_prehistory(pre, task, d, biohash)
    selected = select_fixed_eight(
        full, visitor_history=task.visitor_history,
        demographic_repeat=task.demographic_repeat,
        setting_index=d["reproductive_settings"].index(task.setting),
    )
    arms = prepare_arms(full, selected)
    if (state_fingerprint(arms["eight_founders_capacity8"].state) !=
            state_fingerprint(arms["eight_founders_capacity48"].state)):
        raise AssertionError("Founders not identical in primary capacity contrast")

    if target.exists() or check.exists():
        if not target.is_file() or not check.is_file():
            raise AssertionError("Partial future archive")
        if hashlib.sha256(target.read_bytes()).hexdigest() != check.read_text().strip():
            raise AssertionError("Corrupt resumed future archive")
        old = json.loads(target.read_text())
        if (old["task"] != asdict(task) or old["status"] != STATUS
                or old["source_sha256"] != digest
                or old["protocol_sha256"] != manifest["protocol_sha256"]
                or len(old["futures"]) != 84):
            raise AssertionError("Incompatible resumed future file")
        return key

    futures = []
    for regime, budget, visitor_name, gate in product(
        ARM_NAMES, d["postshock"]["budgets"], ("near", "far"), GATES,
    ):
        futures.append(future_one(
            task, full, selected, d, biology,
            regime=regime, gate=gate,
            future=visitor_name, budget=float(budget),
        ))
    unique = {
        (row["regime"], row["gate"], row["budget"], row["future_visitor"])
        for row in futures
    }
    if len(futures) != 84 or len(unique) != 84:
        raise AssertionError("Incomplete 3-arm x 2-gate future cube")
    raw = {
        "status": STATUS, "task": asdict(task),
        "source_sha256": digest,
        "selected_eight_fingerprint": state_fingerprint(selected),
        "protocol_sha256": manifest["protocol_sha256"],
        "source_hashes": biohash,
        "futures": futures,
    }
    buf = (json.dumps(raw, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()
    _atomic_bytes(target, buf)
    _atomic_bytes(check, (hashlib.sha256(buf).hexdigest() + "\n").encode())
    return key


def run_shard(pre: Path, out: Path, shard: int, workers: int) -> dict:
    if not 0 <= shard < 64 or not 1 <= workers <= 4:
        raise ValueError("Invalid independent history shard/workers")
    manifest = compile_manifest()
    group = tasks()[shard]
    if [case_key(t) for t in group] != manifest["shards"][shard]["case_keys"]:
        raise AssertionError("Mismatched prospective history shard")
    receipt_path = pre / f"orthogonal_pre_shard_{shard:02}.json"
    receipt = json.loads(receipt_path.read_text())
    if (receipt["status"] != "RAW_T400_32_SOURCE_SHARD_NOT_ADJUDICATED"
            or receipt["task_sha256"] != manifest["shards"][shard]["task_sha256"]
            or receipt["case_keys"] != sorted(case_key(t) for t in group)
            or receipt["protocol_sha256"] != manifest["protocol_sha256"]):
        raise AssertionError("No authentic complete prehistory shard")
    out.mkdir(parents=True, exist_ok=True)
    d = prospective_biological_design()
    biology = source_biology(DEFAULT_DESIGN)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        keys = sorted(f.result() for f in as_completed(
            [pool.submit(one_source, out, pre, task, d, biology, manifest)
             for task in group]
        ))
    if keys != sorted(case_key(t) for t in group) or len(keys) != 32:
        raise AssertionError("Incomplete future source list")
    complete = {
        "status": "RAW_FULL_32_SOURCE_2688_FUTURE_SHARD",
        "shard": shard, "visitor_history": 39110901 + shard,
        "n_t400_sources": 32, "future_count": 2688, "case_keys": keys,
        "protocol_sha256": manifest["protocol_sha256"],
        "source_hashes": source_hashes(),
        "no_scientific_adjudication": True,
    }
    _atomic_bytes(out / f"orthogonal_future_shard_{shard:02}.json", (
        json.dumps(complete, sort_keys=True, indent=2) + "\n"
    ).encode())
    return complete


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--prehistory", type=Path)
    p.add_argument("--out", type=Path)
    p.add_argument("--shard-index", type=int, required=True)
    p.add_argument("--workers", type=int, default=2)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--execute-frozen-cohort", action="store_true")
    p.add_argument("--acknowledge-resource-cost", action="store_true")
    a = p.parse_args()
    if not 0 <= a.shard_index < 64:
        raise ValueError("Invalid shard ID")
    if a.dry_run:
        print(json.dumps({"planned_sources": 32, "planned_futures": 2688,
                          "biological_outcomes_created": False}))
        return
    if not (a.execute_frozen_cohort and a.acknowledge_resource_cost):
        raise PermissionError("Two explicit production opt-ins required")
    if a.prehistory is None or a.out is None:
        raise ValueError("Authenticated t400 source and output paths required")
    print(json.dumps(run_shard(a.prehistory, a.out, a.shard_index, a.workers)))


if __name__ == "__main__":
    main()
