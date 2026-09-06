import json
from pathlib import Path

from scripts.audit_chapter2_global_island_master_gap_wave1 import audit as audit_wave1
from scripts.audit_chapter2_global_island_master_gap_wave2 import audit as audit_wave2

ROOT = Path(__file__).resolve().parents[1]
WAVE1_RESULT = ROOT / "data/results/chapter2_global_island_master_gap_wave1_audit_20260906.json"
WAVE2_RESULT = ROOT / "data/results/chapter2_global_island_master_gap_wave2_audit_20260906.json"
PRIORITY = ROOT / "data/design/chapter2_global_island_master_priority_systems_20260906.csv"
DOC = ROOT / "docs/CHAPTER2_GLOBAL_ISLAND_MASTER_EXPANSION_20260906.md"


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


def test_document_keeps_world_before_izu_and_gap_interpretation():
    lower = DOC.read_text(encoding="utf-8").lower()
    assert "do **not** zoom to izu yet" in lower
    assert "4,663" in lower
    assert "111 is not the number of island systems on earth" in lower
    assert "direct partner loss: **0/20**" in lower
    assert "direct partner arrival/replacement: **0/20**" in lower
    assert "california channel islands" in lower
    assert "newfoundland" in lower
    assert "tierra del fuego" in lower
