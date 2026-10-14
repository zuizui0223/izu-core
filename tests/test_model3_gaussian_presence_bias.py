"""Exact genotype class presence vs projected Gaussian integer sampling.

All analytic expectations use the canonical full-joint three-locus child law;
there is no external biological data and no SDE/SPDE validity assertion.
"""
import numpy as np
import pytest

from scripts.audit_model3_gaussian_presence_bias import (
    exact_expected_richness, exact_child_genotype_law,
    projected_gaussian_presence_audit,
)


def test_exact_class_presence_formula_handles_absent_and_certain_types():
    q=np.array([0.,.02,.18,.80])
    for n in (1,8,32):
        r=exact_expected_richness(q,n)
        np.testing.assert_allclose(
            r["probability_present"],1-(1-q)**n,
            atol=1e-12,rtol=0
        )
        assert r["probability_present"][0]==0
        assert r["expected_n_genotype_classes"]==pytest.approx(
            np.sum(1-(1-q)**n),abs=1e-12
        )
    r=exact_expected_richness(np.array([0.,1.]),8)
    assert r["expected_n_genotype_classes"]==pytest.approx(1)


def test_analytic_class_richness_agrees_with_separate_exact_sampling():
    q=np.array([.01,.19,.30,.50])
    exact=exact_expected_richness(q,8)
    rng=np.random.default_rng(3381)
    counts=rng.multinomial(8,q,size=8000)
    observed=np.count_nonzero(counts,axis=1).mean()
    assert abs(observed-exact["expected_n_genotype_classes"])<.04


def test_source_probability_is_a_full_joint_diploid_law():
    for k in (8,32,128):
        q=exact_child_genotype_law(capacity=k,ovule_budget=8.)
        assert q.shape==(27,)
        assert (q>=0).all()
        assert q.sum()==pytest.approx(1,abs=1e-12)


def test_projected_gaussian_audit_has_finite_mc_uncertainty_and_no_promotion():
    r=projected_gaussian_presence_audit(
        capacity=8,ovule_budget=8.,draws=2048,seed=20261009
    )
    assert r["status"]=="PROJECTED_GAUSSIAN_GENOTYPE_PRESENCE_FIDELITY_AUDIT"
    assert r["simulation_repeats_projected_only"]==2048
    assert r["full_spde_validated"] is False
    assert r["original_biology_mutated"] is False
    assert r["genotype_classes"]==27
    assert 0<=r["projected_gaussian_mean_richness"]<=8
    assert 0<=r["exact_multinomial_expected_richness"]<=8
    assert 0<=r["max_abs_genotype_presence_probability_difference"]<=1
    assert np.isfinite(r["projected_gaussian_mean_richness_mc_se"])
    assert np.isfinite(r["richness_difference_projected_minus_exact"])


def test_presence_audit_rejects_undeclared_or_underpowered_sweeps():
    with pytest.raises(ValueError):
        projected_gaussian_presence_audit(capacity=9)
    with pytest.raises(ValueError):
        projected_gaussian_presence_audit(draws=10)
    with pytest.raises(ValueError):
        exact_expected_richness(np.array([-.1,1.1]),8)
