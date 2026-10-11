"""Independent binomial genetic-demographic model source invariants.

Tests use toy hand-authored random seeds 990xx, not frozen 61031001... cohort.
"""
import json
import numpy as np
import pytest

from scripts.audit_chapter2_independent_binomial_kernel import (
    STATUS,load_contract,effective_pollen,per_ovule_fates,
    analytical_gradient,_one_update,exact_paired_interval,classify_ci,
)


def test_contract_and_non_model3_source():
    d,sha=load_contract()
    assert len(sha)==64
    assert d["status"]=="ALTERNATIVE_KERNEL_INPUT_LOCK_BEFORE_RESULTS"
    assert d["grid"]["n_paths"]==2048
    assert d["grid"]["seed_first"]==61031001
    assert d["grid"]["independent_demographic_repeats"]==128
    assert d["constants"]["ovule_maturation"]==.9
    assert "not Model3" in d["model_independence"]


def test_all_ovule_fates_mass_conserved_and_mate_limited_at_n1():
    for timing in ("prior","delayed"):
        for n in (1,2,3,4,5,8,48):
            for a in (0.,.125,.5,.875,1.):
                x=per_ovule_fates(a,n,.8,timing)
                assert x.shape==(3,)
                assert np.all(x>=0) and np.all(x<=1)
                np.testing.assert_allclose(x.sum(),1.,rtol=0,atol=1e-12)
                if n==1:
                    assert x[1]==0.


def test_provable_prior_conflict_has_exact_census_boundary():
    for n in range(1,49):
        r=analytical_gradient(n,.8,"prior")
        assert r["beta_W_local"]>0
        assert np.isclose(r["beta_F"]+r["beta_P"]+r["beta_S"],
                          r["beta_W_local"],atol=1e-12,rtol=0)
        if n<=3:
            assert r["gamma_viable_seeds_group"]>0
            assert r["aligned_positive"]
        if n==4:
            assert abs(r["gamma_viable_seeds_group"])<1e-12
            assert not r["individual_favored_group_harmed"]
        if n>=5:
            assert r["gamma_viable_seeds_group"]<0
            assert r["individual_favored_group_harmed"]
    assert effective_pollen(4,.8)==pytest.approx(.6)
    for n in range(1,49):
        assert analytical_gradient(n,.4,"prior")["aligned_positive"]


def test_delayed_selfing_uses_unfilled_ovules_and_never_source_conflicts():
    for n in (1,2,4,8,48):
        for q in (.4,.8):
            v=analytical_gradient(n,q,"delayed")
            assert v["aligned_positive"] is True
            assert v["individual_favored_group_harmed"] is False
            assert v["beta_P"]==v["beta_F"]==0
            assert v["beta_W_local"]==pytest.approx(v["gamma_viable_seeds_group"])


def test_new_mendelian_genotypes_and_k_lottery_are_bounds_safe():
    original=np.array([[0,0],[0,1],[1,1],[0,1],[0,0],[0,1],[1,1],[0,1]],dtype=np.int8)
    for timing in ("prior","delayed"):
        for expression in ("heritable","frozen_expression"):
            rng=np.random.default_rng(99091)
            next_state=_one_update(original,K=8,q=.8,timing=timing,
                                   mode=expression,frozen_a=float(original.mean()),
                                   rng=rng,phi=.9,v=.6,allee=1.)
            assert next_state.ndim==2 and next_state.shape[1]==2
            assert len(next_state)<=8
            assert np.isin(next_state,[0,1]).all()
    rng=np.random.default_rng(99092)
    solo=np.array([[1,1]],dtype=np.int8)
    res=_one_update(solo,K=8,q=.8,timing="prior",mode="heritable",
                    frozen_a=1.,rng=rng,phi=.9,v=.6,allee=1.)
    assert res.shape[1]==2
    assert np.isin(res,[0,1]).all()


def test_boundary_confidence_does_not_fabricate_direction():
    z=exact_paired_interval(0,0,64)
    assert z[0]<-.05 and z[1]>.05
    assert classify_ci(z)=="inconclusive"
    assert classify_ci(exact_paired_interval(25,0,64))=="positive"
    with pytest.raises(ValueError):
        exact_paired_interval(65,0,64)
