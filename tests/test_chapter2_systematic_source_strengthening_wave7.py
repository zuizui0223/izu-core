import json
from pathlib import Path

from scripts.audit_chapter2_systematic_source_strengthening_wave7 import build_strengthening_audit

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/chapter2_systematic_source_strengthening_wave7_audit_20260904.json"


def test_source_strengthening_wave7_matches_frozen_result():
    computed = build_strengthening_audit()
    frozen = json.loads(RESULT.read_text(encoding="utf-8"))
    assert computed == frozen
    assert computed["effective_search_targets"] == 111
    assert computed["first_pass_search_complete"] is True
    assert computed["starting_source_work_targets"] == 32


def test_austral_and_tuamotu_resolve_without_pseudoreplication():
    payload = build_strengthening_audit()
    wave = payload["wave7"]
    assert wave["reviewed_targets"] == 7
    assert wave["cleared_from_source_work"] == 2
    assert wave["cleared_target_names"] == ["Austral Islands", "Tuamotu Archipelago"]
    assert wave["global_confrontation_candidates_after_review"] == 0
    assert wave["candidate_target_names"] == []
    assert wave["decision_counts"]["resolve_existing_french_polynesia_source_no_new_entry"] == 2
    assert payload["source_work_state_after_wave7"]["targets_requiring_additional_source_work"] == 30


def test_remaining_nested_and_sparse_targets_stay_open():
    payload = build_strengthening_audit()
    wave = payload["wave7"]
    assert wave["remain_open_after_review"] == 5
    assert wave["open_target_names"] == [
        "Gambier Islands",
        "Kiribati / Gilbert Islands",
        "Niue",
        "Tuvalu",
        "Wallis and Futuna",
    ]
    assert wave["decision_counts"]["hold_local_pollination_directness"] == 2
    assert wave["decision_counts"]["hold_direct_pollination_unrecovered"] == 3


def test_full_contract_and_frozen_denominators_remain_unchanged():
    payload = build_strengthening_audit()
    assert payload["wave7"]["full_chapter2_contract_passes"] == 0
    assert payload["full_contract_result"] == {
        "systematic_extension_creates_full_contract": False,
        "source_strengthening_wave7_passes": 0,
    }
    boundary = payload["claim_boundary"].lower()
    assert "not split into new research entries" in boundary
    assert "frozen 25-entry audit" in boundary
    assert "current 36-entry confrontation" in boundary
