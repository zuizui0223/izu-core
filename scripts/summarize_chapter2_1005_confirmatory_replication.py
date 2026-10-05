"""Apply the frozen success rules to the complete 2026-10-05 replication."""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import argparse
import hashlib
import json

import numpy as np

from scripts.model3_temporal_order import first_sustained, order_label
from scripts.run_chapter2_1005_confirmatory_replication import (
    case_key,
    declared_tasks,
    load_design,
    seed_ranges,
)


def find_case(root: Path, key: str) -> Path:
    matches = list(root.rglob(key + ".npz"))
    if len(matches) != 1:
        raise ValueError(f"expected one case for {key}, found {len(matches)}")
    return matches[0]


def verify_complete(root: Path, design_path: Path, design: dict) -> dict[str, Path]:
    expected_tasks = declared_tasks(design)
    expected = {case_key(task): task for task in expected_tasks}
    markers = sorted(root.rglob("shard_*_complete.json"))
    if len(markers) != 16:
        raise ValueError(f"incomplete campaign: expected 16 shard markers, found {len(markers)}")
    design_sha = hashlib.sha256(design_path.read_bytes()).hexdigest()
    keys: list[str] = []
    for marker in markers:
        row = json.loads(marker.read_text(encoding="utf-8"))
        if row["status"] != "completed" or row["shard_count"] != 16:
            raise ValueError(f"invalid shard marker {marker}")
        if row["design_sha256"] != design_sha:
            raise ValueError(f"design mismatch {marker}")
        keys.extend(row["keys"])
    if len(keys) != 4096 or len(set(keys)) != 4096 or set(keys) != set(expected):
        raise ValueError("declared 4096-case campaign is incomplete or mismatched")

    paths: dict[str, Path] = {}
    for key, task in expected.items():
        path = find_case(root, key)
        receipt_path = path.with_suffix(".json")
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        if receipt["task"] != list(task):
            raise ValueError(f"task mismatch {key}")
        if hashlib.sha256(path.read_bytes()).hexdigest() != receipt["sha256"]:
            raise ValueError(f"hash mismatch {key}")
        paths[key] = path
    return paths


def history_trace(paths: dict[str, Path], kind: str, setting: str, rate: float, seed: int, repeats: range, arm: str) -> np.ndarray:
    traces = []
    for rep in repeats:
        key = f"{kind}_{setting}_u{rate}_h{seed}_r{rep}_{arm}"
        with np.load(paths[key]) as z:
            trace = z["trace"].copy()
        if trace.shape != (1001, 10):
            raise ValueError((key, trace.shape))
        traces.append(trace)
    return np.asarray(traces)


def history_mean_trace(traces: np.ndarray) -> np.ndarray:
    occupied = traces[:, :, 0] > 0
    traits = traces[:, :, 1:4]
    total = np.where(occupied[:, :, None], traits, 0.0).sum(axis=0)
    counts = occupied.sum(axis=0)
    return np.divide(total, counts[:, None], out=np.full(total.shape, np.nan), where=counts[:, None] > 0)


def bootstrap_interval(values: np.ndarray, draws: int, seed: int) -> list[float]:
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if not len(values):
        return [float("nan"), float("nan")]
    index = np.random.default_rng(seed).integers(0, len(values), size=(draws, len(values)))
    boot = values[index].mean(axis=1)
    return [float(x) for x in np.quantile(boot, [0.025, 0.975])]


def sequence_readout(design: dict, paths: dict[str, Path]) -> list[dict]:
    histories, repeats = seed_ranges(design)
    seq = design["sequence_campaign"]
    rows: list[dict] = []
    for setting in seq["reproductive_settings"]:
        for rate in seq["mutation_probabilities"]:
            curves = []
            for seed in histories:
                traces = history_trace(paths, "sequence", setting, float(rate), seed, repeats, "far")
                curves.append(history_mean_trace(traces))
            curves = np.asarray(curves)
            founder = curves[:, 0, :]
            delta = curves - founder[:, None, :]
            for threshold in seq["thresholds"]:
                labels: list[str] = []
                events: list[dict] = []
                assurance_binary = []
                for seed, values in zip(histories, delta):
                    ti = first_sustained(
                        -values[:, 1], float(threshold), int(seq["sustained_periods"])
                    )
                    ta = first_sustained(
                        values[:, 2], float(threshold), int(seq["sustained_periods"])
                    )
                    label = order_label(ta, ti, int(seq["tie_tolerance_periods"]))
                    labels.append(label)
                    assurance_binary.append(1.0 if label == "assurance_first" else 0.0)
                    events.append(
                        {
                            "history_seed": seed,
                            "investment_time": ti,
                            "assurance_time": ta,
                            "order": label,
                        }
                    )
                counts = dict(Counter(labels))
                binary = np.asarray(assurance_binary)
                ci = bootstrap_interval(
                    binary,
                    int(seq["bootstrap"]["draws"]),
                    int(seq["bootstrap"]["seed"]) + int(round(float(threshold) * 1000)),
                )
                rows.append(
                    {
                        "setting": setting,
                        "mutation_rate": float(rate),
                        "threshold": float(threshold),
                        "counts": counts,
                        "total_histories": 64,
                        "assurance_first_proportion_all_histories": float(binary.mean()),
                        "assurance_first_bootstrap95": ci,
                        "events": events,
                    }
                )
    return rows


