"""Mutation-access timing is a controlled ABM intervention, not enforced trait order."""
import json
from itertools import product
from pathlib import Path
import numpy as np

from scripts.run_chapter2_island_mutational_priority_pilot import (
    groups, load_pilot, founders_zero_standing, simulate_group
)

ROOT = Path(__file__).resolve().parents[1]


def test_pilot_has_four_settings_and_two_controls_without_retuning():
    d, source = load_pilot()
    assert len(groups(d)) == 256
    assert set(d["schedules"]) == {
        "assurance_first", "investment_first", "both_early", "both_delayed"
    }
    assert set(d["settings"]) == set(source["settings"])
    assert d["post_ovule_budgets"] == [2, 3, 4, 5]
    state = founders_zero_standing(source)
    assert np.all(state.alleles[:, 1:3, :] == 0.5)
    assert np.var(state.alleles[:, 0, :]) > 0


def test_live_model_locked_traits_acquire_no_variation_before_release():
    d, source = load_pilot()
    g = groups(d)[0]
    r = simulate_group(g, d, source)
    assert r["group"] == g
    assert r["mid"]["allele_variance"][1] == 0
    assert r["mid"]["means"][1] == 0.5
    assert len(r["post_cases"]) == 8
    assert {(x["post"], x["budget"]) for x in r["post_cases"]} == set(product(
        d["post_visitor_environments"], d["post_ovule_budgets"]
    ))
    inverse = tuple(list(g[:4]) + ["investment_first"])
    q = simulate_group(inverse, d, source)
    assert q["mid"]["allele_variance"][2] == 0
    assert q["mid"]["means"][2] == 0.5
    assert all(x["occupied"] == int(x["end_n"] > 0) for x in q["post_cases"])


def test_exploratory_result_keeps_sign_heterogeneity_and_no_confirmatory_claim():
    result = json.loads((ROOT /
        "data/results/chapter2_island_mutational_priority_pilot_20261008.json"
    ).read_text())
    assert result["status"].startswith("completed_exploratory")
    assert result["independent_visitor_histories"] == 4
    assert result["poststress_trajectories"] == 2048
    assert result["locked_locus_checks_passed"] == 256
    rows = {x["setting"]: x for x in result["settings"]}
    assert rows["prior_selfing"]["priority_interaction"] > 0
    assert rows["pollen_discount"]["priority_interaction"] < 0
    assert rows["delayed_control"]["priority_interaction"] > 0
    assert rows["assurance_cost"]["priority_interaction"] < 0
    assert any("temporal" in x.lower() or "order" in x.lower()
               for x in result["bounds"])


def test_independent16_randomization_is_new_and_contrast_is_locked():
    d, _ = load_pilot()
    new = json.loads((ROOT /
        "data/design/chapter2_island_mutational_priority_independent16_20261008.json"
    ).read_text())
    assert new["status"] == "frozen_before_independent_16history_mutational_priority_execution"
    assert new["declared_prehistory_groups"] == 512
    assert new["declared_post_stress_cases"] == 4096
    assert new["bootstrap"]["unit"] == "visitor_history"
    assert new["bootstrap"]["draws"] == 9999
    hist = range(new["new_history_seeds"]["first"],
                 new["new_history_seeds"]["last"] + 1)
    assert len(hist) == 16
    assert not (set(hist) & set(d["new_visitor_history_seeds"]))
    assert "prior_selfing" in new["primary_estimand"]
    assert "pollen_discount" in new["primary_estimand"]



def test_failed_independent16_is_retained_and_cannot_be_promoted():
    d = json.loads((ROOT /
        "data/results/chapter2_island_mutational_priority_independent16_20261008.json"
    ).read_text())
    primary = d["frozen_primary"]
    assert d["n_independent_histories"] == 16
    assert d["poststress_cases"] == 4096
    assert primary["passed"] is False
    assert primary["mean"] == -0.0859375
    assert primary["bootstrap95"][0] < 0 < primary["bootstrap95"][1]
    assert len(d["per_setting"]) == 4
    assert all(a["bootstrap95"][0] <= 0 <= a["bootstrap95"][1]
               for a in d["per_setting"])


def test_balanced_schedule_has_equal_mutational_supply_and_no_promoted_gate():
    from scripts.run_chapter2_island_mutational_priority_balanced import (
        load_balanced, declared_groups
    )
    p, d, _ = load_balanced()
    assert p["status"] == "balanced_mutational_opportunity_exploratory_before_execution"
    assert len(declared_groups(d)) == 256
    assert p["mutation_access_generations_per_trait"] == 250
    for name, masks in p["schedules"].items():
        for locus in (1, 2):
            assert sum(length * int(mask[locus]) for length, mask in
                       zip((150, 150, 100), masks)) == 250
    record = json.loads((ROOT /
        "data/results/chapter2_island_mutational_priority_balanced_20261008.json"
    ).read_text())
    assert record["independent_histories"] == 4
    assert record["pooled_descriptive_priority_interaction"] == 0.0
    assert len(record["per_setting"]) == 4
    assert any(r["priority_interaction"] < 0 for r in record["per_setting"])
    assert any(r["priority_interaction"] > 0 for r in record["per_setting"])
