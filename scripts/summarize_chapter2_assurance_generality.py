"""Summarize and adjudicate the frozen four-setting assurance generality campaign."""
from __future__ import annotations

from pathlib import Path
import argparse
import hashlib
import json

import numpy as np

from scripts.run_chapter2_assurance_generality import (
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
    if len(markers) != 32:
        raise ValueError(f"incomplete campaign: expected 32 shard markers, found {len(markers)}")
    design_sha = hashlib.sha256(design_path.read_bytes()).hexdigest()
    keys = []
    for marker in markers:
        row = json.loads(marker.read_text(encoding="utf-8"))
        if row["status"] != "completed" or row["shard_count"] != 32:
            raise ValueError(f"invalid shard marker {marker}")
        if row["design_sha256"] != design_sha:
            raise ValueError(f"design mismatch {marker}")
        keys.extend(row["keys"])
    if len(keys) != 8448 or len(set(keys)) != 8448 or set(keys) != set(expected):
        raise ValueError("declared 8448-case campaign is incomplete or mismatched")
    paths = {}
    for key, task in expected.items():
        path = find_case(root, key)
        receipt = json.loads(path.with_suffix(".json").read_text(encoding="utf-8"))
        if receipt["task"] != list(task):
            raise ValueError(f"task mismatch {key}")
        if hashlib.sha256(path.read_bytes()).hexdigest() != receipt["sha256"]:
            raise ValueError(f"hash mismatch {key}")
        paths[key] = path
    return paths


def load_endpoint(paths: dict[str, Path], task: tuple) -> tuple[bool, float, float]:
    key = case_key(task)
    with np.load(paths[key]) as z:
        trace = z["trace"]
        if trace.shape != (1001, 10):
            raise ValueError((key, trace.shape))
        founder = float(trace[0, 2])
        alive = bool(trace[1000, 0] > 0)
        endpoint = float(trace[1000, 2]) if alive else float("nan")
    return alive, founder, endpoint


def bootstrap_interval(values: list[float], draws: int, seed: int) -> list[float]:
    x = np.asarray(values, dtype=float)
    x = x[np.isfinite(x)]
    if not len(x):
        return [float("nan"), float("nan")]
    index = np.random.default_rng(seed).integers(0, len(x), size=(draws, len(x)))
    boot = x[index].mean(axis=1)
    return [float(v) for v in np.quantile(boot, [0.025, 0.975])]


def structural_control(design: dict, paths: dict[str, Path]) -> dict:
    histories, repeats = seed_ranges(design)
    control = design["structural_control"]
    histories = list(histories)[: int(control["history_count"])]
    repeats = list(repeats)[: int(control["repeat_count"])]
    rate = float(control["mutation_probability"])
    checked = 0
    mismatches = []
    for setting in design["settings"]:
        for seed in histories:
            for rep in repeats:
                for arm in control["arms"]:
                    fixed_task = ("structural", setting, rate, seed, rep, arm, "fixed")
                    evolving_task = ("structural", setting, rate, seed, rep, arm, "evolving")
                    with np.load(paths[case_key(fixed_task)]) as f, np.load(paths[case_key(evolving_task)]) as e:
                        same = np.array_equal(f["trace"], e["trace"], equal_nan=True)
                    checked += 1
                    if not same:
                        mismatches.append(
                            {"setting": setting, "history_seed": seed, "repeat_seed": rep, "arm": arm}
                        )
    return {
        "status": "passed" if not mismatches else "failed",
        "matched_pairs_checked": checked,
        "mismatches": mismatches,
    }


def setting_readout(design: dict, paths: dict[str, Path], setting: str, setting_index: int) -> dict:
    histories, repeats = seed_ranges(design)
    main = design["main_campaign"]
    rate = float(main["mutation_probability"])
    occupancy_counts = {
        mode: {arm: 0 for arm in main["arms"]}
        for mode in main["modes"]
    }
    fixed_history = []
    evolving_history = []
    interaction_history = []
    fixed_far_change_history = []
    eligible_fixed = 0
    eligible_interaction = 0
    eligible_fixed_far = 0

    for seed in histories:
        fixed_pairs = []
        evolving_pairs = []
        interaction_pairs = []
        fixed_far_changes = []
        for rep in repeats:
            rows = {}
            for mode in main["modes"]:
                for arm in main["arms"]:
                    task = ("main", setting, rate, seed, rep, arm, mode)
                    rows[(mode, arm)] = load_endpoint(paths, task)
                    if rows[(mode, arm)][0]:
                        occupancy_counts[mode][arm] += 1

            fnear = rows[("fixed", "near")]
            ffar = rows[("fixed", "far")]
            enear = rows[("evolving", "near")]
            efar = rows[("evolving", "far")]

            if ffar[0]:
                fixed_far_changes.append(ffar[2] - ffar[1])
            if fnear[0] and ffar[0]:
                fixed_pairs.append(ffar[2] - fnear[2])
            if enear[0] and efar[0]:
                evolving_pairs.append(efar[2] - enear[2])
            if fnear[0] and ffar[0] and enear[0] and efar[0]:
                fixed_diff = ffar[2] - fnear[2]
                evolving_diff = efar[2] - enear[2]
                interaction_pairs.append(evolving_diff - fixed_diff)

        if fixed_far_changes:
            fixed_far_change_history.append(float(np.mean(fixed_far_changes)))
            eligible_fixed_far += 1
        if fixed_pairs:
            fixed_history.append(float(np.mean(fixed_pairs)))
            eligible_fixed += 1
        if evolving_pairs:
            evolving_history.append(float(np.mean(evolving_pairs)))
        if interaction_pairs:
            interaction_history.append(float(np.mean(interaction_pairs)))
            eligible_interaction += 1

    draws = int(design["bootstrap"]["draws"])
    base_seed = int(design["bootstrap"]["seed"]) + 1000 * setting_index
    fixed_ci = bootstrap_interval(fixed_history, draws, base_seed + 1)
    evolving_ci = bootstrap_interval(evolving_history, draws, base_seed + 2)
    interaction_ci = bootstrap_interval(interaction_history, draws, base_seed + 3)
    far_change_ci = bootstrap_interval(fixed_far_change_history, draws, base_seed + 4)
    occupancy = {
        mode: {arm: occupancy_counts[mode][arm] / 512 for arm in main["arms"]}
        for mode in main["modes"]
    }
    adm = design["admissibility"]
    admissible = (
        all(v >= float(adm["minimum_arm_occupancy"]) for m in occupancy.values() for v in m.values())
        and eligible_fixed >= int(adm["minimum_eligible_histories"])
        and eligible_interaction >= int(adm["minimum_eligible_histories"])
    )
    fixed_mean = float(np.mean(fixed_history)) if fixed_history else None
    evolving_mean = float(np.mean(evolving_history)) if evolving_history else None
    interaction_mean = float(np.mean(interaction_history)) if interaction_history else None
    far_change_mean = float(np.mean(fixed_far_change_history)) if fixed_far_change_history else None
    passed = (
        admissible
        and fixed_mean is not None
        and interaction_mean is not None
        and fixed_mean < 0
        and fixed_ci[1] < 0
        and interaction_mean > 0
        and interaction_ci[0] > 0
    )
    return {
        "setting": setting,
        "role": design["settings"][setting]["role"],
        "mutation_rate": rate,
        "occupancy": occupancy,
        "eligible_histories_fixed_far": eligible_fixed_far,
        "eligible_histories_fixed_pair": eligible_fixed,
        "eligible_histories_four_cell": eligible_interaction,
        "admissible": admissible,
        "fixed_far_change_from_founders": {
            "mean": far_change_mean,
            "bootstrap95": far_change_ci,
        },
        "fixed_far_minus_near": {
            "mean": fixed_mean,
            "bootstrap95": fixed_ci,
        },
        "evolving_far_minus_near": {
            "mean": evolving_mean,
            "bootstrap95": evolving_ci,
        },
        "attenuation_evolving_minus_fixed": {
            "mean": interaction_mean,
            "bootstrap95": interaction_ci,
        },
        "passes_frozen_rule": passed,
    }


def adjudicate(design: dict, rows: list[dict], structural: dict) -> dict:
    if structural["status"] != "passed":
        return {
            "status": "invalid_structural_control",
            "passed_settings": [],
            "n_passed": 0,
            "journal_route": "No biological adjudication; implementation control failed.",
        }
    passed = [r["setting"] for r in rows if r["passes_frozen_rule"]]
    if len(passed) == 4:
        status = "all_four_confirmed"
        route = "Ecology Letters first; Journal of Ecology backup."
    elif len(passed) > 0:
        status = "partial_generality"
        route = "Journal of Ecology first; attenuation remains setting-dependent secondary evidence."
    else:
        status = "generality_not_confirmed"
        route = "Journal of Ecology first; retain the existing necessity claim only."
    return {
        "status": status,
        "passed_settings": passed,
        "n_passed": len(passed),
        "journal_route": route,
        "frozen_rule": design["frozen_success_rule"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--design", type=Path, required=True)
    parser.add_argument("--input-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    design = load_design(args.design)
    paths = verify_complete(args.input_root, args.design, design)
    structural = structural_control(design, paths)
    rows = [
        setting_readout(design, paths, setting, i)
        for i, setting in enumerate(design["settings"])
    ]
    adjudication = adjudicate(design, rows, structural)
    result = {
        "schema_version": "1.0",
        "date": "2026-10-06",
        "status": "complete_generality_readout",
        "design_sha256": hashlib.sha256(args.design.read_bytes()).hexdigest(),
        "declared_cases": len(paths),
        "independent_visitor_histories": 64,
        "nested_demographic_repeats": 8,
        "structural_control": structural,
        "settings": rows,
        "adjudication": adjudication,
        "claim_boundary": design["reporting_rules"],
    }
    if args.out.exists():
        raise ValueError("preserve existing generality result")
    args.out.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps(adjudication, indent=2))


if __name__ == "__main__":
    main()
