"""Synthetic future trajectories; no admitted scientific donor is executed."""
import json
from dataclasses import replace

import numpy as np
import pytest

from scripts.model3_island.types import Config, PlantState, VisitorState
from scripts.readaptation_contract_20261019 import ROOT
from scripts.readaptation_transfer_20261019 import cohort_digest
from scripts.readaptation_futures_20261019 import run_future


def fixture(n=2, assurance=.5):
    a=np.full((n,3,2),.5); a[:,2]=assurance
    state=PlantState(a,np.arange(n*6).reshape(n,3,2),np.zeros((n,3,2),bool),
                     np.arange(n),np.zeros(n,dtype=int))
    raw=json.loads((ROOT/'data/design/model3_island_v2.json').read_text())['base_config']
    raw.update(capacity=48,years=80,assurance_mode='evolving',assurance_cost=.5,
               assurance_timing='delayed',depression=.5,ovule_budget=8,pollen_discount=0,
               mutation_rate=0,survival=0,activity=0,activity_mode='fixed')
    raw['seed_arrival']['supply']=0
    raw['visitor_arrival']['supply']=0
    return state,Config.from_dict(raw),VisitorState(np.empty(0,dtype=int),np.empty(0),np.empty(0),np.empty(0))


@pytest.mark.parametrize('n,assurance,extinction',[(0,.5,0),(2,0,1)])
def test_absorbing_extinction_retains_every_census(n,assurance,extinction):
    state,config,visitors=fixture(n,assurance)
    result=run_future(state,config,visitors,123,80)
    assert result['population'].shape==(81,)
    assert result['first_extinction']==extinction
    assert not result['population'][extinction:].any()
    assert np.isnan(result['trait_mean'][extinction:]).all()
    assert len(result['state_sha256'])==81
    assert result['assays']['80']['mean_genetic_return'] is None
    assert result['state_offsets'].shape==(82,)
    assert result['parentage_offsets'].shape==(81,)


def test_exact_replay_unaltered_cohort_and_native_parentage():
    from scripts.audit_readaptation_raw_20261019 import audit_future
    state,config,visitors=fixture()
    digest=cohort_digest(state)
    one=run_future(state,config,visitors,234,80)
    assert audit_future(one)['status']=='PASS_RAW_STATE_ARITHMETIC'
    two=run_future(state,config,visitors,234,80)
    assert cohort_digest(state)==digest==one['state_sha256'][0]
    for key,value in one.items():
        if isinstance(value,np.ndarray):
            np.testing.assert_array_equal(value,two[key])
            assert value.tobytes()==two[key].tobytes()
        else:
            assert value==two[key]
    assert set(one['state_allele_origin'].ravel())<=set(state.allele_origin.ravel())
    assert not one['state_mutation_flags'].any()
    for t in range(80):
        old=one['state_ids'][one['state_offsets'][t]:one['state_offsets'][t+1]]
        new=one['state_ids'][one['state_offsets'][t+1]:one['state_offsets'][t+2]]
        parents=one['parentage'][one['parentage_offsets'][t]:one['parentage_offsets'][t+1]]
        assert np.array_equal(parents[:,0],new)
        assert set(parents[:,1:].ravel())<=set(old)


@pytest.mark.parametrize('change',[{'assurance_mode':'fixed'},{'assurance_cost':0},
                                  {'mutation_rate':.01},{'capacity':192}])
def test_rejects_expansion_or_historical_fixed_policy(change):
    state,config,visitors=fixture()
    with pytest.raises(ValueError):
        run_future(state,replace(config,**change),visitors,123,80)


def test_rejects_wrong_horizon_and_immigration():
    state,config,visitors=fixture()
    with pytest.raises(ValueError):
        run_future(state,config,visitors,123,79)
    with pytest.raises(ValueError):
        run_future(state,replace(config,seed_arrival=replace(config.seed_arrival,supply=1)),visitors,123,80)


def test_destination_validation_and_nonzero_service():
    state,config,_=fixture()
    visitors=VisitorState(np.arange(6),np.full(6,.7),np.full(6,.2),np.ones(6))
    config=replace(config,activity=.25)
    result=run_future(state,config,visitors,345,80)
    assert result['reproductive'][0,1]>0
    assert result['config']['activity']==.25
    assert result['visitors']['optima']==[.7]*6
    with pytest.raises(ValueError):
        run_future(state,replace(config,activity=.5),visitors,345,80)
    with pytest.raises(ValueError):
        run_future(state,config,replace(visitors,optima=np.full(6,.6)),345,80)
