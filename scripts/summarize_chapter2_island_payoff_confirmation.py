"""Apply the exact frozen 5-criterion 64-history payoff confirmation gate.

Every 1,024 paired cases and their SHA receipts must be present. Means and
bootstrap resamples are computed over 64 independent visitor histories, after
averaging the two nested demographic repeats. Inadmissible cases are reported
as null, never filled with zero.
"""
from __future__ import annotations
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json

import numpy as np
from scripts.run_chapter2_island_payoff_confirmation import (
    DESIGN, case_key, groups, load_frozen,
)


def load_verified(directory, d):
    data = {}
    for g in groups(d):
        name = case_key(g)
        p = directory / (name + ".json")
        receipt = directory / (name + ".sha256")
        if not p.exists() or not receipt.exists():
            raise FileNotFoundError("missing paired case " + name)
        contents = p.read_bytes()
        if hashlib.sha256(contents).hexdigest() != receipt.read_text().strip():
            raise AssertionError("case checksum mismatch " + name)
        row = json.loads(contents)
        if tuple(row["group"]) != tuple(g):
            raise AssertionError("case identity mismatch " + name)
        data[tuple(g)] = row
    if len(data) != d["group_pairs"]:
        raise AssertionError("confirmation incomplete")
    return data


def independent_history_summary(d, cases):
    histories = list(range(d["visitor_history_seeds"]["first"],
                           d["visitor_history_seeds"]["last"] + 1))
    repeats = list(range(d["nested_demographic_repeats"]["first"],
                           d["nested_demographic_repeats"]["last"] + 1))
    rng = np.random.default_rng(d["bootstrap"]["seed"])
    indexes = rng.integers(0, len(histories), size=(
        d["bootstrap"]["draws"], len(histories)
    ))
    settings = d["settings"]
    modes = d["assurance_modes"]
    metrics = ("viable_maternal", "female_outcross", "pollen_export")
    table = []
    for setting, mode in product(settings, modes):
        for metric in metrics:
            history_means = []
            history_eligible = 0
            n_seen_near = n_seen_far = n_occupied_near = n_occupied_far = 0
            for history in histories:
                vals = []
                for rep in repeats:
                    row = cases[setting, history, rep, mode]
                    n_seen_near += int(metric == "viable_maternal")
                    n_seen_far += int(metric == "viable_maternal")
                    n_occupied_near += int(metric == "viable_maternal" and row["near_population"] > 0)
                    n_occupied_far += int(metric == "viable_maternal" and row["far_population"] > 0)
                    if row["admissible"]:
                        vals.append(row["observed_far_minus_near"][metric])
                if len(vals) == len(repeats):
                    history_means.append(float(np.mean(vals)))
                    history_eligible += 1
                else:
                    history_means.append(None)
            valid = np.array([x for x in history_means if x is not None], dtype=float)
            eligible = len(valid)
            admission = eligible >= d["admission"]["minimum_complete_independent_histories"]
            if eligible == len(histories):
                boot = valid[indexes].mean(axis=1)
            elif eligible >= d["admission"]["minimum_complete_independent_histories"]:
                # Conditional survivor analysis, explicitly labelled by the
                # eligible history count. Never fill extinction endpoints with 0.
                local_rng = np.random.default_rng(
                    d["bootstrap"]["seed"] + settings.index(setting) * 10
                    + modes.index(mode) * 3 + metrics.index(metric)
                )
                valid_draws = local_rng.integers(
                    0, eligible, size=(d["bootstrap"]["draws"], eligible)
                )
                boot = valid[valid_draws].mean(axis=1)
            else:
                boot = None
            mean = float(valid.mean()) if eligible else None
            interval = [float(x) for x in np.percentile(boot, [2.5, 97.5])] if boot is not None else None
            occupancy_ok = (
                n_occupied_near / n_seen_near >= d["admission"]["minimum_terminal_occupancy_per_cell"]
                and n_occupied_far / n_seen_far >= d["admission"]["minimum_terminal_occupancy_per_cell"]
            )
            table.append({
                "setting": setting, "mode": mode, "metric": metric,
                "independent_histories": len(histories),
                "eligible_complete_histories": eligible,
                "admissible": admission and occupancy_ok and interval is not None,
                "mean": mean, "bootstrap95": interval,
                "history_positive_count": int((valid > 0).sum()),
                "history_negative_count": int((valid < 0).sum()),
                "occupancy_near": (n_occupied_near / n_seen_near if n_seen_near else None),
                "occupancy_far": (n_occupied_far / n_seen_far if n_seen_far else None),
            })
    return table


def decide(d, table):
    tests = [
        ("prior_selfing", "evolving", "viable_maternal", 1),
        ("pollen_discount", "evolving", "viable_maternal", 1),
        ("assurance_cost", "evolving", "viable_maternal", -1),
        ("prior_selfing", "evolving", "female_outcross", -1),
        ("pollen_discount", "evolving", "female_outcross", -1),
    ]
    decision = []
    for setting, mode, metric, sign in tests:
        row = next(x for x in table if (x["setting"], x["mode"], x["metric"])
                   == (setting, mode, metric))
        passed = bool(row["admissible"] and row["mean"] is not None
                      and row["bootstrap95"] is not None
                      and (sign * row["mean"] > 0)
                      and (sign * row["bootstrap95"][0 if sign == 1 else 1] > 0))
        decision.append({
            "setting": setting, "mode": mode, "metric": metric,
            "expected_sign": "positive" if sign == 1 else "negative",
            "passes_frozen_rule": passed,
        })
    return {
        "status": "all_five_confirmed" if all(x["passes_frozen_rule"] for x in decision)
                  else "at_least_one_frozen_rule_failed",
        "n_passed": sum(x["passes_frozen_rule"] for x in decision),
        "checks": decision,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    d, _ = load_frozen()
    cases = load_verified(a.input, d)
    table = independent_history_summary(d, cases)
    judgement = decide(d, table)
    result = {
        "status": "complete_independent_payoff_confirmation_readout",
        "frozen_design_sha256": hashlib.sha256(DESIGN.read_bytes()).hexdigest(),
        "n_paired_groups": len(cases),
        "n_prehistories": d["prehistories_cases"],
        "independent_visitor_histories": 64,
        "nested_demographic_repeats": 2,
        "readout": table,
        "adjudication": judgement,
        "claim_boundaries": [
            "No natural island calibration", "No direct temporal-order intervention",
            "No post-switch long-term population rescue observation",
            "No inference on evolutionary fitness from maternal output alone",
            "Four-setting PR411 results are unchanged",
        ],
    }
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps(judgement))


if __name__ == "__main__":
    main()
