"""Fail-closed, NO-BIOLOGY R2 independent validation feasibility audit.

All numbers are algebraic assumptions and prospective *candidate* compute
budgets, not a power claim, biological experiment, random seed registry or
author approval.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import pytest

from scripts.review_chapter2_r2_independent_feasibility_20261025 import (
    ALPHA,CO_PRIMARY_COUNT,ENDPOINT_RANGES,FUTURE_AXES,LOW_COPIES,REPEATS,
    ROOT,STATUS,SOURCE_BLOBS,VARIANCE_SCENARIOS,
    PROTOCOL,PARENT,CHRONOLOGY,
    git_blob_sha,checked_sources,biallelic_population_mean,
    compensated_triallelic_counts,diploid_phenotype_preserving_I_recode,
    scenario_variance,static_cost,review,
)


def test_existing_study_remains_unapproved_with_pinned_source_provenance(monkeypatch):
    src=checked_sources()
    assert src["original_384_source_run_id"]==39233450099
    assert src["old_source_founder_count"]==12
    assert src["old_22_selected_source_founder_count"]==11
    assert src["new_biological_experiment_authorized"] is False
    for p in (PROTOCOL,PARENT,CHRONOLOGY):
        assert git_blob_sha(p)==SOURCE_BLOBS[p.name]
    original=json.loads(PROTOCOL.read_text(encoding="utf-8"))
    assert original["status"]=="DESIGN_ONLY_NOT_AUTHORIZED_NOT_PREREGISTERED"
    assert all(value is False for value in original["run_gate"].values())
    assert original["independent_sampling"]["future_founder_source_count"] is None
    assert original["independent_sampling"]["sample_size_power_and_precision_contract"] is None
    # Negative control: any changed original source receipt/protocol must fail
    # before a design estimate could be reported from an unrecognized source.
    monkeypatch.setitem(SOURCE_BLOBS,PROTOCOL.name,"0"*40)
    with pytest.raises(AssertionError,match="blob SHA changed"):
        checked_sources()


def test_biallelic_mean_is_not_identifiable_independently_of_copy_count():
    assert biallelic_population_mean(.25,.5,12)==pytest.approx(.46875)
    assert biallelic_population_mean(.25,.5,24)==pytest.approx(.4375)
    assert biallelic_population_mean(.25,.5,36)==pytest.approx(.40625)
    assert (.46875-.40625)==pytest.approx(.0625)
    for bad in (None,True,1.5,-1,97):
        with pytest.raises((ValueError,TypeError)):
            biallelic_population_mean(.25,.5,bad)
    with pytest.raises(ValueError):
        biallelic_population_mean(.5,.25,12)


def test_three_allele_mean_matched_copy_support_not_constant_variance():
    found=[compensated_triallelic_counts(x) for x in LOW_COPIES]
    assert LOW_COPIES==(12,24,36)
    assert [(r["low_I_copies"],r["middle_I_copies"],r["high_I_copies"])
            for r in found]==[(12,72,12),(24,48,24),(36,24,36)]
    assert [r["expected_allele_mean"] for r in found]==[.5]*3
    assert [r["allele_value_variance"] for r in found]==pytest.approx(
        [.015625,.03125,.046875],abs=1e-15)
    assert all(r["genetic_allocation_status"]==
        "FREQUENCY_ONLY_NOT_A_DIPLOID_GENOTYPE_INTERVENTION" for r in found)
    for invalid in (True,0,-1,49,1.5,None):
        with pytest.raises(ValueError):
            compensated_triallelic_counts(invalid)



def test_per_plant_diploid_recode_is_phenotypically_identical_but_genetically_distinct():
    # This is a mathematical 48-diploid source TEMPLATE, not a Model3 evolution.
    results=[diploid_phenotype_preserving_I_recode(k) for k in (8,16,24)]
    assert [r["artificial_I_heterozygous_recodes"] for r in results]==[8,16,24]
    assert all(r["N_mathematical_plants_not_simulated"]==48 for r in results)
    assert all(r["original_and_candidate_expressed_I_equal_for_every_plant"] for r in results)
    assert all(r["original_and_candidate_phenotype_mean"]==.625 for r in results)
    assert all(r["original_and_candidate_phenotype_variance"]==.015625 for r in results)
    assert [r["changed_I_numeric_allele_copy_counts"] for r in results]==[
        {"0.25":8,"0.5":32,"0.75":56},
        {"0.25":16,"0.5":16,"0.75":64},
        {"0.25":24,"0.5":0,"0.75":72},
    ]
    assert [r["changed_I_numeric_allele_value_variance"] for r in results]==pytest.approx(
        [2.5/96,3.5/96,4.5/96],abs=1e-15)
    assert all(r["new_population_or_offspring_updates"]==0 for r in results)
    assert all(r["current_native_phenotype_dependent_reproductive_ledger_would_match_if_M_A_visitors_unchanged"] for r in results)
    assert all(r["full_genotype_origin_pairing_and_future_Mendelian_outcomes_not_identified"] for r in results)
    for invalid in (True,-1,25,1.5,None):
        with pytest.raises(ValueError):
            diploid_phenotype_preserving_I_recode(invalid)


def test_budget_counts_crossed_sources_not_as_independent_outcomes():
    eight=static_cost(8,8,1)
    assert eight["independent_founder_labels"]==8
    assert eight["independent_visitor_history_labels"]==8
    assert eight["shared_original_history_prefixes"]==128
    assert eight["paired_t30_future_forks"]==768
    assert eight["history_prefix_updates_if_later_authorized"]==3840
    assert eight["future_population_updates_if_later_authorized"]==38400
    assert eight["hypothetical_total_population_updates_if_later_authorized"]==42240
    big=static_cost(32,32,2)
    assert big["shared_original_history_prefixes"]==4096
    assert big["paired_t30_future_forks"]==24576
    assert big["hypothetical_total_population_updates_if_later_authorized"]==1351680
    assert big["biological_population_updates_executed"]==0
    assert big["no_biology_dispatched"]
    for invalid in (True,0,1,1.5,None):
        with pytest.raises(ValueError):
            static_cost(invalid,8,2)
    # R=1 is a valid *single nested realization*, not an invalid source size.
    assert static_cost(8,8,1)["nested_demographic_repeats_per_cell"]==1
    for invalid in (True,0,-1,1.5,None):
        with pytest.raises(ValueError):
            static_cost(8,8,invalid)


def test_two_way_crossed_sensitivity_never_treats_grid_cells_as_independent():
    r=VARIANCE_SCENARIOS["moderate_hypothetical"]
    a=r["paired_low_I_loss_risk_difference"]
    # Two independent axes appear separately, nested replication decreases
    # only the within-cell term, not the founder/visitor variation.
    v=scenario_variance(a,32,32,2,"paired_low_I_loss_risk_difference")
    assert v==pytest.approx(.0020703125,abs=1e-15)
    assert scenario_variance(a,32,32,4,"paired_low_I_loss_risk_difference")<v
    assert scenario_variance(a,32,32,32,"paired_low_I_loss_risk_difference")>(a["founder"]+a["visitor"])/32
    for scenario in VARIANCE_SCENARIOS.values():
        for outcome,components in scenario.items():
            max_abs=max(abs(z) for z in ENDPOINT_RANGES[outcome])
            assert sum(components.values())<=max_abs**2
            assert scenario_variance(components,8,8,1,outcome)>0
            assert scenario_variance(components,64,64,4,outcome)>0
    with pytest.raises(ValueError):
        scenario_variance({"founder":-1,"visitor":0,"interaction":0,"nested":0},
                          8,8,2,"paired_low_I_loss_risk_difference")
    with pytest.raises(ValueError):
        scenario_variance({"founder":5,"visitor":0,"interaction":0,"nested":0},
                          8,8,2,"paired_low_I_loss_risk_difference")
    with pytest.raises(ValueError):
        scenario_variance(a,1,8,2,"paired_low_I_loss_risk_difference")


def test_review_is_complete_math_only_and_never_authorizes_actions():
    d=review()
    assert d["status"]==STATUS
    assert d["evidence_rank"]=="MATHEMATICAL_DESIGN_REVIEW_NOT_A_REGISTERED_STUDY"
    assert d["new_biological_simulation_updates"]==0
    assert d["new_statistical_experiments"]==0
    assert d["dispatched_actions"]==0
    assert d["may_dispatch_biological_futures"] is False
    assert d["prospectively_registered"] is False
    assert d["author_signoff"] is False
    assert d["sample_size_authorized"] is False
    assert d["population_power_validated"] is False
    assert d["SESOI_minimum_important_I_or_loss_risk_contrast"] is None
    assert d["other_M_A_genotype_covariance_or_ancestry_preserved"] is False
    assert d["source_genotype_construction_method_approved"] is False
    assert d["mean_invariant_I_access_requires_unassessed_genotype_reallocation"]
    assert d["three_allele_copy_compensation_changes_allelic_variance"]
    assert d["initial_phenotypic_mean_and_variance_can_be_held_fixed_under_artificial_I_recode"] is True
    assert len(d["diploid_per_plant_phenotype_preserving_access_illustration"])==3
    assert all(z["new_population_or_offspring_updates"]==0 for z in
               d["diploid_per_plant_phenotype_preserving_access_illustration"])
    assert d["hypothetical_co_primary_count"]==CO_PRIMARY_COUNT==2
    assert d["nominal_familywise_alpha_sensitivity_only"]==ALPHA==.05
    assert len(d["candidate_allocation_grid"])==len(FUTURE_AXES)*len(REPEATS)==12
    assert all(not x["candidate"]["biological_population_updates_executed"]
               for x in d["candidate_allocation_grid"])
    assert all(set(x["precision_sensitivity"])==set(VARIANCE_SCENARIOS)
               for x in d["candidate_allocation_grid"])
    assert all("hypothetical" in x for x in d["variance_scenarios_hypothetical_not_data_estimated"])
    assert math.isfinite(d["normal_quantile_proxy"])
    # JSON-serialization itself is required by the immutable Actions receipt.
    assert json.loads(json.dumps(d,allow_nan=False))["status"]==STATUS
