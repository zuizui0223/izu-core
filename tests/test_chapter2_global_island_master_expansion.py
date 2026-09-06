import json
from pathlib import Path

from scripts.audit_chapter2_global_island_master_gap_wave1 import audit as audit_wave1
from scripts.audit_chapter2_global_island_master_gap_wave2 import audit as audit_wave2
from scripts.audit_chapter2_global_island_master_tranche3 import audit as audit_tranche3
from scripts.audit_chapter2_global_island_master_tranche4 import audit as audit_tranche4
from scripts.audit_chapter2_global_island_master_tranche5 import audit as audit_tranche5
from scripts.audit_chapter2_small_island_supplement import audit as audit_small
from scripts.audit_chapter2_global_master_manuscript_value_review import audit as audit_value_review
from scripts.audit_chapter2_izu_final_mechanistic_zoom import audit as audit_izu_final

ROOT = Path(__file__).resolve().parents[1]
WAVE1_RESULT = ROOT / "data/results/chapter2_global_island_master_gap_wave1_audit_20260906.json"
WAVE2_RESULT = ROOT / "data/results/chapter2_global_island_master_gap_wave2_audit_20260906.json"
PRIORITY = ROOT / "data/design/chapter2_global_island_master_priority_systems_20260906.csv"
DOC = ROOT / "docs/CHAPTER2_GLOBAL_ISLAND_MASTER_EXPANSION_20260906.md"
CURRENT_DOC = ROOT / "docs/CHAPTER2_WORLD_CONFRONTATION_SATURATION_AND_IZU_ZOOM_20260906.md"


def test_wave1_audit_is_reproducible_after_wave2_progress():
    recorded = json.loads(WAVE1_RESULT.read_text(encoding="utf-8"))
    assert audit_wave1() == recorded
    assert recorded["priority_queue"] == {
        "documented_omitted_geographic_systems": 20,
        "searched_wave1": 8,
        "next_wave": 12,
    }
    assert recorded["active_manuscript_boundary"]["mutated_by_wave1"] is False


def test_combined_20_system_master_gap_audit_is_reproducible():
    recorded = json.loads(WAVE2_RESULT.read_text(encoding="utf-8"))
    assert audit_wave2() == recorded
    combined = recorded["combined_20_system_review"]
    assert combined["systems"] == 20
    assert combined["primary_verified_sources"] == 10
    assert combined["full_contract_passes"] == 0
    assert combined["direct_measurement_counts"]["direct_plant_response"] == 10
    assert combined["direct_measurement_counts"]["direct_assurance_breeding"] == 9
    assert combined["direct_measurement_counts"]["direct_realized_community_shift"] == 7
    assert combined["direct_measurement_counts"]["direct_partner_loss"] == 0
    assert combined["direct_measurement_counts"]["direct_partner_arrival_replacement"] == 0


def test_independent_master_provenance_and_threshold_are_locked():
    recorded = json.loads(WAVE2_RESULT.read_text(encoding="utf-8"))
    provenance = recorded["master_provenance"]
    assert provenance["source_repository"] == "zuizui0223/island"
    assert provenance["source_commit"] == "f1462cd1aa76b2703bc2df159996a4ab65510a25"
    assert provenance["source_blob"] == "42f31df81db250ebfe46b35ebce6cb1c52b19fc9"
    assert provenance["area_threshold_km2"] == 20
    assert provenance["candidate_island_polygons"] == 4663
    assert recorded["search_frame_boundary"]["individual_polygons_treated_as_independent_ecological_systems"] is False


def test_first_master_gap_tranche_is_closed_without_izu_or_manuscript_mutation():
    text = PRIORITY.read_text(encoding="utf-8")
    assert ",next_wave," not in text
    assert "Izu Islands" not in text

    recorded = json.loads(WAVE2_RESULT.read_text(encoding="utf-8"))
    boundary = recorded["active_manuscript_boundary"]
    assert boundary["descriptive_research_entries"] == 42
    assert boundary["exact_geographic_labels"] == 37
    assert boundary["formal_identifiability_research_entries"] == 25
    assert boundary["formal_full_contracts"] == "0_of_25"
    assert boundary["formal_external_prediction"] == "not_evaluable"
    assert boundary["mutated_by_master_gap_review"] is False


def test_historical_first20_document_preserves_pre_saturation_state():
    lower = DOC.read_text(encoding="utf-8").lower()
    assert "do **not** zoom to izu yet" in lower
    assert "4,663" in lower
    assert "111 is not the number of island systems on earth" in lower
    assert "direct partner loss: **0/20**" in lower
    assert "direct partner arrival/replacement: **0/20**" in lower
    assert "california channel islands" in lower
    assert "newfoundland" in lower
    assert "tierra del fuego" in lower


