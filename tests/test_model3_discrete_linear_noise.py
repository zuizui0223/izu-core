"""Exact finite offspring law versus Gaussian one-step fluctuation on fixed support."""
import numpy as np
import pytest

from scripts.audit_model3_discrete_linear_noise import (
    BERRY_ESSEEN_C,finite_offspring_mean_clt,restricted_reference_support,
)


def test_source_model3_mating_gives_nontrivial_child_phenotype_distribution():
    values,p=restricted_reference_support()
    np.testing.assert_array_equal(values,[.25,.5,.75])
    assert len(p)==3 and (p>0).all()
    np.testing.assert_allclose(p.sum(),1.,rtol=0,atol=1e-12)


def test_exact_convolution_and_normal_error_obey_general_berry_esseen_bound():
    values,p=restricted_reference_support()
    r=finite_offspring_mean_clt(values,p,sizes=(8,16,32,64,128))
    assert r["status"]=="EXACT_DISCRETE_GENERATION_CLT_DIAGNOSTIC"
    assert r["temporal_SDE_or_SPDE_validated"] is False
    assert r["rare_allele_loss_or_whole_population_extinction_validated"] is False
    assert r["geographic_INLA_performed"] is False
    rows=r["rows"]
    assert [x["N"] for x in rows]==[8,16,32,64,128]
    assert all(0<=x["exact_gaussian_kolmogorov_distance"]<=
               x["berry_esseen_bound"]+1e-11 for x in rows)
    assert rows[-1]["exact_gaussian_kolmogorov_distance"] < (
        rows[0]["exact_gaussian_kolmogorov_distance"]
    )
    assert r["berry_esseen_conservative_constant"]==BERRY_ESSEEN_C
    for x in rows:
        assert x["sample_mean_variance"]==pytest.approx(
            r["child_trait_variance"]/x["N"],rel=1e-12
        )


def test_symmetric_binomial_example_has_nonzero_gaussian_atom_error():
    # Independent of ecological mating assumptions, validates exact polynomial
    # convolution and the left-limit correction at discrete mass atoms.
    p=np.array([.25,.50,.25])
    out=finite_offspring_mean_clt(
        np.array([.25,.5,.75]),p,sizes=(8,32,128)
    )
    assert out["child_trait_mean"]==pytest.approx(.5)
    assert all(row["exact_gaussian_kolmogorov_distance"]>0
               for row in out["rows"])


def test_invalid_distribution_and_unsupported_continuous_projection_fail_closed():
    with pytest.raises(ValueError):
        finite_offspring_mean_clt(
            np.array([.25,.5,.75]),np.array([0.,0.,1.])
        )
    with pytest.raises(ValueError):
        finite_offspring_mean_clt(
            np.array([.25,.4,.75]),np.array([.25,.5,.25])
        )
    with pytest.raises(ValueError):
        finite_offspring_mean_clt(
            np.array([.25,.5,.75]),np.array([.25,.5,.25]),sizes=(8,8)
        )
