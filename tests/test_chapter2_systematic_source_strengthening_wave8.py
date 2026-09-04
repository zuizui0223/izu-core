import json
from pathlib import Path

from scripts.audit_chapter2_systematic_source_strengthening_wave8 import build_strengthening_audit

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/chapter2_systematic_source_strengthening_wave8_audit_20260905.json"


def test_source_strengthening_wave8_matches_frozen_result():
    computed = build_strengthening_audit()
    frozen = json.loads(RESULT.read_text(encoding="utf-8"))
    assert computed == frozen
    assert computed["effective_search_targets"] == 111
    assert computed["first_pass_search_complete"] is True
    assert computed["starting_source_work_targets"] == 30


def test_wave8_clears_four_targets_and_leaves_three_open():
    payload = build_strengthening_audit()
    wave = payload["wave8"]
    assert wave["reviewed_targets"] == 7
    assert wave["cleared_from_source_work"] == 4
    assert wave["cleared_target_names"] == [
        "Christmas Island",
        "Comoros and Mayotte",
        "Palau",
        "Solomon Islands",
    ]
    assert wave["remain_open_after_review"] == 3
    assert wave["open_target_names"] == [
        "Cayman Islands",
        "Chatham Islands",
        "Norfolk Island",
    ]
    assert payload["source_work_state_after_wave8"]["targets_requiring_additional_source_work"] == 26
    assert wave["full_chapter2_contract_passes"] == 0


def test_wave8_preserves_promotion_and_effectiveness_caveats():
    payload = build_strengthening_audit()
    wave = payload["wave8"]
    assert wave["global_confrontation_candidates_after_review"] == 4
    assert wave["candidate_target_names"] == wave["cleared_target_names"]
    assert wave["decision_counts"] == {
        "eligible_new_group": 1,
        "eligible_new_group_with_effectiveness_caveat": 1,
        "hold_direct_pollination_unrecovered": 1,
        "hold_local_pollination_directness": 1,
        "hold_overlap_unresolved_pacific_multi_system": 2,
        "hold_pollination_mechanism_unresolved": 1,
    }
    assert wave["source_verification_counts"] == {
        "authoritative_primary_conservation_field_report": 1,
        "authoritative_taxonomy_plus_conflicting_conservation_account": 1,
        "primary_article_verified_direct_bat_pollination": 1,
        "primary_article_verified_pollen_vector": 1,
        "primary_articles_verified_archipelago_flower_interaction_plus_mayotte_pollination": 1,
        "primary_articles_verified_local_association_pollination_unproven": 1,
        "search_documented_no_qualifying_primary_pollination_source": 1,
    }


def test_wave8_does_not_change_manuscript_facing_breadth():
    boundary = build_strengthening_audit()["manuscript_boundary"]
    assert boundary == {
        "source_backed_research_entries": 39,
        "exact_geographic_labels": 34,
        "changed_by_wave8": False,
        "formal_external_prediction": "not_evaluable",
        "frozen_full_contracts": "0_of_25",
    }


def test_wave8_still_recovers_no_full_contract():
    payload = build_strengthening_audit()
    assert payload["full_contract_result"] == {
        "systematic_extension_creates_full_contract": False,
        "source_strengthening_wave8_passes": 0,
    }
    boundary = payload["claim_boundary"].lower()
    assert "39 research entries / 34 exact labels" in boundary
    assert "not_evaluable" in boundary
