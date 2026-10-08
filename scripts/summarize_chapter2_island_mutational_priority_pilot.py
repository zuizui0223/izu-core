"""Audit all mutational-priority pilot cells; descriptive history-level contrasts only."""
from __future__ import annotations
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np

from scripts.run_chapter2_island_mutational_priority_pilot import groups, load_pilot


def analyze(d, rows):
    expected = set(groups(d))
    actual = {tuple(row["group"]) for row in rows}
    if len(rows) != len(expected) or actual != expected:
        raise ValueError("incomplete or duplicate historical groups")
    expected_stress = set(product(
        d["post_visitor_environments"], d["post_ovule_budgets"]
    ))
    by = {}
    for row in rows:
        g = tuple(row["group"])
        if row["mid"] is None or row["end_pre"] is None or row["post_cases"] is None:
            raise ValueError("undefined historical endpoint " + str(g))
        observed_stress = {(x["post"], x["budget"]) for x in row["post_cases"]}
        if observed_stress != expected_stress or len(row["post_cases"]) != 8:
            raise ValueError("incomplete postshock grid " + str(g))
        for k in (1, 2):
            mask = d["schedules"][g[-1]]["phase1_mutation_mask"]
            if not mask[k] and (abs(row["mid"]["means"][k] - 0.5) > 1e-12
                                or abs(row["mid"]["allele_variance"][k]) > 1e-12):
                raise AssertionError("locked mutational state drifted " + str(g))
        by[g] = row

    settings = d["settings"]
    histories = d["new_visitor_history_seeds"]
    repeats = d["nested_demographic_repeat_seeds"]
    schedules = tuple(d["schedules"])
    historical_rows = []
    summaries = []
    for setting in settings:
        values = []
        for h in histories:
            record = {"setting": setting, "history": h, "schedules": {}}
            for schedule in schedules:
                arms = {}
                for pre in d["pre_visitor_environments"]:
                    groups_for_arm = [
                        by[(setting, h, rep, pre, schedule)] for rep in repeats
                    ]
                    arms[pre] = {
                        "occupancy": float(np.mean([
                            z["occupied"] for r in groups_for_arm
                            for z in r["post_cases"]
                        ])),
                        "initial_viability": float(np.mean([
                            z["initial_viable"] for r in groups_for_arm
                            for z in r["post_cases"]
                        ])),
                        "end_investment": float(np.mean([
                            r["end_pre"]["means"][1] for r in groups_for_arm
                        ])),
                        "end_assurance": float(np.mean([
                            r["end_pre"]["means"][2] for r in groups_for_arm
                        ])),
                    }
                record["schedules"][schedule] = {
                    "arms": arms,
                    "far_minus_near_occupancy": (
                        arms["far"]["occupancy"] - arms["near"]["occupancy"]
                    ),
                }
            record["priority_interaction"] = (
                record["schedules"]["assurance_first"]["far_minus_near_occupancy"]
                - record["schedules"]["investment_first"]["far_minus_near_occupancy"]
            )
            values.append(record["priority_interaction"])
            historical_rows.append(record)

        summaries.append({
            "setting": setting, "independent_histories": len(histories),
            "nested_demographic_repeats": len(repeats),
            "priority_interaction_mean": float(np.mean(values)),
            "history_interactions": values,
            "sign_counts": {
                "positive": sum(v > 0 for v in values),
                "negative": sum(v < 0 for v in values),
                "zero": sum(v == 0 for v in values),
            },
            "schedules": {
                schedule: {
                    "far_minus_near_occupancy": float(np.mean([
                        r["schedules"][schedule]["far_minus_near_occupancy"]
                        for r in historical_rows if r["setting"] == setting
                    ])),
                    "near_occupancy": float(np.mean([
                        r["schedules"][schedule]["arms"]["near"]["occupancy"]
                        for r in historical_rows if r["setting"] == setting
                    ])),
                    "far_occupancy": float(np.mean([
                        r["schedules"][schedule]["arms"]["far"]["occupancy"]
                        for r in historical_rows if r["setting"] == setting
                    ])),
                } for schedule in schedules
            },
        })
    return {
        "status": "completed_exploratory_mutational_priority_not_confirmatory",
        "n_independent_visitor_histories": len(histories),
        "n_nested_demographic_repeats": len(repeats),
        "n_prehistory_groups": len(rows),
        "n_poststress_trajectories": 8 * len(rows),
        "locked_group_checks_passed": len(rows),
        "pooled_priority_mean_descriptive": float(np.mean([
            r["priority_interaction"] for r in historical_rows
        ])),
        "per_setting": summaries,
        "per_history": historical_rows,
        "boundaries": [
            "Mutation availability timing is not an intervention on observed phenotypic trait-change order.",
            "Early-access traits have more time for mutation and selection.",
            "I/A founder standing variation was reset; results are not numerically comparable to older persistence trajectories.",
            "Four independent visitor histories do not support confirmatory inference.",
            "The small-population stress grid was chosen using prior exploratory history."
        ],
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--shard-count", type=int, default=4)
    args = p.parse_args()
    d, _ = load_pilot()
    rows = []
    receipts = {}
    for shard in range(args.shard_count):
        path = args.input / f"priority_shard_{shard:02d}.json"
        raw = path.read_bytes()
        receipts[path.name] = hashlib.sha256(raw).hexdigest()
        rows.extend(json.loads(raw))
    result = analyze(d, rows)
    result["source_shard_sha256"] = receipts
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({
        "status": result["status"],
        "groups": result["n_prehistory_groups"],
        "poststress": result["n_poststress_trajectories"],
        "pooled_priority": result["pooled_priority_mean_descriptive"],
    }))


if __name__ == "__main__":
    main()
