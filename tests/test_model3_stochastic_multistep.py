"""Check restricted 3-update stochastic bridge against canonical finite ABM.

This is a distributional engineering comparison, not an independent visitor
history campaign, a proof of global process equivalence, or SDE/SPDE fidelity.
"""
from dataclasses import replace
import json
from pathlib import Path

import numpy as np
import pytest

from scripts.audit_model3_stochastic_multistep import exact_markov_step
from scripts.model3_island.density import make_grid
from scripts.model3_island.population import advance,subset
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.randomness import stream,STREAM_IDS
from scripts.model3_island.types import Config,PlantState,VisitorState


def fixture():
    d=json.loads(Path("data/design/model3_ch2_bridge_20260927.json").read_text())
    base=Config.from_dict(d["base_config"])
    cfg=replace(base,capacity=8,survival=0.,mutation_rate=0.,
                ovule_budget=2.5,assurance_mode="evolving",
                seed_arrival=replace(base.seed_arrival,supply=0.))
    alleles=np.array([
        [[.25,.75],[.25,.25],[.75,.75]],
        [[.75,.75],[.25,.75],[.25,.25]],
        [[.25,.25],[.75,.75],[.25,.75]],
        [[.25,.75],[.75,.25],[.25,.75]],
    ])
    state=PlantState(
        alleles,np.zeros((4,3,2),dtype=np.int64),
        np.zeros((4,3,2),dtype=bool),np.arange(4,dtype=np.int64),
        np.zeros(4,dtype=np.int64))
    visitor=VisitorState(
        np.array([1,2],dtype=np.int64),
        np.array([.25,.75]),np.array([.2,.2]),
        np.array([.8,.8]))
    grid=make_grid(([.25,.75],)*3)
    return state,visitor,cfg,grid


def test_exact_markov_bridge_three_generations_matches_canonical_abm():
    founders,visitor,config,grid=fixture()
    n_trials=384
    occupancy_a,occupancy_b=[],[]
    size_a,size_b=[],[]
    means_a,means_b=[],[]
    for i in range(n_trials):
        original=founders
        alternative=founders
        streams={name:stream(i+20261009,name,0) for name in STREAM_IDS}
        rng=np.random.default_rng(i+220261009)
        for year in range(3):
            ledger=reproduce(original,visitor,config)
            empty=subset(original,np.empty(0,dtype=int))
            original,_=advance(original,ledger,empty,config,streams,year=year)
            alternative=exact_markov_step(
                alternative,visitor,config,grid,rng,year=year)
        na,nb=len(original.ids),len(alternative.ids)
        occupancy_a.append(bool(na));occupancy_b.append(bool(nb))
        size_a.append(na);size_b.append(nb)
        if na:means_a.append(original.alleles.mean(axis=(0,2)))
        if nb:means_b.append(alternative.alleles.mean(axis=(0,2)))
    # Independent Monte Carlo cohorts compared within predeclared loose
    # engineering bounds; ecological sample is ONE fixed visitor sequence.
    assert abs(np.mean(occupancy_a)-np.mean(occupancy_b))<0.12
    assert abs(np.mean(size_a)-np.mean(size_b))<0.55
    assert len(means_a)>50 and len(means_b)>50
    np.testing.assert_allclose(
        np.mean(means_a,axis=0),np.mean(means_b,axis=0),
        rtol=0,atol=0.085
    )


def test_multistep_bridge_never_mutates_or_immigrates():
    state,visitor,config,grid=fixture()
    rng=np.random.default_rng(43)
    for invalid in (
        replace(config,mutation_rate=.01),
        replace(config,survival=.2),
        replace(config,seed_arrival=replace(config.seed_arrival,supply=.1)),
    ):
        with pytest.raises(ValueError,match="restricted bridge"):
            exact_markov_step(state,visitor,invalid,grid,rng,year=0)
    with pytest.raises(ValueError,match="support cannot silently project"):
        exact_markov_step(
            state,visitor,config,make_grid(([0.,1.],)*3),rng,year=0
        )


def test_empty_population_remains_extinct_without_immigration():
    state,visitor,config,grid=fixture()
    empty=subset(state,np.empty(0,dtype=int))
    returned=exact_markov_step(empty,visitor,config,grid,
                               np.random.default_rng(72),year=1)
    assert len(returned.ids)==0
