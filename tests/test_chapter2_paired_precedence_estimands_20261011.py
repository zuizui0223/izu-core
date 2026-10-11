"""Frozen historical paired order estimands: do not conflate chronological onset."""
import json
import pytest
from scripts.audit_chapter2_paired_precedence_estimands_20261011 import (
    STATUS,SETTINGS,MUTATION,THRESHOLDS,LABELS,load_frozen_readout,
    aligned_events,summarize_pairs,audit
)


def test_archived_source_is_complete_and_history_alignment_is_exact():
    d=load_frozen_readout()
    assert d["verified_new_cases"]==2048
    assert d["verified_near_references"]==2048
    for s in SETTINGS:
        for m in MUTATION:
            for t in THRESHOLDS:
                pairs=aligned_events(d,s,m,t)
                assert len(pairs)==64
                assert [x["history_seed"] for x in pairs]==list(range(76001,76065))
                assert all(x["far_from_founder_order"] in LABELS for x in pairs)
                assert all(x["far_minus_near_order"] in LABELS for x in pairs)
                assert sum(sum(x.values()) for x in summarize_pairs(pairs)["order_cross_tab_6x6"].values())==64


def test_confirmed_delayed_cost_source_relabels_are_not_all_strict_reversals():
    d=load_frozen_readout()
    p=aligned_events(d,"assurance_cost",.01,.05)
    s=summarize_pairs(p)
    assert s["within_far_counts"]=={"assurance_first":51,"near_simultaneous":13}
    assert s["incremental_far_minus_near_counts"]=={
        "near_simultaneous":20,"investment_first":32,
        "assurance_first":10,"investment_only":2,
    }
    assert s["reclassified_any_reason"]==52
    assert s["strict_opposite_order"]==22
    assert s["reclassified_but_not_strict_opposite"]==30
    assert s["order_cross_tab_6x6"]["assurance_first"]["investment_first"]==22
    assert s["within_median_lag_I_minus_A"]==pytest.approx(24)
    assert s["divergence_both_crossing_n"]==62
    assert s["divergence_median_lag_I_minus_A"]==pytest.approx(-6.5)
    assert s["n_original_independent_history_clusters"]==64


def test_prior_selfing_is_distinct_and_censoring_is_explicit():
    d=load_frozen_readout()
    s=summarize_pairs(aligned_events(d,"prior_selfing",.01,.05))
    assert s["within_far_counts"]=={"assurance_first":38,"near_simultaneous":26}
    assert s["incremental_far_minus_near_counts"]=={
        "investment_only":31,"assurance_only":4,"investment_first":3,
        "neither":16,"assurance_first":7,"near_simultaneous":3
    }
    assert s["reclassified_any_reason"]==56
    assert s["strict_opposite_order"]==2
    assert s["divergence_both_crossing_n"]==13
    assert s["within_median_lag_I_minus_A"]==pytest.approx(6)


def test_all_12_cells_and_threshold_sensitivity_including_mutation_zero():
    d=audit()
    assert d["status"]==STATUS
    assert d["n_new_evolutionary_histories"]==0
    assert d["n_independent_ecological_systems"]==0
    assert d["analysis_count"]==len(SETTINGS)*len(MUTATION)*len(THRESHOLDS)==12
    seen={(r["setting"],r["mutation_rate"],r["crossing_threshold"]) for r in d["results"]}
    assert seen=={(s,m,t) for s in SETTINGS for m in MUTATION for t in THRESHOLDS}
    assert all(r["paired_summary"]["n_original_independent_history_clusters"]==64
               for r in d["results"])
    assert all(r["paired_summary"]["reclassified_any_reason"]>=
               r["paired_summary"]["strict_opposite_order"] for r in d["results"])
    assert all(r["sustained_updates"]==20 for r in d["results"])
    assert all(r["near_simultaneous_tolerance"]==5 for r in d["results"])
    assert any("does not demonstrate when selection coefficients" in t
               for t in d["interpretation_ceiling"])
    json.dumps(d,allow_nan=False)


def test_reject_incomplete_fake_readout(tmp_path):
    fake=tmp_path/"false_readout.json"
    fake.write_text(json.dumps({"status":"incomplete","temporal_order":[]}))
    with pytest.raises(ValueError):
        load_frozen_readout(fake)
