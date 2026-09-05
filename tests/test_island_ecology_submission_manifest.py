import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OIKOS_MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260831.json"
JECOLOGY_FALLBACK = ROOT / "data/design/island_ecology_jecology_submission_manifest.json"
DATA_CODE = ROOT / "docs/ISLAND_ECOLOGY_DATA_CODE_AVAILABILITY_20260824.md"


def test_oikos_manifest_is_active_and_current_submission_contract_is_explicit():
    manifest = json.loads(OIKOS_MANIFEST.read_text(encoding="utf-8"))
    assert manifest["schema_version"] == "1.8"
    assert manifest["journal_target"] == "Oikos"
    assert manifest["article_type"] == "Research Paper"
    assert manifest["routing_status"] == "active_first_submission_route"
    assert manifest["fallback_route"] == "Journal of Ecology Research Article"
    assert manifest["project_tier"] == "Tier_B"
    assert manifest["story"] == "simulation_to_world_confrontation_to_process_measurement_bottleneck_to_izu_mechanistic_resolution_zoom"
    assert manifest["active_manuscript"] == "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
    assert manifest["oikos_rtf_renderer"] == "scripts/render_oikos_submission_rtf.py"
    assert manifest["submission_ready"] is False
    assert manifest["remaining_blocker"] == "author_supplied_identity_prior_work_context_and_submission_declarations"
    assert "author_contributions" not in manifest["remaining_before_actual_submission"]
    assert "planned_public_repository" not in manifest["remaining_before_actual_submission"]

    breadth = manifest["world_breadth_extension"]
    assert breadth["formal_identifiability_research_entries"] == 25
    assert breadth["frozen_exact_geographic_overlap_labels"] == 21
    assert breadth["post_freeze_source_verified_research_entries"] == 17
    assert breadth["post_freeze_exact_geographic_groups"] == 16
    assert breadth["combined_descriptive_research_entries_before_cross_layer_deduplication"] == 42
    assert breadth["combined_exact_overlap_labels_before_higher_level_archipelago_deduplication"] == 37
    assert breadth["post_freeze_direct_or_historical_arrival_entries"] == 4
    assert breadth["manuscript_value_promoted_entries"] == 3
    assert set(breadth["manuscript_value_promoted_geographic_groups"]) == {
        "crete",
        "trinidad_tobago",
        "iceland",
    }
    assert breadth["separate_multi_group_syntheses"] == 1
    assert breadth["southern_ocean_source_native_island_groups"] == 11
    assert breadth["southern_ocean_flowering_plant_species"] == 321
    assert breadth["formal_external_prediction_reopened"] is False
    assert breadth["frozen_25_measurement_fractions_recomputed"] is False
    assert breadth["independent_archipelago_denominator_claimed"] is False

    claims = manifest["claim_ceiling"]
    assert claims["relational_response_headline"] == "response_direction_depends_on_state_evaluated_against_realized_community"
    assert claims["formal_external_prediction"] == "not_evaluable"
    assert claims["external_full_contracts"] == "0_of_25"
    assert claims["direct_response_outcome"] == "21_of_25"
    assert claims["direct_partner_arrival_replacement"] == "2_of_25"
    assert claims["post_freeze_breadth_extension_changes_frozen_25_metrics"] is False
    assert claims["izu_beyond_composition_sorting"] == "unsupported"
    assert claims["izu_oshima_bridge"] == "unsupported"
    assert claims["chapter3_used_as_validation"] is False

    robustness = manifest["relational_robustness"]
    assert robustness["historical_freeze_rewritten"] is False
    assert robustness["community_largest_across_prespecified_seeds"] is True
    assert robustness["community_largest_across_steps_30_60_120_240"] is True
    assert robustness["mixed_at_zero_trait_adjustment"] == "64_of_96"
    assert robustness["equal_initial_richness_mixed"] == "53_of_96"

    oikos = manifest["oikos_initial_submission_contract"]
    assert oikos["double_blind"] is True
    assert oikos["article_type"] == "Research Paper"
    assert oikos["abstract_max_words"] == 300
    assert oikos["active_abstract_target_words"] == 278
    assert oikos["upload_file_format"] == "RTF"
    assert oikos["single_column"] is True
    assert oikos["double_spaced"] is True
    assert oikos["continuous_line_numbers"] is True
    assert oikos["page_numbers"] is True
    assert oikos["introduction_begins_page_two"] is True
    assert oikos["supporting_information_separate"] is True
    assert oikos["supporting_information_references_generic_only"] is True
    assert oikos["corresponding_author_orcid_required"] is True
    assert oikos["significance_prior_author_work_context_required"] is True
    assert oikos["data_archiving_statement_required"] is True
    assert oikos["planned_public_repository_must_be_named"] is True
    assert oikos["planned_public_repository"] == "Dryad Digital Repository"
    assert oikos["dryad_selected_for_accepted_stage_public_archiving"] is True
    assert oikos["ethics_statement_ready"] is True
    assert oikos["credit_required_at_initial_submission"] is False
    assert oikos["credit_required_at_revision"] is True
    assert oikos["data_and_code_ready_for_first_submission"] is True
    assert oikos["old_within_cell_noise_wording_blocked_from_submission_si"] is True


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
