import json
from pathlib import Path

from scripts.audit_chapter2_systematic_source_strengthening_wave4 import build_strengthening_audit

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/chapter2_systematic_source_strengthening_wave4_audit_20260904.json"


def test_source_strengthening_wave4_matches_frozen_result():
    computed = build_strengthening_audit()
    frozen = json.loads(RESULT.read_text(encoding="utf-8"))
    assert computed == frozen
    assert computed["effective_search_targets"] == 111
    assert computed["starting_source_work_targets"] == 39


def test_wave4_clears_only_rapa_nui_source_quality():
    payload = build_strengthening_audit()
    wave = payload["wave4"]
    assert wave["reviewed_targets"] == 8
    assert wave["cleared_from_source_work"] == 1
    assert wave["cleared_target_names"] == ["Rapa Nui / Easter Island"]
    assert wave["remain_open_after_review"] == 7
    assert wave["global_confrontation_candidates_after_review"] == 0
    assert wave["candidate_target_names"] == []
    assert payload["source_work_state_after_wave4"]["targets_requiring_additional_source_work"] == 38


def test_wave4_keeps_directness_gaps_explicit():
    payload = build_strengthening_audit()
    wave = payload["wave4"]
    assert wave["decision_counts"] == {
        "hold_direct_pollination_unrecovered": 5,
        "hold_local_pollination_directness": 2,
        "retain_breeding_system_record_not_promote": 1,
    }
    assert "Palau" in wave["open_target_names"]
    assert "Solomon Islands" in wave["open_target_names"]
    assert "Tonga" in wave["open_target_names"]
    assert payload["source_work_state_after_wave4"]["palau_source_state"] == "primary_article_explicitly_reports_no_published_pollination_observations"
    assert wave["full_chapter2_contract_passes"] == 0


def test_wave4_does_not_turn_exsitu_breeding_into_extant_transition():
    payload = build_strengthening_audit()
    assert payload["source_work_state_after_wave4"]["rapa_nui_source_state"] == "ex_situ_self_pollination_and_controlled_breeding_record_not_extant_transition"
    boundary = payload["claim_boundary"].lower()
    assert "rapa nui is cleared only as an ex-situ breeding-system record" in boundary
    assert "frozen 25-entry audit" in boundary
    assert "current 36-entry confrontation" in boundary
    assert "formal prediction readiness" in boundary
