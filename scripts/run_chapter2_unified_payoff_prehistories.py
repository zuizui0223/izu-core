"""Run only frozen 400-update PREHISTORIES for unified Chapter 2.

Never runs postshock branches or reads postshock outcomes. Persists the full
diploid plant state and all per-plant lineage metadata needed to fork the
identical t400 population into subsequent demographic regimes.
"""
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict
from pathlib import Path
import argparse
import hashlib
import json
import os
import numpy as np

from scripts.plan_chapter2_unified_payoff_evolution_persistence import (
    DESIGN, load_design, prehistory_tasks,
)
from scripts.run_chapter2_assurance_generality import (
    config as base_config,
    founders,
    load_design as load_biology,
)
from scripts.run_model3_persistent_isolation import exposure
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import stream, STREAM_IDS
from scripts.model3_island.selection import investment_invasion_terms

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/design/chapter2_assurance_generality_20261006.json"
FIELDS = ("alleles", "allele_origin", "mutation_flags", "ids", "birth_years")
SOURCE_FILES = (
    "data/design/chapter2_assurance_generality_20261006.json",
    "data/design/model3_ch2_bridge_20260927.json",
    "scripts/run_chapter2_assurance_generality.py",
    "scripts/run_model3_persistent_isolation.py",
    "scripts/plan_chapter2_unified_payoff_evolution_persistence.py",
    "scripts/run_chapter2_unified_payoff_prehistories.py",
    "scripts/run_chapter2_unified_payoff_postshock.py",
    "scripts/summarize_chapter2_unified_payoff_evolution_persistence.py",
    "scripts/model3_island/run.py",
    "scripts/model3_island/reproduction.py",
    "scripts/model3_island/population.py",
    "scripts/model3_island/history.py",
    "scripts/model3_island/types.py",
    "scripts/model3_island/randomness.py",
    "scripts/model3_island/selection.py",
)


def source_hashes() -> dict:
    return {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
            for p in SOURCE_FILES}


def key(task) -> str:
    return (f"{task.setting}_{task.mode}_{task.environment}_"
            f"h{task.history}_r{task.repeat}")


def census(state) -> dict:
    if not len(state.ids):
        return {"n": 0, "means": None, "variances": None}
    traits = state.alleles.mean(axis=2)
    return {
        "n": len(state.ids),
        "means": traits.mean(axis=0).tolist(),
        "variances": traits.var(axis=0).tolist(),
    }


def local_gradient(state, visitors, cfg):
    if not len(state.ids):
        return None
    means = state.alleles.mean(axis=(0, 2)).copy()
    if cfg.assurance_mode == "fixed":
        means[2] = cfg.fixed_assurance
    terms = investment_invasion_terms(means, visitors, cfg)
    names = ("gradient", "maternal_outcross_component",
             "paternal_export_component", "selfing_displacement_component",
             "ovule_allocation_cost_component")
    data = {name: float(np.asarray(terms[name])) for name in names}
    if abs(data["gradient"] - sum(data[x] for x in names[1:])) > 1e-10:
        raise AssertionError("nonadditive corrected rare-mutant selection")
    return data


