"""Exploratory Gaussian genotype projection decomposed into clipping and rounding."""
import numpy as np
import pytest
from scripts.audit_model3_gaussian_projection_mechanism import dissect_projection


def test_gaussian_projection_decomposition_adds_to_total_bias():
    res=dissect_projection(capacity=8,draws=2048)
    assert res["status"]=="POST_OUTCOME_EXPLORATORY_GAUSSIAN_PROJECTION_MECHANISM"
    assert res["post_outcome_exploratory"] is True
    assert res["full_SDE_SPDE_validated"] is False
    assert res["biology_unmodified"] is True
    assert res["no_INLA_geographic"] is True
    lhs=res["bias_from_gaussian_clip_normalize_before_rounding"]+res[
        "additional_richness_shift_due_to_deterministic_integer_rounding"
    ]
    assert lhs==pytest.approx(res["total_largest_remainder_minus_exact"],
                              abs=1e-12)
    assert 0<=res["fraction_gaussian_draws_with_any_negative_genotype_count"]<=1
    assert 0<=res["mean_clipped_negative_mass"]
    assert res["se_total_largest_remainder"]>=0
    assert res["se_paired_rounding_effect"]>=0


def test_multinomial_readout_is_an_expectation_not_extra_sampling():
    # A fixed p=(1/2,1/2) with n=2 yields exact expected richness 1.5.
    p=np.array([.5,.5])
    expected=-np.expm1(2*np.log1p(-p))
    assert expected.sum()==pytest.approx(1.5)
    # But largest-remainder on integer counts (1,1) gives richness 2.
    integer=np.floor(2*p).astype(int)
    assert (integer>0).sum()==2


def test_projection_mechanism_sweep_is_restricted_and_nonpromoting():
    with pytest.raises(ValueError):
        dissect_projection(capacity=9)
    with pytest.raises(ValueError):
        dissect_projection(draws=12)
