from dataclasses import replace
import numpy as np
import pytest

from test_model3_island_state import config_fixture
from scripts.model3_island.types import VisitorState
from scripts.model3_island.history import make_history, permute_exposure, reach_probability


@pytest.mark.parametrize('kernel',['exponential','heavy_tail'])
def test_reach_probability_and_invalid_units(kernel):
    values=[reach_probability(d,1,kernel) for d in (0,1,5)]
    assert values[0]==1 and values[0]>values[1]>values[2]>=0
    with pytest.raises(ValueError): reach_probability(-1,1,kernel)
    with pytest.raises(ValueError): reach_probability(1,0,kernel)


def test_zero_arrivals_and_multiple_arrivals_with_replay():
    c=config_fixture(); zero=replace(c.seed_arrival,supply=0)
    h=make_history(replace(c,seed_arrival=zero,visitor_arrival=zero),seed=22)
    assert all(len(v.ids)==0 for v in h.visitors)
    assert all(len(p.ids)==0 for p in h.seed_candidates)
    high=replace(c.seed_arrival,supply=20,distance=0,establishment=1,loss_hazard=0)
    c=replace(c,seed_arrival=high,visitor_arrival=high)
    h=make_history(c,seed=22); again=make_history(c,seed=22)
    assert len(h.visitors[1].ids)>1 and len(h.seed_candidates[0].ids)>1
    for v,w,p,q in zip(h.visitors,again.visitors,h.seed_candidates,again.seed_candidates):
        np.testing.assert_array_equal(v.optima,w.optima)
        np.testing.assert_array_equal(p.alleles,q.alleles)
    # Seed supply changes must not perturb visitor history.
    other=make_history(replace(c,seed_arrival=zero),seed=22)
    for a,b in zip(h.visitors,other.visitors): np.testing.assert_array_equal(a.ids,b.ids)


def test_background_resource_requirement_and_separation_initialization():
    c=config_fixture()
    with pytest.raises(ValueError): make_history(replace(c,background_resources=0),seed=1)
    with pytest.raises(ValueError): make_history(replace(c,island_history='separation'),seed=1)
    v=VisitorState(ids=np.array([10]),optima=np.array([.3]),breadths=np.array([.2]),effectiveness=np.array([1.]))
    h=make_history(replace(c,island_history='separation',initial_visitors=1),seed=1,inherited_visitors=v)
    np.testing.assert_array_equal(h.visitors[0].ids,v.ids)
    assert h.initialization=='separation'


def test_chronology_preserves_visitors_seed_timing_and_recovery_suffix():
    c=replace(config_fixture(),initial_visitors=2)
    h=make_history(c,seed=5)
    recovery=make_history(replace(c,years=2,seed_arrival=replace(c.seed_arrival,supply=20,distance=0)),seed=6)
    order=np.arange(c.years)[::-1]
    p=permute_exposure(h,order,recovery)
    for i,j in enumerate(order):
        np.testing.assert_array_equal(p.visitors[i].optima,h.visitors[j].optima)
        np.testing.assert_array_equal(p.seed_candidates[i].alleles,h.seed_candidates[i].alleles)
    np.testing.assert_array_equal(p.visitors[-1].optima,recovery.visitors[-1].optima)
    for k,candidates in enumerate(recovery.seed_candidates):
        np.testing.assert_array_equal(p.seed_candidates[c.years+k].birth_years,
                                      candidates.birth_years+c.years)
    with pytest.raises(ValueError): permute_exposure(h,np.zeros(c.years,dtype=int),recovery)


def test_recovery_cannot_reuse_existing_seed_individual_ids():
    c=config_fixture()
    arrival=replace(c.seed_arrival,supply=20,distance=0)
    h=make_history(replace(c,seed_arrival=arrival),seed=5)
    with pytest.raises(ValueError): permute_exposure(h,np.arange(c.years),h)