def run_one(task, settings, biology):
    cfg = base_config(biology, task.setting, settings["prehistory"]["mutation_rate"],
                      task.mode)
    if cfg.seed_arrival.supply != 0:
        raise ValueError("unmodelled plant immigration in prehistory")
    visitor = exposure(task.history, task.environment)
    state = founders(biology)
    seed = int(np.random.SeedSequence(
        [task.history, task.repeat]).generate_state(1)[0])
    rng = {name: stream(seed, name, 0) for name in STREAM_IDS}
    snapshots = []
    payoff = []
    checkpoints = set(settings["prehistory"]["occupancy_census_times"])
    gradient_times = set(settings["prehistory"]["local_diagnostic_times"])
    for t in range(settings["prehistory"]["updates"] + 1):
        if t in checkpoints:
            record = {"t": t, **census(state)}
            if t in gradient_times:
                record["local_fixed_resident_gradient"] = local_gradient(
                    state, visitor.visitors[t], cfg)
            snapshots.append(record)
        if t == settings["prehistory"]["updates"]:
            break
        ledger = reproduce(state, visitor.visitors[t], cfg)
        if t in gradient_times and len(state.ids):
            f = float(ledger.outcross.sum())
            s = float(ledger.self_viable.sum())
            payoff.append({
                "t": t, "maternal_outcross": f,
                "paternal_outcross": f,
                "pollen_export": float(ledger.exported.sum()),
                "viable_selfed_maternal": s,
                "total_viable_maternal": float(ledger.maternal.sum()),
                "realized_viable_selfing_fraction": s / (f + s)
                    if f + s > 0 else None,
                "reproductive_cost_fraction": float(np.mean(
                    1.0 - ledger.ovules / cfg.ovule_budget)),
            })
        state, _info = advance(
            state, ledger, visitor.seed_candidates[t], cfg, rng, year=t,
            mutation_traits=(True, True, task.mode == "evolving"),
        )
        if task.mode == "fixed" and len(state.ids):
            if not np.all(state.alleles[:, 2, :] == cfg.fixed_assurance):
                raise AssertionError("fixed assurance mutated during prehistory")
    if snapshots[-1]["t"] != settings["prehistory"]["updates"]:
        raise AssertionError("no t400 genetic endpoint recorded")
    return state, {
        "task": asdict(task),
        "status": "complete_prehistory_unadjudicated",
        "snapshots": snapshots,
        "payoff_snapshots": payoff,
        "postshock_results_exposed": False,
    }


def atomic_write(path, raw):
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_bytes(raw)
    os.replace(temp, path)


def persist_one(out, task, settings, biology, hashes):
    out = Path(out)
    basename = key(task)
    npz = out / f"{basename}.npz"
    receipt = out / f"{basename}.json"
    if receipt.exists():
        old = json.loads(receipt.read_text())
        if (old["task"] != asdict(task) or old["source_hashes"] != hashes
                or not npz.exists()
                or hashlib.sha256(npz.read_bytes()).hexdigest() != old["state_sha256"]):
            raise ValueError("existing prehistory receipt differs: " + basename)
        return basename
    state, meta = run_one(task, settings, biology)
    tmp = npz.with_suffix(".npz.tmp")
    with tmp.open("wb") as handle:
        np.savez_compressed(handle, **{
            name: getattr(state, name) for name in FIELDS
        })
    os.replace(tmp, npz)
    meta["source_hashes"] = hashes
    meta["design_sha256"] = hashlib.sha256(DESIGN.read_bytes()).hexdigest()
    meta["state_sha256"] = hashlib.sha256(npz.read_bytes()).hexdigest()
    atomic_write(receipt, (json.dumps(meta, sort_keys=True,
                                      allow_nan=False, indent=2) + "\n").encode())
    return basename


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--shard-index", type=int, required=True)
    parser.add_argument("--shard-count", type=int, default=64)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    d = load_design()
    biology = load_biology(SOURCE)
    tasks = prehistory_tasks(d)
    if not 0 <= args.shard_index < args.shard_count or args.shard_count <= 0:
        raise ValueError("invalid shard")
    jobs = [t for i, t in enumerate(tasks)
            if i % args.shard_count == args.shard_index]
    if args.dry_run:
        print(json.dumps({"prehistory_tasks": len(jobs),
                          "full_campaign": len(tasks),
                          "design_sha256": hashlib.sha256(DESIGN.read_bytes()).hexdigest()}))
        return
    args.out.mkdir(parents=True, exist_ok=True)
    hashes = source_hashes()
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(persist_one, args.out, t, d, biology, hashes)
                   for t in jobs]
        completed = sorted(f.result() for f in as_completed(futures))
    if len(completed) != len(jobs):
        raise RuntimeError("incomplete prehistory shard")
    atomic_write(args.out / f"prehistory_shard_{args.shard_index:02d}.json",
        (json.dumps({
            "status": "raw_prehistories_complete_not_adjudicated",
            "design_sha256": hashlib.sha256(DESIGN.read_bytes()).hexdigest(),
            "source_hashes": hashes,
            "case_keys": completed,
        }, indent=2) + "\n").encode())
    print(json.dumps({"prehistory_cases": len(completed),
                      "shard": args.shard_index, "status": "raw_only"}))


if __name__ == "__main__":
    main()
