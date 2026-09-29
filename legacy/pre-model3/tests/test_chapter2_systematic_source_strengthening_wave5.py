import json
from pathlib import Path

from scripts.audit_chapter2_systematic_source_strengthening_wave5 import build_strengthening_audit

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/chapter2_systematic_source_strengthening_wave5_audit_20260904.json"


def test_source_strengthening_wave5_matches_frozen_result():
    computed = build_strengthening_audit()
    frozen = json.loads(RESULT.read_text(encoding="utf-8"))
    assert computed == frozen
    assert computed["effective_search_targets"] == 111
    assert computed["first_pass_search_complete"] is True
    assert computed["starting_source_work_targets"] == 38


def test_four_targets_are_cleared_and_three_remain_open():
    payload = build_strengthening_audit()
    wave = payload["wave5"]
    assert wave["reviewed_targets"] == 7
    assert wave["cleared_from_source_work"] == 4
    assert wave["cleared_target_names"] == [
        "Crete",
        "Iceland",
        "Philippines",
        "Trinidad and Tobago",
    ]
    assert wave["remain_open_after_review"] == 3
    assert wave["open_target_names"] == ["ABC Islands", "Bermuda", "Christmas Island"]
    assert payload["source_work_state_after_wave5"]["targets_requiring_additional_source_work"] == 34


def test_candidate_and_subtarget_boundaries_are_explicit():
    payload = build_strengthening_audit()
    wave = payload["wave5"]
    assert wave["global_confrontation_candidates_after_review"] == 5
    assert wave["cleared_candidates"] == 4
    assert wave["candidate_target_names"] == [
        "ABC Islands",
        "Crete",
        "Iceland",
        "Philippines",
        "Trinidad and Tobago",
    ]
    assert wave["decision_counts"] == {
        "eligible_new_group": 4,
        "eligible_new_group_with_subtarget_limit": 1,
        "hold_direct_pollination_unrecovered": 2,
    }
    assert payload["source_work_state_after_wave5"]["abc_scope_state"] == "curacao_direct_broad_abc_incomplete"


def test_full_contract_and_frozen_denominators_remain_unchanged():
    payload = build_strengthening_audit()
    assert payload["wave5"]["full_chapter2_contract_passes"] == 0
    assert payload["full_contract_result"] == {
        "systematic_extension_creates_full_contract": False,
        "source_strengthening_wave5_passes": 0,
    }
    boundary = payload["claim_boundary"].lower()
    assert "frozen 25-entry identifiability audit" in boundary
    assert "current 36-entry descriptive confrontation" in boundary
    assert "curacao evidence is not generalized" in boundary
