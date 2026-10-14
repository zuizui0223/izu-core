"""Adversarial no-biology test of six-class SOURCE-first aggregation."""
from copy import deepcopy
from hashlib import sha256
from math import isclose

import pytest

from scripts.audit_chapter2_Q2_cluster_precision_review_20261014 import (
    ARMS, CLASSES, OLD_CONTEXTS, paired_source_level_class_contrasts,
)
from scripts.audit_chapter2_Q2_sixclass_source_aggregation_20261014 import (
    aggregate_supplied_paired_six_class_rows,
    aggregate_validated_source_vectors,
)


def _toy_paired_sixclass_cases(*, opposite_source: bool, histories: int=2):
    """All original six-class labels are artificial *schema* fixtures only."""
    rows=[]
    for source in ("S0","S1"):
        for history in range(histories):
            for context in OLD_CONTEXTS:
                for arm in ARMS:
                    # S0 A-first -> I-first, S1 is either reverse or same.
                    if source=="S0" or not opposite_source:
                        category="assurance_first" if arm==0 else "investment_first"
                    else:
                        category="investment_first" if arm==0 else "assurance_first"
                    rows.append({
                        "source_id":source,
                        "original_source_genome_sha256":sha256(
                            ("TOY-ONLY-GENOME-"+source).encode()
                        ).hexdigest(),
                        "history_id":f"toy-h{history}",
                        "future_master_identity":f"TOY-NO-Model3-{source}-h{history}",
                        "context":context,
                        "m":arm,
                        "category":category,
                        "extinct_by_horizon":False,
                    })
    return rows


def test_perfectly_opposing_source_effects_cancel_in_primary_six_class_vector():
    """2 opposed source shifts: EACH TV=1, pooled TV=0, not 'big effect'."""
    rows=_toy_paired_sixclass_cases(opposite_source=True)
    result=aggregate_supplied_paired_six_class_rows(rows)
    assert result["status"]=="SOURCE_LEVEL_SIX_CLASS_VECTOR_ARITHMETIC_ONLY"
    assert result["new_biological_futures_generated"]==0
    assert result["raw_genomes_or_genuine_source_independence_verified"] is False
    assert result["number_source_clusters_assumed_distinct"]==2
    assert result["n_paired_histories_per_source"]==2
    assert result["six_classes_in_original_order"]==list(CLASSES)
    assert result["no_Q2_sustained_response_confirmed"] is True
    assert result["no_Q4_persistence_inference"] is True
    for ctx in result["original_visitor_context_summaries"]:
        delta=ctx["primary_source_averaged_six_class_probability_difference_m12_minus_m0"]
        assert set(delta)==set(CLASSES)
        assert all(v==0 for v in delta.values())
        assert ctx["primary_vector_sums_to_zero"] is True
        assert ctx["population_averaged_arm_total_variation_after_source_aggregation"]==0
        assert ctx["mean_source_conditional_total_variation_BEFORE_source_aggregation"]==1
        assert ctx["source_effect_cancellation_gap"]==1
        assert ctx["secondary_D_from_aggregated_vector"]==0
        assert ctx["source_D_positive_count"]==1
        assert ctx["source_D_negative_count"]==1
        assert ctx["source_D_zero_within_tolerance_count"]==0


def test_same_direction_across_both_sources_is_not_cancelled():
    result=aggregate_supplied_paired_six_class_rows(
        _toy_paired_sixclass_cases(opposite_source=False)
    )
    for c in result["original_visitor_context_summaries"]:
        v=c["primary_source_averaged_six_class_probability_difference_m12_minus_m0"]
        assert v["assurance_first"]==-1
        assert v["investment_first"]==1
        assert all(v[k]==0 for k in CLASSES if k not in
                   ("assurance_first","investment_first"))
        assert c["population_averaged_arm_total_variation_after_source_aggregation"]==1
        assert c["mean_source_conditional_total_variation_BEFORE_source_aggregation"]==1
        assert c["source_effect_cancellation_gap"]==0
        assert c["secondary_D_from_aggregated_vector"]==-2
        assert c["source_D_positive_count"]==0
        assert c["source_D_negative_count"]==2


def test_strict_source_independence_and_pairing_are_checked_before_aggregation():
    records=_toy_paired_sixclass_cases(opposite_source=True)
    assert len(records)==2*2*3*2
    assert aggregate_supplied_paired_six_class_rows(list(reversed(records)))==(
        aggregate_supplied_paired_six_class_rows(records)
    )
    for mode in ("missing_case","duplicate","source_digest_reuse",
                 "master_reuse","unknown_category"):
        altered=deepcopy(records)
        if mode=="missing_case":
            altered.pop()
        elif mode=="duplicate":
            altered.append(deepcopy(altered[0]))
        elif mode=="source_digest_reuse":
            for row in altered:
                if row["source_id"]=="S1":
                    row["original_source_genome_sha256"]=altered[0][
                        "original_source_genome_sha256"]
        elif mode=="master_reuse":
            for row in altered:
                if row["source_id"]=="S1" and row["history_id"]=="toy-h0":
                    row["future_master_identity"]="TOY-NO-Model3-S0-h0"
        elif mode=="unknown_category":
            altered[0]["category"]="fictitious_order_category"
        with pytest.raises(ValueError):
            aggregate_supplied_paired_six_class_rows(altered)


def test_internal_aggregate_rejects_invalid_six_class_mass_and_wrong_source_roster():
    valid=paired_source_level_class_contrasts(
        _toy_paired_sixclass_cases(opposite_source=True)
    )
    for mode in ("outside_category","out_of_bounds","mass_not_zero",
                 "wrong_secondary_D","duplicated_context","missing_context",
                 "not_admitted"):
        r=deepcopy(valid)
        if mode=="outside_category":
            r["source_records"][0]["six_class_probability_differences_m12_minus_m0"][
                "not_a_six_class"]="fake"
        elif mode=="out_of_bounds":
            r["source_records"][0]["six_class_probability_differences_m12_minus_m0"][
                "assurance_first"]=2.5
        elif mode=="mass_not_zero":
            r["source_records"][0]["six_class_probability_differences_m12_minus_m0"][
                "neither"]=.2
        elif mode=="wrong_secondary_D":
            r["source_records"][0]["secondary_order_score_D_difference"]=8
        elif mode=="duplicated_context":
            r["source_records"].append(deepcopy(r["source_records"][0]))
        elif mode=="missing_context":
            r["source_records"].pop()
        elif mode=="not_admitted":
            r["status"]="PRETEND_THIS_IS_BIOLOGICAL_RESULT"
        with pytest.raises((ValueError,AssertionError)):
            aggregate_validated_source_vectors(r)


def test_single_source_cannot_claim_an_independent_between_source_contrast():
    source_rows=_toy_paired_sixclass_cases(opposite_source=True)
    source_rows=[r for r in source_rows if r["source_id"]=="S0"]
    validated=paired_source_level_class_contrasts(source_rows)
    with pytest.raises(ValueError,match="At least two"):
        aggregate_validated_source_vectors(validated)


def test_outputs_do_not_report_fake_significance_or_external_island_conclusion():
    r=aggregate_supplied_paired_six_class_rows(
        _toy_paired_sixclass_cases(opposite_source=True)
    )
    assert r["no_p_values_or_simultaneous_intervals"] is True
    assert r["raw_genomes_or_genuine_source_independence_verified"] is False
    assert "source-mean" in r["primary_estimand"]
    assert "TV" in " ".join(r["secondary_contrasts"])
    assert r["new_biological_futures_generated"]==0
