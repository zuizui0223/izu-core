"""Regression guards for post-outcome mean-matched assurance ceiling control."""
import numpy as np
import pytest

from scripts.audit_model3_k32_mean_matched_ceiling import (
    tilted_offspring_law, calibrated_laws, variance_parts, run_mean_matched,
)


def test_tilt_preserves_support_mass_and_limits():
    b=np.array([0.,.5,1.,0.])
    q=np.array([.3,.4,.3,0.])
    for s in (-20.,-1.,0.,1.,20.):
        p=tilted_offspring_law(q,b,s)
        assert p.shape==q.shape
        assert np.isclose(p.sum(),1.,atol=1e-12)
        assert np.all(p>=0)
        assert p[-1]==0.
    np.testing.assert_allclose(tilted_offspring_law(q,b,0.),q,atol=1e-12)
    with pytest.raises(ValueError):
        tilted_offspring_law(np.array([1.,-.1]),np.array([0.,1.]),2.)


def test_calibrate_one_cohort_exact_mean_not_realized_sampling():
    b=np.array([0.,.5,1.])
    Q=np.array([[.5,.3,.2],[.1,.8,.1],[.2,.2,.6]])
    for target in (.25,.5,.75,.99):
        r=calibrated_laws(Q,b,target)
        assert r["admissible"] is True
        assert abs(r["calibrated_conditional_mean"]-target)<1e-7
        assert np.allclose(r["laws"].sum(axis=1),1.,atol=1e-12)
        assert np.all(r["laws"]>=0)
    # All parents lost the high allele; reweighting cannot resurrect it.
    blocked=calibrated_laws(np.array([[1.,0.,0.]]),b,.5)
    assert blocked["admissible"] is False
    assert blocked["reason"]=="absorbing_allele_support_prevents_mean_matching"


def test_cumulative_variance_has_required_feedback_covariance_term():
    d=np.array([.1,.3,.7,.5])
    noise=np.array([-.1,.05,-.2,.12])
    r=variance_parts(d,noise)
    assert r["covariance_identity_error"]==pytest.approx(0.,abs=1e-14)
    assert r["total_frequency_change_variance"]==pytest.approx(
        np.var(d+noise,ddof=0))
    with pytest.raises(ValueError):
        variance_parts(np.array([.2]),np.array([.1]))


@pytest.mark.parametrize("budget",[3.,8.])
def test_source_mean_matching_does_not_claim_causal_mechanism(budget):
    r=run_mean_matched(budget=budget,draws=24,seed=99542)
    assert r["status"] in {
        "EXPLORATORY_MEAN_MATCHED_CEILING_COMPARATOR_COMPLETE",
        "MEAN_MATCH_BOUNDARY_UNATTAINABLE",
    }
    if r["status"]=="MEAN_MATCH_BOUNDARY_UNATTAINABLE":
        assert r["no_claim_about_feedback_or_ceiling"] is True
        assert 1<=r["failed_at_generation"]<=8
        return
    c=r["conditions"]
    assert c["K"]==32 and c["mutation_rate"]==0 and c["generations"]==8
    assert c["old_visitor_history"]==26110601
    assert c["independent_visitor_histories"]==1
    assert c["source_model3_biology_edited"] is False
    assert c["comparator_intentionally_changes_mating_payoffs"] is True
    assert c["comparator_reweighted_after_exposure_to_source_outcomes"] is True
    assert c["same_realized_census_every_year"] is True
    assert c["no_confirmatory_cohorts_used"] is True
    assert c["n_surviving"]+c["n_extinct"]==24
    assert len(r["per_generation"])==8
    for year in r["per_generation"]:
        assert abs(year["calibrated_conditional_mean"]-year["source_mean"])<1e-7
        assert year["source_allele_frequency_variance"]>=0
        assert year["mean_matched_comparator_frequency_variance"]>=0
        assert 0<=year["comparator_fixation_fraction"]<=1
    for arm in ("source","mean_matched_comparator"):
        assert 0<=r[arm]["assurance_endpoint_mean"]<=1
        assert 0<=r[arm]["assurance_endpoint_variance"]<=.25
        assert abs(r[arm]["cumulative_frequency_variance"]["covariance_identity_error"])<1e-10


def test_scope_rejects_outside_frozen_biological_design():
    with pytest.raises(ValueError):
        run_mean_matched(budget=4.,draws=32)
    with pytest.raises(ValueError):
        run_mean_matched(budget=8.,draws=4)
