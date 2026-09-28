import json
from pathlib import Path

from scripts.audit_chapter2_systematic_source_strengthening_wave11 import build_strengthening_audit

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/chapter2_systematic_source_strengthening_wave11_audit_20260905.json"


def test_wave11_matches_frozen_result():
    computed = build_strengthening_audit()
    frozen = json.loads(RESULT.read_text(encoding="utf-8"))
    assert computed == frozen
    assert computed["effective_search_targets"] == 111
    assert computed["first_pass_search_complete"] is True
    assert computed["starting_source_work_targets"] == 9


def test_wave11_closes_final_active_source_queue():
    payload = build_strengthening_audit()
    wave = payload["wave11"]
    assert wave["reviewed_targets"] == 9
    assert wave["closed_from_active_source_work"] == 9
    assert wave["global_confrontation_candidates_after_review"] == 0
    assert wave["candidate_target_names"] == []
    assert wave["full_chapter2_contract_passes"] == 0
    state = payload["source_work_state_after_wave11"]
    assert state["targets_requiring_additional_source_work"] == 0
    assert state["source_review_complete_under_current_protocol"] is True
    assert state["reopen_if_new_source_found"] is True


def test_final_terminal_states_do_not_overclaim_evidence():
    payload = build_strengthening_audit()
    wave = payload["wave11"]
    assert wave["terminal_source_gap_targets"] == 6
    assert wave["terminal_source_gap_names"] == [
        "Kiribati / Gilbert Islands",
        "Niue",
        "São Tomé and Príncipe",
        "Tokelau",
        "Tonga",
        "Tuvalu",
    ]
    assert wave["special_terminal_state_targets"] == 3
    assert wave["special_terminal_state_names"] == [
        "Cayman Islands",
        "Gambier Islands",
        "Wallis and Futuna",
    ]
    assert wave["resolution_class_counts"] == {
        "terminal_host_phylogeography_pollinator_pairing_unrecovered": 1,
        "terminal_indirect_local_mutualism_trace": 1,
        "terminal_local_pollinator_association_effectiveness_unrecovered": 1,
        "terminal_source_gap": 6,
    }


def test_wave11_preserves_manuscript_and_prediction_boundaries():
    payload = build_strengthening_audit()
    boundary = payload["manuscript_boundary"]
    assert boundary["source_backed_research_entries"] == 39
    assert boundary["exact_geographic_labels"] == 34
    assert boundary["changed_by_wave11"] is False
    assert boundary["formal_external_prediction"] == "not_evaluable"
    assert boundary["frozen_full_contracts"] == "0_of_25"
    claim = payload["claim_boundary"].lower()
    assert "queue reaches zero" in claim
    assert "not a census of every island" in claim
    assert "reopenable" in claim
    assert "39 research entries / 34 exact labels" in claim
