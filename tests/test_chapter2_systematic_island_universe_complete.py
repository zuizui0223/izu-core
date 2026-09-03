import json
from pathlib import Path

from scripts.audit_chapter2_systematic_island_universe_complete import build_complete_audit

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/chapter2_systematic_island_universe_complete_audit_20260903.json"


def test_complete_systematic_audit_matches_frozen_result():
    computed = build_complete_audit()
    frozen = json.loads(RESULT.read_text(encoding="utf-8"))
    assert computed == frozen
    assert computed["effective_search_targets"] == 111
    assert computed["macroregions"] == 8


def test_first_pass_closes_search_frame_without_overclaiming():
    payload = build_complete_audit()
    completion = payload["search_completion"]
    assert completion["targets_with_documented_search_or_prior_coverage"] == 111
    assert completion["targets_never_reviewed_or_prior_covered"] == 0
    assert completion["first_pass_search_complete"] is True
    assert completion["targets_requiring_additional_source_work"] == 49
    assert completion["directly_not_yet_source_gated"] == 0
    assert completion["source_found_needing_ledger_gate"] == 0
    assert completion["nested_targets_needing_specific_gate"] == 0
    boundary = payload["claim_boundary"].lower()
    assert "not a census of all islands on earth" in boundary
    assert "not 111 independent tests" in boundary
    assert "frozen 25-entry identifiability denominator" in boundary
    assert "current 36-entry descriptive confrontation" in boundary


def test_third_wave_closes_exact_remaining_target_set():
    payload = build_complete_audit()
    wave = payload["third_wave_search_gate"]
    assert wave["reviewed_targets"] == 42
    assert wave["initial_search_inconclusive"] == 23
    assert wave["global_confrontation_candidates_before_dedup"] == 7
    assert wave["targets_requiring_stronger_or_broader_source"] == 36
    assert wave["full_chapter2_contract_passes"] == 0
    assert wave["candidate_targets_before_dedup"] == [
        "Andaman and Nicobar Islands",
        "Madagascar",
        "Sardinia",
        "Sicily",
        "Society Islands",
        "Sri Lanka",
        "Taiwan",
    ]
    assert sum(wave["search_outcome_counts"].values()) == 42
    assert wave["search_outcome_counts"]["initial_search_inconclusive"] == 23
    assert wave["search_outcome_counts"]["source_found_crop_reproductive_strategy"] == 5
    assert wave["search_outcome_counts"]["source_found_direct_network"] == 2


def test_third_wave_dedup_keeps_research_entries_and_geography_separate():
    payload = build_complete_audit()
    dedup = payload["third_wave_dedup_review"]
    assert dedup["rows"] == 7
    assert dedup["confirmed_new_higher_level_groups"] == 5
    assert dedup["confirmed_new_group_names"] == [
        "madagascar",
        "sardinia",
        "sicily",
        "sri_lanka",
        "taiwan_lanyu",
    ]
    assert dedup["existing_current36_groups"] == 1
    assert dedup["existing_group_names"] == ["society_islands"]
    assert dedup["held_for_source_verification"] == 1
    assert dedup["held_group_names"] == ["andaman_nicobar"]
    assert dedup["promotion_decision_counts"] == {
        "eligible_existing_group": 1,
        "eligible_new_group": 5,
        "hold_source_verification": 1,
    }
    assert dedup["current36_changed_by_this_audit"] is False


def test_systematic_search_still_recovers_no_full_contract():
    payload = build_complete_audit()
    result = payload["full_contract_result"]
    assert result == {
        "first_wave_passes": 0,
        "second_wave_passes": 0,
        "third_wave_passes": 0,
        "systematic_extension_creates_full_contract": False,
    }
