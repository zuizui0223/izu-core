"""Run the prospectively frozen four-setting assurance generality campaign.

This runner writes hash-verified trajectory cases only. Biological readout is
performed by the separate summarizer after the complete declared campaign.
"""
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import replace
from pathlib import Path
import argparse
import hashlib
import json
import os
import zipfile

import numpy as np

from scripts.model3_island.types import Config
from scripts.model3_island.run import founders_from_spec
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import stream, STREAM_IDS
from scripts.run_model3_persistent_isolation import exposure

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "data/design/chapter2_assurance_generality_20261006.json"
BRIDGE = ROOT / "data/design/model3_ch2_bridge_20260927.json"


def load_design(path: Path) -> dict:
    design = json.loads(path.read_text(encoding="utf-8"))
    assert design["status"] == "frozen_before_generality_execution"
    assert set(design["settings"]) == {
        "delayed_control", "prior_selfing", "pollen_discount", "assurance_cost"
    }
    assert design["main_campaign"]["declared_cases"] == 8192
    assert design["structural_control"]["declared_cases"] == 256
    return design


def config(design: dict, setting: str, rate: float, mode: str) -> Config:
    if mode not in {"fixed", "evolving"}:
        raise ValueError(mode)
    base = Config.from_dict(json.loads(BRIDGE.read_text(encoding="utf-8"))["base_config"])
    patch = design["settings"][setting]
    return replace(
        base,
        years=int(design["main_campaign"]["periods"]),
        mutation_rate=float(rate),
        mutation_sd=0.05,
        assurance_mode=mode,
        fixed_assurance=float(design["main_campaign"]["fixed_assurance"]),
        assurance_timing=patch["assurance_timing"],
        pollen_discount=float(patch["pollen_discount"]),
        assurance_cost=float(patch["assurance_cost"]),
    )


def founders(design: dict):
    seed = int(design["main_campaign"]["founder_seed"])
    state = founders_from_spec(
        dict(count=48, draw_count=48, means=[0.5, 0.5, 0.5], sd=0.15, birth_year=0),
        seed,
    )
    alleles = state.alleles.copy()
    alleles[:, 2, :] = float(design["main_campaign"]["fixed_assurance"])
    return replace(state, alleles=alleles)


def simulate(
    design: dict,
    setting: str,
    rate: float,
    seed: int,
    rep: int,
    arm: str,
    mode: str,
) -> tuple[np.ndarray, dict]:
    c = config(design, setting, rate, mode)
    h = exposure(seed, arm)
    state = founders(design)
    master = int(np.random.SeedSequence([seed, rep]).generate_state(1)[0])
    streams = {name: stream(master, name, 0) for name in STREAM_IDS}
    steps = int(design["main_campaign"]["periods"])
    trace = np.full((steps + 1, 10), np.nan)
    states = {}
    for t in range(steps + 1):
        trace[t, 0] = len(state.ids)
        if len(state.ids):
            traits = state.alleles.mean(axis=2)
            trace[t, 1:4] = traits.mean(axis=0)
            trace[t, 4:7] = traits.var(axis=0)
            trace[t, 7:] = [len(np.unique(state.alleles[:, k])) for k in range(3)]
            if mode == "fixed":
                assert np.all(traits[:, 2] == c.fixed_assurance)
        if t in [0, 200, 400, steps]:
            states[f"state_{t}"] = state.alleles.copy()
        if t == steps:
            break
        ledger = reproduce(state, h.visitors[t], c)
        state, _ = advance(
            state,
            ledger,
            h.seed_candidates[t],
            c,
            streams,
            year=t,
            mutation_traits=(True, True, mode == "evolving"),
        )
    return trace, states


def seed_ranges(design: dict) -> tuple[range, range]:
    vh = design["main_campaign"]["visitor_history_seeds"]
    dr = design["main_campaign"]["demographic_repeat_seeds"]
    histories = range(int(vh["first"]), int(vh["last"]) + 1)
    repeats = range(int(dr["first"]), int(dr["last"]) + 1)
    assert len(histories) == 64 and len(repeats) == 8
    return histories, repeats


