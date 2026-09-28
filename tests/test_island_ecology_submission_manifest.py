import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OIKOS_MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260927.json"
JECOLOGY_FALLBACK = ROOT / "data/design/island_ecology_jecology_submission_manifest.json"
DATA_CODE = ROOT / "docs/ISLAND_ECOLOGY_DATA_CODE_AVAILABILITY_20260824.md"


def test_oikos_manifest_is_active_bridge_complete_unified_model3_contract():
    manifest = json.loads(OIKOS_MANIFEST.read_text(encoding="utf-8"))
    assert manifest["schema_version"] == "2.2"
    assert manifest["journal_target"] == "Oikos"
    assert manifest["article_type"] == "Research Paper"
    assert manifest["routing_status"] == "active_scientific_route_bridge_complete_package_rebuild"
    assert manifest["fallback_route"] == "Journal of Ecology Research Article"
    assert manifest["scientific_state"] == "unified_model3_bridge_complete_with_real_island_layer_confrontation"
    assert manifest["story"] == "coarse_isolation_regime_to_finite_visitor_and_plant_realization_to_real_island_ABC_confrontation"
    assert manifest["active_manuscript"] == "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
    assert manifest["canonical_story"] == "docs/CHAPTER2_CANONICAL_STORY_20260927.md"
    assert manifest["chapter1_bridge"] == "docs/CHAPTER1_CHAPTER2_CANONICAL_BRIDGE_20260927.md"
    assert manifest["submission_route_firewall"] == "docs/CHAPTER2_SUBMISSION_ROUTE_FIREWALL_20260927.md"
    assert manifest["submission_ready"] is False

    bridge = manifest["prospective_bridge"]
    assert bridge["status"] == "complete"
    assert bridge["cases_verified"] == 24576
    assert bridge["natural_mixed_individual_eps0"] == "12_of_128"
    assert bridge["richness_matched_mixed_individual_eps0"] == "68_of_128"
    assert bridge["pooled_mixed_eps0"] == "0_of_128_both_models"
    assert bridge["large_plant_mixed_individual_eps0"] == "1_of_128"

    real = manifest["real_island_confrontation"]
    assert real["evidence_rich_system_layers"] == 14
    assert real["geographic_clusters"] == 12
    assert real["principal_gap"] == "B_inherited_longitudinal_response_under_measured_visitor_regime"

    legacy = manifest["legacy_model2"]
    assert legacy["status"] == "historical_archive_provenance_only"
    assert legacy["archive_index"] == "legacy/model2/README.md"
    assert legacy["included_in_current_supporting_information"] is False
    assert legacy["included_in_current_review_archive"] is False
    assert legacy["active_benchmarks"] == []

    natural = manifest["formal_natural_evidence_boundary"]
    assert natural["direct_comparable_responses"] == "21_of_25"
    assert natural["direct_partner_arrival_replacement"] == "2_of_25"
    assert natural["complete_A_to_B_to_C_contracts"] == "0_of_25"

    state = manifest["current_submission_state"]
    assert state["scientific_question_closed"] is True
    assert state["original_chapter2_controls_closed"] is True
    assert state["new_field_data_required"] is False

def test_journal_of_ecology_manifest_is_retained_as_fallback_provenance():
    manifest = json.loads(JECOLOGY_FALLBACK.read_text(encoding="utf-8"))
    assert manifest["journal_target"] == "Journal of Ecology"
    assert manifest["article_type"] == "Research Article"
    assert manifest["submission_ready"] is False
    assert manifest["scientific_reopening_required"] is False
    assert manifest["preferred_next_journal_route"] == "Oikos Research paper"
    assert "retained_as_fallback" in manifest["routing_status"]


def test_fallback_manifest_preserves_historical_claim_boundaries():
    manifest = json.loads(JECOLOGY_FALLBACK.read_text(encoding="utf-8"))
    claims = manifest["claim_reassignment"]
    assert claims["H2"] == "conditional_response_geometry_not_minimal_generator_headline"
    assert "directionally_asymmetric" in claims["H3"]
    assert claims["H4"] == "magnitude_attenuation_without_sign_rescue_in_declared_envelope"
    assert claims["H5"] == "comparative_grounding_not_validation_coverage"
    external = manifest["external_system_role"]
    assert external["coverage_11_of_11_must_not_be_used_as_validation"] is True
    assert external["dominica"] == "retained_failed_specific_signed_position_projection"


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
