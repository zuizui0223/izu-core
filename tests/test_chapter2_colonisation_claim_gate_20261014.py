"""Source-authenticated claim admission for genetic-access founder design.

This validates three distinct FIRST-OFFSPRING analytic quantities and
specifically rejects promotion into long-run order or island persistence.
"""
from scripts.audit_chapter2_colonisation_claim_gate_20261014 import claim_gate


def test_source_claim_gate_preserves_the_three_distinct_estimands():
    report=claim_gate()
    assert report["source_status"]=="ORIGINAL_MODEL3_OPERATOR_ON_EXPLICIT_SYNTHETIC_T0_ONLY"
    assert report["new_biological_histories"]==0
    assert report["observed_natural_islands"]==0
    assert report["t0_source_profiles"]==16
    assert report["source_context_m_combinations"]==192
    assert report["order_score_D"]=="NOT_MEASURED_NO_BIOLOGICAL_FUTURES"
    assert report["sustained_twenty_occupied_census_response"]=="NOT_MEASURED"
    assert report["population_persistence_Q4"]=="NOT_MEASURED"
    assert len(report["admitted_claims"])==4
    assert len(report["excluded_claims"])==5


def test_signed_parent_midpoint_access_rises_but_founder_threshold_not_monotonic():
    r=claim_gate()
    for c in r["context_summary"]:
        assert c["artificial_source_profiles"]==16
        assert c["signed_joint_directional_contrast_positive_source_count"]==16
        assert c["m12_minus_m0_signed_parent_midpoint_A_up_I_down_min"]>0
        assert c["m12_minus_m0_signed_parent_midpoint_A_up_I_down_max"]>0
        assert (c["founder_mean_one_child_positive_contrast_count"]+
                c["founder_mean_one_child_negative_contrast_count"]+
                c["founder_mean_one_child_tie_count"])==16
    c0=next(x for x in r["context_summary"] if x["visitor_context"]==0)
    assert c0["founder_mean_one_child_positive_contrast_count"]==5
    assert c0["founder_mean_one_child_negative_contrast_count"]==11
    assert c0["founder_mean_one_child_tie_count"]==0
    assert c0["founder_mean_m0_one_child_both_thresholds_positive_count"]==15
    assert c0["signed_m0_from_outcross_positive_source_count"]==0
    for c in r["context_summary"]:
        if c["visitor_context"]!=0:
            assert c["signed_m0_from_outcross_positive_source_count"]==16


def test_qualifiers_for_unsupported_ecological_and_causal_claims():
    r=claim_gate()
    forbidden=" ".join(r["excluded_claims"])
    assert "long-run evolutionary order" in forbidden
    assert "population survival" in forbidden
    assert "pilot" in forbidden
    assert "empirically independent natural island" in forbidden
    assert "directional selection" in forbidden
    assert r["new_biological_histories"]==0
