"""Post-outcome numeric controls for Gaussian frequency clipping + resampling.

This is an exploration of one imperfect implementation and explicitly
does not validate mutation-enabled Model 3 SDE/SPDE dynamics.
"""
import numpy as np
import pytest

from scripts.audit_model3_stochastic_rounding_ablation import (
    gaussian_clipped_simplex, stochastic_gaussian_count,
    conditional_one_step_ablation, independent_horizon_comparison,
)


def test_clipped_gaussian_is_normalized_and_zero_support_is_absorbing():
    q=np.array([.001,.199,.3,.5,0.,0.],dtype=float)
    rng=np.random.default_rng(321)
    for n in (8,32,128):
        for _ in range(12):
            p=gaussian_clipped_simplex(q,n,rng)
            assert (p>=0).all()
            assert p.sum()==pytest.approx(1,abs=1e-12)
            np.testing.assert_array_equal(p[-2:],[0.,0.])
            c=stochastic_gaussian_count(q,n,rng)
            assert c.shape==q.shape
            assert c.sum()==n
            assert (c>=0).all()
            np.testing.assert_array_equal(c[-2:],[0,0])
    assert stochastic_gaussian_count(q,0,rng).sum()==0
    with pytest.raises(ValueError):
        gaussian_clipped_simplex(np.array([.2,.7]),8,rng)


def test_one_step_richness_decomposition_matches_paired_law():
    r=conditional_one_step_ablation(N=8,draws=2048,seed=20261009)
    assert r["N"]==8
    assert r["draws"]==2048
    assert r["genotype_classes"]==27
    assert r["exact_richness"]>0
    lhs=r["gaussian_clip_plus_largest_remainder_richness"]
    rhs=r["gaussian_clip_plus_multinomial_readout_expected_richness"]+r["paired_rounding_shift"]
    assert lhs==pytest.approx(rhs,abs=1e-12)
    assert 0<r["trace_canonical_frequency_covariance"]<1
    assert 0<=r["trace_conditional_multinomial_component"]
    assert r["trace_extra_gaussian_simplex_variation"]>=-1e-12
    assert r["trace_total_gaussian_plus_multinomial_frequency_covariance"]==pytest.approx(
        r["trace_conditional_multinomial_component"]+
        r["trace_extra_gaussian_simplex_variation"],abs=1e-12
    )


def test_conditional_variance_shows_extra_shock_without_faking_exact_law():
    # In the neutral q=(.5,.5) control, a random simplex P creates
    # between-P variation *on top of* conditional binomial sampling.
    q=np.array([.5,.5])
    n=16
    rng=np.random.default_rng(58)
    conditional=np.empty(6000)
    draws=np.empty(6000)
    for i in range(len(draws)):
        p=gaussian_clipped_simplex(q,n,rng)
        conditional[i]=p[0]
        draws[i]=stochastic_gaussian_count(q,n,rng)[0]/n
    assert conditional.var(ddof=1)>0
    # Additional conditional sampling injects noise, although the two
    # independently sampled arms are not paired exactly.
    assert draws.var(ddof=1)>conditional.var(ddof=1)*.95


@pytest.mark.parametrize("case",[(8,3,3.),(8,8,3.),(32,3,8.)])
def test_independent_multigeneration_comparison_preserves_scope(case):
    k,h,b=case
    r=independent_horizon_comparison(
        K=k,years=h,budget=b,draws=256,seed=20261009
    )
    assert r["status"]=="EXPLORATORY_GAUSSIAN_MULTINOMIAL_MULTIGENERATION_ERROR"
    assert r["joint_diploid_genotypes"]==27
    assert r["post_outcome_exploratory"] is True
    assert r["continuous_time_sde_or_spde_validated"] is False
    assert r["model3_reproduction_unchanged"] is True
    assert r["natural_INLA_used"] is False
    assert 0<=r["absolute_occupancy_difference"]<=1
    assert 0<=r["absolute_mean_class_richness_difference"]<=k


def test_incorrect_sweep_inputs_fail():
    with pytest.raises(ValueError):
        conditional_one_step_ablation(N=12)
    with pytest.raises(ValueError):
        independent_horizon_comparison(K=8,years=10,budget=3.)
