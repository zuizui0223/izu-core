"""Non-peeking contract tests: no simulation or stochastic biological outcomes."""
from copy import deepcopy
from collections import Counter
import pytest

from scripts.plan_chapter2_order_expression_identification import (
    load_protocol, validate_protocol, prehistories, futures,
    compile_protocol, log_budget_weights, decision,
)


def test_exact_three_arm_exposure_balance_and_release():
    d = load_protocol()
    for label, phases in d["path_perturbation"]["arms"].items():
        assert [(x["from"], x["to"]) for x in phases] == [
            (0, 100), (100, 200), (200, 300), (300, 400)
        ], label
        assert phases[-1]["A"] == phases[-1]["I"] == 0
        assert sum((x["to"] - x["from"]) for x in phases if x["A"]) == 200
        assert sum((x["to"] - x["from"]) for x in phases if x["I"]) == 200
    assert d["path_perturbation"]["joint_exposure_update_counts"] == {
        "assurance_first": 100,
        "investment_first": 100,
        "synchronous_time_control": 200,
    }
    assert "NOT a matched overlap negative control" in (
        d["path_perturbation"]["control_caveat"]
    )
    # The first 100 updates uniquely determine assigned temporal precedence.
    assert d["path_perturbation"]["arms"]["assurance_first"][0]["A"] > 0
    assert d["path_perturbation"]["arms"]["assurance_first"][0]["I"] == 0
    assert d["path_perturbation"]["arms"]["investment_first"][0]["I"] < 0
    assert d["path_perturbation"]["arms"]["investment_first"][0]["A"] == 0
    assert "IDENTICAL mutation opportunities" in d["path_perturbation"]["genetic_rule"]


def test_full_independent_history_and_paired_grid():
    d = load_protocol()
    report = compile_protocol(d)
    assert report["status"] == "PROSPECTIVE_DESIGN_ONLY_NO_BIOLOGICAL_OUTCOMES"
    assert report["biological_outcomes_generated"] is False
    assert report["prehistory_groups"] == 3072
    assert report["postshock_forks_per_group"] == 28
    assert report["declared_postshock_trajectories"] == 86016
    assert report["independent_visitor_histories"] == 64
    assert report["nested_repeats"] == 2
    assert sum(report["budget_weights"].values()) == pytest.approx(1)
    assert all(x > 0 for x in report["budget_weights"].values())
    pres = prehistories(d)
    assert len(set(pres)) == 3072
    assert Counter(t.expression_order for t in pres) == {
        "assurance_first": 1024,
        "investment_first": 1024,
        "synchronous_time_control": 1024,
    }
    for h in range(37110801, 37110865):
        assert sum(t.visitor_history == h for t in pres) == 48
    slice_ = list(futures(d, pres[:2]))
    assert len(slice_) == 56
    assert len(set(slice_)) == 56


def test_protocol_rejects_posthoc_reweighting_timing_or_history_reuse():
    original = load_protocol()
    for field, change in (
        ("dose", lambda d: d["path_perturbation"]["arms"]["assurance_first"][2].update({"I": 0})),
        ("second_stage", lambda d: d["path_perturbation"]["arms"]["investment_first"][1].update({"to": 201})),
        ("new_cohort", lambda d: d["independent_histories"].update({"first": 36110801})),
        ("shock", lambda d: d["postshock"].update({"budgets": [2, 3, 4, 5]})),
        ("main_gate", lambda d: d["postshock"].update({"primary_regime": "unbottlenecked_capacity48"})),
        ("failed_test", lambda d: d["source"].update({"earlier_failure": "confirmed"})),
    ):
        changed = deepcopy(original)
        change(changed)
        with pytest.raises((ValueError, AssertionError)):
            validate_protocol(changed)


def test_two_sided_adjudication_and_equivalence_are_distinct():
    assert decision(0.11, (0.06, 0.17)) == "nonzero_order_protocol_effect"
    assert decision(-0.09, (-0.15, -0.01)) == "nonzero_order_protocol_effect"
    assert decision(0.01, (-0.025, 0.035)) == "equivalent_within_predeclared_ROPE"
    assert decision(0.04, (0.00, 0.10)) == "inconclusive"
    assert decision(0.07, (-0.01, 0.15)) == "inconclusive"
    assert decision(0.04, (0.01, 0.09)) == "inconclusive"
    with pytest.raises(ValueError):
        decision(0.1, (0.3, 0.2))


def test_claim_firewall_and_not_previously_failed_gate():
    d = load_protocol()
    assert "FAILED" in d["source"]["earlier_failure"]
    assert "different historical-assurance-access treatment" in d["stop_conditions"][-1] or (
        "PR #414" in " ".join(d["stop_conditions"])
    )
    assert "not causal effect of observed spontaneous" in (
        d["estimation"]["contrast_type"]
    )
    assert "not required" in d["threshold_and_pde"]["pde"]
    assert "every reproductive update t0-400" in d["threshold_and_pde"]["realized_order"]
    assert "NEVER counted" in d["threshold_and_pde"]["realized_order"]
    assert d["estimation"]["bootstrap"]["unit"] == "visitor_history"
    assert d["estimation"]["bootstrap"]["shared_index_all_settings"] is True
