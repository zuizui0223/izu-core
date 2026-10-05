"""Run the prospectively frozen 2026-10-05 confirmatory replication.

No biological readout is produced here. This runner only executes declared
trajectories and writes hash-verified case receipts. The summarizer refuses
partial campaigns.
"""
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
import argparse
import hashlib
import json
import os
import zipfile

import numpy as np

from scripts.run_model3_persistent_isolation import run_case as run_persistent_case
from scripts.run_model3_assurance_intervention import simulate as simulate_assurance

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "data/design/chapter2_1005_confirmatory_replication_20261006.json"


def load_design(path: Path) -> dict:
    design = json.loads(path.read_text(encoding="utf-8"))
    assert design["status"] == "frozen_before_confirmatory_execution"
    assert design["sequence_campaign"]["total_cases"] == 2048
    assert design["fixed_assurance_campaign"]["total_cases"] == 2048
    return design


def seed_ranges(design: dict) -> tuple[range, range]:
    vh = design["new_randomization"]["visitor_history_seeds"]
    dr = design["new_randomization"]["demographic_repeat_seeds"]
    histories = range(int(vh["first"]), int(vh["last"]) + 1)
    repeats = range(int(dr["first"]), int(dr["last"]) + 1)
    assert len(histories) == 64 and len(repeats) == 8
    return histories, repeats


def declared_tasks(design: dict) -> list[tuple]:
    histories, repeats = seed_ranges(design)
    tasks: list[tuple] = []
    for setting in design["sequence_campaign"]["reproductive_settings"]:
        for rate in design["sequence_campaign"]["mutation_probabilities"]:
            for seed in histories:
                for rep in repeats:
                    tasks.append(("sequence", setting, float(rate), seed, rep, "far"))
    for setting in design["fixed_assurance_campaign"]["reproductive_settings"]:
        for rate in design["fixed_assurance_campaign"]["mutation_probabilities"]:
            for seed in histories:
                for rep in repeats:
                    for arm in design["fixed_assurance_campaign"]["arms"]:
                        tasks.append(("fixed_assurance", setting, float(rate), seed, rep, arm))
    assert len(tasks) == 4096
    return tasks


def atomic_json(path: Path, data: dict) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    os.replace(temp, path)


def case_key(task: tuple) -> str:
    kind, setting, rate, seed, rep, arm = task
    return f"{kind}_{setting}_u{rate}_h{seed}_r{rep}_{arm}"


def run_one(out: str, task: tuple) -> str:
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

    kind, setting, rate, seed, rep, arm = task
    if kind == "sequence":
        persistent_task = (
            str(out_path), key, "abm", setting, rate, seed, rep, arm, 0, "jump", False
        )
        run_persistent_case(persistent_task)
        # Replace the generic persistent receipt task with this campaign's declared task.
        generic = json.loads(receipt_path.read_text(encoding="utf-8"))
        assert hashlib.sha256(npz_path.read_bytes()).hexdigest() == generic["sha256"]
        atomic_json(
            receipt_path,
            {"task": list(task), "sha256": generic["sha256"], "kind": "sequence"},
        )
        return key

    if kind == "fixed_assurance":
        trace, states = simulate_assurance(setting, rate, seed, rep, arm, "fixed", steps=1000)
        temp = npz_path.with_suffix(".tmp")
        with temp.open("wb") as handle:
            np.savez_compressed(handle, trace=trace, **states)
        os.replace(temp, npz_path)
        digest = hashlib.sha256(npz_path.read_bytes()).hexdigest()
        atomic_json(
            receipt_path,
            {"task": list(task), "sha256": digest, "kind": "fixed_assurance"},
        )
        return key

    raise ValueError(kind)


def snapshot_sources(out: Path, design_path: Path) -> None:
    source_paths = [
        Path(__file__),
        ROOT / "scripts/run_model3_persistent_isolation.py",
        ROOT / "scripts/run_model3_assurance_intervention.py",
        ROOT / "scripts/model3_temporal_order.py",
        ROOT / "data/design/model3_ch2_bridge_20260927.json",
        design_path,
    ]
    source_paths.extend(sorted((ROOT / "scripts/model3_island").glob("*.py")))
    hashes = {
        p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in source_paths
    }
    manifest = out / "sources.json"
    if manifest.exists():
        assert json.loads(manifest.read_text(encoding="utf-8")) == hashes
        return
    atomic_json(manifest, hashes)
    with zipfile.ZipFile(out / "sources.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for p in source_paths:
            archive.write(p, p.relative_to(ROOT).as_posix())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--design", type=Path, default=DEFAULT_DESIGN)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--shard-index", type=int, required=True)
    parser.add_argument("--shard-count", type=int, default=16)
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args()

    if not (0 <= args.shard_index < args.shard_count):
        raise ValueError("invalid shard index")

    design = load_design(args.design)
    args.out.mkdir(parents=True, exist_ok=True)
    snapshot_sources(args.out, args.design)
    all_tasks = declared_tasks(design)
    shard_tasks = [task for index, task in enumerate(all_tasks) if index % args.shard_count == args.shard_index]
    expected = [case_key(task) for task in shard_tasks]

    completed: list[str] = []
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run_one, str(args.out), task) for task in shard_tasks]
        for future in as_completed(futures):
            completed.append(future.result())

    completed = sorted(completed)
    assert completed == sorted(expected)
    marker = args.out / f"shard_{args.shard_index:02d}_complete.json"
    atomic_json(
        marker,
        {
            "status": "completed",
            "shard_index": args.shard_index,
            "shard_count": args.shard_count,
            "n_cases": len(completed),
            "keys": completed,
            "design_sha256": hashlib.sha256(args.design.read_bytes()).hexdigest(),
        },
    )
    print(json.dumps({"status": "completed", "shard": args.shard_index, "cases": len(completed)}))


if __name__ == "__main__":
    main()
