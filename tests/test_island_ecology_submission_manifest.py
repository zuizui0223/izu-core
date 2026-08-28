import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/design/island_ecology_jecology_submission_manifest.json"
DATA_CODE = ROOT / "docs/ISLAND_ECOLOGY_DATA_CODE_AVAILABILITY_20260824.md"


def test_submission_manifest_keeps_scientific_gate_closed_but_metadata_blocked():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["journal_target"] == "Journal of Ecology"
    assert manifest["article_type"] == "Research Article"
    assert manifest["submission_ready"] is False
    assert manifest["scientific_reopening_required"] is False
    assert manifest["active_scientific_gate"] == "data/design/manuscript_reassessment_gate_20260826.json"
    assert manifest["scientific_reassessment"] == "docs/SCIENTIFIC_REASSESSMENT_AFTER_CRITIQUE_20260826.md"
    assert manifest["paper_scope_independent_of_external_research_programmes"] is True
    assert manifest["research_article_route"] == "mechanistic_response_geometry_funnel_with_world_identifiability_and_izu_resolution_zoom"
    assert manifest["preferred_next_journal_route"] == "Oikos Research paper"
    assert "retained_as_fallback" in manifest["routing_status"]
    assert manifest["scientific_gate_result"]["model_gate_closed"] is True
    assert manifest["focal_izu_triangulation"]["implementation_on_active_branch"] is True
    assert manifest["focal_izu_triangulation"]["structural_audit_on_active_branch"] is True
    assert manifest["focal_izu_triangulation"]["raw_matching_supported"] is True
    assert manifest["focal_izu_triangulation"]["null_corrected_matching_supported"] is False


def test_manifest_routes_frozen_conditional_why_diagnostics_without_reopening():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    claims = manifest["claim_reassignment"]
    assert claims["H2"] == "conditional_response_geometry_not_minimal_generator_headline"
    assert "directionally_asymmetric" in claims["H3"]
    assert claims["H4"] == "magnitude_attenuation_without_sign_rescue_in_declared_envelope"
    assert claims["H5"] == "comparative_grounding_not_validation_coverage"

    external = manifest["external_system_role"]
    assert external["coverage_11_of_11_must_not_be_used_as_validation"] is True
    assert external["dominica"] == "retained_failed_specific_signed_position_projection"

    completed = manifest["scientific_work_completed"]
    assert "response_geometry_analysis_identifying_sign_switch_conditions" in completed
    assert "exact_interaction_kernel_derivation_and_deterministic_code_identity_audit" in completed
    assert "fixed_surface_regime_boundary_driver_diagnostic" in completed
    assert "starting_position_by_community_realization_decomposition" in completed
    assert "local_filtering_directional_asymmetry_diagnostic" in completed
    assert "focal_izu_raw_matching_source_state_triangulation_with_structural_negative_control" in completed
    assert "source_locked_izu_analysis_implementation_and_structural_audit_ported_to_active_submission_branch" in completed
    why = manifest["model_reporting"]["conditional_why_diagnostics"]
    assert why["unchanged_parent_design_identity_verified"] is True
    assert why["ultimate_why_claimed"] is False
    izu = manifest["model_reporting"]["izu_empirical_hygiene"]
    assert izu["fuzzy_or_guild_proxy_imputation_used"] is False
    assert izu["null_corrected_negative_result_reported"] is True
    assert izu["causal_pollinator_selection_not_claimed"] is True

    bundle = manifest["submission_bundle"]
    assert bundle["status"] == "scientifically_complete_metadata_blocked"
    assert bundle["remaining_blocker"] == "author_supplied_metadata_and_submission_declarations"
    assert bundle["izu_reproducibility_files_in_review_archive"] is True
    assert manifest["next_executable_task"].startswith("run repository CI")


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
