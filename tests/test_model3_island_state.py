from dataclasses import asdict, replace
import json

import numpy as np
import pytest

from scripts.model3_island.types import ArrivalConfig, Config, PlantState, VisitorState, History
from scripts.model3_island.randomness import stream, STREAM_IDS


def config_fixture():
    arrival=ArrivalConfig(supply=1.,distance=2.,scale=1.,kernel='exponential',
                          establishment=.5,loss_hazard=.1)
    return Config(schema_version=1,event_order='reproduce-survive-arrive-recruit-v1',
        time_unit='reproductive_year',capacity=48,years=10,survival=0.,
        ovule_budget=8.,pollen_budget=20.,investment_cost=.5,pollen_scale=1.,
        depression=.5,mutation_rate=0.,mutation_sd=.01,assurance_mode='fixed',
        fixed_assurance=.5,assurance_timing='delayed',pollen_discount=0.,assurance_cost=0.,
        activity=.4,activity_mode='fixed',reference_visitor_count=4.,background_ratio=1.,
        background_resources=1.,seed_arrival=arrival,visitor_arrival=arrival,
        island_history='founding',initial_visitors=0,visitor_breadth=.2,
        visitor_effectiveness=1.,source_allele_means=(.5,.5,.5),source_allele_sd=.1)


def plant_fixture(n=2):
    return PlantState(alleles=np.full((n,3,2),.5),allele_origin=np.zeros((n,3,2),dtype=np.int64),
        mutation_flags=np.zeros((n,3,2),dtype=bool),ids=np.arange(n,dtype=np.int64),
        birth_years=np.zeros(n,dtype=np.int64))


def test_configuration_json_roundtrip_and_explicit_fields():
    c=config_fixture()
    assert Config.from_dict(json.loads(json.dumps(asdict(c))))==c
    d=asdict(c)
    del d['depression']
    with pytest.raises(ValueError):
        Config.from_dict(d)
    d=asdict(c); d['unknown_setting']=1
    with pytest.raises(ValueError):
        Config.from_dict(d)


@pytest.mark.parametrize('change', [{'schema_version':2},{'time_unit':'generations'},
    {'capacity':True},{'years':1.1},{'survival':1.1},{'mutation_rate':-1},
    {'pollen_scale':0},{'activity':np.nan},{'visitor_effectiveness':2},
    {'source_allele_means':(.3,.5)},{'event_order':'unversioned'}])
def test_invalid_configuration_rejected(change):
    with pytest.raises(ValueError): replace(config_fixture(),**change)


def test_state_immutable_arrays_and_empty_population():
    p=plant_fixture()
    assert p.alleles.shape==(2,3,2)
    with pytest.raises(ValueError): p.alleles[0,0,0]=.8
    assert plant_fixture(0).alleles.shape==(0,3,2)
    a=np.full((2,3,2),.5)
    q=replace(p,alleles=a)
    a[:]=.1
    assert (q.alleles==.5).all()


@pytest.mark.parametrize('change',[{'alleles':np.ones((2,2,2))},
    {'ids':np.array([1,1])},{'ids':np.array([1.,2.])},
    {'allele_origin':np.full((2,3,2),-1)},{'alleles':np.full((2,3,2),1.1)},
    {'mutation_flags':np.zeros((2,3,2),dtype=int)}])
def test_invalid_plant_state_rejected(change):
    with pytest.raises(ValueError): replace(plant_fixture(),**change)


def test_visitors_and_history_lengths():
    v=VisitorState(ids=np.array([3]),optima=np.array([.5]),breadths=np.array([.2]),
                   effectiveness=np.array([1.]))
    h=History(visitors=(v,v),seed_candidates=(plant_fixture(0),plant_fixture(1)),
              event_order='reproduce-survive-arrive-recruit-v1')
    assert len(h.visitors)==2
    with pytest.raises(ValueError): replace(h,seed_candidates=())
    with pytest.raises(ValueError): replace(v,breadths=np.array([0.]))
    with pytest.raises(ValueError): replace(v,ids=np.array([3,3]))


def test_component_streams_replay_and_do_not_share_state():
    assert len(set(STREAM_IDS.values()))==len(STREAM_IDS)
    expected=stream(42,'visitor_arrivals',7).random(10)
    stream(42,'segregation',19).random(1000)
    np.testing.assert_array_equal(expected,stream(42,'visitor_arrivals',7).random(10))
    assert not np.array_equal(expected,stream(42,'mutation',7).random(10))
    with pytest.raises(ValueError): stream(42,'typo',7)
    with pytest.raises(ValueError): stream(-1,'mutation',7)
