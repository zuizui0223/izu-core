import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OIKOS_MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260831.json"
JECOLOGY_FALLBACK = ROOT / "data/design/island_ecology_jecology_submission_manifest.json"
DATA_CODE = ROOT / "docs/ISLAND_ECOLOGY_DATA_CODE_AVAILABILITY_20260824.md"


def test_oikos_manifest_is_active_and_mechanism_mainline_is_explicit():
    manifest = json.loads(OIKOS_MANIFEST.read_text(encoding="utf-8"))
    assert manifest["schema_version"] == "1.13"
    assert manifest["journal_target"] == "Oikos"
    assert manifest["article_type"] == "Research Paper"
    assert manifest["routing_status"] == "active_first_submission_route"
    assert manifest["fallback_route"] == "Journal of Ecology Research Article"
    assert manifest["project_tier"] == "Tier_B"
    assert manifest["story"] == "conditional_geometry_to_richness_control_to_determinant_rank_crossover_to_bounded_empirical_claim_ceiling"
    assert manifest["narrative_lock"] == "docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md"
    assert manifest["historical_three_result_narrative_lock"] == "docs/CHAPTER2_THREE_RESULT_NARRATIVE_LOCK_20260908.md"
    assert manifest["historical_four_act_narrative_lock"] == "docs/CHAPTER2_FOUR_ACT_NARRATIVE_LOCK_20260902.md"
    assert manifest["active_manuscript"] == "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
    assert manifest["journal_clean_renderer"] == "scripts/render_chapter2_oikos_generality_overlay.py"
    assert manifest["submission_ready"] is False

    roles = manifest["mechanism_mainline_roles"]
    assert "mixed_positive_and_negative" in roles["conditional_geometry"]
    assert "realized_richness_positions_coarse_mean_regime" in roles["richness_control"]
    assert "ordering_changes" in roles["rank_crossover"]
    assert roles["empirical_role"] == "biological_plausibility_and_claim_boundary_not_required_validation"

    hard = manifest["realized_richness_hard_control"]
    assert hard["all_snapshot_pairs_equal_after_matching"] is True
    assert hard["matching_seeds"] == 6
    assert hard["mean_geometry"] == "all_positive_in_6_of_6_matching_seeds"
    assert hard["mixed_individual_realizations_range"] == "51_to_65_of_96"
    assert hard["state_by_community_nonadditivity_range"] == [0.4272397924506457, 0.4850701049302678]

    rank = manifest["system_size_rank_crossover"]
    assert rank["k_values"] == [1, 2, 4, 8, 16]
    assert rank["median_starting_position_share_percent"] == [2.55, 10.33, 27.33, 42.52, 55.84]
    assert rank["median_community_realization_share_percent"] == [72.98, 48.03, 23.52, 18.26, 12.72]
    assert rank["starting_position_exceeds_community_seed_counts"] == [0, 0, 6, 6, 6]
    assert rank["mixed_at_k16_range"] == "28_to_42_of_96"
    assert rank["natural_threshold_claimed"] is False
    assert rank["visitor_richness_equated_to_k"] is False

    breadth = manifest["world_breadth_extension"]
    assert breadth["formal_identifiability_research_entries"] == 25
    assert breadth["combined_descriptive_research_entries_before_cross_layer_deduplication"] == 42
    assert breadth["combined_exact_overlap_labels_before_higher_level_archipelago_deduplication"] == 37
    assert breadth["formal_external_prediction_reopened"] is False

    saturation = manifest["world_saturation_and_izu_continuity"]
    assert saturation["large_island_saturation_rule_met"] is True
    assert saturation["izu_e3_e4_status"] == "future_optional_validation_not_completion_gate"
    assert saturation["chapter3_phenotype_used_to_tune_or_validate_chapter2"] is False

    claims = manifest["claim_ceiling"]
    assert claims["mean_regime_placement"] == "richness_sensitive_in_declared_synthetic_model"
    assert claims["relational_response_headline"] == "branch_identity_depends_on_state_evaluated_against_realized_community_composition"
    assert claims["determinant_ordering"] == "regime_dependent_across_declared_system_size_audit"
    assert claims["system_size_numeric_crossover_is_natural_threshold"] is False
    assert claims["field_e3_e4_required_for_current_paper"] is False
    assert claims["formal_external_prediction"] == "not_evaluable"
    assert claims["external_full_contracts"] == "0_of_25"
    assert claims["chapter3_used_as_validation"] is False

    oikos = manifest["oikos_initial_submission_contract"]
    assert oikos["double_blind"] is True
    assert oikos["abstract_max_words"] == 300
    assert oikos["mechanism_mainline_submission_narrative"] is True
    assert oikos["three_result_submission_narrative"] is False
    assert oikos["four_act_submission_narrative"] is False
    assert oikos["field_e3_e4_required_for_submission"] is False
    assert oikos["system_size_rank_crossover_integrated"] is True
    assert oikos["field_validation_demoted_from_completion_gate"] is True
    assert oikos["planned_public_repository"] == "Dryad Digital Repository"
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
