"""Fidelity/negative gates for an optional Gaussian genotype-frequency closure.

The direct finite Model3 three-locus Mendelian genotype-count Markov kernel
is the exact-law reference. Projected Gaussian rounding is deliberately
only a numerical candidate, not a validated SDE/SPDE.
"""
import numpy as np
import pytest

from scripts.audit_model3_projected_gaussian_genotypes import (
    gaussian_integer_offspring, fixed_support_problem,
    rare_class_projection_diagnostic, horizon_distribution_comparison,
)


def test_gaussian_count_projection_preserves_simplex_and_zero_support():
    q=np.array([.01,.19,.3,.5,0.,0.])
    rng=np.random.default_rng(20261009)
    for n in (0,1,8,16,64,128):
        for _ in range(35):
            k=gaussian_integer_offspring(q,n,rng)
            assert (k>=0).all()
            assert k.dtype.kind in "iu"
            assert int(k.sum())==n
            assert np.array_equal(k[-2:],[0,0])
    with pytest.raises(ValueError):
        gaussian_integer_offspring(np.array([.3,.6]),8,rng)


def test_unconstrained_tangent_noise_has_exact_multinomial_covariance():
    # Analytic identity: epsilon_i = sqrt(N q_i) z_i - q_i sum_j sqrt(N q_j) z_j.
    q=np.array([.03,.17,.32,.48])
    n=32
    cov_target=n*(np.diag(q)-np.outer(q,q))
    rng=np.random.default_rng(314159)
    raw=np.sqrt(n*q)[None,:]*rng.normal(size=(18000,len(q)))
    noise=raw-raw.sum(axis=1,keepdims=True)*q
    np.testing.assert_allclose(noise.sum(axis=1),0,atol=1e-12,rtol=0)
    np.testing.assert_allclose(np.cov(noise.T),cov_target,
                               atol=.11,rtol=.04)


def test_restricted_diploid_problem_retains_three_locus_joint_genotypes():
    for k in (8,32):
        first,grid,visitor,cfg=fixed_support_problem(capacity=k,ovule_budget=8.)
        assert len(first)==27
        assert first.sum()==k
        assert grid.genotypes.shape==(27,3,2)
        assert cfg.mutation_rate==0
        assert cfg.survival==0


@pytest.mark.parametrize("budget",[3.,8.])
def test_multigeneration_projected_gaussian_diagnostic_is_nonpromoting(budget):
    r=horizon_distribution_comparison(
        capacity=8,budget=budget,generations=3,draws=160
    )
    assert r["status"]=="DISCRETE_GAUSSIAN_FULL_GENOTYPE_HORIZON_DIAGNOSTIC"
    assert r["gaussian_closure_approved_for_multigeneration_SPDE"] is False
    assert r["canonical_Model3_modified"] is False
    assert r["no_new_visitor_histories"] is True
    assert r["INLA_geographic_analysis_performed"] is False
    for arm in ("exact_atomic_markov","projected_gaussian"):
        assert r["arms"][arm]["n_replicates"]==160
        assert 0<=r["arms"][arm]["occupancy_probability"]<=1
        assert 0<=r["arms"][arm]["mean_genotype_classes"]<=8
        assert len(r["arms"][arm]["mean_genotype_counts"])==27


def test_rare_genotype_stress_reports_true_finite_loss_not_zero_mean_proxy():
    r=rare_class_projection_diagnostic(
        rare_q=.001,sample_n=8,draws=10000,seed=2731
    )
    assert r["exact_absence_probability"]==pytest.approx(.999**8)
    assert abs(r["empirical_multinomial_absence"]-r["exact_absence_probability"])<.01
    assert 0<=r["empirical_gaussian_projected_absence"]<=1
    assert r["expected_rare_count"]==pytest.approx(.008)
