from dataclasses import replace
import numpy as np
import pytest

from test_model3_island_state import config_fixture, plant_fixture
from test_model3_island_assays import visitors
from scripts.model3_island.types import History
from scripts.model3_island.density import make_grid, mutation_matrix, project_state, density_step
from scripts.model3_island.simulate import simulate
from scripts.model3_meanfield import genotype_grid, meanfield_step, project_founders


def test_gamete_and_mutation_probabilities():
    grid=make_grid((np.array([0.,.5,1.]),)*3)
    np.testing.assert_allclose(grid.gamete_probabilities.sum(axis=1),1,atol=1e-14)
    np.testing.assert_array_equal(mutation_matrix(grid.axes[0],0,.1),np.eye(3))
    for sd in (.01,.1,.5,2.):
        m=mutation_matrix(grid.axes[0],.2,sd)
        np.testing.assert_allclose(m.sum(axis=1),1,atol=1e-12)
        assert (m>=0).all()
        np.testing.assert_allclose(m,m[::-1,::-1],atol=1e-12)
    with pytest.raises(ValueError): mutation_matrix(np.array([.4,.6]),.1,.1)


def test_reflected_mutation_agrees_with_independent_sampling():
    from scripts.model3_island.history import reflect_unit
    nodes=np.array([0.,.25,.5,.75,1.])
    rng=np.random.default_rng(71)
    for center in (0.,.5,1.):
        draws=reflect_unit(center+rng.normal(0,.2,100000))
        bins=np.argmin(abs(draws[:,None]-nodes[None,:]),axis=1)
        observed=np.bincount(bins,minlength=5)/len(draws)
        expected=mutation_matrix(nodes,1,.2)[np.flatnonzero(nodes==center)[0]]
        np.testing.assert_allclose(observed,expected,atol=.005)


def test_density_reproduces_archived_two_locus_operator():
    legacy,kernel=genotype_grid(.3,3)
    grid=make_grid((np.linspace(.2,.4,3),np.linspace(.4,.6,3),np.array([.5])))
    np.testing.assert_allclose(grid.genotypes[:,:2],legacy,atol=1e-15)
    density=np.arange(1,37,dtype=float); density*=.8/density.sum()
    c=replace(config_fixture(),survival=.75,ovule_budget=2.,pollen_budget=5.)
    v=visitors(2)
    actual,ledger=density_step(density*c.capacity,grid,v,plant_fixture(0),c)
    expected=meanfield_step(density,legacy,kernel,v.optima,activity=c.activity,
        survival=c.survival,selfing=c.fixed_assurance,depression=c.depression)
    np.testing.assert_allclose(actual/c.capacity,expected['density'],atol=1e-12)
    assert ledger.outcross.sum()/c.capacity==pytest.approx(expected['outcross'])
    assert ledger.self_viable.sum()/c.capacity==pytest.approx(expected['selfed'])


def test_projected_founders_match_and_zero_reproduction_extinct():
    grid=make_grid((np.array([0.,.5,1.]),)*3)
    c=replace(config_fixture(),years=3,fixed_assurance=0.)
    p=plant_fixture(2)
    projected,counts=project_state(p,grid)
    assert counts.sum()==len(p.ids)
    np.testing.assert_array_equal(projected.alleles,p.alleles)
    h=History((visitors(0),)*3,(plant_fixture(0),)*3,c.event_order)
    r=simulate(c,h,p,replicate=3,grid=grid)
    assert r['population'].tolist()==[2,0,0,0]
    assert r['extinction_year']==1
    assert np.isnan(r['trait_mean'][1:]).all()
    assert r['density_mass'][1:].sum()==0
    np.testing.assert_array_equal(r['visitor_count'],[0,0,0])


def test_recolonization_is_not_uninterrupted_persistence():
    grid=make_grid((np.array([0.,.5,1.]),)*3)
    c=replace(config_fixture(),years=3,fixed_assurance=0.,
              seed_arrival=replace(config_fixture().seed_arrival,establishment=1.))
    immigrant=replace(plant_fixture(1),ids=np.array([2**32]),
                      allele_origin=np.full((1,3,2),2**32),birth_years=np.array([2]))
    h=History((visitors(0),)*3,(plant_fixture(0),immigrant,plant_fixture(0)),c.event_order)
    r=simulate(c,h,plant_fixture(1),replicate=4,grid=grid)
    assert r['population'].tolist()==[1,0,1,0]
    assert r['extinction_year']==1 and r['recolonizations']==1
    assert r['founder_ancestry'][2]==0


def test_mutation_and_pair_replay_preserve_capacity_and_inputs():
    grid=make_grid((np.array([0.,.5,1.]),)*3)
    c=replace(config_fixture(),years=4,mutation_rate=.1,mutation_sd=.1,assurance_mode='evolving')
    p=plant_fixture(3); before=p.alleles.tobytes()
    h=History((visitors(),)*4,(plant_fixture(0),)*4,c.event_order)
    a=simulate(c,h,p,replicate=9,grid=grid)
    b=simulate(c,h,p,replicate=9,grid=grid)
    for key in ('population','trait_mean','density_traits','density_mass'):
        np.testing.assert_array_equal(a[key],b[key])
    assert (a['population']<=c.capacity).all()
    assert (a['density_mass']<=c.capacity+1e-10).all()
    assert p.alleles.tobytes()==before


def test_nonfinite_counts_and_wrong_history_rejected():
    grid=make_grid((np.array([.5]),)*3); c=config_fixture()
    with pytest.raises(ValueError): density_step(np.array([np.nan]),grid,visitors(),plant_fixture(0),c)
    with pytest.raises(ValueError): simulate(c,History((),(),c.event_order),plant_fixture(),replicate=0,grid=grid)

def test_yearly_states_and_density_variance_are_auditable():
    grid=make_grid((np.array([0.,.5,1.]),)*3)
    c=replace(config_fixture(),years=2)
    p=plant_fixture(3)
    h=History((visitors(),)*2,(plant_fixture(0),)*2,c.event_order)
    r=simulate(c,h,p,replicate=21,grid=grid)
    assert r['density_counts'].shape==(3,len(grid.genotypes))
    np.testing.assert_allclose(r['density_counts'].sum(axis=1),r['density_mass'])
    np.testing.assert_array_equal(np.diff(r['state_offsets']),r['population'])
    np.testing.assert_array_equal(r['state_alleles'][:3],r['initial_genotypes'])
    assert r['state_mutation_flags'].shape==r['state_alleles'].shape
    assert r['density_trait_variance'].shape==(3,3)
    np.testing.assert_array_equal(r['final_mutation_flags'],r['state_mutation_flags'][r['state_offsets'][-2]:])
