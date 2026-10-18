"""Small source/analysis fixtures; never run the scientific cohort in CI."""
from dataclasses import replace
import json
import numpy as np
import pytest
from scripts.run_chapter2_budget_companion_20261018 import (
    make_config, make_founders, visitor_community, fresh_seed, streams,
    empty_plants, step, describe, follow_future, assemble_summary,
    validate_native_sources, replay_history,
)
from scripts.model3_island.reproduction import reproduce


def test_native_sources_and_initial_phenotypes_are_pinned():
    assert len(validate_native_sources()) == 5
    f=make_founders(301001)
    assert np.all(f.alleles[:,2,:].mean(axis=1)==.5)
    assert len(np.unique(f.alleles[:,2,:]))==3
    assert np.var(f.alleles[:,2,:])>0
    assert make_config('fixed').ovule_budget==8
    assert make_config('evolving',4.5).assurance_cost==.5


def test_budget_scales_native_output_not_relative_parent_choice():
    f=make_founders(301001)
    for visitor in (visitor_community(302001)[0],visitor_community(302001)[2]):
        for p in ('fixed','evolving'):
            cfg=make_config(p)
            a=reproduce(f,visitor,cfg)
            b=reproduce(f,visitor,replace(cfg,ovule_budget=4.5))
            for attr in ('ovules','outcross','self_viable','maternal','paternal'):
                np.testing.assert_allclose(getattr(b,attr),getattr(a,attr)*4.5/8,rtol=1e-13)
            np.testing.assert_array_equal(a.delivered,b.delivered)
            pa=a.outcross+np.diag(a.self_viable); pb=b.outcross+np.diag(b.self_viable)
            np.testing.assert_allclose(pa/pa.sum(),pb/pb.sum(),rtol=1e-13,atol=1e-15)


def test_fresh_streams_match_across_treatments_but_not_histories():
    seeds=[fresh_seed(f,v,r) for f in range(6) for v in range(6) for r in range(2)]
    assert len(set(seeds))==72
    s=fresh_seed(0,0,0)
    for key in streams(s):
        np.testing.assert_array_equal(streams(s)[key].integers(0,1000,10), streams(s)[key].integers(0,1000,10))
    for bad in (-1,6,True):
        with pytest.raises(ValueError):fresh_seed(bad,0,0)


def test_empty_population_stays_extinct_and_traits_undefined():
    st=empty_plants(make_founders(301001))
    cfg=make_config('fixed',4.5)
    after=step(st,visitor_community(302001)[2],cfg,streams(191),35)
    assert len(after.ids)==0
    d=describe(after,cfg,35,.5)
    assert d['mean_I'] is None and d['accessible'] is None
    assert not d['alive'] and d['n']==0
    with pytest.raises(ValueError):make_config('unknown')


def test_same_seed_future_replays_and_does_not_mutate_checkpoint():
    st=make_founders(301001)
    original=st.alleles.copy()
    a,aa=follow_future(st,'fixed',4.5,123,.5,first_loss=None)
    b,bb=follow_future(st,'fixed',4.5,123,.5,first_loss=None)
    assert a==b
    assert len(aa)==46
    np.testing.assert_array_equal(st.alleles,original)
    for x,y in zip(aa,bb):
        np.testing.assert_array_equal(x.alleles,y.alleles)
    for x in aa:
        assert len(x.ids)<=48
        assert set(np.unique(x.alleles[:,1,:]))<=set(np.unique(st.alleles[:,1,:]))


def test_old_history_replay_matches_logged_events_not_new_sampling():
    for policy,want in [('fixed',69),('evolving',48)]:
        r=replay_history(0,0,0,policy)
        assert r['first_I_loss']==want
        assert r['first_A_loss']==(24 if policy=='evolving' else None)
        assert len(r['checkpoint'].ids)==48
        assert r['final_alive'] is True
