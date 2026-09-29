import json
from pathlib import Path

from scripts.audit_chapter2_systematic_source_strengthening_wave6 import build_strengthening_audit

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/chapter2_systematic_source_strengthening_wave6_audit_20260904.json"


def test_source_strengthening_wave6_matches_frozen_result():
    computed = build_strengthening_audit()
    frozen = json.loads(RESULT.read_text(encoding="utf-8"))
    assert computed == frozen
    assert computed["effective_search_targets"] == 111
    assert computed["first_pass_search_complete"] is True
    assert computed["starting_source_work_targets"] == 34


def test_faroe_and_st_vincent_clear_source_work_with_distinct_roles():
    payload = build_strengthening_audit()
    wave = payload["wave6"]
    assert wave["reviewed_targets"] == 7
    assert wave["cleared_from_source_work"] == 2
    assert wave["cleared_target_names"] == ["Faroe Islands", "Saint Vincent and the Grenadines"]
    assert wave["global_confrontation_candidates_after_review"] == 1
    assert wave["candidate_target_names"] == ["Faroe Islands"]
    assert wave["cleared_candidates"] == 1
    assert payload["source_work_state_after_wave6"]["targets_requiring_additional_source_work"] == 32


def test_open_gaps_and_norfolk_taxonomic_correction_remain_explicit():
    payload = build_strengthening_audit()
    wave = payload["wave6"]
    assert wave["remain_open_after_review"] == 5
    assert wave["open_target_names"] == [
        "Bioko",
        "Cayman Islands",
        "Dalmatian Islands",
        "Norfolk Island",
        "Turks and Caicos",
    ]
    assert wave["decision_counts"]["hold_direct_pollination_unrecovered"] == 3
    assert wave["decision_counts"]["hold_local_pollination_directness"] == 1
    assert wave["decision_counts"]["hold_pollination_mechanism_unresolved"] == 1
    assert payload["source_work_state_after_wave6"]["norfolk_source_state"] == "taxonomic_sex_system_resolved_pollination_mechanism_unresolved"
    assert payload["source_work_state_after_wave6"]["turks_source_state"] == "primary_article_explicitly_reports_pollination_unknown"


def test_historical_faroe_mechanism_is_not_overstated():
    payload = build_strengthening_audit()
    assert payload["source_work_state_after_wave6"]["faroe_source_state"] == "historical_primary_pollination_monograph_with_later_mechanism_caveat"
    assert payload["wave6"]["decision_counts"]["eligible_new_group_historical_primary_with_mechanism_caveat"] == 1


def test_full_contract_and_frozen_denominators_remain_unchanged():
    payload = build_strengthening_audit()
    assert payload["wave6"]["full_chapter2_contract_passes"] == 0
    assert payload["full_contract_result"] == {
        "systematic_extension_creates_full_contract": False,
        "source_strengthening_wave6_passes": 0,
    }
    boundary = payload["claim_boundary"].lower()
    assert "frozen 25-entry identifiability audit" in boundary
    assert "current 36-entry descriptive confrontation" in boundary
    assert "turks and caicos" in boundary
