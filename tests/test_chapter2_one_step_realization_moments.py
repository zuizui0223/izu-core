"""Test exact one-step source Model3 sampling-variance partition.

The fixture is intentionally non-selective and cannot demonstrate adaptive
genetic evolution; it isolates a mechanism hidden by phenotypic averages.
"""
from math import comb

import numpy as np
import pytest

from scripts.audit_chapter2_one_step_realization_moments import (
    cloned_state, exact_binary_direction_failure, one_step_moments, run,
)


@pytest.fixture(scope="module")
def source_report():
    return run()


def test_same_source_phenotype_and_reproductive_ledger_but_different_variance(source_report):
    rows={ (x["type"],x["r"]):x for x in source_report["rows"] }
    assert len(rows)==8
    assert source_report["status"]=="EXACT_SOURCE_ONE_STEP_VARIANCE_NO_EVOLUTION"
    assert source_report["new_ecological_histories"]==0
    assert source_report["n_model_history_replicates"]==0
    for r in (1,2,4,8):
        a=rows["same_expressed_trait_homozygote",r]
        b=rows["same_expressed_trait_heterozygote",r]
        np.testing.assert_allclose(
            a["expected_group_viable_seeds"],
            b["expected_group_viable_seeds"],atol=0,rtol=0)
        am,bm=a["moment"],b["moment"]
        assert am["offspring_expected_mean"]==bm["offspring_expected_mean"]==.5
        assert am["offspring_parent_lottery_variance"]==0.
        assert bm["offspring_parent_lottery_variance"]==0.
        assert am["offspring_mendelian_segregation_variance"]==0.
        np.testing.assert_allclose(
            bm["offspring_mendelian_segregation_variance"],.125,
            atol=1e-13,rtol=0)
        np.testing.assert_allclose(
            bm["next_mean_conditional_variance"],.125/r,
            atol=1e-13,rtol=0)


def test_exact_binary_polynomial_probability_is_binomial_cdf(source_report):
    b=next(x for x in source_report["rows"]
           if x["type"]=="same_expressed_trait_heterozygote" and x["r"]==4)
    # One recruit inherits two independent 0/1 alleles with P=.5.
    # R=4 therefore has B(8,.5) successes. Threshold at offspring
    # expressed mean <=.5 corresponds to <=4 successes in eight gametes.
    expected=sum(comb(8,k) for k in range(5))/2**8
    np.testing.assert_allclose(
        b["at_or_below_initial_mean_probability"],expected,
        atol=1e-14,rtol=0)
    assert expected==.63671875


def test_parent_lottery_can_be_isolated_with_homozygotes():
    # Two 0-allele adults and one 1-allele adult. All are homozygous,
    # so Mendelian segregation variation is exactly zero; a biased
    # parental lottery still produces positive between-parent variation.
    alleles=np.array([[0,0],[0,0],[1,1]],dtype=float)
    parent=np.array([[.1,.1,.1],[.1,.1,.1],[.1,.1,.2]],dtype=float)
    parent/=parent.sum()
    m=one_step_moments(alleles,parent,resident_recruits=4)
    assert m["offspring_parent_lottery_variance"]>0
    assert m["offspring_mendelian_segregation_variance"]==0


def test_one_recruit_allele_polynomial_matches_direct_enumeration():
    state=cloned_state(heterozygous=True)
    q=np.ones((4,4))/16
    out=exact_binary_direction_failure(
        state.alleles[:,0,:],q,resident_recruits=1,threshold=.5)
    np.testing.assert_allclose(
        out["offspring_allele_count_probs"],[.25,.5,.25],
        atol=1e-14,rtol=0)
    assert out["conditional_failure_probability"]==.75


def test_wrong_inputs_fail_closed():
    with pytest.raises(ValueError):
        one_step_moments(np.zeros((2,2)),np.ones((2,2)),
                         resident_recruits=2)
    with pytest.raises(ValueError):
        one_step_moments(np.zeros((2,2)),np.ones((2,2))/4,
                         resident_recruits=0,survivors=())
    with pytest.raises(ValueError):
        exact_binary_direction_failure(
            np.full((2,2),.5),np.ones((2,2))/4,
            resident_recruits=1,threshold=.5)


def test_source_selected_positive_expectation_can_fail_in_one_step(source_report):
    s=source_report["selected_source_case"]
    assert s["status"]=="POST_DISCOVERY_SELECTED_SOURCE_FIXED_STATE"
    assert s["no_biological_trajectories"] is True
    assert s["n_focal_adults"]==4
    np.testing.assert_allclose(s["visitor_optima"],[.45,.5,.55,.6],
                               atol=0,rtol=0)
    m=s["moment"]
    assert m["resident_recruits"]==8 and m["survivor_count"]==0
    assert m["initial_trait_mean"]==.25
    assert m["expected_mean_change_from_initial"]>0
    assert m["offspring_parent_lottery_variance"]>0
    assert m["offspring_mendelian_segregation_variance"]>0
    prob=s["exact_conditional_nonpositive_change"]["conditional_failure_probability"]
    assert .55<prob<.70
    # Original source denominator and delayed selfing keep the mean
    # selective shift small, though mathematically positive.
    np.testing.assert_allclose(
        m["expected_mean_change_from_initial"],.004558652322326329,
        rtol=0,atol=5e-11)
    np.testing.assert_allclose(prob,.6058431728182614,
        rtol=0,atol=5e-10)
