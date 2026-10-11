"""Gate tests for source-locked selected vs neutral within-channel transmission.

All smoke histories use 99041x labels, never the 64 new 61024001..61024064.
No projected survival outcomes may be used from these tests.
"""
from dataclasses import replace

import numpy as np
import pytest

from scripts.audit_chapter2_selected_vs_neutral_parentage_new64 import (
    STATUS,HISTORIES,contract,biological_config,initial_genotypes,
    visitor_history,demographic_streams,neutral_offspring_parent_indices,
    neutral_expected_child_mean,neutralize_transmitted_genomes,run_path
)
from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.model3_island.population import advance
from scripts.model3_island.types import PlantState


def test_source_frozen_and_independent_histories_unexposed():
    d,digest=contract()
    assert len(digest)==64
    assert len(HISTORIES)==64 and HISTORIES.start==61024001
    assert HISTORIES.stop==61024065
    assert d["frozen_conditions"]["full_future_count"]==1024
    assert d["selection_mechanism"]["not_a_true_evolution_freeze"]
    st=initial_genotypes(d)
    assert st.alleles.shape==(8,3,2)
    assert all(np.var(st.alleles[:,locus,:])>0 for locus in range(3))
    for K in (8,48):
        cfg=biological_config(d,K,6.)
        assert cfg.capacity==K
        assert cfg.seed_arrival.supply==0
        assert cfg.survival==0 and cfg.mutation_rate==0


def test_neutral_parentage_keeps_exact_mating_channel_counts():
    rng=np.random.default_rng(990410)
    for n,ns,no in ((1,4,0),(2,7,5),(8,30,30),(48,30,90),(8,0,0)):
        mothers,fathers=neutral_offspring_parent_indices(n,ns,no,rng)
        assert len(mothers)==len(fathers)==ns+no
        assert int(np.sum(mothers==fathers))==ns
        assert int(np.sum(mothers!=fathers))==no
        assert np.all(mothers>=0) and np.all(mothers<n)
        assert np.all(fathers>=0) and np.all(fathers<n)
    with pytest.raises(ValueError):
        neutral_offspring_parent_indices(1,0,1,rng)


def test_neutral_mendelian_expected_allele_dosage_is_parent_mean():
    d,_=contract()
    st=initial_genotypes(d)
    for self_n,out_n in ((1,1),(20,4),(1,64),(64,0),(0,64)):
        expected=neutral_expected_child_mean(st.alleles,self_n,out_n)
        np.testing.assert_allclose(expected,st.alleles.mean(axis=(0,2)),
                                   rtol=0,atol=1e-12)
    # Empirical route-matched founder sampling should agree with theoretical
    # mean without using one of the reserved visitor histories.
    rng=np.random.default_rng(990411)
    mothers,fathers=neutral_offspring_parent_indices(8,2000,2000,rng)
    dosage=st.alleles.mean(axis=2)
    parent_average=.5*(dosage[mothers]+dosage[fathers])
    np.testing.assert_allclose(parent_average.mean(axis=0),dosage.mean(axis=0),
                               rtol=0,atol=.02)


def test_original_advance_still_used_and_neutral_only_replaces_genome():
    d,_=contract()
    st=initial_genotypes(d)
    cfg=biological_config(d,8,8.)
    h=visitor_history(d,990412)
    streams=demographic_streams(d,990412)
    source=reproduce_kb(st,h.visitors[0],cfg,background_denominator_capacity=48)
    direct,info=advance(st,source,h.seed_candidates[0],cfg,streams,year=0)
    neutral=neutralize_transmitted_genomes(
        st,direct,info,cfg,seed=990412,year=0,
        salt=d["frozen_conditions"]["neutral_parentage_rng_salt"]
    )
    np.testing.assert_array_equal(direct.ids,neutral.ids)
    np.testing.assert_array_equal(direct.birth_years,neutral.birth_years)
    assert len(neutral.ids)<=8
    assert info["resident_recruits"]==len(neutral.ids)


def test_monotypic_genetic_control_retains_demographic_occupancy_pathwise():
    d,_=contract()
    cfg=biological_config(d,8,6.)
    h=visitor_history(d,990413)
    source=initial_genotypes(d)
    a=source.alleles.copy()
    a[:,:,:]=.5
    mono=replace(source,alleles=a)
    results=[]
    for mode in ("selected_source","neutral_within_mating_channel"):
        state=mono
        streams=demographic_streams(d,990413)
        trajectory=[]
        for t in range(8):
            if len(state.ids):
                ledger=reproduce_kb(state,h.visitors[t],cfg,
                                    background_denominator_capacity=48)
                parent=state
                state,info=advance(state,ledger,h.seed_candidates[t],cfg,
                                   streams,year=t)
                if mode=="neutral_within_mating_channel":
                    state=neutralize_transmitted_genomes(
                        parent,state,info,cfg,seed=990413,year=t,
                        salt=d["frozen_conditions"]["neutral_parentage_rng_salt"]
                    )
            trajectory.append(len(state.ids))
        results.append(trajectory)
    assert results[0]==results[1]


def test_bounded_smoke_paths_produce_pairable_unconditional_outcomes():
    d,_=contract()
    h=visitor_history(d,990414)
    assert len(h.visitors)==80
    assert all(len(x.ids)==0 for x in h.seed_candidates)
    rows=[
        run_path(d,h,990414,8,6.,"baseline",mode)
        for mode in ("selected_source","neutral_within_mating_channel")
    ]
    assert all(x["visitor_history"]==990414 for x in rows)
    assert all(x["occupied80"] in (0,1) for x in rows)
    assert rows[0]["first_census"]==rows[1]["first_census"]
    for row in rows:
        assert row["occupied80"]<=row["occupied20"]
        if row["occupied80"]==0:
            assert row["end_allele_means_given_occupied"] is None
        else:
            assert len(row["end_allele_means_given_occupied"])==3
