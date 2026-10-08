"""Audited descriptive readout of the island-history transplant pilot.

Four independent visitor histories are far too few for confirmatory inference;
the report deliberately contains no confidence intervals or significance gates.
"""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import argparse
import hashlib
import json

from scripts.run_chapter2_island_history_transplant import (
    DESIGN_PATH, case_id, declared_groups, load_design,
)


def mean_or_none(values):
    clean = [float(v) for v in values if v is not None]
    return sum(clean) / len(clean) if clean else None


def investment(row, stage):
    traits = row[stage]["traits"]
    return None if traits is None else traits[1]


def paired_difference(left, right):
    return left - right if left is not None and right is not None else None


def read_cases(directory, d):
    records = {}
    for group in declared_groups(d):
        for post in d["post_environments"]:
            for mu in d["post_mutation_probabilities"]:
                cid = case_id(group, post, mu)
                p = directory / (cid + ".json")
                sha = directory / (cid + ".sha256")
                if not p.is_file() or not sha.is_file():
                    raise FileNotFoundError("missing case or receipt " + cid)
                actual = hashlib.sha256(p.read_bytes()).hexdigest()
                if actual != sha.read_text().strip():
                    raise ValueError("case receipt mismatch " + cid)
                row = json.loads(p.read_text(encoding="utf-8"))
                if row["case_id"] != cid or row["status"] != "exploratory_pilot_case":
                    raise ValueError("wrong case identity " + cid)
                records[cid] = row
    if len(records) != d["campaign"]["total_cases"]:
        raise ValueError("incomplete pilot")
    return records


def summarize(d, records):
    results = []
    for setting in d["settings"]:
        for mode in d["modes"]:
            for post in d["post_environments"]:
                for mu in d["post_mutation_probabilities"]:
                    history_end = []
                    history_response = []
                    history_immediate = []
                    occupied = []
                    total_eligible_repeats = 0
                    for h in d["visitor_history_seeds"]:
                        repeat_end = []
                        repeat_response = []
                        repeat_immediate = []
                        for rep in d["demographic_repeat_seeds"]:
                            near = records[case_id((setting, h, rep, mode, "near"), post, mu)]
                            far = records[case_id((setting, h, rep, mode, "far"), post, mu)]
                            occupied.extend([int(near["end"]["count"] > 0),
                                             int(far["end"]["count"] > 0)])
                            en = paired_difference(investment(far, "end"),
                                                   investment(near, "end"))
                            sn = paired_difference(investment(far, "switch"),
                                                   investment(near, "switch"))
                            repeat_end.append(en)
                            repeat_response.append(paired_difference(en, sn))
                            fv = far["immediate_post_switch_reproduction"]["maternal_viable_per_plant"]
                            nv = near["immediate_post_switch_reproduction"]["maternal_viable_per_plant"]
                            repeat_immediate.append(paired_difference(fv, nv))
                            total_eligible_repeats += int(en is not None)
                        # The visitor history, not the nested demographic repeat,
                        # is the independent ecological unit.
                        history_end.append(mean_or_none(repeat_end))
                        history_response.append(mean_or_none(repeat_response))
                        history_immediate.append(mean_or_none(repeat_immediate))
                    results.append({
                        "setting": setting, "assurance_mode": mode,
                        "post_environment": post, "post_mutation_probability": mu,
                        "independent_histories": len(d["visitor_history_seeds"]),
                        "nested_pairs": len(d["visitor_history_seeds"]) * len(d["demographic_repeat_seeds"]),
                        "end_investment_far_history_minus_near_history": mean_or_none(history_end),
                        "post_response_far_history_minus_near_history": mean_or_none(history_response),
                        "immediate_maternal_viable_far_history_minus_near_history": mean_or_none(history_immediate),
                        "eligible_history_means": sum(v is not None for v in history_end),
                        "eligible_end_pairs": total_eligible_repeats,
                        "occupied_terminal_cases": sum(occupied),
                        "total_terminal_cases": len(occupied),
                    })
    # An explicit 0 versus 0.01 post-mutation contrast holds the same
    # switch population and post-visitor history fixed.
    mutation_rows = []
    for setting in d["settings"]:
        for mode in d["modes"]:
            for pre in d["pre_environments"]:
                for post in d["post_environments"]:
                    paired = []
                    identical_switches = 0
                    for h in d["visitor_history_seeds"]:
                        for rep in d["demographic_repeat_seeds"]:
                            group = (setting, h, rep, mode, pre)
                            zero = records[case_id(group, post, 0)]
                            positive = records[case_id(group, post, 0.01)]
                            if zero["switch_genetic_snapshot_sha256"] != positive["switch_genetic_snapshot_sha256"]:
                                raise AssertionError("forked genetic snapshot is not identical")
                            identical_switches += 1
                            paired.append(paired_difference(investment(positive, "end"),
                                                            investment(zero, "end")))
                    mutation_rows.append({
                        "setting": setting, "assurance_mode": mode,
                        "pre_environment": pre, "post_environment": post,
                        "identical_switch_pairs": identical_switches,
                        "post_mutation_effect_on_end_investment": mean_or_none(paired),
                        "eligible_pairs": sum(v is not None for v in paired),
                    })
    return {
        "status": "completed_exploratory_screen_not_confirmatory",
        "design_sha256": hashlib.sha256(DESIGN_PATH.read_bytes()).hexdigest(),
        "source": "512 hash-verified pilot cases",
        "independent_visitor_histories": len(d["visitor_history_seeds"]),
        "nested_demographic_repeats": len(d["demographic_repeat_seeds"]),
        "ecological_contrast": results, "post_mutation_contrast": mutation_rows,
        "claim_boundary": [
            "No significance, journal gate or empirical island validation",
            "No direct manipulation of evolutionary temporal order",
            "Effects involving surviving trait endpoints are survivor-conditioned",
            "Immediate viable maternal output is not long-term population persistence",
            "No new result replaces the prospectively confirmed four-setting campaign",
        ],
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    d, _ = load_design()
    result = summarize(d, read_cases(a.input, d))
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"],
                      "case_count": d["campaign"]["total_cases"],
                      "comparison_rows": len(result["ecological_contrast"])}))


if __name__ == "__main__":
    main()
