"""Run the prospectively frozen new-demographic-seed validation.

This runner requires an extracted exact Model 3 source snapshot. It does not
use the mutable repository implementation for the biological simulation.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from hashlib import sha256
import json
import os
from pathlib import Path
import sys

import numpy as np


def _verify_source_root(root: Path, bridge: dict) -> None:
    for rel, expected in bridge["source_hashes"].items():
        path = root / rel
        if not path.exists():
            raise FileNotFoundError(path)
        got = sha256(path.read_bytes()).hexdigest()
        if got != expected:
            raise ValueError(f"source hash mismatch for {rel}: {got} != {expected}")


def _one_history(payload):
    source_root, bridge, validation, hs = payload
    source_root = Path(source_root)
    sys.path.insert(0, str(source_root))

    from scripts.model3_island.types import Config
    from scripts.model3_island.density import make_grid, project_state
    from scripts.model3_island.run import founders_from_spec
    from scripts.model3_island.reproduction import reproduce
    from scripts.model3_island.population import advance
    from scripts.model3_island.randomness import stream, STREAM_IDS
    from scripts.model3_island_bridge_ops import prepare_arms

    base = Config.from_dict(bridge["base_config"])
    grid = make_grid(bridge["grid_axes"])
    arms = prepare_arms(base, seed=int(hs), pool_size=int(bridge["pool_size"]))
    projection_mode = bridge["projection_mode"]

    def finite_terminal(cfg, history, founders, replicate):
        state, _ = project_state(founders, grid)
        initial = float(state.alleles.mean(axis=2)[:, 1].mean()) if len(state.ids) else None
        streams = {name: stream(replicate, name, 0) for name in STREAM_IDS}
        for year in range(cfg.years):
            ledger = reproduce(state, history.visitors[year], cfg)
            state, _ = advance(
                state, ledger, history.seed_candidates[year], cfg, streams, year=year
            )
            if projection_mode == "grid":
                state, _ = project_state(state, grid)
        terminal = float(state.alleles.mean(axis=2)[:, 1].mean()) if len(state.ids) else None
        change = None if initial is None or terminal is None else float(terminal - initial)
        return int(len(state.ids)), change

    rows = []
    for start in validation["validation_source"]["starts"]:
        for arm in validation["validation_source"]["arms"]:
            cfg, history = arms[arm]
            founders = founders_from_spec(
                {
                    "count": cfg.capacity,
                    "draw_count": 48,
                    "means": [0.5, float(start), 0.5],
                    "sd": 0.15,
                    "birth_year": 0,
                },
                int(bridge["founder_seed"]),
            )
            for demo in validation["validation_source"]["new_demographic_seeds"]:
                replicate = int(
                    np.random.SeedSequence([int(hs), int(demo)]).generate_state(1)[0]
                )
                pop, change = finite_terminal(cfg, history, founders, replicate)
                rows.append(
                    {
                        "history_seed": int(hs),
                        "start": float(start),
                        "arm": arm,
                        "demographic_seed": int(demo),
                        "terminal_population": pop,
                        "occupied": bool(pop > 0),
                        "investment_change": change,
                    }
                )
    return rows


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--source-root", type=Path, required=True)
    p.add_argument(
        "--bridge-design",
        type=Path,
        default=Path("data/design/model3_ch2_bridge_execution_20260927.json"),
    )
    p.add_argument(
        "--validation-design",
        type=Path,
        default=Path("data/design/chapter2_finite_history_signal_validation_20261003.json"),
    )
    p.add_argument("--shard-index", type=int, required=True)
    p.add_argument("--shard-count", type=int, default=16)
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()

    bridge = json.loads(a.bridge_design.read_text(encoding="utf-8"))
    validation = json.loads(a.validation_design.read_text(encoding="utf-8"))
    if bridge["status"] != "frozen":
        raise ValueError("frozen bridge design required")
    if validation["status"] != "prospective_frozen_before_new_demographic_execution":
        raise ValueError("frozen validation design required")
    if bridge["base_config"]["depression"] != validation["validation_source"]["inbreeding_depression"]:
        raise ValueError("depression differs from validation lock")
    if bridge["years"] != validation["validation_source"]["horizon"]:
        raise ValueError("horizon differs from validation lock")
    _verify_source_root(a.source_root, bridge)

    histories = [int(x) for x in bridge["history_seeds"]]
    selected = histories[a.shard_index :: a.shard_count]
    if not selected:
        raise ValueError("empty shard")

    payloads = [(str(a.source_root), bridge, validation, h) for h in selected]
    rows = []
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")
    with ProcessPoolExecutor(max_workers=max(1, a.workers)) as ex:
        futures = [ex.submit(_one_history, payload) for payload in payloads]
        for fut in as_completed(futures):
            rows.extend(fut.result())

    rows.sort(
        key=lambda r: (
            r["history_seed"],
            r["start"],
            r["arm"],
            r["demographic_seed"],
        )
    )
    expected = (
        len(selected)
        * len(validation["validation_source"]["starts"])
        * len(validation["validation_source"]["arms"])
        * len(validation["validation_source"]["new_demographic_seeds"])
    )
    if len(rows) != expected:
        raise ValueError(f"expected {expected} rows, got {len(rows)}")
    out = {
        "schema_version": "1.0",
        "status": "complete_new_demographic_validation_shard",
        "shard_index": a.shard_index,
        "shard_count": a.shard_count,
        "history_seeds": selected,
        "starts": validation["validation_source"]["starts"],
        "demographic_seeds": validation["validation_source"]["new_demographic_seeds"],
        "arms": validation["validation_source"]["arms"],
        "rows": rows,
    }
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(out, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps({"status": out["status"], "histories": len(selected), "rows": len(rows)}))


if __name__ == "__main__":
    main()
