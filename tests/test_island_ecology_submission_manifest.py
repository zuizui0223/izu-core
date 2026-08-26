import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/design/island_ecology_jecology_submission_manifest.json"
DATA_CODE = ROOT / "docs/ISLAND_ECOLOGY_DATA_CODE_AVAILABILITY_20260824.md"


def test_submission_manifest_blocks_submission_during_scientific_reassessment():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["journal_target"] == "Journal of Ecology"
    assert manifest["article_type"] == "Research Article"
    assert manifest["submission_ready"] is False
    assert manifest["scientific_reopening_required"] is True
    assert manifest["active_scientific_gate"] == "data/design/manuscript_reassessment_gate_20260826.json"
    assert manifest["scientific_reassessment"] == "docs/SCIENTIFIC_REASSESSMENT_AFTER_CRITIQUE_20260826.md"
    assert manifest["paper_scope_independent_of_external_research_programmes"] is True


def test_manifest_demotes_overstated_claims_and_routes_next_scientific_work():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    claims = manifest["claim_reassignment"]
    assert claims["H2"] == "demoted_to_model_specific_sensitivity_and_endpoint_geometry"
    assert "bidirectional_local_context_filtering" in claims["H3"]
    assert "structural_parameter_result" in claims["H4"]
    assert claims["H5"] == "demoted_from_validation_to_comparative_grounding"

    external = manifest["external_system_role"]
    assert external["strict_systems"] == 13
    assert external["coverage_11_of_11_must_not_be_used_as_validation"] is True
    assert external["dominica"] == "retained_failed_specific_signed_position_projection"

    required = manifest["required_new_scientific_work"]
    assert "response_geometry_analysis_identifying_sign_switch_conditions" in required
    assert "parameter_robustness_sweep_over_key_island_perturbation_and_matching_parameters" in required
    assert "local_context_sign_change_robustness_map" in required
    assert "assurance_sign_rescue_threshold_map" in required

    bundle = manifest["submission_bundle"]
    assert bundle["status"] == "blocked_while_scientific_reassessment_gate_is_open"
    assert bundle["author_metadata_is_not_current_active_blocker"] is True
    assert manifest["next_executable_task"].startswith("build_response_geometry")


def test_data_code_statement_preserves_anonymous_review_and_paper_scope():
    text = DATA_CODE.read_text(encoding="utf-8")
    lower = text.lower()
    assert "anonymized review archive" in lower
    assert "no new unpublished field dataset" in lower
    assert "immutable versioned archive" in lower
    assert "persistent doi" in lower
    assert "independent research programmes" in lower
    assert "neither dependencies nor validation requirements" in lower
    assert "issue #91" not in lower
    assert "real-world signed functional-position" not in lower
