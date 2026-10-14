"""Neutral Mendelian matched-census counterfactual; no canonical source edits."""
import numpy as np
import pytest
from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_k32_pathwise_selection_drift import allele_frequency_basis
from scripts.audit_model3_k32_neutral_census_control import (
    neutral_child_genotype_law, run_neutral_control,
)


def test_uniform_nonself_mendelian_kernel_is_normalized_unbiased():
    first,grid,_,_=fixed_support_problem(capacity=32,ovule_budget=8.)
    b=allele_frequency_basis(grid)
    for c in (first, first//8, np.eye(1,len(first),np.flatnonzero(first)[0],
                        dtype=np.int64).ravel()):
        q=neutral_child_genotype_law(c,grid)
        assert len(q)==27
        assert (q>=0).all()
        assert q.sum()==pytest.approx(1.,abs=1e-11)
        np.testing.assert_allclose(q@b,c@b/c.sum(),atol=1e-12,rtol=0)


def test_zero_and_single_genotype_copy_neutral_support():
    first,grid,_,_=fixed_support_problem(capacity=32,ovule_budget=8.)
    zero=np.zeros_like(first)
    np.testing.assert_array_equal(neutral_child_genotype_law(zero,grid),zero)
    for n in (1,32):
        current=zero.copy()
        current[int(np.flatnonzero(first)[0])]=n
        q=neutral_child_genotype_law(current,grid)
        np.testing.assert_allclose(q.sum(),1.,atol=1e-12)
    with pytest.raises(ValueError):
        neutral_child_genotype_law(np.array([1,-1]),grid)


@pytest.mark.parametrize("budget",[3.,8.])
def test_eight_generation_neutral_counterfactual_provenance_and_pairing(budget):
    r=run_neutral_control(budget=budget,draws=32,seed=142)
    c=r["conditions"]
    assert c["K"]==32 and c["mutation_rate"]==0
    assert c["generations"]==8 and c["old_visitor_history"]==26110601
    assert c["independent_visitor_histories"]==1
    assert c["canonical_source_biology_edited"] is False
    assert c["confirmatory_cohorts_used"] is False
    assert c["neutral_control_intentionally_different_reproductive_operator"] is True
    assert c["neutral_census_forced_to_source_same_trajectory"] is True
    assert r["same_realized_census_each_year"] is True
    assert len(r["per_generation"])==8
    assert c["n_source_survivors"]+c["n_source_extinct"]==32
    if c["n_source_survivors"]:
        s=r["source_survivor_endpoint_high_allele_frequency"]["mean"]
        n=r["neutral_survivor_endpoint_high_allele_frequency"]["mean"]
        delta=r["paired_survivor_source_minus_neutral"]["mean"]
        np.testing.assert_allclose(np.asarray(s)-n,delta,atol=1e-12,rtol=0)
        for frequencies in (s,n):
            assert len(frequencies)==3
            assert np.all(np.asarray(frequencies)>=0)
            assert np.all(np.asarray(frequencies)<=1)
    for i,step in enumerate(r["per_generation"]):
        assert step["generation"]==i+1
        assert step["survived"]<=step["started"]
        np.testing.assert_allclose(step["neutral_expected_direction"],0.)


def test_scope_refuses_outside_confirmatory_mode():
    with pytest.raises(ValueError):
        run_neutral_control(budget=4.,draws=32)
    with pytest.raises(ValueError):
        run_neutral_control(budget=8.,draws=3)
