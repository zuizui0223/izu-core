"""No new ecological outcomes: t20 transplant source-lock and split-factor gates.

Only smoke on an artificial seed 990451 outside the existing exposed 64.
The full 64-history original source t20 overlap must be checked by production,
NOT guessed by the focused unit tests.
"""
import json

import numpy as np
import pytest

from scripts.audit_chapter2_t20_joint_genome_transplant import (
    contract,original_contract,initial_genotypes,visitor_history,
    replay_original_t20,transplant_diploid_source,run_future,paired_effect,
    future_streams,DONORS,K_TARGET,POST_OPERATORS,EXPECTED_SOURCE_COUNTS,
)


def test_source_design_is_post_outcome_and_does_not_mislabel_new_visitor_ids():
    d,h=contract()
    orig,_=original_contract()
    assert len(h)==64
    assert d["reuse_disclosure"].startswith("The same previously exposed 64")
    assert d["source_pre20"]["selected_and_neutral_pre20_occupied_expected"] == {
        "selected":58,"neutral":52,"both":50}
    assert orig["frozen_conditions"]["visitor_history_first"]==61024001
    assert d["transplant"]["recipient_census_N0"]==8
    assert d["transplant"]["target_capacity_K"]==[8,48]
    assert d["transplant"]["recipient_pollen_background_B"]==48
    assert d["transplant"]["factorial_cells_per_eligible_history"]==8


def test_whole_genomes_resampled_with_new_ids_and_origins():
    original,_=original_contract()
    donor=initial_genotypes(original)
    for label in DONORS:
        state,indices=transplant_diploid_source(
            donor,seed=990451,donor_label=label)
        assert len(indices)==len(state.ids)==8
        assert len(np.unique(state.ids))==8
        assert (state.birth_years==20).all()
        np.testing.assert_array_equal(state.alleles,donor.alleles[indices])
        np.testing.assert_array_equal(state.allele_origin,
                                      donor.allele_origin[indices])
        np.testing.assert_array_equal(state.mutation_flags,
                                      donor.mutation_flags[indices])
        state2,indices2=transplant_diploid_source(
            donor,seed=990451,donor_label=label)
        assert indices2==indices
        np.testing.assert_array_equal(state2.alleles,state.alleles)
    with pytest.raises(ValueError):
        transplant_diploid_source(donor,seed=990451,donor_label="unknown")


def test_source_t20_replay_without_exposing_original_visitor_histories():
    original,_=original_contract()
    history=visitor_history(original,990451)
    selected=replay_original_t20(
        original,history,990451,"selected_source")
    neutral=replay_original_t20(
        original,history,990451,"neutral_within_mating_channel")
    assert len(selected.ids)<=48 and len(neutral.ids)<=48
    assert selected.alleles.shape[1:]==neutral.alleles.shape[1:]==(3,2)


def test_sham_same_genomes_same_future_population_trajectory():
    original,_=original_contract()
    history=visitor_history(original,990451)
    founder=initial_genotypes(original)
    source,indices=transplant_diploid_source(
        founder,seed=990451,donor_label=DONORS[0])
    for K in K_TARGET:
        for f in POST_OPERATORS:
            a=run_future(original,history,990451,source,K,f)
            b=run_future(original,history,990451,source,K,f)
            assert a==b
            assert a["occupied80"] in (0,1)
            if not a["occupied80"]:
                assert a["final_allele_mean_given_occupied"] is None
            else:
                assert len(a["final_allele_mean_given_occupied"])==3


def test_inconclusive_diagnostic_when_all_paired_labels_agree():
    x=[{"a":{"occupied80":1},"b":{"occupied80":1}}
       for _ in range(50)]
    r=paired_effect(x,"a","b")
    assert r["n_eligible"]==50
    assert r["paired_difference"]==0
    assert r["classification"]=="inconclusive"
    assert r["conservative_95"][0]<-.05
    assert r["conservative_95"][1]>.05
    json.dumps(r,allow_nan=False)