def fixed_readout(design: dict, paths: dict[str, Path]) -> list[dict]:
    histories, repeats = seed_ranges(design)
    fixed = design["fixed_assurance_campaign"]
    rows: list[dict] = []
    for setting in fixed["reproductive_settings"]:
        rate = float(fixed["mutation_probabilities"][0])
        far_history = []
        paired_history = []
        arm_occupancy = {"near": 0, "far": 0}
        eligible_far = 0
        eligible_paired = 0
        founder_values = []
        for seed in histories:
            by_arm = {}
            for arm in fixed["arms"]:
                traces = history_trace(paths, "fixed_assurance", setting, rate, seed, repeats, arm)
                alive = traces[:, 1000, 0] > 0
                arm_occupancy[arm] += int(alive.sum())
                founder_values.extend(traces[:, 0, 2].tolist())
                endpoint = traces[:, 1000, 2]
                changes = endpoint - traces[:, 0, 2]
                by_arm[arm] = (changes, alive, endpoint)
            far_change, far_alive, _ = by_arm["far"]
            if far_alive.any():
                far_history.append(float(far_change[far_alive].mean()))
                eligible_far += 1
            near_change, near_alive, _ = by_arm["near"]
            paired = far_alive & near_alive
            if paired.any():
                paired_history.append(float((far_change[paired] - near_change[paired]).mean()))
                eligible_paired += 1

        far_values = np.asarray(far_history, dtype=float)
        paired_values = np.asarray(paired_history, dtype=float)
        base_seed = int(fixed["bootstrap"]["seed"])
        far_ci = bootstrap_interval(far_values, int(fixed["bootstrap"]["draws"]), base_seed)
        paired_ci = bootstrap_interval(paired_values, int(fixed["bootstrap"]["draws"]), base_seed + 1)
        occupancy = {arm: arm_occupancy[arm] / 512 for arm in fixed["arms"]}
        admissible = (
            occupancy["near"] >= 0.90
            and occupancy["far"] >= 0.90
            and eligible_far >= 60
            and eligible_paired >= 60
        )
        rows.append(
            {
                "setting": setting,
                "mutation_rate": rate,
                "fixed_assurance": float(fixed["fixed_assurance"]),
                "founder_investment_mean": float(np.mean(founder_values)),
                "occupancy": occupancy,
                "eligible_histories_far": eligible_far,
                "eligible_histories_paired": eligible_paired,
                "admissible": admissible,
                "far_investment_change": {
                    "mean": float(far_values.mean()) if len(far_values) else None,
                    "bootstrap95": far_ci,
                },
                "far_minus_near_investment": {
                    "mean": float(paired_values.mean()) if len(paired_values) else None,
                    "bootstrap95": paired_ci,
                },
            }
        )
    return rows


def adjudicate(design: dict, sequence: list[dict], fixed: list[dict]) -> dict:
    primary = design["primary_cell"]
    seq = next(
        row
        for row in sequence
        if row["setting"] == primary["reproductive_setting"]
        and row["mutation_rate"] == float(primary["mutation_probability"])
        and row["threshold"] == float(design["sequence_campaign"]["primary_threshold"])
    )
    intervention = next(
        row
        for row in fixed
        if row["setting"] == primary["reproductive_setting"]
        and row["mutation_rate"] == float(primary["mutation_probability"])
    )
    sequence_success = (
        seq["assurance_first_proportion_all_histories"] > 0.5
        and seq["assurance_first_bootstrap95"][0] > 0.5
    )
    if not intervention["admissible"]:
        intervention_success = None
    else:
        far = intervention["far_investment_change"]
        pair = intervention["far_minus_near_investment"]
        intervention_success = (
            far["mean"] < 0
            and far["bootstrap95"][1] < 0
            and pair["mean"] < 0
            and pair["bootstrap95"][1] < 0
        )
    if intervention_success is None:
        status = "inconclusive"
    elif sequence_success and intervention_success:
        status = "confirmed"
    else:
        status = "not_confirmed"
    return {
        "status": status,
        "sequence_success": sequence_success,
        "fixed_assurance_success": intervention_success,
        "primary_sequence": seq,
        "primary_fixed_assurance": intervention,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--design", type=Path, required=True)
    parser.add_argument("--input-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    design = load_design(args.design)
    paths = verify_complete(args.input_root, args.design, design)
    sequence = sequence_readout(design, paths)
    fixed = fixed_readout(design, paths)
    adjudication = adjudicate(design, sequence, fixed)
    result = {
        "schema_version": "1.0",
        "status": "complete_confirmatory_readout",
        "design_sha256": hashlib.sha256(args.design.read_bytes()).hexdigest(),
        "declared_cases": len(paths),
        "independent_visitor_histories": 64,
        "nested_demographic_repeats": 8,
        "sequence": sequence,
        "fixed_assurance": fixed,
        "adjudication": adjudication,
        "claim_boundary": design["reporting_rules"],
    }
    if args.out.exists():
        raise ValueError("preserve existing confirmatory result")
    args.out.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps(adjudication, indent=2))


if __name__ == "__main__":
    main()
