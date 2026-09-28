import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260927.json"
WORLD_VALUE = ROOT / "data/results/chapter2_global_master_manuscript_value_review_audit_20260906.json"
IZU_FINAL = ROOT / "data/results/chapter2_izu_final_mechanistic_zoom_audit_20260906.json"
IZU_RATIONALE = ROOT / "data/design/chapter2_izu_focal_system_rationale_20260906.json"
THESIS = ROOT / "THESIS_CHAPTER_POSITIONING.md"


def test_world_program_is_preserved_as_layer_specific_claim_ceiling_not_model_fit():
    text = MANUSCRIPT.read_text(encoding="utf-8").lower()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert "layer-specific confrontation with real island systems" in text
    assert "no system was assigned a synthetic `k`, s/c/i regime, trait coordinate or model 3 parameter cell" in text
    assert "natural evidence is therefore a confrontation layer rather than a calibration layer" in text
    assert "future same-unit transition-linked study" in text
    natural = manifest["formal_natural_evidence_boundary"]
    assert natural["research_entries"] == 25
    assert natural["complete_A_to_B_to_C_contracts"] == "0_of_25"
    assert natural["breadth_entries"] == 42
    assert manifest["current_submission_state"]["new_field_data_required"] is False

def test_world_saturation_assets_remain_frozen_for_reviewer_audit():
    value = json.loads(WORLD_VALUE.read_text(encoding="utf-8"))
    assert set(value["promote_final_synthesis_ids"]) == {
        "gulf_california_cardon",
        "surtsey_honckenya_2014",
        "tiritiri_hihi_2022",
    }
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    natural = manifest["formal_natural_evidence_boundary"]
    assert natural["breadth_entries"] == 42
    assert natural["breadth_geographic_labels"] == 37
    assert natural["complete_A_to_B_to_C_contracts"] == "0_of_25"

def test_izu_empirical_assets_remain_boundary_evidence_not_completion_gate():
    text = MANUSCRIPT.read_text(encoding="utf-8").lower()
    thesis = THESIS.read_text(encoding="utf-8").lower()
    izu = json.loads(IZU_FINAL.read_text(encoding="utf-8"))
    rationale = json.loads(IZU_RATIONALE.read_text(encoding="utf-8"))

    assert "izu supplies the most resolved a-layer branching contrast" in text
    assert "natural evidence is therefore a confrontation layer rather than a calibration layer" in text
    assert "future same-unit transition-linked study" in text
    assert "current cross-sectional evidence cannot retrospectively identify" in text
    assert "parallel/future validation" in thesis
    assert izu["izu_current_evidence"]["current_functional_exposure_to_matching"]["supported"] is True
    assert izu["izu_current_evidence"]["matching_to_pollen"]["leave_one_island_sign_stable"] is False
    assert izu["still_missing_in_izu"]["field_data_status"] == "implementation_ready_field_data_missing"
    assert "measurement continuity" in rationale["selection_rule"].lower()


def test_chapter2_to_chapter3_handoff_does_not_use_chapter3_as_validation():
    thesis = THESIS.read_text(encoding="utf-8")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert "Chapter 3 phenotype values are not used to tune, rescue or validate Chapter 2" in thesis
    assert manifest["claim_ceiling"]["cross_sectional_morphology_treated_as_B_layer"] is False
