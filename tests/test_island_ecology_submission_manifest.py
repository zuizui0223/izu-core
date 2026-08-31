import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OIKOS_MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260831.json"
JECOLOGY_FALLBACK = ROOT / "data/design/island_ecology_jecology_submission_manifest.json"
DATA_CODE = ROOT / "docs/ISLAND_ECOLOGY_DATA_CODE_AVAILABILITY_20260824.md"


def test_oikos_manifest_is_active_and_metadata_blocked():
    manifest = json.loads(OIKOS_MANIFEST.read_text(encoding="utf-8"))
    assert manifest["journal_target"] == "Oikos"
    assert manifest["article_type"] == "Research Paper"
    assert manifest["routing_status"] == "active_first_submission_route"
    assert manifest["fallback_route"] == "Journal of Ecology Research Article"
    assert manifest["project_tier"] == "Tier_B"
    assert manifest["story"] == "simulation_to_world_confrontation_to_identifiability_bottleneck_to_izu_mechanistic_resolution_zoom"
    assert manifest["submission_ready"] is False
    assert manifest["remaining_blocker"] == "author_supplied_identity_metadata_and_submission_declarations"
    assert manifest["claim_ceiling"]["formal_external_prediction"] == "not_evaluable"
    assert manifest["claim_ceiling"]["external_full_contracts"] == "0_of_25"
    assert manifest["claim_ceiling"]["izu_beyond_composition_sorting"] == "unsupported"
    assert manifest["claim_ceiling"]["chapter3_used_as_validation"] is False
    oikos = manifest["oikos_initial_submission_contract"]
    assert oikos["double_blind"] is True
    assert oikos["article_type"] == "Research Paper"
    assert oikos["abstract_max_words"] == 300
    assert oikos["significance_statement_required"] is True
    assert oikos["data_and_code_ready_for_first_submission"] is True


def test_journal_of_ecology_manifest_is_retained_as_fallback_provenance():
    manifest = json.loads(JECOLOGY_FALLBACK.read_text(encoding="utf-8"))
    assert manifest["journal_target"] == "Journal of Ecology"
    assert manifest["article_type"] == "Research Article"
    assert manifest["submission_ready"] is False
    assert manifest["scientific_reopening_required"] is False
    assert manifest["research_article_route"] == "mechanistic_response_geometry_funnel_with_world_identifiability_and_izu_resolution_zoom"
    assert manifest["preferred_next_journal_route"] == "Oikos Research paper"
    assert "retained_as_fallback" in manifest["routing_status"]
    assert manifest["scientific_gate_result"]["model_gate_closed"] is True
    assert manifest["focal_izu_triangulation"]["raw_matching_supported"] is True
    assert manifest["focal_izu_triangulation"]["null_corrected_matching_supported"] is False


def test_fallback_manifest_preserves_frozen_claim_boundaries():
    manifest = json.loads(JECOLOGY_FALLBACK.read_text(encoding="utf-8"))
    claims = manifest["claim_reassignment"]
    assert claims["H2"] == "conditional_response_geometry_not_minimal_generator_headline"
    assert "directionally_asymmetric" in claims["H3"]
    assert claims["H4"] == "magnitude_attenuation_without_sign_rescue_in_declared_envelope"
    assert claims["H5"] == "comparative_grounding_not_validation_coverage"
    external = manifest["external_system_role"]
    assert external["coverage_11_of_11_must_not_be_used_as_validation"] is True
    assert external["dominica"] == "retained_failed_specific_signed_position_projection"
    why = manifest["model_reporting"]["conditional_why_diagnostics"]
    assert why["unchanged_parent_design_identity_verified"] is True
    assert why["ultimate_why_claimed"] is False
    izu = manifest["model_reporting"]["izu_empirical_hygiene"]
    assert izu["fuzzy_or_guild_proxy_imputation_used"] is False
    assert izu["null_corrected_negative_result_reported"] is True
    assert izu["causal_pollinator_selection_not_claimed"] is True


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
