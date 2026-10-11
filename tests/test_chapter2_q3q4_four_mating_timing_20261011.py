"""Exact Q3→Q4 timing checks across original four mating-system rule sets."""
import json

import numpy as np
import pytest

from scripts.audit_chapter2_q3q4_four_mating_timing_20261011 import (
    STATUS, SETTING_NAMES, BUDGETS, N0, source_mu_q,
    matrix, occupancy_trajectory, audit,
)


@pytest.mark.parametrize("setting", SETTING_NAMES)
def test_all_four_rules_share_identical_heterozygote_start(setting):
    counts=(0,N0,0)
    native_mu,native_q=source_mu_q(counts,6.,setting,"native")
    fixed_mu,fixed_q=source_mu_q(counts,6.,setting,"fixed_expression")
    assert native_mu == pytest.approx(fixed_mu,abs=1e-12)
    np.testing.assert_allclose(native_q,fixed_q,rtol=0,atol=1e-12)
    np.testing.assert_allclose(native_q,[.25,.5,.25],rtol=0,atol=1e-12)
    tn=matrix(6.,setting,"native")
    tf=matrix(6.,setting,"fixed_expression")
    assert tn.shape==(165,165)
    np.testing.assert_allclose(tn.sum(axis=1),1,atol=1e-12,rtol=0)
    np.testing.assert_allclose(tf.sum(axis=1),1,atol=1e-12,rtol=0)
    ix=tuple(__import__(
        "scripts.audit_chapter2_q3q4_exact_genotype_factorial_20261011",
        fromlist=["states"]).states()).index((0,N0,0))
    np.testing.assert_allclose(tn[ix],tf[ix],rtol=0,atol=1e-12)


def test_four_mating_systems_at_budget6_have_same_sign_but_not_effect_size():
    r=audit()
    assert r["status"]==STATUS and r["state_count"]==165
    assert r["n_total_source_comparisons"]==12
    assert r["new_histories"]==r["new_genetic_trajectories"]==0
    assert r["independent_confirmation"] is False
    d={x["setting"]:x for x in r["results"] if x["resource_budget"]==6.}
    expect={
      "delayed_control":(-.0039708198486585,22,-.01904540063805,-.88589072),
      "prior_selfing":(-.0012237250278442,19,-.01772636112118,-.66515331),
      "pollen_discount":(-.0002227736810872,17,-.01690459243654,-.55516755),
      "assurance_cost":(-.0005318239237264,16,-.01723656641703,-.53683446),
    }
    for setting,(d80,t_min,minimum,auc) in expect.items():
        x=d[setting]
        assert x["P80_native_minus_fixed"]==pytest.approx(d80,abs=1e-10)
        assert x["first_negative_delta_t"]==2
        assert x["most_negative_delta_t"]==t_min
        assert x["minimum_delta"]==pytest.approx(minimum,abs=1e-9)
        assert x["occupied_years_expectation_difference_T1_to_T80"]==pytest.approx(
          auc,abs=1e-7
        )
        assert abs(x["trajectory_t0_to_t80_delta"][0]) < 1e-12
        assert abs(x["trajectory_t0_to_t80_delta"][1]) < 1e-12
        assert x["trajectory_t0_to_t80_delta"][2]<0


def test_all_resource_settings_and_extinction_floor_are_visible():
    result=audit()
    for name in SETTING_NAMES:
        low=next(x for x in result["results"] if x["setting"]==name and x["resource_budget"]==4.5)
        mid=next(x for x in result["results"] if x["setting"]==name and x["resource_budget"]==6.)
        high=next(x for x in result["results"] if x["setting"]==name and x["resource_budget"]==8.)
        assert low["P80_native_minus_fixed"]>=0
        assert mid["P80_native_minus_fixed"]<0
        assert high["P80_native_minus_fixed"]<0
        assert low["first_negative_delta_t"]==2
        assert high["first_negative_delta_t"]==2
        assert low["minimum_delta"]<-0.009
        for x in (low,mid,high):
            assert len(x["trajectory_t0_to_t80_delta"])==81
            assert x["occupied_years_expectation_difference_T1_to_T80"]<0
            assert np.isclose(
                x["occupied_years_expectation_difference_T1_to_T80"],
                sum(x["trajectory_t0_to_t80_delta"][1:]),atol=1e-10
            )
    json.dumps(result,allow_nan=False)


def test_reject_unknown_rule_and_off_grid_resource():
    with pytest.raises(ValueError):
        source_mu_q((0,8,0),6.,"invented","native")
    with pytest.raises(ValueError):
        source_mu_q((0,8,0),5.5,"prior_selfing","native")
    with pytest.raises(ValueError):
        source_mu_q((0,8,0),6.,"prior_selfing","invented")
