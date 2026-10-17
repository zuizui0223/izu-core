"""Source-only final primary-thesis/registered-inference guard, no new biology.

The primary *manuscript* claim is editorial and cannot retrospectively replace
the 2026-10-16 source-frozen co-primary genotype-carrier estimands.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISION = ROOT / "docs/audits/CHAPTER2_MAIN_HYPOTHESIS_DECISION_20261017.json"
Q1 = ROOT / "docs/CHAPTER2_TWO_PROPOSITION_EVIDENCE_RECEIPT_20261016.json"
Q2 = ROOT / "docs/audits/CHAPTER2_Q2_I_SUPPORT_384_ORIGINAL_READOUT_20261016.json"
Q4 = ROOT / "data/results/chapter2_island_demographic_independent32_20261008.json"
ONE_PAPER = ROOT / "docs/CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md"
INTERPRETATION = ROOT / "docs/CHAPTER2_MAIN_HYPOTHESIS_DECISION_20261017.md"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def support_block(decision, key):
    return next(row for row in decision["supporting_logic"] if row["id"] == key)


def test_manuscript_claim_is_precendence_not_causal_necessity():
    d, q1 = read(DECISION), read(Q1)
    assert d["status"] == "EDITORIAL_PRIMARY_CLAIM_LOCKED_WITH_REGISTERED_INFERENCE_UNCHANGED"
    assert d["primary_manuscript_hypothesis"]["id"] == "H_MAIN_NONSEQUENTIAL_NECESSITY"
    assert d["manuscript_decision"]["not_replace_original_preregistered_primaries"] is True
    assert d["manuscript_decision"]["not_ascribe_to_wild_islands"] is True
    assert d["manuscript_decision"]["not_treat_multi_cohort_logic_as_one_identified_mediation_chain"] is True
    assert q1["original_same_mating_condition"]["assurance_first"]["events"] == 51
    assert q1["original_same_mating_condition"]["assurance_first"]["visitor_histories"] == 64
    original = d["primary_manuscript_hypothesis"]
    assert original["assurance_first_original_history"]["successes"] == 51
    assert original["fixed_A_counterexample"]["fixed_expressed_A"] == .5
    assert original["fixed_A_counterexample"]["still_selfing"] is True
    q1_settings = q1["fresh_founder_q1"]["settings"]
    assert len(q1_settings) == 4
    for j, item in enumerate(q1_settings):
        assert item["negative_fixed_founder_means"] == 8
        assert item["fixed_far_change_bootstrap95"][1] < 0
        assert item["fixed_far_change_from_actual_founder_mean"] == (
            original["fixed_A_counterexample"]["new_eight_founder_fixed_A_far_change_from_founder_means"][j]
        )
        assert item["fixed_far_change_bootstrap95"] == (
            original["fixed_A_counterexample"]["new_eight_founder_fixed_A_far_change_cis"][j]
        )


def test_384_registered_primary_did_not_become_confirmed_or_equivalent():
    d, r = read(DECISION), read(Q2)
    q2 = support_block(d, "H_Q2_CARRIER_NUMBER_ORDER_AND_EVENT")
    assert q2["status"] == "REGISTERED_BOTH_COPRIMARY_INCONCLUSIVE"
    assert q2["joint_result"] == r["registered_inference"]["result"] == "both_inconclusive"
    assert r["original_run"]["original_cases"] == 384
    assert q2["original_action_run"] == r["original_run"]["run_id"] == 38918737325
    assert q2["registered_joint_gate"] == "BOTH co-primary adjusted intervals must exclude zero"
    assert len(q2["co_primary"]) == 2
    for key,record in zip(("carrier_order_score_delta", "carrier_I_event_delta"),q2["co_primary"]):
        origin = r["coprimary"][key]
        assert record["estimate"] == origin["estimate"]
        assert record["bonferroni_simultaneous_97_5_CI"] == origin["simultaneous_familywise_CI"]
        assert record["excludes_zero"] is origin["excludes_zero"] is False
        assert origin["simultaneous_familywise_CI"][0] < 0 < origin["simultaneous_familywise_CI"][1]
    assert r["original_six_class_cells"]["far"]["dense_reachable"]["I_events"] == 20
    assert r["original_six_class_cells"]["far"]["sparse_reachable"]["I_events"] == 8
    assert q2["structural_control_far_I_events"] == r["original_six_class_cells"]["far"]["dense_unreachable"]["I_events"] == 0
    assert q2["structural_control_near_I_events"] == r["original_six_class_cells"]["near"]["dense_unreachable"]["I_events"] == 0


def test_access_proof_and_demographic_results_remain_separate_cohorts():
    d, original, q4 = read(DECISION), read(Q1), read(Q4)
    access = support_block(d, "H_ACCESS_SUPPORT_BOUND")
    assert access["status"] == "MATHEMATICAL_UNDER_PREMISES_AND_SOURCE_OBSERVED"
    assert access["numeric_evidence"]["excluded_before_fixation"] == original["support_loss"]["excluded_before_fixation"] == 703
    assert access["numeric_evidence"]["excluded_before_fixation_without_prior_I_event"] == 702
    assert original["support_loss"]["among_703_preexisting_I_event"] == 1
    assert access["numeric_evidence"]["conditioned_positive_parental_weighting_but_zero_child_copies"] == original["support_loss"]["conditional_expected_low_I_allele_frequency_favouring_but_realized_zero"] == 315
    q4_claim = support_block(d, "H_Q4_CONDITIONAL_OCCUPANCY")
    assert q4_claim["status"] == "SUPPORTED_SEPARATE_REGISTERED_STRESS_INTERACTION_NO_ORDER_MEDIATION"
    assert q4["predeclared_pooled_primary"]["pass"] is True
    assert q4_claim["pooled_interaction_points"] == 100*q4["predeclared_pooled_primary"]["mean"]
    assert q4_claim["ci_points"] == [100*v for v in q4["predeclared_pooled_primary"]["bootstrap95"]]


def test_editorial_lock_does_not_change_existing_paper_or_original_Q1_Q4():
    d=read(DECISION)
    text=INTERPRETATION.read_text(encoding="utf-8")
    source=ONE_PAPER.read_text(encoding="utf-8")
    assert "384経路" in text and "両方未確定" in text
    assert "51/64" in text and "703" in text
    assert "採用する中心命題" in text
    assert "Both co-primary intervals included zero" in source
    assert "A evolvability **continued during the future**" in source
    assert "not a natural mediation analysis" in source
    assert source.splitlines()[0].startswith("# Selection, sequence and finite realization")
    assert d["further_work_status"].startswith("No additional biological cohorts authorized")
    assert d["manuscript_decision"]["not_replace_original_preregistered_primaries"] is True
