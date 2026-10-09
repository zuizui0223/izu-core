"""Frozen-source correctness gates for nonlinear/rounding/realization audit."""
import numpy as np
import pytest

from scripts.audit_model3_k32_nonlinearity_rounding import (
    unbiased_integer_counts, exact_conditional_observables,
    realized_observables, run_decomposition,
)
from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_stochastic_bridge import genotype_count_markov_step


def test_unbiased_rounding_preserves_bounds_zeros_and_each_expectation():
    x=np.array([2.25,3.1,0.,4.65,1.])
    assert sum(x)==pytest.approx(11.)
    rng=np.random.default_rng(12345)
    samples=np.array([unbiased_integer_counts(x,rng) for _ in range(12000)])
    assert samples.shape==(12000,len(x))
    assert samples.dtype.kind in "iu"
    assert samples.min()>=0
    assert samples[:,2].max()==0
    assert samples.sum(axis=1).min()==11
    assert samples.sum(axis=1).max()==11
    np.testing.assert_allclose(samples.mean(axis=0),x,atol=.03,rtol=0)


def test_randomized_rounding_noninteger_total_and_capacity():
    rng=np.random.default_rng(44)
    x=np.array([.2,0.,1.15,30.55]) # sums to 31.9
    samples=np.array([unbiased_integer_counts(x,rng) for _ in range(8000)])
    assert samples.sum(axis=1).max()<=32
    assert np.all(np.isin(samples.sum(axis=1),[31,32]))
    np.testing.assert_allclose(samples.mean(axis=0),x,atol=.04,rtol=0)
    with pytest.raises(ValueError):
        unbiased_integer_counts(np.array([20.,13.]),rng)


def test_exact_next_genotype_and_allele_analytic_quantities_have_valid_bounds():
    initial,grid,vis,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    a=exact_conditional_observables(initial,grid,vis,cfg,0)
    assert len(a)==7
    assert 0<=a[0]<=32 and 0<=a[1]<=1
    assert 0<=a[2]<=27 and 0<=a[3]<=6
    assert np.all((a[4:]>=0)&(a[4:]<=1))
    zeros=exact_conditional_observables(np.zeros_like(initial),grid,vis,cfg,0)
    np.testing.assert_array_equal(zeros,[0.,1.,0.,6.,0.,0.,0.])
    assert realized_observables(np.zeros_like(initial),grid).tolist()==zeros.tolist()


def test_exact_analytic_one_step_is_compatible_with_finite_source_draws():
    initial,grid,vis,cfg=fixed_support_problem(capacity=32,ovule_budget=3.)
    target=exact_conditional_observables(initial,grid,vis,cfg,0)
    sampled=np.array([
        realized_observables(genotype_count_markov_step(
            initial,grid,vis,cfg,np.random.default_rng(7090+i),year=0
        ),grid) for i in range(600)
    ])
    error=np.abs(sampled.mean(axis=0)-target)
    se=sampled.std(axis=0,ddof=1)/np.sqrt(len(sampled))
    # Finite MC allows a conservative 5-sigma tolerance plus tiny zero-variance.
    assert np.all(error <= 5*se+1e-6)


@pytest.mark.parametrize("budget",[3.,8.])
def test_telescoping_components_preserve_source_scope_and_identity(budget):
    data=run_decomposition(budget=budget,draws=16,rounds=20,seed=123456)
    c=data["conditions"]
    assert c["K"]==32 and c["generations"]==8
    assert c["mutation_rate"]==0 and c["visitor_history"]==26110601
    assert c["independent_visitor_histories"]==1
    assert c["canonical_biology_modified"] is False
    assert c["prospective_confirmatory_histories_used"] is False
    assert len(data["steps"])==8
    for step in data["steps"]:
        z=step["components"]
        for k in data["outcomes"]:
            assert z["total_realized_minus_representative"][k] == pytest.approx(
                z["finite_realization_residual"][k]+
                z["population_state_distribution_contrast"][k]+
                z["rounding_convention_contrast"][k],abs=1e-10
            )
    first=data["steps"][0]
    for k in data["outcomes"]:
        assert first["components"]["population_state_distribution_contrast"][k] == pytest.approx(0.,abs=1e-9)
        assert first["components"]["rounding_convention_contrast"][k] == pytest.approx(0.,abs=1e-9)


def test_reject_bad_count_history_and_unplanned_budget():
    with pytest.raises(ValueError):
        run_decomposition(budget=4.,draws=16,rounds=16)
    with pytest.raises(ValueError):
        run_decomposition(budget=8.,draws=8,rounds=16)
