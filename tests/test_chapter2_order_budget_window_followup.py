"""Independent window confirmation tests: synthetic arrays / plan only, NO fresh histories."""
import json
from pathlib import Path

import numpy as np
import pytest

from scripts.chapter2_order_budget_window_followup import (
    history_shard, history_window_residual, inference, load_followup,
    plan, smooth_cv_losses,
)
from scripts.plan_chapter2_order_expression_identification import prehistories


def test_plan_has_64_nonreused_independent_histories_and_57344_futures():
    spec, d = load_followup()
    p = plan(spec, d)
    assert p["new_visitor_histories_sampled"] == 0
    assert (p["prehistories"], p["postshock_cases"]) == (2048, 57344)
    assert p["arms"] == ["assurance_first", "investment_first"]
    assert p["budgets"] == [0.5, 1, 2, 3, 4, 5, 8]
    tasks = prehistories(d)
    assert {x.visitor_history for x in tasks} == set(range(38110901, 38110965))
    assert {x.demographic_repeat for x in tasks} == {38111901, 38111902}
    for shard in range(64):
        sample = history_shard(tasks, 38110901, shard, 64)
        assert len(sample) == 32
        assert {t.visitor_history for t in sample} == {38110901 + shard}


def test_window_formula_and_refusal_to_use_forks_as_history():
    budgets = [0.5, 1, 2, 3, 4, 5, 8]
    d = np.zeros((64, 7))
    d[:, 3] = -0.12
    d[:, 4] = -0.08
    result = history_window_residual(d, budgets)
    assert result.shape == (64,)
    assert np.allclose(result, -0.10)
    with pytest.raises(ValueError):
        history_window_residual(np.zeros((57344, 7)), budgets)
    with pytest.raises(ValueError):
        history_window_residual(np.zeros((64, 7)), budgets[::-1])


def test_synthetic_fixed_window_vs_smooth_and_practical_equivalence():
    budgets = [0.5, 1, 2, 3, 4, 5, 8]
    null = inference(np.zeros((64, 7)), budgets)
    assert null["predeclared_joint_decision"] == "window_residual_practically_equivalent"
    assert not null["window_gate_passed"]
    assert not null["smooth_gate_passed"]
    d = np.zeros((64, 7))
    d[:, 3:5] = -0.12
    positive = inference(d, budgets)
    assert positive["window_gate_passed"]
    assert positive["smooth_gate_passed"]
    assert positive["predeclared_joint_decision"] == (
        "fixed_window_confirmed_beyond_specified_cubic_smooth")
    assert positive["history_bootstrap95"][1] < 0
    assert positive["histories"] == 64


def test_smooth_cubic_did_does_not_trigger_window():
    budgets = [0.5, 1, 2, 3, 4, 5, 8]
    x = np.log(np.array(budgets) / 3)
    d = np.tile(0.01 + 0.002 * x + 0.003 * x*x + 0.004 * x*x*x, (64, 1))
    res = inference(d, budgets)
    assert res["predeclared_joint_decision"] != (
        "fixed_window_confirmed_beyond_specified_cubic_smooth")
    assert not res["smooth_gate_passed"]


def test_production_is_workflow_dispatch_only_and_default_is_plan_preflight():
    workflow = Path(".github/workflows/chapter2-order-budget-window-independent.yml").read_text()
    header = workflow.split("permissions:", 1)[0]
    assert "workflow_dispatch:" in header
    assert "push:" not in header
    assert "pull_request:" not in header
    assert "schedule:" not in header
    assert "default: preflight_only" in header
    assert "default: false" in header
    assert "source_commit_sha:" in header
    assert "full_cohort_launch_approved" in workflow
    assert "github.ref == 'refs/heads/main'" in workflow
    assert 'test "$REVIEWED_SHA" = "$CHECKED_OUT_SHA"' in workflow
    assert "inputs.mode == 'full_cohort'" in workflow
    assert "inputs.full_cohort_launch_approved == true" in workflow
    assert "needs: preflight" in workflow
    assert "--execute-frozen-cohort" in workflow
    assert "tests/test_chapter2_order_budget_window_followup.py" in workflow


def test_new_visitor_histories_not_in_existing_science_tests():
    import ast
    p = Path("tests/test_chapter2_order_budget_window_followup.py").read_text()
    parsed = ast.parse(p)
    invoked = {
        node.func.id for node in ast.walk(parsed)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    assert not {"simulate_prehistory", "one_future"} & invoked
    d = json.loads(Path("data/design/chapter2_order_budget_window_independent_20261009.json").read_text())
    assert not d["cohort"]["outcomes_exposed"]
    assert d["frozen_source"]["prior_result_status"] == "equivalent_within_predeclared_ROPE"
