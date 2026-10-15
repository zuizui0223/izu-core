"""Source-authenticated Q2 F1 four-sign STATIC native-return screen tests.

These tests never produce offspring or run population.advance.
"""
from __future__ import annotations

import json

import numpy as np
import pytest

from scripts.audit_chapter2_original_F1_signed_quadrant_null_20261015 import (
    SIGNED_CELLS,
)
from scripts.audit_chapter2_Q2_original_F1_focal_return_20261015 import (
    OUTPUT, SIGN_VALUES, FOCAL_ID, M_SUPPORT, TOL, audit, focal_state,
    original_M_access, one_focal_W, read_original_signed_access,
)
from scripts.audit_chapter2_original_founder_compatibility_20261014 import (
    original_fixture, source_state, original_context,
)
from scripts.model3_island import reproduction


def test_original_signed_prior_still_authenticated_and_symmetric():
    rec=read_original_signed_access()
    assert rec["status"]=="SOURCE_AUTHENTICATED_NATIVE_T0_SIGN_NULL_NO_NEW_BIOLOGY"
    assert rec["new_biological_trajectories"]==0
    assert rec["new_offspring_births"]==0
    assert len(rec["contexts"])==3
    for row in rec["contexts"]:
        assert set(row["m6_signed_events"])==set(SIGNED_CELLS)
        assert set(row["m0_signed_events"])==set(SIGNED_CELLS)
        assert all(p==0 for p in row["m0_signed_events"].values())
        assert max(row["m6_signed_events"].values())-min(row["m6_signed_events"].values())<=TOL


def test_original_I_preserved_parent_source_support_and_one_focal_only():
    original=source_state(original_fixture(),"confirmation")
    source=original_M_access(original)
    assert source["m6_original_carrier_ids"]==[1,3,6,9,11,14]
    assert source["M_F1_conditional_support"]==[
        {"M":.5,"probability":.25},
        {"M":.5625,"probability":.5},
        {"M":.625,"probability":.25},
    ]
    for M,weight in M_SUPPORT:
        assert weight>0
        for sign,(A,I) in SIGN_VALUES.items():
            new=focal_state(original,M,A,I)
            assert new.ids.shape==(48,)
            assert np.array_equal(new.ids,original.ids)
            assert np.array_equal(new.alleles[0],original.alleles[0])
            assert np.array_equal(new.alleles[2:],original.alleles[2:])
            assert np.array_equal(new.alleles[FOCAL_ID].mean(axis=1),[M,I,A])
            assert np.array_equal(new.mutation_flags,original.mutation_flags)


def test_focal_slot_choice_does_not_create_static_return_direction():
    # Original I-homozygote 5 has the same expressed t0 phenotype as ID 1.
    # Replacing either ID must give the same native W: biology uses adult
    # phenotype, not hidden genealogical I copies, for reproduction.
    original=source_state(original_fixture(),"confirmation")
    fixture=original_fixture()
    for c in (0,3,4):
        cfg,v=original_context(fixture,"confirmation",c)
        for sign,(A,I) in SIGN_VALUES.items():
            reference=one_focal_W(reproduction.reproduce(
                focal_state(original,.5625,A,I,focal_id=1),v,cfg),1)
            alternative=one_focal_W(reproduction.reproduce(
                focal_state(original,.5625,A,I,focal_id=5),v,cfg),5)
            assert abs(reference["parental_genome_W"]-
                       alternative["parental_genome_W"])<TOL


def test_native_W_ranking_full_original_F1_grid_and_frozen_numbers():
    result=audit()
    frozen=json.loads(OUTPUT.read_text(encoding="utf-8"))
    assert result["status"]==frozen["status"]
    assert result["schema"]==frozen["schema"]
    assert result["n_contexts"]==3
    assert result["n_M_levels"]==3
    assert result["n_focal_trait_comparisons"]==36
    assert (result["new_offspring_births"],
            result["new_population_advance_calls"],
            result["new_evolutionary_histories"])==(0,0,0)
    assert result["m6_signed_A_I_tail_probability_equal_across_four_signs"]
    assert len(result["native_four_corner_rows"])==len(frozen["native_four_corner_rows"])==9
    for actual,source in zip(result["native_four_corner_rows"],
                             frozen["native_four_corner_rows"]):
        assert (actual["context"],actual["one_possible_F1_M"])==(
            source["context"],source["one_possible_F1_M"])
        assert actual["highest_focal_W_sign"]=="A_up_I_down"
        assert actual["top_W_minus_runner_up"]>0.04
        assert set(actual["static_focal_expected_returns_by_sign"])==set(SIGN_VALUES)
        for sign,vals in actual["static_focal_expected_returns_by_sign"].items():
            recorded=source["static_focal_expected_returns_by_sign"][sign]
            for key in ("female_outcross_F","male_outcross_P","viable_self_S",
                        "parental_genome_W","intrinsic_ovule_budget"):
                assert abs(vals[key]-recorded[key])<TOL
            assert abs(vals["parental_genome_W"]-
                       (vals["female_outcross_F"]+vals["male_outcross_P"])/2-
                       vals["viable_self_S"])<TOL
    assert [x["context"] for x in result["context_mean_W_summary"]]==[0,3,4]
    for actual,source in zip(result["context_mean_W_summary"],
                             frozen["context_mean_W_summary"]):
        assert actual["max_expected_return_sign"]=="A_up_I_down"
        assert actual["W_A_up_I_down_minus_second_highest"]>0.04
        for sign in SIGN_VALUES:
            assert abs(actual["source_supported_conditional_M_averaged_focal_W_by_sign"][sign]-
                       source["source_supported_conditional_M_averaged_focal_W_by_sign"][sign])<TOL


def test_source_scope_is_not_realized_selection_or_Q4():
    result=audit()
    assert result["independent_genetic_source_backgrounds"]==1
    assert result["only_one_original_adult_phenotype_replaced_at_a_time"]
    claims=" ".join(result["claim_ceiling"])
    for word in ("density","selection","20-census","Q4","one original"):
        assert word in claims