def test_large_island_saturation_requires_two_consecutive_zero_novelty_tranches():
    t3 = audit_tranche3()
    t4 = audit_tranche4()
    t5 = audit_tranche5()

    assert t3["saturation_tranche_eligible_by_size"] is True
    assert t3["material_novelty_events"] == 1
    assert t3["zero_novelty_saturation_tranche"] is False
    assert t3["large_island_saturation_met"] is False

    assert t4["zero_novelty_saturation_tranche"] is True
    assert t4["consecutive_zero_novelty_tranches_after_this"] == 1
    assert t4["large_island_saturation_met"] is False

    assert t5["zero_novelty_saturation_tranche"] is True
    assert t5["consecutive_zero_novelty_tranches_after_this"] == 2
    assert t5["large_island_saturation_met"] is True
    assert t5["direct_historical_partner_loss"] == 0
    assert t5["direct_historical_partner_arrival_replacement"] == 0
    assert t5["full_contract_passes"] == 0


def test_small_island_supplement_moves_but_does_not_close_turnover_bottleneck():
    payload = audit_small()
    supplement = payload["supplement"]
    assert supplement["preselected_systems"] == 8
    assert supplement["reviewed_systems"] == 8
    assert supplement["direct_measurement_counts"]["direct_partner_loss"] == 0
    assert supplement["direct_measurement_counts"]["direct_partner_arrival_replacement"] == 1
    assert supplement["direct_historical_partner_arrival_systems"] == ["Tiritiri Matangi Island"]
    assert supplement["partial_historical_partner_arrival_systems"] == ["Surtsey"]
    assert set(supplement["material_novelty_systems"]) == {"Surtsey", "Tiritiri Matangi Island"}
    assert supplement["full_contract_passes"] == 0
    assert payload["bottleneck_update"]["status"] == "partially_moved_not_closed"


def test_post_saturation_value_review_keeps_only_distinct_core_roles():
    payload = audit_value_review()
    assert payload["candidate_systems"] == 13
    assert set(payload["promote_final_synthesis_ids"]) == {
        "surtsey_honckenya_2014",
        "tiritiri_hihi_2022",
        "gulf_california_cardon",
    }
    assert payload["historical_bottleneck"]["direct_partner_loss_closed"] is False
    assert payload["historical_bottleneck"]["full_source_transition_realization_response_contracts"] == 0
    assert payload["izu_transition_gate"]["ready_for_final_izu_mechanistic_zoom"] is True


def test_final_izu_zoom_resolves_contemporary_chain_but_not_historical_transition():
    payload = audit_izu_final()
    evidence = payload["izu_current_evidence"]
    assert payload["entry_gate"]["final_izu_zoom_allowed"] is True
    assert payload["world_to_izu_bottleneck"]["same_core_bottleneck_persists"] is True
    assert evidence["historical_proboscis_species_level_recovery"] == "202_of_209_current_named_taxa"
    assert evidence["current_functional_exposure_to_matching"]["supported"] is True
    assert evidence["current_functional_exposure_to_matching"]["all_izu5_leave_one_island_coefficients_positive"] is True
    assert evidence["matching_to_pollen"]["average_direction_positive"] is True
    assert evidence["matching_to_pollen"]["leave_one_island_sign_stable"] is False
    assert evidence["response_branching"] == {
        "shared_targets": 8,
        "corrected_matching_lower": 8,
        "tube_shorter": 3,
        "tube_longer": 4,
        "tube_equal": 1,
        "pollen_lower": 4,
        "pollen_higher": 4,
        "full_matching_lower_tube_shorter_pollen_lower": 2,
    }
    assert evidence["second_boundary_replication"]["causal_boundary_effect_identifiable"] is False
    assert payload["still_missing_in_izu"]["field_data_status"] == "implementation_ready_field_data_missing"
    assert payload["claim_boundary"]["historical_bombus_causation_identified"] is False
    assert payload["claim_boundary"]["formal_external_prediction_reopened"] is False


def test_current_synthesis_document_records_saturation_small_islands_and_izu_zoom():
    lower = CURRENT_DOC.read_text(encoding="utf-8").lower()
    assert "zero-novelty 2/2" in lower
    assert "tiritiri matangi" in lower
    assert "surtsey" in lower
    assert "gulf of california" in lower
    assert "202/209" in lower
    assert "8/8 lower" in lower
    assert "3 shorter / 4 longer / 1 unchanged" in lower
    assert "4 lower / 4 higher" in lower
    assert "implementation_ready_field_data_missing" in lower
    assert "0/25 full contracts" in lower
    assert "not_evaluable" in lower


def test_expansion_and_izu_zoom_do_not_mutate_active_or_frozen_denominators():
    payloads = (
        audit_wave1(),
        audit_wave2(),
        audit_tranche3(),
        audit_tranche4(),
        audit_tranche5(),
        audit_small(),
        audit_value_review(),
        audit_izu_final(),
    )
    for payload in payloads:
        boundary = payload["active_manuscript_boundary"] if "active_manuscript_boundary" in payload else None
        if boundary is None:
            assert payload["claim_boundary"]["formal_external_prediction_reopened"] is False
            assert payload["claim_boundary"]["active_descriptive_breadth_mutated"] is False
            continue
        assert boundary["descriptive_research_entries"] == 42
        assert boundary["exact_geographic_labels"] == 37
        assert boundary["formal_identifiability_research_entries"] == 25
        assert boundary["formal_full_contracts"] == "0_of_25"
        assert boundary["formal_external_prediction"] == "not_evaluable"
