"""Strict scientific readout of failed independent16 and balanced mutational priority.

No automatic relabelling of a frozen FAILED test based on newer controls.
"""
from __future__ import annotations
from pathlib import Path
import argparse
import json
import numpy as np

from scripts.run_chapter2_island_mutational_priority_balanced import load_balanced
from scripts.run_chapter2_island_mutational_priority_independent16 import load_followup
from scripts.summarize_chapter2_island_mutational_priority_pilot import analyze

ROOT = Path(__file__).resolve().parents[1]


def read_rows(input_dir, prefix, shards):
    out = []
    for i in range(shards):
        out.extend(json.loads(
            (input_dir / f"{prefix}_{i:02d}.json").read_text(encoding="utf-8")
        ))
    return out


def historical_matrix(result, settings):
    history_ids = sorted({x["history"] for x in result["per_history"]})
    indexed = {(r["setting"], r["history"]): r for r in result["per_history"]}
    mat = np.array([
        [indexed[(setting, h)]["priority_interaction"]
         for setting in settings] for h in history_ids
    ])
    return mat


def assess(variant, rows):
    if variant == "independent16":
        d, _source = load_followup()[1:]
        record = json.loads((ROOT /
            "data/results/chapter2_island_mutational_priority_independent16_20261008.json"
        ).read_text(encoding="utf-8"))
        result = analyze(d, rows)
        mat = historical_matrix(result, d["settings"])
        if mat.shape != (16, 4):
            raise AssertionError("not 16 independent histories")
        ip = d["settings"].index("prior_selfing")
        idisc = d["settings"].index("pollen_discount")
        contrast = mat[:, ip] - mat[:, idisc]
        rng = np.random.default_rng(3210082026)
        index = rng.integers(0, 16, size=(9999, 16))
        sampled = contrast[index].mean(axis=1)
        interval = [float(x) for x in np.percentile(sampled, [2.5, 97.5])]
        mean = float(contrast.mean())
        passed = mean > 0 and interval[0] > 0
        frozen = record["frozen_primary"]
        if (passed or frozen["passed"]
            or abs(mean - frozen["mean"]) > 1e-12
            or not np.allclose(interval, frozen["bootstrap95"], atol=1e-12)):
            raise AssertionError("cannot relabel or alter failed independent16 result")
        result["independent16_primary"] = {
            "mean": mean, "bootstrap95": interval,
            "passes_frozen_rule": passed
        }
    elif variant == "balanced":
        _protocol, d, _source = load_balanced()
        record = json.loads((ROOT /
            "data/results/chapter2_island_mutational_priority_balanced_20261008.json"
        ).read_text(encoding="utf-8"))
        result = analyze(d, rows)
        if (abs(result["pooled_priority_mean_descriptive"] -
                record["pooled_descriptive_priority_interaction"]) > 1e-12):
            raise AssertionError("balanced pooled result drifted")
        expected = {x["setting"]: x for x in record["per_setting"]}
        for row in result["per_setting"]:
            if abs(row["priority_interaction_mean"] -
                   expected[row["setting"]]["priority_interaction"]) > 1e-12:
                raise AssertionError("balanced per-setting result drifted")
        result["balanced_total_mutation_access_generations"] = 250
    else:
        raise ValueError("unrecognized variant")
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--variant", choices=["independent16", "balanced"], required=True)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--shard-count", type=int, default=4)
    a = p.parse_args()
    prefix = "priority_independent16_shard" if a.variant == "independent16" else "priority_balanced_shard"
    result = assess(a.variant, read_rows(a.input, prefix, a.shard_count))
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({
        "variant": a.variant, "groups": result["n_prehistory_groups"],
        "poststress": result["n_poststress_trajectories"],
        "all_controls_accepted": True
    }))


if __name__ == "__main__":
    main()
