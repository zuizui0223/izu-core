"""History-level bootstrap and frozen gate for island demographic confirmation.

No post-hoc selection of particular stress levels. Read and verify ALL eight
shards; aggregate the eight post-treatment occupancy flags per prehistory,
then the four-setting evolving-versus-fixed contrast within visitor history.
"""
from __future__ import annotations
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json

import numpy as np
from scripts.run_chapter2_island_demographic_independent32 import load_frozen, tasks


def read_shards(directory, d):
    observed = {}
    sha = {}
    for shard in range(8):
        name = f"demographic_independent32_shard_{shard:02d}.json"
        path = directory / name
        raw = path.read_bytes()
        sha[name] = hashlib.sha256(raw).hexdigest()
        rows = json.loads(raw)
        for row in rows:
            key = tuple(row["group"])
            if key in observed or not isinstance(row["post_cases"], list):
                raise ValueError("duplicate or extinct prehistory " + str(key))
            if len(row["post_cases"]) != 8:
                raise ValueError("missing post cases " + str(key))
            expected = set(product(
                d["post_environments"], d["stress_ovule_budgets"]
            ))
            actual = {(p["post"], p["ovule_budget"]) for p in row["post_cases"]}
            if actual != expected:
                raise ValueError("incomplete stress grid " + str(key))
            for p in row["post_cases"]:
                if p["occupied"] not in (0, 1):
                    raise ValueError("invalid occupancy")
                if bool(p["terminal_N"]) != bool(p["occupied"]):
                    raise ValueError("occupancy contradicts endpoint")
            observed[key] = row
    expected_keys = set(tasks(d))
    if set(observed) != expected_keys or len(observed) != d["total_groups"]:
        raise ValueError("missing or unexpected history groups")
    return observed, sha


def evaluate(d, rows):
    names = list(d["settings"])
    histories = list(range(
        d["independent_visitor_histories"]["first"],
        d["independent_visitor_histories"]["last"] + 1,
    ))
    rep, = d["demographic_repeat_seeds"]
    individual = []
    for h in histories:
        setting_rows = {}
        for setting in names:
            cf = {}
            for mode in ("fixed", "evolving"):
                def integrated(pre):
                    case = rows[setting, mode, h, rep, pre]
                    return float(np.mean([
                        x["occupied"] for x in case["post_cases"]
                    ]))
                near = integrated("near")
                far = integrated("far")
                cf[mode] = {
                    "near": near, "far": far, "delta": far - near,
                }
            setting_rows[setting] = {
                **cf,
                "interaction": (
                    cf["evolving"]["delta"] - cf["fixed"]["delta"]
                ),
            }
        individual.append({"history": h, "settings": setting_rows})

    matrix = np.array([
        [r["settings"][setting]["interaction"] for setting in names]
        for r in individual
    ])
    rng = np.random.default_rng(d["bootstrap"]["seed"])
    index = rng.integers(0, len(histories), size=(
        d["bootstrap"]["draws"], len(histories),
    ))
    boot = matrix[index].mean(axis=1)
    pooled_boot = boot.mean(axis=1)
    pooled_mean = float(matrix.mean())
    pooled_ci = [float(x) for x in np.percentile(
        pooled_boot, [2.5, 97.5],
    )]
    per_setting = []
    for i, setting in enumerate(names):
        values = matrix[:, i]
        per_setting.append({
            "setting": setting,
            "fixed_delta": float(np.mean([
                r["settings"][setting]["fixed"]["delta"]
                for r in individual
            ])),
            "evolving_delta": float(np.mean([
                r["settings"][setting]["evolving"]["delta"]
                for r in individual
            ])),
            "interaction": float(values.mean()),
            "bootstrap95": [float(x) for x in np.percentile(
                boot[:, i], [2.5, 97.5],
            )],
            "positive_history_count": int(np.sum(values > 0)),
            "negative_history_count": int(np.sum(values < 0)),
            "zero_history_count": int(np.sum(values == 0)),
        })
    return {
        "independent_histories": len(histories),
        "nested_demographic_repeats": len(d["demographic_repeat_seeds"]),
        "historical_groups": len(rows),
        "post_trajectories": 8 * len(rows),
        "pooled_primary": {
            "mean": pooled_mean,
            "bootstrap95": pooled_ci,
            "passes_frozen_rule": bool(
                pooled_mean > 0 and pooled_ci[0] > 0
            ),
        },
        "per_setting": per_setting,
        "individual_history_differences": individual,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    d, _ = load_frozen()
    rows, digests = read_shards(args.input, d)
    result = evaluate(d, rows)
    result["status"] = "frozen_independent_history_readout"
    result["design_sha256"] = hashlib.sha256(
        Path(__file__).resolve().parents[1]
        .joinpath("data/design/chapter2_island_demographic_independent32_20261008.json")
        .read_bytes()
    ).hexdigest()
    result["shard_sha256"] = digests
    result["claim_boundary"] = [
        "This test uses a pre-declared pooled rule but the stress grid was motivated by an earlier exposed pilot.",
        "The population bottleneck and fecundity reduction jointly change density-dependent pollen transfer.",
        "Only one demographic replicate per independent visitor history.",
        "No direct ordering-of-trait-change intervention.",
        "No direct calibration of geographical distance, island area, time scale or natural extinction.",
    ]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps(result["pooled_primary"]))


if __name__ == "__main__":
    main()
