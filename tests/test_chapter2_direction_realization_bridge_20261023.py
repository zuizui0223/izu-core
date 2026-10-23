"""Read-only regression tests for R1–R5 payoff/finite-response boundary.

No population steps, newly fitted hypotheses, or changes to registered biology.
"""
import math

import pytest

from scripts.audit_chapter2_direction_realization_bridge_20261023 import (
    crossed_competing_event_identity,
    read_only_audit,
    source_no_visitor_payoff,
    transfer_source_signs,
)


@pytest.mark.parametrize("timing", ["delayed", "prior"])
@pytest.mark.parametrize("mode", ["fixed", "evolving"])
def test_no_visitor_payoff_decreases_with_floral_investment(timing, mode):
    result = source_no_visitor_payoff(timing=timing, mode=mode)
    assert result["log_relative_fitness_high_minus_low_I"] == pytest.approx(-0.16, abs=1e-12)
    assert result["source_gradient_at_I_0p5"] == pytest.approx(-0.4, abs=1e-12)


def test_strict_source_comparison_rejects_invalid_assumptions():
    with pytest.raises(ValueError):
        source_no_visitor_payoff(timing="invalid", mode="fixed")
    with pytest.raises(ValueError):
        source_no_visitor_payoff(timing="delayed", mode="fixed", investment_cost=0)


def test_R5_archived_no_visitor_signs_stay_distinct_from_selection():
    d = transfer_source_signs()
    assert d["fixed"]["positive_I_exact_signs"] == 27
    assert d["evolving"]["positive_I_exact_signs"] == 29
    assert d["fixed"]["occupied_futures"] == 704
    assert d["evolving"]["occupied_futures"] == 1024
    assert d["fixed"]["cohorts"] == d["evolving"]["cohorts"] == 32
    assert d["fixed"]["not_an_independent_founder_count"]
    assert d["fixed"]["signs_do_not_establish_biologically_large_changes"]


def test_R4_original_sealed_competing_event_partition():
    r = crossed_competing_event_identity()
    assert r["B8"]["first_genetic_loss_diff_count"] == 2132
    assert r["B8"]["first_extinction_diff_count"] == 0
    assert r["B8"]["alive_with_I_support_diff_pp"] == -8.328125
    assert r["B4p5"]["first_genetic_loss_diff_count"] == 3122
    assert r["B4p5"]["first_extinction_diff_count"] == -12227
    assert r["B4p5"]["alive_with_I_support_diff_pp"] == 35.56640625
    assert r["B8"]["post_outcome_not_registered"]
    assert r["B4p5"]["post_outcome_not_registered"]


def test_cannot_promote_exploratory_bridge_to_new_biology():
    report = read_only_audit()
    assert report["new_biological_simulations"] == 0
    assert report["new_preregistered_endpoints"] == 0
    assert len(report["source_payoffs"]) == 4
    assert report["status"] == "EXPLORATORY_READ_ONLY_NO_NEW_BIOLOGY"
