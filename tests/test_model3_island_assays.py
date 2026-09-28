from dataclasses import replace
import numpy as np
import pytest

from test_model3_island_state import config_fixture, plant_fixture
from scripts.model3_island.types import VisitorState
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.assays import investment_assay
from scripts.model3_evolution import pollen_transfer
from scripts.model3_reproduction import reproductive_ledger


def visitors(n=1, effectiveness=1., optimum=.5):
    return VisitorState(ids=np.arange(n),optima=np.full(n,optimum),
                        breadths=np.full(n,.2),effectiveness=np.full(n,effectiveness))


def test_reproduction_reproduces_legacy_annual_ledger():
    p=plant_fixture(3); c=config_fixture(); v=visitors(2)
    actual=reproduce(p,v,c)
    transfer=pollen_transfer(p.alleles[:,:2].mean(axis=2),v.optima,.2,c.activity,10,48)
    expected=reproductive_ledger(transfer,4*np.exp(-.5*p.alleles[:,1].mean(axis=1)**2),
        np.ones(3),np.full(3,.5),np.full(3,.5))
    np.testing.assert_allclose(actual.outcross,2*expected['outcross_by_donor_recipient'],atol=1e-12)
    np.testing.assert_allclose(actual.self_viable,2*expected['selfed_viable'],atol=1e-12)
    np.testing.assert_allclose(actual.exported,actual.delivered.sum(axis=1)+actual.lost,atol=1e-12)
    assert actual.self_raw.sum()+actual.outcross.sum()<=actual.ovules.sum()+1e-12
    assert actual.maternal.sum()==pytest.approx(actual.paternal.sum())


@pytest.mark.parametrize('v',[visitors(0),visitors(1,0)])
def test_no_effective_pollination_and_assurance_disabled(v):
    p=plant_fixture(); c=replace(config_fixture(),fixed_assurance=0.)
    r=reproduce(p,v,c)
    assert r.outcross.sum()==0 and r.self_raw.sum()==0
    assert reproduce(plant_fixture(0),v,c).outcross.shape==(0,0)


def test_prior_selfing_competes_for_ovules_delayed_uses_remaining():
    p=plant_fixture(3); c=replace(config_fixture(),activity=10.)
    delayed=reproduce(p,visitors(),c)
    prior=reproduce(p,visitors(),replace(c,assurance_timing='prior'))
    np.testing.assert_allclose(prior.outcross,delayed.outcross*.5)
    np.testing.assert_allclose(prior.self_raw,prior.ovules*.5)
    assert (delayed.self_raw<prior.self_raw).all()


def test_visitor_duplication_differs_between_richness_and_abundance_modes():
    p=plant_fixture(3); c=config_fixture()
    np.testing.assert_allclose(reproduce(p,visitors(1),c).outcross,reproduce(p,visitors(2),c).outcross)
    c=replace(c,activity_mode='count_scaled')
    assert reproduce(p,visitors(2),c).outcross.sum()>reproduce(p,visitors(1),c).outcross.sum()
    assert reproduce(p,visitors(1,optimum=0),c).outcross.sum()<reproduce(p,visitors(1),c).outcross.sum()


def test_assay_holds_states_and_separates_cost_from_pollination():
    p=plant_fixture(); c=config_fixture(); before=p.alleles.tobytes()
    r=investment_assay(p,visitors(0),c,step=.001)
    fine=investment_assay(p,visitors(0),c,step=.0005)
    np.testing.assert_allclose(r['total_gradient'],fine['total_gradient'],rtol=1e-5)
    assert (r['total_gradient']<0).all()
    assert (r['outcross_gradient']==0).all()
    free=investment_assay(p,visitors(0),replace(c,investment_cost=0.),step=.001)
    np.testing.assert_array_equal(free['total_gradient'],[0,0])
    assert p.alleles.tobytes()==before
    alleles=p.alleles.copy(); alleles[0,1]=0; alleles[1,1]=1
    edges=investment_assay(replace(p,alleles=alleles),visitors(),c,step=.001)
    assert edges['scheme']==['forward','backward']


def test_assurance_cost_and_discount_are_explicit():
    p=plant_fixture(); c=config_fixture()
    base=reproduce(p,visitors(),c)
    changed=reproduce(p,visitors(),replace(c,pollen_discount=1.,assurance_cost=1.))
    assert (changed.exported<base.exported).all()
    assert (changed.ovules<base.ovules).all()
    with pytest.raises(ValueError): investment_assay(p,visitors(),c,step=0)
