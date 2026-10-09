"""Independent engineering gates for mutation-aware Model 3 stochastic moments.

No Model 3 source edits. Tests use the canonical reproduction and advance()
directly. The mutation stress regime is a numerical diagnosis, not a new
ecological setting or a calibrated natural mutation-rate inference.
"""
from dataclasses import replace
import json
from pathlib import Path

import numpy as np
import pytest

from scripts.audit_model3_stochastic_mutation_scaling import (
    exact_mutation_one_step_trait_moments,
    dirichlet_simplex_boundary_diagnostic,
    population_size_noise_scaling,
    reflected_allele_moments,
)
from scripts.audit_model3_stochastic_bridge import (
    exact_one_step_trait_moments, parent_pair_probabilities,
    offspring_genotype_distribution,
)
from scripts.model3_island.density import make_grid
from scripts.model3_island.history import reflect_unit
from scripts.model3_island.population import advance, subset
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.randomness import stream, STREAM_IDS
from scripts.model3_island.types import Config, PlantState, VisitorState


def fixture(rate=.01, sd=.05, capacity=8, budget=4., mode="evolving"):
    source=json.loads(Path(
        "data/design/model3_ch2_bridge_20260927.json"
    ).read_text())["base_config"]
    base=Config.from_dict(source)
    c=replace(
        base,capacity=capacity,ovule_budget=float(budget),
        survival=0., mutation_rate=float(rate),mutation_sd=float(sd),
        assurance_mode=mode,
        seed_arrival=replace(base.seed_arrival,supply=0.),
    )
    alleles=np.array([
        [[0.,.5],[.25,.75],[0.,1.]],
        [[1.,1.],[.25,.75],[1.,0.]],
        [[0.,0.],[1.,.75],[.5,.75]],
        [[1.,0.],[.25,.75],[.75,.75]],
    ],dtype=float)
    state=PlantState(
        alleles, np.zeros((4,3,2),dtype=np.int64),
        np.zeros((4,3,2),dtype=bool),
        np.arange(4,dtype=np.int64),np.zeros(4,dtype=np.int64)
    )
    visitor=VisitorState(
        np.array([1,2],dtype=np.int64),
        np.array([.25,.75]),
        np.array([.2,.2]),
        np.array([.8,.8])
    )
    return state,visitor,c


@pytest.mark.parametrize("x",[0.,0.25,0.5,0.75,1.])
def test_reflected_mutation_integral_matches_canonical_sampling(x):
    rate,sd=.5,.2
    mu,second=reflected_allele_moments(x,rate,sd)
    rng=np.random.default_rng(299100+int(100*x))
    sampled=np.full(75000,x,dtype=float)
    changed=rng.random(len(sampled))<rate
    sampled[changed]=reflect_unit(
        sampled[changed]+rng.normal(0,sd,changed.sum())
    )
    assert abs(sampled.mean()-mu)<.004
    assert abs(np.mean(sampled**2)-second)<.004
    if x==0:
        assert mu>0
    if x==1:
        assert mu<1


def test_mutation_zero_reduces_to_original_mendelian_moment_kernel():
    state,visitor,c=fixture(rate=0.)
    ledger=reproduce(state,visitor,c)
    zero=exact_one_step_trait_moments(state,ledger,c)
    with_mutation=exact_mutation_one_step_trait_moments(state,ledger,c)
    np.testing.assert_allclose(zero["offspring_mean"],
                               with_mutation["offspring_mean"],atol=1e-12,rtol=0)
    np.testing.assert_allclose(zero["offspring_covariance"],
                               with_mutation["offspring_covariance"],atol=1e-12,rtol=0)
    np.testing.assert_allclose(zero["occupied_trait_mean_covariance"],
                               with_mutation["occupied_population_trait_mean_covariance"],
                               atol=1e-12,rtol=0)


def test_mutating_one_generation_moments_vs_canonical_ABM():
    state,visitor,c=fixture(rate=.5,sd=.2,budget=4.)
    ledger=reproduce(state,visitor,c)
    target=exact_mutation_one_step_trait_moments(state,ledger,c)
    empty=subset(state,np.empty(0,dtype=int))
    seen=[]
    extinct=0
    for r in range(2048):
        streams={name:stream(88101000+r,name,0) for name in STREAM_IDS}
        new,_=advance(
            state,ledger,empty,c,streams,year=0,
            mutation_traits=(True,True,True)
        )
        if len(new.ids):
            seen.append(new.alleles.mean(axis=(0,2)))
        else:
            extinct+=1
    assert len(seen)>100
    assert abs(extinct/2048-target["probability_extinct"])<.06
    np.testing.assert_allclose(
        np.asarray(seen).mean(axis=0),
        target["occupied_population_trait_mean"],
        atol=.025,rtol=0
    )
    np.testing.assert_allclose(
        np.cov(np.asarray(seen).T),
        target["occupied_population_trait_mean_covariance"],
        atol=.014,rtol=0
    )
    assert target["allele_grid_projection_used"] is False


