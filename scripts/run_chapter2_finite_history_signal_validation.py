"""Independent new-demographic-seed validation for Chapter 2 finite history signal.

Runs only the prospectively frozen validation seeds. The workflow restores the
exact source snapshot from the original bridge before invoking this module.
"""
from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path

import numpy as np

from scripts.model3_island.density import make_grid
from scripts.model3_island.run import founders_from_spec
from scripts.model3_island.simulate import simulate
from scripts.model3_island.types import Config
from scripts.model3_island_bridge_ops import prepare_arms

PAIR_ARMS = {
    "natural": ("near", "far"),
    "visitor_pooled": ("pool_near", "pool_far"),
    "large_plant_capacity": ("large_near", "large_far"),
}


def _verify_exact_source(parent: dict) -> str:
    h = sha256()
    for path, expected in sorted(parent["source_hashes"].items()):
        raw = Path(path).read_bytes()
        actual = sha256(raw).hexdigest()
        if actual != expected:
            raise ValueError(f"exact-source hash mismatch: {path}: {actual} != {expected}")
        h.update(path.encode())
        h.update(actual.encode())
    return h.hexdigest()


def _change(result: dict) -> float | None:
    pop = np.asarray(result["population"])
    trait = np.asarray(result["trait_mean"])
    if not (pop[0] > 0 and pop[-1] > 0 and np.isfinite(trait[[0, -1], 1]).all()):
        return None
    return float(trait[-1, 1] - trait[0, 1])


def run_shard(validation: dict, parent: dict, shard_index: int, shard_count: int) -> dict:
    if validation["status"] != "prospective_frozen_before_new_demographic_execution":
        raise ValueError("validation design is not prospectively frozen")
    if parent["status"] != "frozen":
        raise ValueError("parent bridge is not frozen")
    if validation["validation_source"]["new_demographic_seeds"] != [201, 202, 203, 204]:
        raise ValueError("validation demographic seeds changed")
    if validation["validation_source"]["inbreeding_depression"] != parent["base_config"]["depression"]:
        raise ValueError("validation depression differs from frozen bridge")
    if validation["validation_source"]["horizon"] != parent["years"]:
        raise ValueError("validation horizon differs from frozen bridge")
    if validation["validation_source"]["starts"] != parent["starts"]:
        raise ValueError("validation starts differ from frozen bridge")

    source_hash_root = _verify_exact_source(parent)
    all_histories = list(parent["history_seeds"])
    histories = [h for i, h in enumerate(all_histories) if i % shard_count == shard_index]
    if not histories:
        raise ValueError("empty validation shard")

    base = Config.from_dict(parent["base_config"])
    grid = make_grid(parent["grid_axes"])
    starts = [float(x) for x in validation["validation_source"]["starts"]]
    demos = [int(x) for x in validation["validation_source"]["new_demographic_seeds"]]
    expected_arms = set(validation["validation_source"]["arms"])
    needed_arms = {a for pair in PAIR_ARMS.values() for a in pair}
    if expected_arms != needed_arms:
        raise ValueError("validation arm set differs from frozen pair map")

    rows = []
    simulated_arm_trajectories = 0
    for hs in histories:
        arms = prepare_arms(base, seed=int(hs), pool_size=int(parent["pool_size"]))
        for start in starts:
            arm_results = {}
            for arm in sorted(needed_arms):
                cfg, history = arms[arm]
                spec = {
                    "count": cfg.capacity,
                    "draw_count": 48,
                    "means": [0.5, start, 0.5],
                    "sd": 0.15,
                    "birth_year": 0,
                }
                founders = founders_from_spec(spec, int(parent["founder_seed"]))
                for ds in demos:
                    replicate = int(np.random.SeedSequence([int(hs), int(ds)]).generate_state(1)[0])
                    result = simulate(
                        cfg,
                        history,
                        founders,
                        replicate=replicate,
                        grid=grid,
                        projection_mode=parent["projection_mode"],
                    )
                    arm_results[arm, ds] = {
                        "change": _change(result),
                        "terminal_population": int(np.asarray(result["population"])[-1]),
                        "extinction_year": int(result["extinction_year"]),
                    }
                    simulated_arm_trajectories += 1

            for intervention, (near, far) in PAIR_ARMS.items():
                for ds in demos:
                    n = arm_results[near, ds]
                    f = arm_results[far, ds]
                    effect = None
                    if n["change"] is not None and f["change"] is not None:
                        effect = float(f["change"] - n["change"])
                    rows.append(
                        {
                            "history_seed": int(hs),
                            "start": float(start),
                            "demographic_seed": int(ds),
                            "intervention": intervention,
                            "near_terminal_population": n["terminal_population"],
                            "far_terminal_population": f["terminal_population"],
                            "near_extinction_year": n["extinction_year"],
                            "far_extinction_year": f["extinction_year"],
                            "effect_far_minus_near": effect,
                        }
                    )

    expected_arm_trajectories = len(histories) * len(starts) * len(demos) * len(needed_arms)
    if simulated_arm_trajectories != expected_arm_trajectories:
        raise ValueError("arm trajectory denominator mismatch")
    expected_rows = len(histories) * len(starts) * len(demos) * len(PAIR_ARMS)
    if len(rows) != expected_rows:
        raise ValueError("paired row denominator mismatch")

    return {
        "schema_version": "1.0",
        "status": "complete_finite_history_signal_validation_shard",
        "shard_index": int(shard_index),
        "shard_count": int(shard_count),
        "source_hash_root": source_hash_root,
        "history_seeds": histories,
        "starts": starts,
        "demographic_seeds": demos,
        "simulated_arm_trajectories": simulated_arm_trajectories,
        "paired_rows": len(rows),
        "rows": rows,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--validation-design", required=True)
    p.add_argument("--parent-design", required=True)
    p.add_argument("--shard-index", type=int, required=True)
    p.add_argument("--shard-count", type=int, required=True)
    p.add_argument("--out", required=True)
    a = p.parse_args()

    validation = json.loads(Path(a.validation_design).read_text(encoding="utf-8"))
    parent = json.loads(Path(a.parent_design).read_text(encoding="utf-8"))
    result = run_shard(validation, parent, a.shard_index, a.shard_count)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": result["status"],
                "shard_index": result["shard_index"],
                "histories": len(result["history_seeds"]),
                "simulated_arm_trajectories": result["simulated_arm_trajectories"],
                "paired_rows": result["paired_rows"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
