"""Re-execute the frozen 16-new-history mutational-priority experiment.

The prespecified primary sign-difference test later FAILED. No rerun may
expand the history set, alter the schedules, or relabel that gate.
"""
from __future__ import annotations
from concurrent.futures import ProcessPoolExecutor, as_completed
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import os

from scripts.run_chapter2_assurance_generality import load_design as load_source
from scripts.run_chapter2_island_mutational_priority_pilot import (
    load_pilot, simulate_group
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_island_mutational_priority_independent16_20261008.json"


def load_followup(path=DESIGN):
    protocol = json.loads(Path(path).read_text(encoding="utf-8"))
    if protocol["status"] != "frozen_before_independent_16history_mutational_priority_execution":
        raise ValueError("unexpected cohort protocol")
    d, source = load_pilot()
    d = dict(d)
    d["new_visitor_history_seeds"] = list(range(
        protocol["new_history_seeds"]["first"],
        protocol["new_history_seeds"]["last"] + 1
    ))
    d["nested_demographic_repeat_seeds"] = list(protocol["demographic_repeat_seeds"])
    if (d["schedules"].keys() != dict.fromkeys(protocol["schedules"]).keys()
        or len(d["new_visitor_history_seeds"]) != 16
        or d["post_ovule_budgets"] != protocol["post_ovule_budgets"]):
        raise AssertionError("independent design differs from frozen pilot mechanics")
    return protocol, d, source


def tasks(d):
    return list(product(
        d["settings"], d["new_visitor_history_seeds"],
        d["nested_demographic_repeat_seeds"],
        d["pre_visitor_environments"], d["schedules"]
    ))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--shard-index", type=int, default=0)
    p.add_argument("--shard-count", type=int, default=4)
    p.add_argument("--workers", type=int, default=2)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    protocol, d, source = load_followup()
    all_groups = tasks(d)
    if (len(all_groups) != protocol["declared_prehistory_groups"]
        or not 0 <= args.shard_index < args.shard_count):
        raise ValueError("invalid shard or declared task count")
    chosen = [g for i, g in enumerate(all_groups)
              if i % args.shard_count == args.shard_index]
    if args.dry_run:
        print(json.dumps({"groups": len(chosen), "stress_cases": len(chosen)*8}))
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
        raise RuntimeError("independent16 incomplete")
    raw = (json.dumps(rows, sort_keys=True, allow_nan=False) + "\n").encode()
    path = args.out / f"priority_independent16_shard_{args.shard_index:02d}.json"
    tmp = path.with_suffix(".tmp")
    tmp.write_bytes(raw)
    os.replace(tmp, path)
    print(json.dumps({
        "historical_groups": len(rows), "poststress_cases": 8*len(rows),
        "sha256": hashlib.sha256(raw).hexdigest()
    }))


if __name__ == "__main__":
    main()
