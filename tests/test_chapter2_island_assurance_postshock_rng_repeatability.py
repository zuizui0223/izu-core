"""Protect nested-RNG residual analysis from pseudo-replication and mediation claims."""
import json
from itertools import product
from pathlib import Path

from scripts.run_chapter2_island_assurance_postshock_rng_repeatability import (
    load_design, declared_groups, simulate_pair
)
from scripts.summarize_chapter2_island_assurance_postshock_rng_repeatability import (
    analyze
)

ROOT = Path(__file__).resolve().parents[1]


def test_frozen_design_reuses_four_histories_but_has_eight_new_post_rng_streams():
    d, parent, biology, source = load_design()
    assert len(declared_groups(d)) == 16
    assert d["historical_visitor_seeds"] == [35100801,35100802,35100803,35100804]
    assert parent["demographic_repeat_seed"] == 35101801
    assert len(d["new_postshock_demographic_repeat_ids"]) == 8
    assert d["n_postshock_trajectories"] == 2048
    assert d["post_ovule_budgets"] == [3.0,4.0]
    assert d["settings"] == list(source["settings"])


def test_live_short_plant_reproduction_preserves_matched_rng_treatments():
    d, parent, biology, source = load_design()
    short = {**d, "post_updates": 2,
             "new_postshock_demographic_repeat_ids": [0,1]}
    setting, history = declared_groups(d)[0]
    rows = simulate_pair((setting, history), short, parent, biology, source)
    assert len(rows) == 32
    assert set(x["variant"] for x in rows) == {
        "full_donor", "recipient_mean_target"
    }
    assert all(x["occupied"] == int(x["end_n"] > 0) for x in rows)
    for bg, post, budget, repeat in product(
        short["backgrounds"], short["future_visitor_environments"],
        short["post_ovule_budgets"], short["new_postshock_demographic_repeat_ids"]
    ):
        paired = [x for x in rows if (
            x["background"],x["post"],x["budget"],x["repeat"]
        ) == (bg,post,budget,repeat)]
        assert len(paired) == 2
        assert abs(paired[0]["assurance_mean"]-
                   paired[1]["assurance_mean"]) < 1e-12


def test_readout_is_history_unit_and_preserves_discordant_signs():
    d, _, _, _ = load_design()
    rows = []
    for setting,h in declared_groups(d):
        for bg,post,budget,repeat,variant in product(
            d["backgrounds"],d["future_visitor_environments"],
            d["post_ovule_budgets"],d["new_postshock_demographic_repeat_ids"],
            d["treatments"]
        ):
            occ = int(variant == "full_donor" and
                      setting == "pollen_discount" and bg == "far")
            rows.append({
                "setting":setting,"history":h,"background":bg,
                "post":post,"budget":budget,"repeat":repeat,
                "variant":variant,"occupied":occ,"end_n":occ,
                "viable_maternal":1.0
            })
    out = analyze(d, rows)
    assert out["n_independent_visitor_histories"] == 4
    assert out["n_postshock_demographic_rng_repeats"] == 8
    assert out["n_stress_trajectories"] == 2048
    assert out["n_matched_stress_pairs"] == 1024
    assert len(out["results"]) == 8
    pollen = next(r for r in out["results"] if
                  (r["setting"],r["recipient_background"]) ==
                  ("pollen_discount","far"))
    assert pollen["discordant_pairs"] == 128
    assert pollen["mean_occupancy_difference"] == 1.0


def test_observed_rng_residual_is_not_globally_positive():
    observed = json.loads((ROOT /
        "data/results/chapter2_island_assurance_postshock_rng_repeatability_20261008.json"
    ).read_text())
    assert observed["independent_ecological_histories"] == 4
    assert observed["n_postshock_trajectories"] == 2048
    rows = observed["findings"]
    assert len(rows) == 8
    assert all(row["matched_postshock_pairs"] == 128 for row in rows)
    assert any(r["mean_occupancy_difference"] > 0 for r in rows)
    assert any(r["mean_occupancy_difference"] < 0 for r in rows)
    assert sum(r["discordant_pairs"] for r in rows) > 0
    assert any("failed" in b.lower() for b in observed["bounds"])
