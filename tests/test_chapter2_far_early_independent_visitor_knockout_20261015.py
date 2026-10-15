"""Registered independent 64-history/2-founder initial200 visitor knockout guards."""
from dataclasses import replace
import json

import numpy as np
import pytest

from scripts.model3_island.types import VisitorState
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.run_chapter2_assurance_generality import load_design, config, DEFAULT_DESIGN
from scripts.run_chapter2_far_early_independent_visitor_knockout_20261015 import (
    PROTOCOL, SETTINGS, VISITOR_REGIMES, MODES, FOUNDERS,
    DEMOGRAPHY, FIRST, LAST, YEAR_END, founder_pair, price_ensemble,
)
from scripts.summarize_chapter2_far_early_independent_visitor_knockout_20261015 import (
    interval,
)


def test_new_histories_and_original_source_condition_locked():
    p=json.loads(PROTOCOL.read_text(encoding="utf-8"))
    f=p["factorization"]
    assert p["status"]=="PROSPECTIVELY_FROZEN_BEFORE_NEW_INDEPENDENT_MODEL_RUN"
    assert f["visitor_history_seed_first"]==FIRST==28110601
    assert f["visitor_history_seed_last"]==LAST==28110664
    assert f["n_paths"]==64*2*4*2*2==2048
    assert f["total_native_updates"]==2048*YEAR_END==409600
    assert tuple(f["settings"])==SETTINGS
    assert tuple(f["visitor_regimes"])==VISITOR_REGIMES
    assert tuple(f["assurance_modes"])==MODES
    assert tuple(f["founder_seeds"])==FOUNDERS
    assert tuple(f["paired_demographic_seeds_by_founder"])==DEMOGRAPHY
    assert p["technical_pilot_after_original_design_freeze"]["visitor_seed"]==FIRST


def test_independent_founder_pair_same_genomes_within_treatments():
    a=founder_pair(FOUNDERS[0])
    b=founder_pair(FOUNDERS[0])
    c=founder_pair(FOUNDERS[1])
    assert np.array_equal(a.alleles,b.alleles)
    assert not np.array_equal(a.alleles,c.alleles)
    assert np.all(a.alleles[:,2,:]==.5)
    assert np.all(c.alleles[:,2,:]==.5)


def test_exact_no_visitor_is_no_pollen_but_positive_selfing():
    d=load_design(DEFAULT_DESIGN)
    st=founder_pair(FOUNDERS[0])
    none=VisitorState(np.empty(0,dtype=np.int64),np.empty(0),np.empty(0),np.empty(0))
    c=config(d,"assurance_cost",.01,"evolving")
    led=reproduce(st,none,c)
    assert led.outcross.sum()==0
    assert led.exported.sum()==0
    assert led.self_viable.sum()>0
    assert np.isfinite(price_ensemble(st,led))


def test_no_mutation_fixed_vs_evolving_one_year_exact_identical():
    d=load_design(DEFAULT_DESIGN)
    st=founder_pair(FOUNDERS[0])
    none=VisitorState(np.empty(0,dtype=np.int64),np.empty(0),np.empty(0),np.empty(0))
    states=[]
    for mode in MODES:
        c=replace(config(d,"delayed_control",0.0,mode),years=1)
        led=reproduce(st,none,c)
        rngseed=int(np.random.SeedSequence([FIRST,DEMOGRAPHY[0]]).generate_state(1)[0])
        streams={name:stream(rngseed,name,0) for name in STREAM_IDS}
        from scripts.model3_island.population import subset
        empty=subset(st,np.empty(0,dtype=int))
        empty=replace(empty,birth_years=np.empty(0,dtype=np.int64))
        child,info=advance(st,led,empty,c,streams,year=0,
                           mutation_traits=(True,True,mode=="evolving"))
        states.append((child.alleles,info["parentage"]))
    assert np.array_equal(states[0][0],states[1][0])
    assert np.array_equal(states[0][1],states[1][1])


def test_prespecified_bootstrap_is_seed_clustered_and_familywise():
    v=np.full(63,0.025)
    r=interval(v,seed=20261015,bonferroni=True)
    assert r["n_original_independent_seed_clusters"]==63
    assert r["familywise_bonferroni_4"] is True
    assert r["cluster_bootstrap_interval"]==pytest.approx([.025,.025])
    with pytest.raises(AssertionError):
        interval(np.ones(62),seed=10)
