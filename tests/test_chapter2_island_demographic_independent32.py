"""Lock the independent history demographic gate and scientific inference boundary."""
import json
from pathlib import Path

import pytest

from scripts.run_chapter2_island_demographic_independent32 import (
    load_frozen, tasks, run_group,
)
from scripts.summarize_chapter2_island_demographic_independent32 import evaluate

ROOT = Path(__file__).resolve().parents[1]


def test_design_is_frozen_new_history_and_full_grid():
    d, _ = load_frozen()
    assert d["status"] == "frozen_before_new_history_demographic_confirmation"
    assert d["independent_visitor_histories"]["count"] == 32
    assert d["demographic_repeat_seeds"] == [30101801]
    assert d["stress_ovule_budgets"] == [2, 3, 4, 5]
    assert d["post_updates"] == 80
    assert d["post_capacity"] == d["source_bottleneck_n"] == 8
    assert len(tasks(d)) == d["total_groups"] == 512
    assert set(t[2] for t in tasks(d)) == set(range(30100801, 30100833))
    assert len(set(tasks(d))) == 512


def test_one_actual_model_group_performs_full_paired_post_grid():
    d, source = load_frozen()
    row = run_group(tasks(d)[0], d, source)
    assert row["pre_survivors"] >= 8
    assert len(row["post_cases"]) == 8
    assert len({(x["post"], x["ovule_budget"]) for x in row["post_cases"]}) == 8
    for x in row["post_cases"]:
        assert x["occupied"] == int(x["terminal_N"] > 0)
        assert 0 <= x["terminal_N"] <= 8
        if x["terminal_N"] == 0:
            assert x["end_traits"] is None


def test_survival_bootstrap_has_32_histories_not_4096():
    d, _ = load_frozen()
    rows = {}
    # Unit fixture: simulate a strong positive interaction in every visitor
    # history, with complete post-treatment cases. Not an observed result.
    for key in tasks(d):
        setting, mode, h, rep, pre = key
        occupied = int(mode == "evolving" and pre == "far")
        rows[key] = {
            "group": key,
            "post_cases": [
                {"post": post, "ovule_budget": budget, "occupied": occupied}
                for post in d["post_environments"]
                for budget in d["stress_ovule_budgets"]
            ]
        }
    r = evaluate(d, rows)
    assert r["independent_histories"] == 32
    assert r["nested_demographic_repeats"] == 1
    assert r["post_trajectories"] == 4096
    assert r["pooled_primary"]["mean"] == pytest.approx(1)
    assert r["pooled_primary"]["bootstrap95"] == pytest.approx([1, 1])


def test_recorded_offline_result_keeps_prior_selfing_uncertainty():
    d = json.loads((ROOT / "data/results/chapter2_island_demographic_independent32_20261008.json").read_text())
    assert d["independent_histories"] == 32
    assert d["post_switch_trajectories"] == 4096
    assert d["predeclared_pooled_primary"]["pass"] is True
    assert d["predeclared_pooled_primary"]["mean"] == pytest.approx(0.1083984375)
    assert d["predeclared_pooled_primary"]["bootstrap95"] == pytest.approx(
        [0.0654296875, 0.1513671875]
    )
    assert len(d["per_setting"]) == 4
    prior = next(row for row in d["per_setting"]
                 if row["setting"] == "prior_selfing")
    assert prior["interaction"] > 0
    assert prior["bootstrap95"][0] < 0 < prior["bootstrap95"][1]
    assert d["archive"]["github_actions_confirmation"] is False
    assert "temporal" in " ".join(d["scientific_boundary"]).lower()
