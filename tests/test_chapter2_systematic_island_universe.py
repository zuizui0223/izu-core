import json
from pathlib import Path

from scripts.audit_chapter2_systematic_island_universe import build_audit

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/chapter2_systematic_island_universe_audit_v1_20260903.json"


def test_systematic_island_universe_matches_frozen_audit():
    computed = build_audit()
    frozen = json.loads(RESULT.read_text(encoding="utf-8"))
    assert computed == frozen
    assert computed["seed_target_rows"] == 110
    assert computed["effective_target_rows_after_source_native_recovery"] == 111
    assert computed["macroregions"] == 8
    coverage = computed["coverage_after_second_wave"]
    assert coverage["targets_with_documented_search_or_prior_coverage"] == 69
    assert coverage["targets_never_yet_directly_reviewed_or_prior_covered"] == 42
    assert coverage["targets_requiring_additional_source_work"] == 55
    assert coverage["directly_not_yet_source_gated"] == 37
    assert coverage["source_found_needing_ledger_gate"] == 0
    assert coverage["nested_targets_needing_specific_gate"] == 5


def test_systematic_universe_does_not_redefine_frozen_chapter2_denominators():
    computed = build_audit()
    boundary = computed["claim_boundary"].lower()
    assert "frozen 25-entry identifiability denominator" in boundary
    assert "current 36-entry descriptive confrontation" in boundary
    assert "not promotion" in boundary
    assert "search-inconclusive targets remain coverage gaps" in boundary


def test_source_native_overlap_recovery_corrects_search_frame():
    computed = build_audit()
    correction = computed["source_native_overlap_corrections"]
    assert correction["rows"] == 10
    assert correction["current36_source_native_targets_confirmed"] == 10
    assert correction["new_search_targets_added"] == 1
    assert correction["added_target_names"] == ["Three Kings Islands"]
    assert correction["source_reference"] == "10.1093/aob/mcaf005"
    assert computed["macroregion_counts"]["Australasia / Southern Ocean"] == 12
    assert computed["effective_priority_counts"]["covered"] == 27


def test_first_wave_source_gate_is_explicit_and_bounded():
    computed = build_audit()
    gate = computed["first_wave_source_gate"]
    assert gate["gated_targets"] == 7
    assert gate["eligible_for_breadth_after_dedup_review"] == 6
    assert gate["retain_search_record_not_confrontation"] == 1
    assert gate["full_chapter2_contract_passes"] == 0


def test_first_wave_dedup_prevents_pseudoreplication():
    computed = build_audit()
    dedup = computed["first_wave_dedup_review"]
    assert dedup["rows"] == 7
    assert dedup["eligible_research_entries"] == 6
    assert dedup["eligible_higher_level_groups"] == 5
    assert dedup["confirmed_new_higher_level_groups_relative_to_current36"] == 3
    assert dedup["promotion_decision_counts"] == {
        "do_not_promote": 1,
        "eligible_existing_group": 2,
        "eligible_new_group": 2,
        "eligible_shared_new_group": 2,
    }
    assert dedup["current36_changed_by_this_audit"] is False


def test_second_wave_search_and_dedup_are_explicit():
    computed = build_audit()
    wave = computed["second_wave_search_gate"]
    assert wave["reviewed_targets"] == 19
    assert wave["global_confrontation_candidates_before_dedup"] == 5
    assert wave["full_chapter2_contract_passes"] == 0
    assert wave["targets_requiring_stronger_or_broader_source"] == 13
    assert wave["search_outcome_counts"]["initial_search_inconclusive"] == 8
    assert wave["search_outcome_counts"]["source_found_direct"] == 3

    dedup = computed["second_wave_dedup_review"]
    assert dedup["rows"] == 5
    assert dedup["confirmed_new_higher_level_groups"] == 2
    assert dedup["confirmed_new_group_names"] == ["comoros_mayotte", "socotra"]
    assert dedup["existing_current36_groups"] == 1
    assert dedup["overlap_unresolved_groups"] == 2
    assert dedup["overlap_unresolved_group_names"] == ["cook_islands", "samoa"]
    assert dedup["promotion_decision_counts"] == {
        "eligible_existing_group": 1,
        "eligible_new_group": 2,
        "hold_overlap_unresolved": 2,
    }
    assert dedup["current36_changed_by_this_audit"] is False


def test_high_priority_search_pool_remains_explicit():
    computed = build_audit()
    assert computed["effective_priority_counts"]["high"] == 37
    assert computed["seed_coverage_status_counts"]["source_found_needs_ledger_gate"] == 7
    assert computed["seed_coverage_status_counts"]["umbrella_source_verified"] == 11
