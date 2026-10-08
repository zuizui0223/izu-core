"""Audit whether mutational-access timing actually changed phenotypic order.

The ordering rule is the *first* recorded generation at which a population
mean differs >= 0.05 from its initial value 0.5. A single trait crossing is
reported separately from two-trait precedence; never interpret the finite
threshold as onset of selection or an intervention directly on phenotype.

This is an exploratory compliance diagnostic, NOT a survival causal estimate.
"""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import argparse
import json

from scripts.run_chapter2_island_mutational_priority_balanced import (
    load_balanced, declared_groups
)
from scripts.run_chapter2_island_mutational_priority_independent16 import (
    load_followup, tasks
)


def order(first_hit):
    a = first_hit["assurance"]
    i = first_hit["investment"]
    if a is None and i is None:
        return "neither"
    if a is None:
        return "I_only"
    if i is None:
        return "A_only"
    if a < i:
        return "A_before_I"
    if i < a:
        return "I_before_A"
    return "tie"


def audit(variant, rows):
    if variant == "balanced":
        _protocol, d, _source = load_balanced()
        expected = declared_groups(d)
        n_histories = len(d["new_visitor_history_seeds"])
    elif variant == "independent16":
        _protocol, d, _source = load_followup()
        expected = tasks(d)
        n_histories = len(d["new_visitor_history_seeds"])
    else:
        raise ValueError("unknown order variant")
    actual = [tuple(row["group"]) for row in rows]
    if len(actual) != len(expected) or set(actual) != set(expected):
        raise ValueError("missing or duplicated historical groups")
    results = []
    for setting in d["settings"]:
        for schedule in d["schedules"]:
            chosen = [
                row for row in rows
                if row["group"][0] == setting and row["group"][-1] == schedule
            ]
            count = Counter(order(row["first_hit"]) for row in chosen)
            # Mutation access does not imply that BOTH traits cross. Preserve
            # one-trait-only and never-crossed cases in the denominator.
            n = len(chosen)
            expected_n = (n_histories * len(d["nested_demographic_repeat_seeds"])
                          * len(d["pre_visitor_environments"]))
            if n != expected_n:
                raise AssertionError("unbalanced historical group count")
            results.append({
                "setting": setting, "schedule": schedule,
                "historical_groups": n,
                "A_before_I": count["A_before_I"],
                "I_before_A": count["I_before_A"],
                "A_only": count["A_only"], "I_only": count["I_only"],
                "tie": count["tie"], "neither": count["neither"],
                "mean_final_A": sum(
                    row["end_pre"]["means"][2] for row in chosen
                ) / n,
                "mean_final_I": sum(
                    row["end_pre"]["means"][1] for row in chosen
                ) / n,
            })
    pooled = {}
    for schedule in d["schedules"]:
        items = [x for x in results if x["schedule"] == schedule]
        by_order = {
            k: sum(row[k] for row in items)
            for k in ("A_before_I", "I_before_A", "A_only", "I_only", "tie", "neither")
        }
        n = sum(row["historical_groups"] for row in items)
        assigned = (by_order["A_before_I"] + by_order["A_only"]
                    if schedule == "assurance_first"
                    else by_order["I_before_A"] + by_order["I_only"]
                    if schedule == "investment_first" else None)
        pooled[schedule] = {
            "historical_groups": n,
            **by_order,
            "intended_trait_preceded_or_only": assigned,
            "descriptive_fraction": assigned / n if assigned is not None else None,
        }
        if sum(by_order.values()) != n:
            raise ArithmeticError("order accounting does not sum to n")
    return {
        "status": "post_outcome_exploratory_order_compliance_not_confirmation",
        "variant": variant, "independent_visitor_histories": n_histories,
        "threshold": "first absolute population mean departure >=0.05 from initial 0.5",
        "setting_by_schedule": results, "pooled_by_schedule": pooled,
        "inference_limit": [
            "Historical groups include shared visitor histories, two pre-pollination arms and sometimes nested demographic repeats.",
            "A_only/I_only are one-trait crossings, not evidence the other trait never experiences selection.",
            "Mutational-access timing changes exposure to mutation and the selection time available after first emergence.",
            "Observing an order difference does not establish a corresponding survival consequence.",
            "The independent16 survival sign-contrast failed its frozen bootstrap gate; balanced n=4 had zero pooled effect."
        ],
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--variant", choices=("independent16", "balanced"), required=True)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--shard-count", type=int, default=4)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    prefix = ("priority_independent16_shard" if a.variant == "independent16"
              else "priority_balanced_shard")
    rows = []
    for i in range(a.shard_count):
        rows.extend(json.loads(
            (a.input / f"{prefix}_{i:02d}.json").read_text()
        ))
    result = audit(a.variant, rows)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({
        "variant": a.variant,
        "pools": result["pooled_by_schedule"]
    }))


if __name__ == "__main__":
    main()
