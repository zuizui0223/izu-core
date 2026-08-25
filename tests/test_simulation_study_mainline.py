import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "data/design/simulation_study_mainline_20260824.json"


def test_island_ecology_primary_claim_and_package_state():
    state = json.loads(STATE.read_text(encoding="utf-8"))
    assert state["chapter2_scientific_status"] == "complete_and_frozen_for_submission"
    assert state["study_type"] == "island_ecology_simulation_with_qualitative_external_island_challenges"
    assert state["field_data_required_for_primary_claim"] is False
    assert state["empirical_mechanism_mapping_required_for_primary_claim"] is False
    assert state["external_system_role"] == "comparative_held_out_island_response_state_challenge_not_parameter_calibration"
    assert state["paper_scope_independent_of_external_research_programmes"] is True
    assert state["active_gate"]["name"] == "island_ecology_submission_metadata_only"
    assert state["primary_ecological_contribution"].startswith("a_state_dependent_island_response_model")
    assert state["core_story"] == "docs/ISLAND_ECOLOGY_CORE_STORY_20260824.md"
    assert state["hypothesis_recovery"] == "data/design/island_ecology_hypothesis_recovery_20260824.json"
    assert state["manuscript_reassembly_spec"] == "docs/ISLAND_ECOLOGY_MANUSCRIPT_REASSEMBLY_SPEC_20260824.md"
    assert state["primary_manuscript"] == "docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V2_20260824.md"
    assert state["supporting_information"] == "docs/ISLAND_ECOLOGY_JECOLOGY_SUPPLEMENT_20260824.md"
    assert state["h2_analytical_sign_decomposition"] == "docs/ISLAND_ECOLOGY_H2_SIGN_DECOMPOSITION_20260825.md"
    assert state["cover_letter"] == "docs/ISLAND_ECOLOGY_JECOLOGY_COVER_LETTER_20260824.md"
    assert state["archived_pre_submission_scientific_draft"] == "docs/ISLAND_ECOLOGY_MANUSCRIPT_DRAFT_20260824.md"
    assert state["archived_legacy_ecology_first_draft"] == "docs/SIMULATION_MANUSCRIPT_DRAFT_20260824.md"
    assert "frozen_scientific_manuscript" not in state
    assert "legacy_ecology_first_draft" not in state
    assert state["reference_map"] == "docs/ISLAND_ECOLOGY_REFERENCE_MAP_20260824.md"
    assert state["figure_captions"] == "docs/ISLAND_ECOLOGY_FIGURE_CAPTIONS_20260824.md"
    assert state["journal_positioning"] == "docs/ISLAND_ECOLOGY_JOURNAL_POSITIONING_20260824.md"
    assert state["journal_format_contract"] == "docs/ISLAND_ECOLOGY_JOURNAL_OF_ECOLOGY_FORMAT_20260824.md"
    assert state["data_code_availability"] == "docs/ISLAND_ECOLOGY_DATA_CODE_AVAILABILITY_20260824.md"
    assert state["submission_manifest"] == "data/design/island_ecology_jecology_submission_manifest.json"

    mechanism = state["ecological_mechanism_readout"]
    assert mechanism["branch_generator_independent_replication"] == "replicated_minimal_generator"
    assert mechanism["h2_endpoint_sign_identity"] == "sign_delta_reproduction_equals_sign_delta_service_equals_sign_delta_functional_opportunity"
    assert mechanism["h2_endpoint_sign_identity_role"] == "analytical_unpacking_of_frozen_v12_not_new_scientific_result"
    assert mechanism["original_full_mixed_sign_run_fraction"] == 0.4166666666666667
    assert mechanism["independent_full_mixed_sign_run_fraction"] == 0.4166666666666667
    assert mechanism["original_initial_trait_off_mixed_sign_run_fraction"] == 0.0
    assert mechanism["independent_initial_trait_off_mixed_sign_run_fraction"] == 0.0
    assert mechanism["network_context_sign_rescue_count"] == 16
    assert mechanism["network_context_worsening_count"] == 11
    assert mechanism["assurance_attenuation_count"] == 207
    assert mechanism["assurance_sign_rescue_count_independent"] == 0
    assert mechanism["universal_post_establishment_island_syndrome_supported"] is False

    current = state["current_state"]
    assert current["strict_external_systems"] == 13
    assert current["branching_systems"] == 3
    assert current["same_direction_systems"] == 6
    assert current["buffering_or_alternative_systems"] == 2
    assert current["empirical_axis_decoupling_constraints"] == 1
    assert current["retained_falsifications"] == 1

    hypotheses = state["hypothesis_status"]
    assert hypotheses["H1_universal_post_establishment_response"] == "rejected"
    assert hypotheses["H2_state_dependent_branching"] == "supported_within_declared_abm_independently_replicated_and_analytically_sign_decomposed"
    assert hypotheses["H3_context_dependent_branch_allocation"] == "supported_bidirectionally_within_declared_abm"
    assert hypotheses["H4_autonomous_assurance_buffering"] == "partially_supported_magnitude_attenuation_only"
    assert hypotheses["H5_cross_island_response_architecture_recurrence"] == "supported_at_qualitative_state_level"

    submission = state["submission_logic"]
    assert submission["primary_scientific_hypotheses_closed"] is True
    assert submission["new_simulation_required"] is False
    assert submission["new_field_data_required"] is False
    assert submission["new_external_system_search_required"] is False
    assert submission["primary_journal_target"] == "Journal of Ecology"
    assert submission["fallback_journals"] == ["Functional Ecology", "Oikos"]
    assert submission["method_first_MEE_is_primary_target"] is False
    assert submission["ecology_figure_routing_complete"] is True
    assert submission["reference_map_complete"] is True
    assert submission["figure_captions_complete"] is True
    assert submission["intext_citations_integrated"] is True
    assert submission["reference_list_assembled"] is True
    assert submission["jecology_numbered_abstract_assembled"] is True
    assert submission["expanded_methods_assembled"] is True
    assert submission["h2_analytical_sign_decomposition_assembled"] is True
    assert submission["main_figure_table_crossreferences_assembled"] is True
    assert submission["supporting_information_assembled"] is True
    assert submission["cover_letter_assembled"] is True
    assert submission["review_data_code_statement_assembled"] is True
    assert submission["submission_manifest_assembled"] is True
    assert submission["submission_format_validation"] == "passed_python_3_10_3_11_3_12"
    assert submission["title_page_metadata"] == "pending_author_and_affiliation_metadata"
    assert submission["external_research_programmes_part_of_paper"] is False
    assert "future_empirical_tests" not in submission
    assert "highest_value_future_test" not in submission
    assert "unresolved_empirical_sidelines_block_submission" not in submission

    supporting = state["supporting_method_layer"]
    assert supporting["role"] == "inference_guard_and_supplement_not_primary_scientific_novelty"
    assert state["archived_alternative_framings"]["status"] == "not_current_mainline_method_first_spin_off_only"

    completed = {row["name"]: row["status"] for row in state["completed_gates"]}
    assert completed["h2_analytical_sign_decomposition"] == "complete_model_internal_endpoint_identity"
    assert completed["island_ecology_H1_H5_primary_manuscript_assembled"] == "complete"
    assert completed["island_ecology_main_figure_routing"].startswith("ecology_first_main_Fig1_to_Fig4")
    assert completed["island_ecology_reference_map_and_figure_captions"] == "complete"
    assert completed["island_ecology_jecology_submission_draft"] == "expanded_methods_and_crossreferences_complete_ci_passed"
    assert completed["island_ecology_supporting_information"] == "assembled_with_h2_analytical_sign_decomposition"
    assert completed["island_ecology_cover_letter"] == "assembled_pending_author_metadata"
    assert completed["island_ecology_submission_manifest_and_data_code_statement"] == "assembled"
    assert completed["external_research_programmes_separated_from_paper"] == "complete"
    assert completed["chapter2_scientific_closure"] == "complete_no_scientific_blockers"

    assert "external_research_programmes_as_submission_dependencies_or_extensions" in state["not_mainline"]
    assert state["protected_boundaries"]["external_research_programmes"] == "out_of_scope_and_not_part_of_submission"
    assert state["protected_boundaries"]["h2_sign_decomposition"] == "model_internal_endpoint_identity_not_a_real_world_trait_or_mechanism_identification"
    assert state["next_executable_task"].startswith("fill_title_page_author_and_affiliation_metadata")
