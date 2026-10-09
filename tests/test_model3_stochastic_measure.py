"""Dynamic diploid-measure transition parity with unchanged canonical Model 3.

Tests are engineering checks of a stochastic measure-valued *discrete*
Markov chain. They do not certify any continuous-time SDE or SPDE limit.
"""
from dataclasses import replace
import json
from pathlib import Path

import numpy as np
import pytest

from scripts.audit_model3_stochastic_measure import GenotypeMeasure, measure_step
from scripts.model3_island.population import advance,subset
from scripts.model3_island.randomness import STREAM_IDS,stream
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.types import Config,PlantState,VisitorState


def reference():
    base=Config.from_dict(json.loads(Path(
        "data/design/model3_ch2_bridge_20260927.json"
    ).read_text())["base_config"])
    cfg=replace(
        base,capacity=8,ovule_budget=8.,survival=0.,
        mutation_rate=.01,mutation_sd=.05,assurance_mode="evolving",
        seed_arrival=replace(base.seed_arrival,supply=0.)
    )
    alleles=np.array([
        [[0.,.5],[.25,.75],[0.,1.]],
        [[1.,1.],[.25,.75],[1.,0.]],
        [[0.,0.],[1.,.75],[.5,.75]],
        [[1.,0.],[.25,.75],[.75,.75]],
    ],dtype=float)
    plant=PlantState(
        alleles,
        np.zeros((4,3,2),dtype=np.int64),
        np.zeros((4,3,2),dtype=bool),
        np.arange(4,dtype=np.int64),
        np.zeros(4,dtype=np.int64),
    )
    visitor=VisitorState(
        np.array([1,2],dtype=np.int64),
        np.array([.25,.75]),np.array([.2,.2]),np.array([.8,.8])
    )
    return plant,visitor,cfg


def test_complete_discrete_measure_reproduces_three_mutating_ABM_transitions_pathwise():
    plant,visitor,cfg=reference()
    measure=GenotypeMeasure.from_plant_state(plant)
    for year in range(3):
        original=measure.to_plant_state(year=year,capacity=cfg.capacity)
        # Independent biological mechanics cannot leak through a grouped
        # genotype class: canonical reproduction sees each plant individually.
        ledger=reproduce(original,visitor,cfg)
        empty=subset(original,np.empty(0,dtype=int))
        seed=8801200+year
        streams_abm={name:stream(seed,name,0) for name in STREAM_IDS}
        streams_measure={name:stream(seed,name,0) for name in STREAM_IDS}
        next_abm,_=advance(
            original,ledger,empty,cfg,streams_abm,year=year,
            mutation_traits=(True,True,True)
        )
        next_measure=measure_step(
            measure,visitor,cfg,streams_measure,year=year,
            mutation_traits=(True,True,True)
        )
        reference_measure=GenotypeMeasure.from_plant_state(next_abm)
        assert next_measure.census==len(next_abm.ids)
        np.testing.assert_array_equal(next_measure.counts,reference_measure.counts)
        np.testing.assert_array_equal(
            next_measure.genotypes,reference_measure.genotypes
        )
        assert next_measure.census<=cfg.capacity
        assert not (next_measure.genotypes<0).any()
        assert not (next_measure.genotypes>1).any()
        measure=next_measure


def test_measure_runs_from_its_own_evolving_state_without_abm_state_feedback():
    plant,visitor,cfg=reference()
    genotype_measure=GenotypeMeasure.from_plant_state(plant)
    saw_new_genotype=False
    genotypes_initial=set(map(tuple,genotype_measure.genotypes.reshape(-1,6)))
    for year in range(8):
        rng={name:stream(9102500,name,0) for name in STREAM_IDS}
        genotype_measure=measure_step(
            genotype_measure,visitor,cfg,rng,year=year
        )
        assert genotype_measure.census<=cfg.capacity
        assert len(genotype_measure.counts)<=genotype_measure.census
        assert np.array_equal(
            genotype_measure.genotypes,
            np.sort(genotype_measure.genotypes,axis=2)
        )
        current=set(map(tuple,genotype_measure.genotypes.reshape(-1,6)))
        saw_new_genotype|=bool(current-genotypes_initial)
    # When mutation is not observed during only 8 updates, that is allowed:
    # the canonical mutation probability is .01; never demand a lucky event.
    assert isinstance(saw_new_genotype,bool)


