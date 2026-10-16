"""Prospectively frozen, *new founder* crossed Q1 Model 3 campaign.

Never change the historical 2026-10-06 producer, design or results.  Reuse its
biological operators, mating settings, fixed/evolvable A implementation,
exogenous near/far visitor histories, and 1000-update endpoint unchanged.
New independent founder draws are crossed with new visitor histories.
Technical smoke calls with fewer than 1000 updates are not scientific cases.
"""
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import replace
from pathlib import Path
import argparse
import hashlib
import json
import os

import numpy as np

from scripts.model3_island.run import founders_from_spec
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.run_model3_persistent_isolation import exposure
from scripts.run_chapter2_assurance_generality import config, load_design as original_design

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_q1_fresh_founder_generality_20261016.json"
MAIN_NAMES = ("delayed_control", "prior_selfing", "pollen_discount", "assurance_cost")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def atomic_json(path: Path, data: dict) -> None:
    if path.exists():
        raise FileExistsError("Original result is immutable: " + str(path))
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True, allow_nan=False) + "\n",
                   encoding="utf-8")
    os.replace(tmp, path)


def load_frozen(path: Path = DESIGN) -> tuple[dict, dict]:
    d = json.loads(path.read_text(encoding="utf-8"))
    assert d["status"] == "frozen_before_any_new_founder_outcome"
    assert tuple(d["settings"]) == MAIN_NAMES
    source = original_design(ROOT / d["source_biology"])
    assert tuple(source["settings"]) == MAIN_NAMES
    orig = source["main_campaign"]
    assert orig["periods"] == d["updates"] == 1000
    assert orig["mutation_probability"] == d["mutation_probability"] == .01
    assert orig["fixed_assurance"] == .5
    founders = d["founder_genomes"]
    visitors = d["visitor_histories"]
    f = range(founders["first_seed"], founders["last_seed"] + 1)
    h = range(visitors["first_seed"], visitors["last_seed"] + 1)
    assert len(f) == founders["n_independent"] == 8
    assert len(h) == visitors["n_independent"] == 8
    assert founders["exclude_original_founder_seed"] == orig["founder_seed"]
    assert orig["founder_seed"] not in f
    assert not set(h).intersection(range(26110601, 26110665))
    assert founders["n"] == founders["draw_count"] == 48
    assert founders["means"] == [.5, .5, .5]
    assert founders["sd"] == .15
    assert founders["A_initial_alleles"] == [.5, .5]
    assert d["main_cases"] == 1024 and d["total_cases"] == 1088
    assert d["null_control"]["cases"] == 64
    assert d["demography"]["nested_repeats_per_founder_visitor"] == 1
    assert d["resource_constraints"]["shards"] == 32
    assert not d["visitor_histories"]["plant_and_pollinator_coevolution"]
    return d, source


def founder(d: dict, seed: int):
    f = d["founder_genomes"]
    pop = founders_from_spec(
        {"count": f["n"], "draw_count": f["draw_count"],
         "means": f["means"], "sd": f["sd"], "birth_year": 0},
        seed,
    )
    alleles = pop.alleles.copy()
    alleles[:, 2, :] = f["A_initial_alleles"]
    return replace(pop, alleles=alleles)


def declared_tasks(d: dict) -> list[tuple]:
    main = []
    f = d["founder_genomes"]
    h = d["visitor_histories"]
    rep = d["demography"]["repeat_seed"]
    for setting in d["settings"]:
        for fs in range(f["first_seed"], f["last_seed"] + 1):
            for vs in range(h["first_seed"], h["last_seed"] + 1):
                for arm in h["arms"]:
                    for mode in d["modes"]:
                        main.append(("main", setting, d["mutation_probability"],
                                     fs, vs, rep, arm, mode))
    n = d["null_control"]
    null = []
    for setting in n["settings"]:
        for fs in n["founder_seeds"]:
            for vs in n["visitor_history_seeds"]:
                for arm in n["arms"]:
                    for mode in n["modes"]:
                        null.append(("null", setting, n["mutation_probability"],
                                     fs, vs, rep, arm, mode))
    assert len(main) == d["main_cases"] == 1024
    assert len(null) == n["cases"] == 64
    tasks = main + null
    assert len(tasks) == d["total_cases"] == len(set(tasks)) == 1088
    return tasks


def task_key(task: tuple) -> str:
    kind, setting, rate, fs, vs, rep, arm, mode = task
    return f"{kind}_{setting}_u{rate}_f{fs}_v{vs}_r{rep}_{arm}_{mode}"


