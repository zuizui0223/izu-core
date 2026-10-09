"""Validate the *protocol only* for an independent founder/capacity intervention.

This module does not import any simulation runner and never produces plant
histories or future outcomes. It validates design declarations, not raw data.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "data/design/chapter2_orthogonal_founder_capacity_20261009.json"


def validate_protocol(path: Path = PROTOCOL) -> dict:
    d = json.loads(path.read_text(encoding="utf-8"))
    if d["status"] != "PRE_OUTCOME_PROTOCOL_ONLY_NOT_EXECUTABLE":
        raise AssertionError("Outcomes or executable protocol must not be silently substituted")
    old = d["originating_observation"]
    if not old["prior_outcomes_already_exposed"] or old["source_prs"] != [429, 430]:
        raise AssertionError("Existing outcome exposure and original PRs must be recorded")
    c = d["new_independent_cohort"]
    first, last, n = (c["visitor_history_first"], c["visitor_history_last"],
                      c["visitor_history_count"])
    if c["status"] != "UNGENERATED" or last - first + 1 != n or n != 64:
        raise AssertionError("New full cohort not prospectively declared")
    if not (c["each_history_fresh_prehistory_and_t400_genotypes"]
            and c["no_conditioning_on_t400_or_terminal_survival"]
            and c["all_stochastic_trajectories_including_extinction_admitted"]):
        raise AssertionError("Fresh selection-free prehistories required")
    for a, b in c["forbid_overlap_with_previous_history_ranges"]:
        if not (last < a or first > b):
            raise AssertionError("Previously exposed visitor histories overlap new range")

    arms = d["experimental_arms"]
    expected = {
        "eight_founders_capacity8": (8, "fixed_eight"),
        "eight_founders_capacity48": (48, "fixed_eight"),
        "all_available_founders_capacity48": (48, "full"),
    }
    if len(arms) != 3 or {a["name"] for a in arms} != set(expected):
        raise AssertionError("Exact three valid study arms required")
    if any((a["capacity"], a["founder_group"]) != expected[a["name"]]
           for a in arms):
        raise AssertionError("Founder/capacity assignments were changed")
    if (d["forbidden_arm"]["founder_count"],
            d["forbidden_arm"]["capacity"]) != (48, 8):
        raise AssertionError("Illegal F48/C8 arm must remain forbidden")

    rng = d["paired_future_randomness"]
    if not (rng["same_eight_founder_ids_across_capacity_arms"]
            and rng["same_random_stream_initialization_for_all_three_arms_and_both_viability_gates"]
            and {"regime_index", "viability_gate"}.issubset(
                set(rng["seed_must_not_include"].split(",") if isinstance(rng["seed_must_not_include"], str) else rng["seed_must_not_include"]))):
        raise AssertionError("Unpaired/unstable random-stream setup")
    gates = d["postzygotic_gates"]
    if [(x["name"], x["selfed_seed_retention"], x["outcrossed_seed_retention"])
            for x in gates] != [("baseline", 1, 1), ("self_half", 0.5, 1)]:
        raise AssertionError("Postzygotic factorial changed")

    g = d["complete_future_grid"]
    n_sources = n * len(g["reproductive_settings"]) * len(
        g["historical_environments"]) * len(g["assigned_expression_orders"]
        ) * g["nested_demographic_repeats"]
    branches = len(g["budgets"]) * len(g["future_visitor_environments"]
                ) * len(arms) * len(gates)
    if (n_sources, branches, n_sources * branches) != (
            g["n_prehistory_sources"], g["futures_per_source"],
            g["expected_future_records"]):
        raise AssertionError("Full-cohort source/future count mismatch")
    if (g["postshock_updates"] != 80
            or g["budgets"] != [0.5, 1, 2, 3, 4, 5, 8]):
        raise AssertionError("Frozen postshock horizon/budgets changed")

    e = d["estimands"]
    if (e["primary"] != "tau_eight_founders_capacity8_minus_tau_eight_founders_capacity48"
            or e["cluster_unit"] != "visitor_history"
            or e["cluster_bootstrap"] != {
                "draws": 9999, "seed": 2026100943,
                "interval": "percentile_two_sided_95",
                "resample": "64 paired visitor-history rows",
            } or e["primary_minimum_meaningful_absolute"] != 0.005
            or not e["no_interim_peeking_or_outcome_based_sample_size_change"]):
        raise AssertionError("Frozen primary estimand or inference changed")

    return {
        "status": d["status"],
        "new_independent_visitor_histories": n,
        "sources": n_sources,
        "futures_per_source": branches,
        "planned_futures": n_sources * branches,
        "production_executed": False,
    }


if __name__ == "__main__":
    print(json.dumps(validate_protocol(), ensure_ascii=False, sort_keys=True))
