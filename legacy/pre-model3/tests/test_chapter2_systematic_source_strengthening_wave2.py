import json
from pathlib import Path

from scripts.audit_chapter2_systematic_source_strengthening_wave2 import build_strengthening_audit

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/chapter2_systematic_source_strengthening_wave2_audit_20260904.json"


def test_source_strengthening_wave2_matches_frozen_result():
    computed = build_strengthening_audit()
    frozen = json.loads(RESULT.read_text(encoding="utf-8"))
    assert computed == frozen
    assert computed["effective_search_targets"] == 111
    assert computed["first_pass_search_complete"] is True
    assert computed["starting_source_work_targets"] == 48


def test_five_targets_are_cleared_without_creating_full_contract():
    payload = build_strengthening_audit()
    wave = payload["wave2"]
    assert wave["reviewed_targets"] == 6
    assert wave["cleared_from_source_work"] == 5
    assert wave["cleared_target_names"] == [
        "Cabo Verde",
        "Corsica",
        "Cyprus",
        "Maltese Islands",
        "Tasmania",
    ]
    assert wave["new_global_confrontation_candidates"] == 5
    assert wave["candidate_target_names"] == wave["cleared_target_names"]
    assert wave["decision_counts"] == {
        "eligible_new_group": 5,
        "hold_mechanism_conflict": 1,
    }
    assert wave["source_verification_counts"] == {
        "authoritative_sources_conflict_unresolved": 1,
        "primary_article_verified": 4,
        "primary_government_research_report": 1,
    }
    assert wave["full_chapter2_contract_passes"] == 0
    assert payload["source_work_state_after_wave2"]["targets_requiring_additional_source_work"] == 43


def test_norfolk_conflict_remains_open():
    payload = build_strengthening_audit()
    wave = payload["wave2"]
    assert wave["remain_open_after_review"] == 1
    assert wave["open_target_names"] == ["Norfolk Island"]
    assert wave["decision_counts"]["hold_mechanism_conflict"] == 1
    assert payload["source_work_state_after_wave2"]["norfolk_source_state"] == "authoritative_mechanism_conflict_unresolved"


def test_frozen_denominators_remain_untouched():
    boundary = build_strengthening_audit()["claim_boundary"].lower()
    assert "frozen 25-entry identifiability denominator" in boundary
    assert "current 36-entry descriptive confrontation" in boundary
    assert "formal prediction readiness" in boundary
