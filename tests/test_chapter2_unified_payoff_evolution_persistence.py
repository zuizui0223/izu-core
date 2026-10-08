"""Design-only, non-peeking contract for the unified island ecological process."""
from collections import Counter
import json
import math
from pathlib import Path

import pytest

from scripts.plan_chapter2_unified_payoff_evolution_persistence import (
    DESIGN, load_design, log_trapezoid_weights, prehistory_tasks, shock_tasks,
    validate_counts
)

ROOT = Path(__file__).resolve().parents[1]


def test_new_independent_cohort_and_complete_task_grid():
    d = load_design()
    assert d["status"] == "prospective_new_cohort_protocol_design_only_not_executed"
    plan = validate_counts(d)
    assert plan["independent_visitor_histories"] == 64
    assert plan["nested_demographic_repeats"] == 2
    assert plan["prehistories"] == 2048
    assert plan["postshock_branches_per_prehistory"] == 42
    assert plan["postshock_trajectories"] == 86016
    assert sum(plan["budget_weights"].values()) == pytest.approx(1)
    assert plan["sha256"] and len(plan["sha256"]) == 64
    tasks = prehistory_tasks(d)
    per_setting = Counter(t.setting for t in tasks)
    assert all(per_setting[s] == 512 for s in d["reproductive_settings"])
    assert len(set(t.history for t in tasks)) == 64
    new = set(t.history for t in tasks)
    old_ranges = [
        range(26110601, 26110665),
        range(30100801, 30100833),
        range(32100801, 32100817),
    ]
    assert not any(new.intersection(old) for old in old_ranges)


def test_budget_quadrature_rejects_selection_of_favourable_midrange():
    d = load_design()
    weighted = log_trapezoid_weights(d["postshock"]["budgets"])
    assert list(weighted) == [0.5, 1, 2, 3, 4, 5, 8]
    assert min(weighted.values()) > 0
    assert weighted[0.5] > 0 and weighted[8] > 0
    assert sum(weighted.values()) == pytest.approx(1)
    with pytest.raises(ValueError):
        log_trapezoid_weights([2, 2, 4])
    with pytest.raises(ValueError):
        log_trapezoid_weights([0, 1])


def test_every_historical_population_forks_to_every_declared_stress():
    d = load_design()
    selected = prehistory_tasks(d)[:3]
    forks = list(shock_tasks(d, selected))
    assert len(forks) == 3 * 42
    for p in selected:
        own = [t for t in forks if t.prehistory == p]
        assert len(own) == 42
        assert set(t.regime for t in own) == {
            "fecundity_only", "founder_bottleneck", "bottleneck_small_capacity",
        }
        assert {t.budget for t in own} == set(d["postshock"]["budgets"])
        assert {t.future_environment for t in own} == {"near", "far"}


def test_two_stage_gate_preserves_statistical_and_scientific_boundaries():
    d = load_design()
    stage1 = d["causal_estimates"]["primary_stage1_evolution"]
    stage2 = d["causal_estimates"]["primary_stage2_persistence"]
    assert "All four settings" in stage1["rule"]
    assert "Pooled mean history_delta>0" in stage2["success_rule"]
    assert stage2["primary_regime"] == "bottleneck_small_capacity"
    assert d["inference"]["bootstrap"]["unit"] == "independent visitor history"
    assert d["inference"]["bootstrap"]["draws"] == 9999
    assert d["postshock"]["no_plant_immigration"] is True
    assert d["fixed_assurance_allele_value"] == 0.5
    assert "mode=fixed blocks A mutation" in d["postshock"]["evolutionary_mask_rule"]
    assert "both historical groups use mode=evolving" in d["postshock"]["evolutionary_mask_rule"]
    assert "mutation_traits=(True,True,True)" in d["postshock"]["evolutionary_mask_rule"]
    assert "BOTH prior fixed-A and prior evolving-A histories" in d["postshock"]["evolutionary_access_rule"]
    assert "identical POSTSHOCK A-evolving rules" in (
        d["causal_estimates"]["primary_stage2_persistence"]["history_delta"]
    )
    assert d["causal_estimates"]["optional_density_model"]["status"] == "not_part_of_primary_gate"
    assert d["execution_rule"].startswith("DESIGN ONLY")
    assert not list(ROOT.glob("data/results/chapter2_unified_payoff_evolution_persistence_20261008*"))


def test_prior_independent32_pass_does_not_count_as_a_new_outcome():
    old = json.loads((ROOT / "data/results/chapter2_assurance_generality_20261006.json").read_text())
    assert old["adjudication"]["status"] == "all_four_confirmed"
    d = load_design()
    assert d["histories"]["first"] > 36000000
    assert d["status"].endswith("not_executed")
    assert "historical" in d["causal_estimates"]["primary_stage2_persistence"]["label"] or (
        "persistence" in d["causal_estimates"]["primary_stage2_persistence"]["label"]
    )
