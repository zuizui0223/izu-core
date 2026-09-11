import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260831.json"
WORLD_VALUE = ROOT / "data/results/chapter2_global_master_manuscript_value_review_audit_20260906.json"
IZU_FINAL = ROOT / "data/results/chapter2_izu_final_mechanistic_zoom_audit_20260906.json"
IZU_RATIONALE = ROOT / "data/design/chapter2_izu_focal_system_rationale_20260906.json"
THESIS = ROOT / "THESIS_CHAPTER_POSITIONING.md"


def test_world_program_is_preserved_as_bounded_claim_ceiling_not_main_result():
    text = MANUSCRIPT.read_text(encoding="utf-8").lower()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert "world and izu evidence are retained only as biological plausibility" in text
    assert "same-block visitor" in text and "future validation" in text
    assert manifest["world_breadth_extension"]["formal_identifiability_research_entries"] == 25
    assert manifest["claim_ceiling"]["external_full_contracts"] == "0_of_25"
    assert manifest["claim_ceiling"]["formal_external_prediction"] == "not_evaluable"
    assert manifest["empirical_validation_role"]["field_e3_e4_required_for_current_paper"] is False


def test_world_saturation_assets_remain_frozen_for_reviewer_audit():
    value = json.loads(WORLD_VALUE.read_text(encoding="utf-8"))
    assert set(value["promote_final_synthesis_ids"]) == {
        "gulf_california_cardon",
        "surtsey_honckenya_2014",
        "tiritiri_hihi_2022",
    }
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    saturation = manifest["world_saturation_and_izu_continuity"]
    assert saturation["large_island_saturation_rule_met"] is True
    assert saturation["consecutive_zero_novelty_tranches"] == 2
    assert saturation["small_island_full_contracts"] == "0_of_8"


def test_izu_empirical_assets_remain_boundary_evidence_not_completion_gate():
    text = MANUSCRIPT.read_text(encoding="utf-8").lower()
    thesis = THESIS.read_text(encoding="utf-8").lower()
    izu = json.loads(IZU_FINAL.read_text(encoding="utf-8"))
    rationale = json.loads(IZU_RATIONALE.read_text(encoding="utf-8"))

    assert "izu evidence are retained only as biological plausibility" in text
    assert "not a completion gate" in text
    assert "parallel/future validation" in thesis
    assert izu["izu_current_evidence"]["current_functional_exposure_to_matching"]["supported"] is True
    assert izu["izu_current_evidence"]["matching_to_pollen"]["leave_one_island_sign_stable"] is False
    assert izu["still_missing_in_izu"]["field_data_status"] == "implementation_ready_field_data_missing"
    assert "measurement continuity" in rationale["selection_rule"].lower()


def test_chapter2_to_chapter3_handoff_does_not_use_chapter3_as_validation():
    thesis = THESIS.read_text(encoding="utf-8")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert "Chapter 3 phenotype values are not used to tune, rescue or validate Chapter 2" in thesis
    assert manifest["claim_ceiling"]["chapter3_used_as_validation"] is False