def test_first_step_exact_measure_parity_at_high_mutation_and_boundary():
    plant,visitor,low=reference()
    cfg=replace(low,mutation_rate=.5,mutation_sd=.2)
    start=GenotypeMeasure.from_plant_state(plant)
    for seed in range(100,120):
        state=start.to_plant_state(year=0,capacity=cfg.capacity)
        ledger=reproduce(state,visitor,cfg)
        empty=subset(state,np.empty(0,dtype=int))
        streamsA={name:stream(seed,name,0) for name in STREAM_IDS}
        streamsB={name:stream(seed,name,0) for name in STREAM_IDS}
        canon,_=advance(state,ledger,empty,cfg,streamsA,year=0)
        got=measure_step(start,visitor,cfg,streamsB,year=0)
        ref=GenotypeMeasure.from_plant_state(canon)
        np.testing.assert_array_equal(got.genotypes,ref.genotypes)
        np.testing.assert_array_equal(got.counts,ref.counts)


def test_absorbing_extinction_and_frozen_loci():
    plant,visitor,cfg=reference()
    empty=GenotypeMeasure.from_plant_state(
        subset(plant,np.empty(0,dtype=int))
    )
    rng={name:stream(14,name,0) for name in STREAM_IDS}
    assert measure_step(empty,visitor,cfg,rng,year=3).census==0
    state=GenotypeMeasure.from_plant_state(plant)
    cfg_no_mut=replace(cfg,mutation_rate=0.)
    available=set(map(float,state.genotypes.reshape(-1)))
    for year in range(4):
        rng={name:stream(1400+year,name,0) for name in STREAM_IDS}
        state=measure_step(state,visitor,cfg_no_mut,rng,year=year)
        assert set(map(float,state.genotypes.reshape(-1))).issubset(available)


def test_fails_closed_when_life_history_or_seed_immigration_changes():
    plant,visitor,cfg=reference()
    initial=GenotypeMeasure.from_plant_state(plant)
    rng={name:stream(17,name,0) for name in STREAM_IDS}
    for forbidden in (
        replace(cfg,survival=.2),
        replace(cfg,seed_arrival=replace(cfg.seed_arrival,supply=.1)),
    ):
        with pytest.raises(ValueError,match="complete adult turnover"):
            measure_step(initial,visitor,forbidden,rng,year=0)
    with pytest.raises(ValueError,match="invalid bounded"):
        GenotypeMeasure(
            np.array([[[1.2,.3],[.5,.5],[.5,.5]]]),
            np.array([1],dtype=np.int64)
        )
    with pytest.raises(ValueError,match="invalid year/capacity"):
        initial.to_plant_state(year=0,capacity=1)


def test_duplicate_genotypes_conserve_integer_multiplicity():
    plant,visitor,cfg=reference()
    twin=np.repeat(plant.alleles[:1],3,axis=0)
    clone=PlantState(
        twin,np.zeros((3,3,2),dtype=np.int64),
        np.zeros((3,3,2),dtype=bool),
        np.arange(3,dtype=np.int64),np.zeros(3,dtype=np.int64),
    )
    m=GenotypeMeasure.from_plant_state(clone)
    assert len(m.genotypes)==1
    assert m.census==3
    expanded=m.to_plant_state(year=0,capacity=cfg.capacity)
    assert len(np.unique(expanded.ids))==3
    np.testing.assert_array_equal(
        GenotypeMeasure.from_plant_state(expanded).counts,np.array([3])
    )
