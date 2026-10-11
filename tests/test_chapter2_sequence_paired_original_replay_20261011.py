"""Pair archived Model3 crossing estimands to the REAL original diploid replay."""
import numpy as np
import pytest
import json
import sys

import scripts.audit_chapter2_sequence_paired_original_replay_20261011 as paired_module

from scripts.audit_chapter2_sequence_paired_original_replay_20261011 import (
    STATUS_PAIRED,original_order_pair_100_updates, original_expected,
)


def test_original_history76001_all_six_frozen_crossings_reproduced_from_rng():
    # Eight original demographic repeats × paired near/far = 16 actual
    # (not new) source histories. The source's original 1000-update crossing
    # events all occur by t43, so a 100-update prefix plus 20-repro-period
    # persistence completely recovers them without post-hoc invented censoring.
    d=original_order_pair_100_updates(
        seed=76001,setting="assurance_cost",
        years=100,gradient_until=0,sample_n=2)
    assert d["status"]==STATUS_PAIRED
    assert d["n_original_near_and_far_replays"]==16
    assert d["n_original_demographic_repeats"]==8
    assert d["n_original_visitor_history_clusters"]==1
    assert d["all_six_frozen_original_events_reproduced"] is True
    assert d["direct_archive_NPZ_identity_verified"] is False
    assert len(d["original_observed_crossings"])==6
    assert len(d["original_10_column_trace_sha_by_case"])==16
    assert all(e["original_event_agrees_with_prefix_replay"]
               for e in d["original_observed_crossings"])
    by={(e["contrast"],e["threshold"]):e for e in d["original_observed_crossings"]}
    within=by["far_change_from_founders",.05]
    assert within["replayed_assurance_crossing"]==5
    assert within["replayed_investment_crossing"]==20
    assert within["replayed_category"]=="assurance_first"
    incremental=by["paired_far_minus_near",.05]
    assert incremental["replayed_assurance_crossing"]==17
    assert incremental["replayed_investment_crossing"]==15
    assert incremental["replayed_category"]=="near_simultaneous"
    # Distinct referents: historical A-first within the far arm, but
    # extra far-minus-near divergence in investment starts two updates earlier.
    for contrast in ("far_change_from_founders","paired_far_minus_near"):
        for th in (.025,.05,.1):
            expected=original_expected(76001,"assurance_cost",th,contrast)
            e=by[contrast,th]
            assert (e["replayed_assurance_crossing"],e["replayed_investment_crossing"],
                    e["replayed_category"])==(
                    expected["assurance_time"],expected["investment_time"],
                    expected["order"])
    assert len(d["annual_pooled_trait_delta_from_founder_far"])==101
    assert len(d["annual_pooled_far_minus_near_trait_delta"])==101
    assert len(d["sampled_actual_genotype_local_gradients"])==16
    assert all(len(x["sampled_local_focal_selection"])==1
               for x in d["sampled_actual_genotype_local_gradients"])


def test_invalid_bounded_original_history_prefix_fails_closed():
    with pytest.raises(ValueError):
        original_order_pair_100_updates(seed=76002,years=100)
    with pytest.raises(ValueError):
        original_order_pair_100_updates(setting="prior_selfing",years=100)
    with pytest.raises(ValueError):
        original_order_pair_100_updates(years=62)


def synthetic_paired_comparisons(monkeypatch,matching_cases,years=100,legacy_claim=False):
    """Exercise aggregation only; the fabricated traces execute no biology."""
    calls=[]
    def supplied_record(setting,seed,rep,arm,**kwargs):
        index=len(calls)
        calls.append((rep,arm))
        matched=index<matching_cases
        trace=np.full((years+1,10),.5)
        trace[:,0]=48
        return {
            "trace":trace.tolist(),"source_trace_sha256":"synthetic-comparison-only",
            "sampled_local_focal_selection":[],
            "verification":{
                "verified_against_exact_original_archive":legacy_claim,
                "historical_source_identity_verified":False,
                "runtime_identity_verified":False,
                "original_annual_genomes_verified":False,
                "original_discovery_full_replay_completed":False,
                "supplied_case_record_verified":matched,
                "replay_matches_supplied_prefix":matched,
                "full_supplied_record_reproduced":matched and years==1000,
                "compared_censuses":years+1 if matched else 0,
                "compared_updates":years if matched else 0,
                "compared_checkpoint_years":([t for t in (0,200,400,1000) if t<=years]
                                             if matched else []),
            },
        }
    monkeypatch.setattr(paired_module,"replay",supplied_record)
    result=original_order_pair_100_updates(years=years,require_all_frozen_crossings=False)
    assert len(calls)==16
    return result


@pytest.mark.parametrize("matching_cases,years",((0,100),(15,100),(16,100),(16,1000)))
def test_paired_comparison_does_not_promote_supplied_record_agreement(monkeypatch,matching_cases,years):
    result=synthetic_paired_comparisons(monkeypatch,matching_cases,years)
    verification=result["verification"]
    assert verification["case_records_expected"]==16
    assert verification["case_records_compared"]==matching_cases
    assert verification["all_supplied_case_records_agree"] is (matching_cases==16)
    assert verification["all_supplied_trace_prefixes_agree"] is (matching_cases==16)
    assert verification["all_full_supplied_records_reproduced"] is (matching_cases==16 and years==1000)
    assert result["direct_archive_NPZ_identity_verified"] is False
    for key in ("verified_against_exact_original_archive","historical_source_identity_verified",
                "runtime_identity_verified","original_annual_genomes_verified",
                "original_discovery_full_replay_completed"):
        assert verification[key] is False
    compared=[x["verification"] for x in result["original_10_column_trace_sha_by_case"]]
    assert sum(v["compared_censuses"]>0 for v in compared)==matching_cases
    assert all(v["compared_updates"] in (0,years) for v in compared)


def test_paired_legacy_true_flag_is_not_an_archive_authentication_contract(monkeypatch):
    result=synthetic_paired_comparisons(monkeypatch,16,legacy_claim=True)
    assert result["direct_archive_NPZ_identity_verified"] is False
    assert result["verification"]["verified_against_exact_original_archive"] is False
    assert result["verification"]["all_supplied_case_records_agree"] is True
    assert all(row["archive_verified"] is False and
               row["verification"]["verified_against_exact_original_archive"] is False
               for row in result["original_10_column_trace_sha_by_case"])


def test_paired_cli_exposes_comparison_and_authentication_separately(monkeypatch,tmp_path,capsys):
    result=synthetic_paired_comparisons(monkeypatch,15)
    monkeypatch.setattr(paired_module,"original_order_pair_100_updates",lambda **kwargs:result)
    out=tmp_path/"paired.json"
    monkeypatch.setattr(sys,"argv",["paired","--out",str(out)])
    paired_module.main()
    printed=json.loads(capsys.readouterr().out)
    saved=json.loads(out.read_text())
    assert printed["archive_NPZ_identity_verified"] is False
    assert printed["verification"]["case_records_compared"]==15
    assert printed["verification"]["all_supplied_case_records_agree"] is False
    assert saved["verification"]==printed["verification"]
