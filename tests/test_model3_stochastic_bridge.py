"""Frozen-biology one-generation stochastic bridge; no new visitor histories.

These tests compare the analytic restricted SDE moment target with *real*
canonical Model 3 advance(), and check a genotype-frequency SPDE noise kernel.
The test is a one-generation engineering validation, not a new ecological
confirmation and not a continuous-time convergence proof.
"""
from dataclasses import replace
import json
from pathlib import Path

import numpy as np
import pytest

from scripts.audit_model3_stochastic_bridge import (
    capped_poisson_distribution,
    draw_exact_frequency,
    draw_one_step_census,
    exact_one_step_trait_moments,
    frequency_noise_covariance,
    offspring_genotype_distribution,
    parent_pair_probabilities,
)
from scripts.model3_island.density import make_grid
from scripts.model3_island.population import advance, subset
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.model3_island.types import Config, PlantState, VisitorState


def reference_case(budget=0.25, n=4):
    source = json.loads(Path(
        "data/design/model3_ch2_bridge_20260927.json"
    ).read_text(encoding="utf-8"))
    base = Config.from_dict(source["base_config"])
    cfg = replace(
        base, capacity=8, survival=0., mutation_rate=0.,
        ovule_budget=float(budget), assurance_mode="evolving",
        seed_arrival=replace(base.seed_arrival, supply=0.),
    )
    a = np.array([
        [[.25,.75],[.25,.25],[.75,.75]],
        [[.75,.75],[.25,.75],[.25,.25]],
        [[.25,.25],[.75,.75],[.25,.75]],
        [[.25,.75],[.75,.25],[.25,.75]],
    ], dtype=float)[:n]
    plant = PlantState(
        a, np.arange(n*6,dtype=np.int64).reshape(n,3,2),
        np.zeros((n,3,2),dtype=bool), np.arange(n,dtype=np.int64),
        np.zeros(n,dtype=np.int64),
    )
    visitors = VisitorState(
        np.array([1,2],dtype=np.int64),np.array([.25,.75]),
        np.array([.2,.2]),np.array([.8,.8])
    )
    grid = make_grid(([.25,.75],)*3)
    ledger = reproduce(plant, visitors, cfg)
    return plant, ledger, cfg, grid


def test_poisson_cap_and_extinction_probability():
    p = capped_poisson_distribution(1.8, 8)
    assert p.shape == (9,)
    assert p.sum() == pytest.approx(1, abs=1e-12)
    assert p[0] == pytest.approx(np.exp(-1.8))
    assert capped_poisson_distribution(0, 8)[0] == 1
    assert capped_poisson_distribution(100, 8)[-1] == pytest.approx(1)
    with pytest.raises(ValueError):
        capped_poisson_distribution(-1, 8)


@pytest.mark.parametrize("budget", [0.25, 2.0])
def test_exact_offspring_trait_moments_match_full_mendelian_genotype_law(budget):
    plant, ledger, config, grid = reference_case(budget)
    w,_ = parent_pair_probabilities(plant,ledger,config)
    q = offspring_genotype_distribution(plant,w,grid)
    expected = exact_one_step_trait_moments(plant,ledger,config)
    genotypes = grid.genotypes.mean(axis=2)
    mu = q @ genotypes
    covariance = ((genotypes-mu).T * q)@(genotypes-mu)
    np.testing.assert_allclose(expected["offspring_mean"],mu,rtol=0,atol=1e-12)
    np.testing.assert_allclose(expected["offspring_covariance"],covariance,rtol=0,atol=1e-12)
    assert expected["probability_extinct"] == pytest.approx(
        np.exp(-expected["recruitment_intensity"])
    )
    assert expected["continuous_time_sde_validated"] is False


def test_restricted_analytic_moments_against_actual_canonical_abm():
    plant, ledger, config, _ = reference_case(0.25)
    expected = exact_one_step_trait_moments(plant,ledger,config)
    candidates = subset(plant, np.empty(0,dtype=int))
    observed = []
    extinct = 0
    for s in range(1024):
        master = s + 92107001
        streams = {name:stream(master,name,0) for name in STREAM_IDS}
        new,_ = advance(
            plant,ledger,candidates,config,streams,year=0,
            mutation_traits=(True,True,True)
        )
        if len(new.ids):
            observed.append(new.alleles.mean(axis=(0,2)))
        else:
            extinct += 1
    # Conservative Monte Carlo tolerances for 1024 independent samples.
    assert abs(extinct/1024-expected["probability_extinct"]) < 0.075
    assert len(observed) > 30
    np.testing.assert_allclose(
        np.mean(observed,axis=0),
        expected["occupied_population_trait_mean"], rtol=0, atol=0.035,
    )
    empirical = np.cov(np.asarray(observed).T)
    predicted = np.array(expected["occupied_trait_mean_covariance"])
    np.testing.assert_allclose(empirical,predicted,rtol=0,atol=0.020)


def test_spde_noise_precursor_conserves_mass_and_allele_covariance():
    plant,ledger,config,grid=reference_case(2.0)
    w,_=parent_pair_probabilities(plant,ledger,config)
    q=offspring_genotype_distribution(plant,w,grid)
    cov=frequency_noise_covariance(q,8)
    assert cov.shape==(27,27)
    assert np.linalg.eigvalsh(cov).min()>-1e-12
    np.testing.assert_allclose(cov@np.ones(len(q)),0,rtol=0,atol=1e-12)
    assert np.max(cov-np.diag(np.diag(cov)))<=1e-12
    rng=np.random.default_rng(914)
    samples=np.array([draw_exact_frequency(q,8,rng) for _ in range(2048)])
    assert np.all(samples>=0)
    np.testing.assert_allclose(samples.sum(axis=1),1,rtol=0,atol=1e-12)
    np.testing.assert_allclose(samples.mean(axis=0),q,rtol=0,atol=.025)
    np.testing.assert_allclose(np.cov(samples.T),cov,rtol=0,atol=.006)


def test_markov_frequency_kernel_reports_extinction_as_missing():
    plant,ledger,config,grid=reference_case(0.25)
    rng=np.random.default_rng(20261009)
    cells=[draw_one_step_census(plant,ledger,config,rng,grid) for _ in range(400)]
    for n,q in cells:
        assert 0<=n<=config.capacity
        if n==0:
            assert q is None
        else:
            assert q is not None and np.isclose(q.sum(),1)
            assert (q>=0).all()


def test_fail_closed_when_assumptions_do_not_hold():
    plant,ledger,config,grid=reference_case()
    for wrong in (
        replace(config,survival=0.5),
        replace(config,mutation_rate=0.01),
        replace(config,seed_arrival=replace(config.seed_arrival,supply=0.1)),
    ):
        with pytest.raises(ValueError,match="restricted exact kernel"):
            exact_one_step_trait_moments(plant,ledger,wrong)
    w,_=parent_pair_probabilities(plant,ledger,config)
    off_grid=make_grid(([0.,1.],)*3)
    with pytest.raises(ValueError,match="cannot silently project"):
        offspring_genotype_distribution(plant,w,off_grid)
    with pytest.raises(ValueError):
        frequency_noise_covariance(np.array([.5,.5]),0)
