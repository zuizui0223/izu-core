import json
from pathlib import Path

from scripts.audit_chapter2_systematic_source_strengthening_wave10 import build_strengthening_audit

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/chapter2_systematic_source_strengthening_wave10_audit_20260905.json"


def test_wave10_matches_frozen_result():
    computed = build_strengthening_audit()
    frozen = json.loads(RESULT.read_text(encoding="utf-8"))
    assert computed == frozen
    assert computed["effective_search_targets"] == 111
    assert computed["first_pass_search_complete"] is True
    assert computed["starting_source_work_targets"] == 19


def test_wave10_closes_ten_without_creating_candidates():
    payload = build_strengthening_audit()
    wave = payload["wave10"]
    assert wave["reviewed_targets"] == 10
    assert wave["closed_from_active_source_work"] == 10
    assert wave["global_confrontation_candidates_after_review"] == 0
    assert wave["candidate_target_names"] == []
    assert wave["full_chapter2_contract_passes"] == 0
    assert payload["source_work_state_after_wave10"]["targets_requiring_additional_source_work"] == 9


def test_terminal_states_remain_distinct_and_reopenable():
    payload = build_strengthening_audit()
    assert payload["terminal_gap_rule"]["enabled"] is True
    assert payload["terminal_gap_rule"]["reopen_if_new_source_found"] is True
    assert payload["wave10"]["resolution_class_counts"] == {
        "terminal_authoritative_conflict": 1,
        "terminal_geography_covered_process_gap": 1,
        "terminal_primary_source_explicit_unknown": 1,
        "terminal_source_gap": 7,
    }
    state = payload["source_work_state_after_wave10"]
    assert state["terminal_special_state_targets"] == [
        "Chatham Islands",
        "Norfolk Island",
        "Turks and Caicos",
    ]
    assert state["terminal_source_gap_targets"] == [
        "Ascension Island",
        "Bioko",
        "Dalmatian Islands",
        "Marshall Islands",
        "Nauru",
        "Selvagens",
        "Tristan da Cunha",
    ]


def test_wave10_preserves_manuscript_and_prediction_boundaries():
    payload = build_strengthening_audit()
    boundary = payload["manuscript_boundary"]
    assert boundary["source_backed_research_entries"] == 39
    assert boundary["exact_geographic_labels"] == 34
    assert boundary["changed_by_wave10"] is False
    assert boundary["formal_external_prediction"] == "not_evaluable"
    assert boundary["frozen_full_contracts"] == "0_of_25"
    claim = payload["claim_boundary"].lower()
    assert "without converting source gaps" in claim
    assert "19 to 9" in claim
    assert "39 research entries / 34 exact labels" in claim
