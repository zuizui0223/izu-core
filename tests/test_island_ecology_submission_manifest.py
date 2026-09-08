import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OIKOS_MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260831.json"
JECOLOGY_FALLBACK = ROOT / "data/design/island_ecology_jecology_submission_manifest.json"
DATA_CODE = ROOT / "docs/ISLAND_ECOLOGY_DATA_CODE_AVAILABILITY_20260824.md"


def test_oikos_manifest_is_active_and_three_result_reframe_is_explicit():
    manifest = json.loads(OIKOS_MANIFEST.read_text(encoding="utf-8"))
    assert manifest["schema_version"] == "1.12"
    assert manifest["journal_target"] == "Oikos"
    assert manifest["article_type"] == "Research Paper"
    assert manifest["routing_status"] == "active_first_submission_route"
    assert manifest["fallback_route"] == "Journal of Ecology Research Article"
    assert manifest["project_tier"] == "Tier_B"
    assert manifest["story"] == "mechanistic_prediction_to_real_world_compositional_exposure_to_izu_biological_consequence"
    assert manifest["narrative_lock"] == "docs/CHAPTER2_THREE_RESULT_NARRATIVE_LOCK_20260908.md"
    assert manifest["historical_four_act_narrative_lock"] == "docs/CHAPTER2_FOUR_ACT_NARRATIVE_LOCK_20260902.md"
    assert manifest["active_manuscript"] == "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
    assert manifest["journal_clean_renderer"] == "scripts/render_chapter2_oikos_generality_overlay.py"
    assert manifest["oikos_rtf_renderer"] == "scripts/render_oikos_submission_rtf.py"
    assert manifest["submission_ready"] is False
    assert manifest["remaining_blocker"] == "author_supplied_identity_prior_work_context_ethics_confirmation_and_submission_declarations"

    roles = manifest["three_result_inference_roles"]
    assert "richness_sensitive_coarse_regime" in roles["result_1_mechanistic_prediction"]
    assert "partner_turnover_rewiring" in roles["result_2_real_world_exposure"]
    assert "izu_contemporary_functional_structure" in roles["result_3_biological_consequence"]
    assert roles["identifiability_role"] == "claim_boundary_and_robustness_only_not_coequal_study_objective"

    breadth = manifest["world_breadth_extension"]
    assert breadth["formal_identifiability_research_entries"] == 25
    assert breadth["frozen_exact_geographic_overlap_labels"] == 21
    assert breadth["combined_descriptive_research_entries_before_cross_layer_deduplication"] == 42
    assert breadth["combined_exact_overlap_labels_before_higher_level_archipelago_deduplication"] == 37
    assert breadth["formal_external_prediction_reopened"] is False
    assert breadth["frozen_25_measurement_fractions_recomputed"] is False

    saturation = manifest["world_saturation_and_izu_continuity"]
    assert saturation["large_island_saturation_rule_met"] is True
    assert saturation["consecutive_zero_novelty_tranches"] == 2
    assert saturation["small_island_direct_historical_partner_loss"] == "0_of_8"
    assert saturation["small_island_direct_partner_arrival_reintroduction"] == "1_of_8"
    assert saturation["small_island_full_contracts"] == "0_of_8"
    assert saturation["izu_focal_selection_rule"] == "measurement_continuity_after_world_saturation_not_proximity_representativeness_or_positive_model_fit"
    assert saturation["chapter3_phenotype_used_to_tune_or_validate_chapter2"] is False

    robustness = manifest["relational_robustness"]
    assert robustness["historical_freeze_rewritten"] is False
    assert robustness["mixed_at_zero_trait_adjustment"] == "64_of_96"
    assert robustness["equal_initial_richness_mixed"] == "53_of_96"
    assert robustness["equal_initial_richness_claim"] == "initial_richness_reduction_not_required_for_mixed_individual_realizations_only"

    hard = manifest["realized_richness_hard_control"]
    assert hard["all_snapshot_pairs_equal_after_matching"] is True
    assert hard["matching_seeds"] == 6
    assert hard["mean_geometry"] == "all_positive_in_6_of_6_matching_seeds"
    assert hard["mixed_individual_realizations_range"] == "51_to_65_of_96"
    assert hard["state_by_community_nonadditivity_range"] == [0.4272397924506457, 0.4850701049302678]
    assert hard["prespecified_gate_decision"] == "blocker_failed_reframe_before_author_metadata"
    assert hard["reframe_integrated"] is True

    exposure = manifest["result2_external_exposure"]
    assert exposure["independent_context_examples"] == 2
    assert exposure["wanshan_yongxing"]["partner_turnover"] == 0.979601473000006
    assert exposure["wanshan_yongxing"]["pollinator_richness_lrr_interval"][0] < 0 < exposure["wanshan_yongxing"]["pollinator_richness_lrr_interval"][1]
    assert exposure["ogasawara_anijima_context"]["partner_turnover"] == 0.6816731479429761
    assert exposure["ogasawara_anijima_context"]["pollinator_richness_lrr_interval"][0] < 0 < exposure["ogasawara_anijima_context"]["pollinator_richness_lrr_interval"][1]
    assert exposure["pooled_universal_island_effect_claimed"] is False

    claims = manifest["claim_ceiling"]
    assert claims["mean_regime_placement"] == "richness_sensitive_in_declared_synthetic_model"
    assert claims["relational_response_headline"] == "branch_identity_depends_on_state_evaluated_against_realized_community_composition"
    assert claims["external_compositional_exposure"] == "partner_turnover_beyond_decisive_richness_loss_supported_in_two_independent_source_native_contexts"
    assert claims["formal_external_prediction"] == "not_evaluable"
    assert claims["external_full_contracts"] == "0_of_25"
    assert claims["identifiability_role"] == "claim_boundary_not_primary_result"
    assert claims["izu_beyond_composition_sorting"] == "unsupported_for_historical_signed_position_projection"
    assert claims["izu_contemporary_fdq_to_corrected_matching"] == "supported_with_leave_one_island_sign_stability"
    assert claims["izu_matching_to_pollen"] == "positive_on_average_not_leave_one_island_sign_stable"
    assert claims["izu_cross_channel_branching"] == "matching_lower_8_of_8_tube_3_shorter_4_longer_1_unchanged_pollen_4_lower_4_higher"
    assert claims["chapter3_used_as_validation"] is False

    oikos = manifest["oikos_initial_submission_contract"]
    assert oikos["double_blind"] is True
    assert oikos["article_type"] == "Research Paper"
    assert oikos["abstract_max_words"] == 300
    assert oikos["three_result_submission_narrative"] is True
    assert oikos["four_act_submission_narrative"] is False
    assert oikos["identifiability_is_coequal_study_objective"] is False
    assert oikos["upload_file_format"] == "RTF"
    assert oikos["double_spaced"] is True
    assert oikos["continuous_line_numbers"] is True
    assert oikos["page_numbers"] is True
    assert oikos["introduction_begins_page_two"] is True
    assert oikos["supporting_information_separate"] is True
    assert oikos["planned_public_repository"] == "Dryad Digital Repository"
    assert oikos["data_and_code_ready_for_first_submission"] is True
    assert oikos["realized_richness_reframe_required_and_integrated"] is True
    assert oikos["three_result_reframe_required_and_integrated"] is True
    assert oikos["supporting_appendix_s19_included"] is True
    assert oikos["supporting_table_s9_included"] is True


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
