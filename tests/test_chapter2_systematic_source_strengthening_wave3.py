import json
from pathlib import Path

from scripts.audit_chapter2_systematic_source_strengthening_wave3 import build_strengthening_audit

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/chapter2_systematic_source_strengthening_wave3_audit_20260904.json"


def test_source_strengthening_wave3_matches_frozen_result():
    computed = build_strengthening_audit()
    frozen = json.loads(RESULT.read_text(encoding="utf-8"))
    assert computed == frozen
    assert computed["effective_search_targets"] == 111
    assert computed["first_pass_search_complete"] is True
    assert computed["starting_source_work_targets"] == 43


def test_wave3_clears_four_targets_but_keeps_three_open():
    payload = build_strengthening_audit()
    wave = payload["wave3"]
    assert wave["reviewed_targets"] == 7
    assert wave["cleared_from_source_work"] == 4
    assert wave["cleared_target_names"] == [
        "Guadeloupe",
        "Marquesas Islands",
        "Pitcairn Islands",
        "Virgin Islands",
    ]
    assert wave["remain_open_after_review"] == 3
    assert wave["open_target_names"] == [
        "Cayman Islands",
        "Chatham Islands",
        "Comoros and Mayotte",
    ]
    assert payload["source_work_state_after_wave3"]["targets_requiring_additional_source_work"] == 39


def test_direct_search_resolution_is_not_auto_promotion():
    payload = build_strengthening_audit()
    wave = payload["wave3"]
    assert wave["global_confrontation_candidates_after_review"] == 4
    assert wave["candidate_target_names"] == [
        "Comoros and Mayotte",
        "Guadeloupe",
        "Marquesas Islands",
        "Virgin Islands",
    ]
    assert wave["cleared_candidates"] == 3
    assert "Pitcairn Islands" not in wave["candidate_target_names"]
    assert wave["decision_counts"]["retain_direct_search_record_not_promote"] == 1
    assert wave["decision_counts"]["hold_local_pollination_directness"] == 2
    assert wave["full_chapter2_contract_passes"] == 0


def test_wave3_preserves_scope_and_claim_boundaries():
    payload = build_strengthening_audit()
    state = payload["source_work_state_after_wave3"]
    assert state["comoros_scope_state"] == "mayotte_direct_broad_comoros_incomplete"
    assert state["cayman_source_state"] == "pollinator_association_without_direct_local_plant_pollination"
    assert state["chatham_source_state"] == "geography_covered_process_locality_incomplete"
    boundary = payload["claim_boundary"].lower()
    assert "frozen 25-entry identifiability denominator" in boundary
    assert "current 36-entry descriptive confrontation" in boundary
    assert "pitcairn" in boundary
    assert "comoros/mayotte" in boundary
