"""Algebraic ONLY: test exact randomized-history ITT and ROPE decisions.

No biological trajectories, archived or prospective, are simulated here.
"""
import pytest

from scripts.plan_chapter2_order_expression_identification import (
    load_protocol, prehistories,
)
from scripts.chapter2_order_confirmatory_readout import evaluate


@pytest.mark.parametrize("signal,expected,mean", [
    (True, "nonzero_order_protocol_effect", 1.0),
    (False, "equivalent_within_predeclared_ROPE", 0.0),
])
def test_synthetic_full_history_itt_and_mandatory_sensitivities(
    signal, expected, mean
):
    d = load_protocol()
    grid = {
        (regime,float(budget),future)
        for regime in d["postshock"]["arms"]
        for budget in d["postshock"]["budgets"]
        for future in d["postshock"]["future_environments"]
    }
    post = {}
    for task in prehistories(d):
        # This is algebra, not a statement about actual future biological
        # occupancy. All 64 independent histories remain equally weighted.
        occupied = int(
            signal and task.expression_order == "assurance_first"
            and task.environment == "far"
        )
        post[task] = {cell: {"occupied":occupied} for cell in grid}
    result = evaluate(d, post)
    primary = result["main_order_history_DID"]
    assert primary["decision"] == expected
    assert primary["pooled_mean"] == pytest.approx(mean)
    assert primary["history_bootstrap95"] == pytest.approx([mean,mean])
    for regime in d["postshock"]["arms"]:
        aggregate = result["all_regime_aggregate"][regime]
        assert aggregate["pooled_order_effect"] == pytest.approx(mean)
        for setting in d["reproductive_settings"]:
            s = aggregate["setting_order_effects"][setting]
            assert s["mean"] == pytest.approx(mean)
            assert s["bootstrap95"] == pytest.approx([mean,mean])
        sensitivity = result["sensitivity_by_regime_budget_future"][regime]
        assert set(sensitivity) == {str(b) for b in d["postshock"]["budgets"]}
        for b in sensitivity.values():
            assert set(b) == {"near","far"}
            assert all(x["pooled_mean"] == pytest.approx(mean) for x in b.values())
