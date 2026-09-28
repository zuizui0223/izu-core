import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260927.json"


def test_oikos_manifest_is_model3_only_contract():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["schema_version"] == "2.3"
    assert manifest["journal_target"] == "Oikos"
    assert manifest["article_type"] == "Research Paper"
    assert manifest["scientific_state"] == "unified_model3_bridge_complete_with_real_island_layer_confrontation"
    assert manifest["story"] == "pollination_to_reproductive_selection_to_expected_inheritance_to_finite_population_realization"
    assert manifest["active_manuscript"] == "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
    assert manifest["canonical_story"] == "docs/CHAPTER2_CANONICAL_STORY_20260927.md"
    assert manifest["submission_surfaces"]["journal_clean_renderer"] == "scripts/render_chapter2_oikos_generality_overlay.py"
    assert "compatibility_renderer" not in manifest["submission_surfaces"]
    assert manifest["submission_surfaces"]["legacy_archive"] == "legacy/"


def test_manifest_preserves_bridge_and_claim_boundary():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    bridge = manifest["prospective_bridge"]
    assert bridge["status"] == "complete"
    assert bridge["cases_verified"] == 24576
    assert bridge["natural_mixed_individual_eps0"] == "12_of_128"
    assert bridge["richness_matched_mixed_individual_eps0"] == "68_of_128"
    assert bridge["pooled_mixed_eps0"] == "0_of_128_both_models"
    assert bridge["large_plant_mixed_individual_eps0"] == "1_of_128"
    assert manifest["claim_ceiling"]["natural_branch_prevalence_estimated"] is False
    assert manifest["claim_ceiling"]["historical_bombus_causation_identified"] is False


def test_manifest_marks_model2_legacy_only():
    legacy = json.loads(MANIFEST.read_text(encoding="utf-8"))["legacy_model2"]
    assert legacy["status"] == "historical_archive_provenance_only"
    assert legacy["archive_index"] == "legacy/model2/README.md"
    assert legacy["included_in_current_supporting_information"] is False
    assert legacy["included_in_current_review_archive"] is False
