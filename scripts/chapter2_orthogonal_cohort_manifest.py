"""Compile the prospective independent Chapter 2 task manifest WITHOUT simulations.

A manifest is only an enumerated, SHA-anchored specification. No prehistory
plant states, visitor trajectories, or future experimental outcomes are created.
"""
from __future__ import annotations

from dataclasses import asdict
from itertools import product
import argparse
import hashlib
import json
from pathlib import Path

from scripts.plan_chapter2_order_expression_identification import Prehistory
from scripts.plan_chapter2_orthogonal_founder_capacity import (
    PROTOCOL, validate_protocol,
)
from scripts.chapter2_order_prehistory_runner import (
    case_key, source_hashes,
)

SHARDS = 64
SOURCE_PER_SHARD = 32
FUTURES_PER_SOURCE = 84


def tasks():
    validate_protocol()
    frozen = json.loads(Path(PROTOCOL).read_text(encoding="utf-8"))
    h = frozen["new_independent_cohort"]
    grid = frozen["complete_future_grid"]
    repeat_start = 39111901
    repeat_ids = (repeat_start, repeat_start + 1)
    if grid["nested_demographic_repeats"] != len(repeat_ids):
        raise AssertionError("Demographic repeat identities changed")

    all_tasks = []
    for history_id in range(h["visitor_history_first"],
                            h["visitor_history_last"] + 1):
        group = [
            Prehistory(setting, environment, order, history_id, repeat)
            for setting, environment, order, repeat in product(
                grid["reproductive_settings"],
                grid["historical_environments"],
                grid["assigned_expression_orders"],
                repeat_ids,
            )
        ]
        if len(group) != SOURCE_PER_SHARD:
            raise AssertionError("Require exactly 32 t400 sources per visitor history")
        all_tasks.append(group)

    if len(all_tasks) != SHARDS or sum(map(len, all_tasks)) != 2048:
        raise AssertionError("Prospective source count changed")
    keys = [case_key(t) for shard in all_tasks for t in shard]
    if len(set(keys)) != len(keys):
        raise AssertionError("Duplicate prospective case key")
    if any(not 39110901 <= t.visitor_history <= 39110964
           for shard in all_tasks for t in shard):
        raise AssertionError("Old exposed histories are forbidden")
    return all_tasks


def compile_manifest() -> dict:
    """Freeze hashes and all expected source identities in a reviewable document."""
    groups = tasks()
    spec_bytes = Path(PROTOCOL).read_bytes()
    hashes = source_hashes()
    meta = {
        "status": "PLAN_ONLY_NO_OUTCOMES",
        "protocol_sha256": hashlib.sha256(spec_bytes).hexdigest(),
        "source_code_sha256": hashes,
        "n_histories": SHARDS,
        "n_sources": SHARDS * SOURCE_PER_SHARD,
        "futures_per_source": FUTURES_PER_SOURCE,
        "expected_futures": SHARDS * SOURCE_PER_SHARD * FUTURES_PER_SOURCE,
        "shards": [],
    }
    for i, group in enumerate(groups):
        rows = [asdict(t) for t in group]
        canon = json.dumps(rows, sort_keys=True, separators=(",", ":"))
        meta["shards"].append({
            "shard_index": i,
            "visitor_history_id": 39110901 + i,
            "n_sources": len(group),
            "case_keys": [case_key(t) for t in group],
            "task_sha256": hashlib.sha256(canon.encode()).hexdigest(),
            "expected_futures": FUTURES_PER_SOURCE * len(group),
        })
    if (sum(s["expected_futures"] for s in meta["shards"]) != 172032
            or any(s["expected_futures"] != 2688 for s in meta["shards"])):
        raise AssertionError("Partial independent history/future manifest")
    return meta


def validate_manifest(m: dict) -> None:
    """Fail closed if even one history, genotype source or future is omitted."""
    if not isinstance(m, dict) or m["status"] != "PLAN_ONLY_NO_OUTCOMES":
        raise AssertionError("Result-shaped input is not a task manifest")
    expected = compile_manifest()
    if m != expected:
        raise AssertionError("Source ID/shard/protocol SHA changed")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, help="Optional manifest JSON file; never a result")
    args = p.parse_args()
    plan = compile_manifest()
    validate_manifest(plan)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            json.dumps(plan, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps({
        "status": plan["status"],
        "n_histories": plan["n_histories"],
        "n_sources": plan["n_sources"],
        "expected_futures": plan["expected_futures"],
        "scientific_outcomes_generated": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
