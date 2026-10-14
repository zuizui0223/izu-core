"""Pilot with equal 250-update mutational access per focal trait per schedule.

Reuses the unchanged mutation/selection/reproduction mechanics of the
three-phase-capable mutational-priority runner; no genotype expression reset.
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
from scripts.run_chapter2_island_mutational_priority_pilot import simulate_group

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_island_mutational_priority_balanced_20261008.json"


def load_balanced(path=DESIGN):
    protocol = json.loads(Path(path).read_text(encoding="utf-8"))
    if protocol["status"] != "balanced_mutational_opportunity_exploratory_before_execution":
        raise ValueError("unexpected protocol")
    for name, masks in protocol["schedules"].items():
        if len(masks) != 3 or any(not m[0] for m in masks):
            raise AssertionError("matching mutation must remain active " + name)
        for locus in (1, 2):
            generations = (150 * int(masks[0][locus]) +
                           150 * int(masks[1][locus]) +
                           100 * int(masks[2][locus]))
            if generations != protocol["mutation_access_generations_per_trait"]:
                raise AssertionError("unequal mutation duration " + name)
    d = dict(
        source_biology=protocol["source_biology"],
        settings=protocol["settings"],
        new_visitor_history_seeds=protocol["new_history_seeds"],
        nested_demographic_repeat_seeds=protocol["nested_repeats"],
        pre_visitor_environments=protocol["pre_environments"],
        post_visitor_environments=protocol["post_environments"],
        initial_phase_generations=150,
        second_phase_generations=300,
        total_prehistory_generations=400,
        post_stress_generations=protocol["post_updates"],
        mutation_rate=protocol["mutation_rate"],
        mutation_sd=protocol["mutation_sd"],
        post_bottleneck_capacity=protocol["post_capacity"],
        post_bottleneck_n=protocol["post_bottleneck_n"],
        post_ovule_budgets=protocol["post_ovule_budgets"],
        post_visitor_seed_offset=protocol["post_seed_offset"],
        schedules={
            name: dict(
                phase1_mutation_mask=masks[0],
                phase2_mutation_mask=masks[1],
                phase3_mutation_mask=masks[2],
            )
            for name, masks in protocol["schedules"].items()
        }
    )
    source = load_source(ROOT / protocol["source_biology"])
    return protocol, d, source


def declared_groups(d):
    return list(product(
        d["settings"], d["new_visitor_history_seeds"],
        d["nested_demographic_repeat_seeds"], d["pre_visitor_environments"],
        d["schedules"],
    ))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--shard-count", type=int, default=4)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    protocol, d, source = load_balanced()
    tasks = declared_groups(d)
    if (len(tasks) != protocol["declared_prehistory_groups"]
        or not 0 <= args.shard_index < args.shard_count):
        raise ValueError("wrong task count or shard choice")
    selected = [x for i, x in enumerate(tasks)
                if i % args.shard_count == args.shard_index]
    if args.dry_run:
        print(json.dumps({"groups": len(selected), "cases": len(selected)*8}))
        return
    args.out.mkdir(parents=True, exist_ok=True)
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        rows = [f.result() for f in as_completed(
            pool.submit(simulate_group, x, d, source) for x in selected
        )]
    rows.sort(key=lambda r: tuple(r["group"]))
    if len(rows) != len(selected) or any(
        r["post_cases"] is None or len(r["post_cases"]) != 8 for r in rows
    ):
        raise RuntimeError("missing balanced experiment cases")
    raw = (json.dumps(rows, sort_keys=True, allow_nan=False) + "\n").encode()
    path = args.out / f"priority_balanced_shard_{args.shard_index:02d}.json"
    temp = path.with_suffix(".tmp")
    temp.write_bytes(raw)
    os.replace(temp, path)
    print(json.dumps({
        "groups": len(rows), "cases": 8*len(rows),
        "sha256": hashlib.sha256(raw).hexdigest()
    }))


if __name__ == "__main__":
    main()
