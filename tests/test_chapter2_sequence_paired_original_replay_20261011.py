"""Pair archived Model3 crossing estimands to the REAL original diploid replay."""
import numpy as np
import pytest

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
