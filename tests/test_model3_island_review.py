"""Reproductions of the five findings from the independent whole-branch review."""
from dataclasses import replace
import numpy as np

from test_model3_island_state import config_fixture,plant_fixture
from test_model3_island_assays import visitors
from test_model3_island_summary import record
from scripts.model3_island.types import History
from scripts.model3_island.density import make_grid
from scripts.model3_island.simulate import simulate
from scripts.model3_island.run import history_from_spec
from scripts.model3_island.campaign import build_design
from scripts.model3_island.summarize import summarize,paired_contrast


def test_realized_parentage_and_selfed_recruits_are_preserved():
    c=replace(config_fixture(),years=3,capacity=4,fixed_assurance=1.,ovule_budget=100.)
    h=History((visitors(0),)*3,(plant_fixture(0),)*3,c.event_order)
    r=simulate(c,h,plant_fixture(4),replicate=18,grid=make_grid(([.5],)*3))
    assert r['parentage'].shape==(12,3)  # child, mother, father IDs
    np.testing.assert_array_equal(r['parentage'][:,1],r['parentage'][:,2])
    assert r['parentage_offsets'].tolist()==[0,4,8,12]
    keys=r['demographic_keys'].tolist()
    assert r['demographic'][:,keys.index('resident_selfed_recruits')].tolist()==[4,4,4]
    assert r['demographic'][:,keys.index('resident_outcross_recruits')].sum()==0
    for y in range(3):
        rows=r['parentage'][4*y:4*(y+1)]
        parents=r['state_ids'][r['state_offsets'][y]:r['state_offsets'][y+1]]
        assert np.isin(rows[:,1:],parents).all()


def test_matched_initialization_control_shares_whole_future_history():
    c=replace(config_fixture(),years=200,initial_visitors=4)
    f=history_from_spec(c,{'kind':'assembly'},72001)
    s=history_from_spec(replace(c,island_history='separation'),{'kind':'assembly'},72001)
    for a,b in zip(f.visitors,s.visitors):
        for key in ('ids','optima','breadths','effectiveness'):
            np.testing.assert_array_equal(getattr(a,key),getattr(b,key))


def test_every_recovery_treatment_has_same_horizon_matched_uninterrupted_control():
    d=build_design(pilot=False)
    cells=next(f['cells'] for f in d['families'] if f['name']=='recovery')
    lookup={c['id']:c for c in cells}
    for c in cells:
        if not any(s['count']==0 for s in c['history']['segments']): continue
        control=lookup[c['counterfactual']]
        for key in ('config_patch','founders','grid_axes','projection_mode','immigration_mode'):
            assert c[key]==control[key]
        assert sum(s['years'] for s in c['history']['segments'])==sum(s['years'] for s in control['history']['segments'])
        assert all(s['count']==4 for s in control['history']['segments'])
        assert c['history'].get('seed_window')==control['history'].get('seed_window')


def test_resident_density_control_is_independent_of_individual_demographic_draws():
    c=replace(config_fixture(),capacity=8,years=3,
        seed_arrival=replace(config_fixture().seed_arrival,establishment=1.))
    a=plant_fixture(4).alleles.copy();a[:,1,:]=np.array([0.,.25,.75,1.])[:,None]
    p=replace(plant_fixture(4),alleles=a)
    incoming=[]
    for y in range(3):
        incoming.append(replace(plant_fixture(1),ids=np.array([2**32+y]),
            allele_origin=np.full((1,3,2),2**32+y),birth_years=np.array([y+1])))
    h=History((visitors(),)*3,tuple(incoming),c.event_order)
    g=make_grid(([0.,.25,.5,.75,1.],)*2+([.5],))
    x=simulate(c,h,p,replicate=1,grid=g,immigration_mode='resident_matched')
    y=simulate(c,h,p,replicate=2,grid=g,immigration_mode='resident_matched')
    np.testing.assert_array_equal(x['density_counts'],y['density_counts'])


def test_empty_initial_island_has_no_initial_lineage_or_trait_change_baseline():
    r=record('empty',.7,.6,ancestry=0.)
    r['result']['population'][0]=0
    r['result']['trait_mean'][0]=np.nan
    r['result']['founder_ancestry'][0]=np.nan
    cell=summarize([r],{})['cells'][0]
    assert cell['founder_lineage_persistence'] is None
    assert cell['mean_founder_ancestry'] is None
    assert cell['n_initial_lineage_baselines']==0 and cell['n_trait_change_eligible']==0
    assert cell['sign_disagreement'] is None
    other=record('established',.6,.6)
    pair=paired_contrast([r],[other])
    assert pair['n_joint_survivors']==1 and pair['n_trait_change_eligible']==0
    assert pair['eligible_pairs']==[] and pair['conditional_mean_b_minus_a'] is None

def test_saved_parentage_counts_cannot_disagree_with_recruitment():
    import pytest
    from scripts.model3_island.audit import validate_arrays
    from scripts.model3_island.storage import pack_result
    c=replace(config_fixture(),years=2,capacity=4,fixed_assurance=1.,ovule_budget=100.)
    h=History((visitors(0),)*2,(plant_fixture(0),)*2,c.event_order)
    r=simulate(c,h,plant_fixture(4),replicate=18,grid=make_grid(([.5],)*3))
    arrays=pack_result(r,{'density_counts':'checkpoints_and_replay_digest','checkpoint_every':1})
    case={'cell':{'kind':'trajectory'},'config':{'years':2,'capacity':4}}
    validate_arrays(arrays,case)
    arrays['parentage']=arrays['parentage'].copy();arrays['parentage'][0,1]=99999999
    with pytest.raises(ValueError,match='parentage'):validate_arrays(arrays,case)