def simulate(d: dict, source: dict, task: tuple,
             *, steps: int | None = None) -> tuple[np.ndarray, dict]:
    kind, setting, rate, fs, vs, rep, arm, mode = task
    cfg = config(source, setting, rate, mode)
    env = exposure(vs, arm)
    plants = founder(d, fs)
    nsteps = d["updates"] if steps is None else steps
    if not isinstance(nsteps, int) or not 1 <= nsteps <= d["updates"]:
        raise ValueError("Invalid technical/full duration")
    assert len(env.visitors) >= nsteps
    master = int(np.random.SeedSequence([vs, rep]).generate_state(1)[0])
    streams = {name: stream(master, name, 0) for name in STREAM_IDS}
    trace = np.full((nsteps + 1, 10), np.nan)
    snapshots = {}
    for t in range(nsteps + 1):
        trace[t, 0] = len(plants.ids)
        if len(plants.ids):
            z = plants.alleles.mean(axis=2)
            trace[t, 1:4] = z.mean(axis=0)
            trace[t, 4:7] = z.var(axis=0)
            trace[t, 7:] = [len(np.unique(plants.alleles[:, k])) for k in range(3)]
            if mode == "fixed":
                assert np.all(z[:, 2] == cfg.fixed_assurance)
        if t in (0, 200, 400, nsteps):
            snapshots[f"state_{t}"] = plants.alleles.copy()
        if t == nsteps:
            break
        led = reproduce(plants, env.visitors[t], cfg)
        plants, _ = advance(
            plants, led, env.seed_candidates[t], cfg, streams,
            year=t, mutation_traits=(True, True, mode == "evolving"),
        )
    return trace, snapshots


def source_manifest() -> dict:
    paths = [
        Path(__file__),
        ROOT / "scripts/run_chapter2_assurance_generality.py",
        ROOT / "scripts/run_model3_persistent_isolation.py",
        ROOT / "data/design/model3_ch2_bridge_20260927.json",
        ROOT / "data/design/chapter2_assurance_generality_20261006.json",
        DESIGN,
    ] + sorted((ROOT / "scripts/model3_island").glob("*.py"))
    return {p.relative_to(ROOT).as_posix(): sha(p.read_bytes()) for p in paths}


def execute(out: str, d: dict, source: dict, task: tuple,
            manifest_digest: str) -> str:
    root = Path(out)
    key = task_key(task)
    npz = root / (key + ".npz")
    receipt = root / (key + ".json")
    if receipt.exists():
        data = json.loads(receipt.read_text(encoding="utf-8"))
        if (data.get("task") != list(task) or
                data.get("manifest_sha256") != manifest_digest or
                not npz.is_file() or sha(npz.read_bytes()) != data["sha256"]):
            raise ValueError("Invalid existing case, refusing overwrite: " + key)
        return key
    if npz.exists():
        raise FileExistsError("Unreceipted original result: " + key)
    trace, snapshots = simulate(d, source, task)
    tmp = npz.with_suffix(".npz.tmp")
    with tmp.open("wb") as handle:
        np.savez_compressed(handle, trace=trace, **snapshots)
    os.replace(tmp, npz)
    atomic_json(receipt, {
        "task": list(task), "sha256": sha(npz.read_bytes()),
        "manifest_sha256": manifest_digest, "endpoint": d["updates"],
        "status": "complete",
    })
    return key


def run_shard(d: dict, source: dict, out: Path, shard: int,
              count: int, workers: int) -> dict:
    if (count != d["resource_constraints"]["shards"] or
            not 0 <= shard < count or
            not 1 <= workers <= d["resource_constraints"]["workers_per_shard"]):
        raise ValueError("Frozen shard/worker contract changed")
    out.mkdir(parents=True, exist_ok=True)
    source_data = source_manifest()
    raw = json.dumps(source_data, sort_keys=True, separators=(",", ":")).encode()
    digest = sha(raw)
    manifest_path = out / "sources.json"
    if manifest_path.exists():
        if json.loads(manifest_path.read_text()) != source_data:
            raise ValueError("Source manifest diverged")
    else:
        atomic_json(manifest_path, source_data)
    tasks = [t for index, t in enumerate(declared_tasks(d))
             if index % count == shard]
    keys = [task_key(t) for t in tasks]
    # No scientific readout from individual shards.
    with ProcessPoolExecutor(max_workers=workers) as pool:
        fs = [pool.submit(execute, str(out), d, source, t, digest)
              for t in tasks]
        finished = sorted(f.result() for f in as_completed(fs))
    if finished != sorted(keys):
        raise AssertionError("incomplete shard")
    output = {
        "status": "completed", "shard": shard, "shards": count,
        "keys": finished, "cases": len(finished),
        "design_sha256": sha(DESIGN.read_bytes()),
        "manifest_sha256": digest, "original_biology_unchanged": True,
    }
    atomic_json(out / f"shard_{shard:02d}_complete.json", output)
    return output


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--shard-index", required=True, type=int)
    p.add_argument("--shard-count", type=int, default=32)
    p.add_argument("--workers", type=int, default=2)
    args = p.parse_args()
    design, source = load_frozen()
    print(json.dumps(run_shard(design, source, args.out, args.shard_index,
                               args.shard_count, args.workers)))


if __name__ == "__main__":
    main()