def test_mutation_mask_and_fixed_assurance_enforced_at_birth():
    state,visitor,c=fixture(rate=.4,sd=.15)
    l=reproduce(state,visitor,c)
    zero=exact_mutation_one_step_trait_moments(
        state,l,replace(c,mutation_rate=0.)
    )
    mask=exact_mutation_one_step_trait_moments(
        state,l,c,mutation_traits=(False,False,False)
    )
    np.testing.assert_allclose(zero["offspring_mean"],mask["offspring_mean"],atol=1e-12)
    np.testing.assert_allclose(
        zero["offspring_covariance"],mask["offspring_covariance"],atol=1e-12
    )
    fixed=replace(c,assurance_mode="fixed",fixed_assurance=.5)
    lf=reproduce(state,visitor,fixed)
    active=exact_mutation_one_step_trait_moments(state,lf,fixed)
    frozen=exact_mutation_one_step_trait_moments(
        state,lf,fixed,mutation_traits=(True,True,False)
    )
    np.testing.assert_allclose(active["offspring_mean"],frozen["offspring_mean"],atol=1e-12)
    np.testing.assert_allclose(
        active["offspring_covariance"],frozen["offspring_covariance"],atol=1e-12
    )


def test_conditional_sample_size_covariance_exactly_inverse_N_and_empirical():
    state,visitor,c=fixture(rate=0.)
    l=reproduce(state,visitor,c)
    w,_=parent_pair_probabilities(state,l,c)
    # No genotype grid projection: exact founding support includes 0,.25,
    # .5,.75,1; test only a small *sparse* genotype probability vector.
    q=np.array([.12,.28,.32,.28])
    out=population_size_noise_scaling(q,sizes=(8,16,32,64,128))
    cov_ref=np.diag(q)-np.outer(q,q)
    rng=np.random.default_rng(261009)
    for row in out["scale"]:
        n=row["N"]
        draws=rng.multinomial(n,q,size=2500)/n
        observed=np.cov(draws.T)
        target=cov_ref/n
        np.testing.assert_allclose(
            np.diag(observed),np.diag(target),
            atol=.012/n,rtol=.16
        )
        assert row["trace_covariance"]==pytest.approx(
            np.trace(cov_ref)/n,rel=1e-12
        )
    assert out["geographic_INLA_performed"] is False


def test_scaling_is_conditional_not_a_capacity_experiment():
    q=np.array([.02,.98])
    out=population_size_noise_scaling(q,sizes=(8,64,192))
    v=[r["trace_covariance"] for r in out["scale"]]
    assert v[0]/v[1]==pytest.approx(8.)
    assert v[1]/v[2]==pytest.approx(3.)
    risks=[r["negative_frequency_probability_lower_bound"]
           for r in out["scale"]]
    assert risks[0]>=risks[1]>=risks[2]>0
    with pytest.raises(ValueError):
        population_size_noise_scaling(q,sizes=(8,8))
    with pytest.raises(ValueError):
        reflected_allele_moments(1.1,.01,.05)

def test_mutation_conditioned_three_generation_old_history_preflight():
    from scripts.run_model3_mutation_multistep_preflight import (
        run_mutation_multistep_preflight,
    )
    receipt=run_mutation_multistep_preflight(
        n_draws=256,updates=3,mutation_rate=.01,mutation_sd=.05
    )
    assert receipt["status"]=="OLD_HISTORY_MUTATION_THREE_UPDATE_CONDITIONAL_GATES_PASS"
    assert len(receipt["results"])==3
    assert receipt["independent_visitor_histories"]==1
    assert receipt["new_visitor_histories_drawn"]==0
    assert receipt["canonical_Model3_modified"] is False
    assert receipt["full_multigeneration_SDE_validated"] is False
    assert receipt["full_trait_space_SPDE_validated"] is False
    assert receipt["geographic_INLA_performed"] is False

def test_simplex_covariance_matching_cannot_reproduce_rare_genotype_loss():
    q=np.array([.02,.98])
    result=dirichlet_simplex_boundary_diagnostic(
        q,8,draws=12000,seed=20261009
    )
    assert result["status"]=="moment_matched_simplex_but_genetic_loss_not_reproduced"
    assert result["theoretical_multinomial_absence_probability"]==pytest.approx(.98**8)
    assert result["empirical_multinomial_absence_probability"]>.80
    assert result["empirical_dirichlet_absence_probability"]==0.
    assert result["max_empirical_dirichlet_mean_error"]<.025
    assert result["max_empirical_dirichlet_covariance_error"]<.005
    assert result["formal_dirichlet_and_multinomial_first_two_moments_equal"] is True
    assert result["full_SPDE_genetic_loss_validated"] is False
    with pytest.raises(ValueError,match="N>=2"):
        dirichlet_simplex_boundary_diagnostic(q,1)
