import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260831.json"
WORLD_VALUE = ROOT / "data/results/chapter2_global_master_manuscript_value_review_audit_20260906.json"
IZU_FINAL = ROOT / "data/results/chapter2_izu_final_mechanistic_zoom_audit_20260906.json"


def test_manuscript_keeps_frozen_formal_denominator_separate_from_geography_first_expansion():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    assert "21/25" in text
    assert "2/25" in text
    assert "None of the 25 entries" in text
    assert "did not reopen the frozen 25-entry formal denominator" in text
    assert "Formal external prediction remains `not_evaluable`" in text

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["world_breadth_extension"]["formal_identifiability_research_entries"] == 25
    assert manifest["claim_ceiling"]["external_full_contracts"] == "0_of_25"
    assert manifest["claim_ceiling"]["formal_external_prediction"] == "not_evaluable"


def test_manuscript_records_outcome_independent_world_saturation_and_small_island_bottleneck_movement():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    assert "4,663 candidate island polygons >=20 km2" in text
    assert "zero-novelty 2/2" in text
    assert "Tiritiri Matangi supplied a direct dated partner-reintroduction history" in text
    assert "Surtsey supplied a partially bounded empty-island colonization chronology" in text
    assert "direct historical partner loss remained 0/8" in text
    assert "full contracts remained 0/8" in text

    value = json.loads(WORLD_VALUE.read_text(encoding="utf-8"))
    assert set(value["promote_final_synthesis_ids"]) == {
        "gulf_california_cardon",
        "surtsey_honckenya_2014",
        "tiritiri_hihi_2022",
    }


def test_manuscript_separates_signed_position_failure_from_contemporary_fdq_signal():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    assert "historical signed-position projection as a predictor of beyond-background sorting" in text
    assert "FDQ coefficient was +1.943" in text
    assert "+2.059" in text
    assert "All five leave-one-island coefficients" in text
    assert "does not identify historical *Bombus* loss as the cause" in text


def test_manuscript_records_downstream_branching_and_remaining_field_contract():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    assert "three shorter, four longer and one unchanged" in text
    assert "four lower and four higher" in text
    assert "Only two of eight targets" in text
    assert "usable observation effort including zero-visit windows" in text
    assert "single-visit pollen deposition with no-visit controls" in text
    assert "true temporal partner-regime transition" in text
    assert "single Oshima bridge site" in text

    izu = json.loads(IZU_FINAL.read_text(encoding="utf-8"))
    assert izu["world_to_izu_bottleneck"]["same_core_bottleneck_persists"] is True
    assert izu["izu_current_evidence"]["current_functional_exposure_to_matching"]["supported"] is True
    assert izu["izu_current_evidence"]["matching_to_pollen"]["leave_one_island_sign_stable"] is False
    assert izu["still_missing_in_izu"]["field_data_status"] == "implementation_ready_field_data_missing"