def declared_tasks(design: dict) -> list[tuple]:
    histories, repeats = seed_ranges(design)
    tasks = []
    main = design["main_campaign"]
    rate = float(main["mutation_probability"])
    for setting in design["settings"]:
        for seed in histories:
            for rep in repeats:
                for arm in main["arms"]:
                    for mode in main["modes"]:
                        tasks.append(("main", setting, rate, seed, rep, arm, mode))
    control = design["structural_control"]
    control_histories = list(histories)[: int(control["history_count"])]
    control_repeats = list(repeats)[: int(control["repeat_count"])]
    control_rate = float(control["mutation_probability"])
    for setting in design["settings"]:
        for seed in control_histories:
            for rep in control_repeats:
                for arm in control["arms"]:
                    for mode in control["modes"]:
                        tasks.append(("structural", setting, control_rate, seed, rep, arm, mode))
    assert len(tasks) == 8448
    return tasks


def case_key(task: tuple) -> str:
    kind, setting, rate, seed, rep, arm, mode = task
    return f"{kind}_{setting}_u{rate}_h{seed}_r{rep}_{arm}_{mode}"


def atomic_json(path: Path, data: dict) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    os.replace(temp, path)


def run_one(out: str, design: dict, task: tuple) -> str:
    out_path = Path(out)
    key = case_key(task)
    npz_path = out_path / f"{key}.npz"
    receipt_path = out_path / f"{key}.json"
    if receipt_path.exists():
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        assert receipt["task"] == list(task)
        assert npz_path.exists()
        assert hashlib.sha256(npz_path.read_bytes()).hexdigest() == receipt["sha256"]
        return key
    _, setting, rate, seed, rep, arm, mode = task
    trace, states = simulate(design, setting, rate, seed, rep, arm, mode)
    temp = npz_path.with_suffix(".tmp")
    with temp.open("wb") as handle:
        np.savez_compressed(handle, trace=trace, **states)
    os.replace(temp, npz_path)
    digest = hashlib.sha256(npz_path.read_bytes()).hexdigest()
    atomic_json(receipt_path, {"task": list(task), "sha256": digest})
    return key


def snapshot_sources(out: Path, design_path: Path) -> None:
    paths = [
        Path(__file__).resolve(),
        BRIDGE,
        design_path.resolve(),
        ROOT / "scripts/run_model3_persistent_isolation.py",
    ]
    paths.extend(sorted((ROOT / "scripts/model3_island").glob("*.py")))
    hashes = {
        p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in paths
    }
    manifest = out / "sources.json"
    if manifest.exists():
        assert json.loads(manifest.read_text(encoding="utf-8")) == hashes
        return
    atomic_json(manifest, hashes)
    with zipfile.ZipFile(out / "sources.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for p in paths:
            archive.write(p, p.relative_to(ROOT).as_posix())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--design", type=Path, default=DEFAULT_DESIGN)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--shard-index", type=int, required=True)
    parser.add_argument("--shard-count", type=int, default=32)
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args()
    if not (0 <= args.shard_index < args.shard_count):
        raise ValueError("invalid shard index")

    design_path = args.design if args.design.is_absolute() else ROOT / args.design
    design_path = design_path.resolve()
    design = load_design(design_path)
    args.out.mkdir(parents=True, exist_ok=True)
    snapshot_sources(args.out, design_path)
    all_tasks = declared_tasks(design)
    shard_tasks = [
        task for index, task in enumerate(all_tasks)
        if index % args.shard_count == args.shard_index
    ]
    expected = sorted(case_key(task) for task in shard_tasks)
    completed = []
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run_one, str(args.out), design, task) for task in shard_tasks]
        for future in as_completed(futures):
            completed.append(future.result())
    completed = sorted(completed)
    assert completed == expected
    atomic_json(
        args.out / f"shard_{args.shard_index:02d}_complete.json",
        {
            "status": "completed",
            "shard_index": args.shard_index,
            "shard_count": args.shard_count,
            "n_cases": len(completed),
            "keys": completed,
            "design_sha256": hashlib.sha256(design_path.read_bytes()).hexdigest(),
        },
    )
    print(json.dumps({"status": "completed", "shard": args.shard_index, "cases": len(completed)}))


if __name__ == "__main__":
    main()
