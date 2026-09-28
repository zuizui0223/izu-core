import json
from pathlib import Path

from scripts.audit_chapter2_systematic_source_strengthening_wave9 import build_strengthening_audit

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/chapter2_systematic_source_strengthening_wave9_audit_20260905.json"


def test_source_strengthening_wave9_matches_frozen_result():
    computed = build_strengthening_audit()
    frozen = json.loads(RESULT.read_text(encoding="utf-8"))
    assert computed == frozen
    assert computed["effective_search_targets"] == 111
    assert computed["first_pass_search_complete"] is True
    assert computed["starting_source_work_targets"] == 26


def test_terminal_gap_rule_closes_search_without_claiming_biological_absence():
    payload = build_strengthening_audit()
    rule = payload["terminal_gap_rule"]
    assert rule["enabled"] is True
    assert rule["reopen_if_new_source_found"] is True
    lower = rule["definition"].lower()
    assert "literature/source state" in lower
    assert "not evidence of biological absence" in lower


def test_wave9_closes_all_seven_from_active_source_work():
    payload = build_strengthening_audit()
    wave = payload["wave9"]
    assert wave["reviewed_targets"] == 7
    assert wave["closed_from_active_source_work"] == 7
    assert wave["terminal_source_gap_targets"] == 5
    assert wave["terminal_source_gap_names"] == [
        "Bermuda",
        "Chagos Archipelago",
        "Cocos (Keeling) Islands",
        "Desventuradas Islands",
        "Lakshadweep",
    ]
    assert wave["direct_or_partial_evidence_resolutions"] == 2
    assert payload["source_work_state_after_wave9"]["targets_requiring_additional_source_work"] == 19
    assert wave["full_chapter2_contract_passes"] == 0


def test_maldives_and_abc_keep_bounded_evidence_roles():
    payload = build_strengthening_audit()
    wave = payload["wave9"]
    assert wave["global_confrontation_candidates_after_review"] == 2
    assert wave["candidate_target_names"] == ["ABC Islands", "Maldives"]
    assert wave["resolution_class_counts"] == {
        "direct_source_resolved": 1,
        "terminal_partial_subtarget_evidence": 1,
        "terminal_source_gap": 5,
    }
    assert wave["decision_counts"]["retain_candidate_with_curacao_subtarget_limit"] == 1
    assert wave["decision_counts"]["eligible_new_group_with_visitation_effectiveness_caveat"] == 1


def test_wave9_keeps_terminal_gaps_out_of_confrontation_candidates():
    payload = build_strengthening_audit()
    terminal_names = set(payload["wave9"]["terminal_source_gap_names"])
    candidate_names = set(payload["wave9"]["candidate_target_names"])
    assert terminal_names.isdisjoint(candidate_names)
    assert payload["wave9"]["decision_counts"]["terminal_no_qualifying_primary_process_source"] == 2


def test_wave9_preserves_manuscript_and_prediction_boundaries():
    payload = build_strengthening_audit()
    assert payload["manuscript_boundary"] == {
        "source_backed_research_entries": 39,
        "exact_geographic_labels": 34,
        "changed_by_wave9": False,
        "formal_external_prediction": "not_evaluable",
        "frozen_full_contracts": "0_of_25",
    }
    assert payload["full_contract_result"] == {
        "systematic_extension_creates_full_contract": False,
        "source_strengthening_wave9_passes": 0,
    }
    lower = payload["claim_boundary"].lower()
    assert "39-entry / 34-label" in lower
    assert "not_evaluable" in lower
