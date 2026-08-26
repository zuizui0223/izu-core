import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "data/design/simulation_study_mainline_20260824.json"


def test_chapter2_is_reopened_for_response_geometry_before_submission():
    state = json.loads(STATE.read_text(encoding="utf-8"))
    assert state["chapter2_scientific_status"] == "reopened_for_scientific_reassessment_before_submission"
    assert state["scientific_reassessment"] == "docs/SCIENTIFIC_REASSESSMENT_AFTER_CRITIQUE_20260826.md"
    assert state["scientific_reassessment_gate"] == "data/design/manuscript_reassessment_gate_20260826.json"
    assert state["study_type"] == "island_ecology_response_geometry_and_simulation_reassessment_with_comparative_external_grounding"
    assert state["field_data_required_for_current_gate"] is False
    assert state["empirical_mechanism_mapping_required_for_current_gate"] is False
    assert state["external_system_role"] == "comparative_grounding_and_boundary_examples_not_validation_coverage"
    assert state["paper_scope_independent_of_external_research_programmes"] is True
    assert state["active_gate"]["name"] == "response_geometry_and_parameter_robustness"
    assert state["pre_reassessment_manuscript_status"] == "retained_for_provenance_not_submission_ready"


def test_frozen_results_are_preserved_but_claim_roles_are_demoted():
    state = json.loads(STATE.read_text(encoding="utf-8"))
    mechanism = state["ecological_mechanism_readout"]
    assert mechanism["h2_endpoint_sign_identity"] == "sign_delta_reproduction_equals_sign_delta_service_equals_sign_delta_functional_opportunity"
    assert mechanism["h2_endpoint_sign_identity_role"] == "model_structure_that_locates_sign_upstream_not_a_discovery"
    assert mechanism["original_full_mixed_sign_runs"] == "5_of_12"
    assert mechanism["independent_full_mixed_sign_runs"] == "5_of_12"
    assert mechanism["original_full_mixed_sign_run_fraction"] == 0.4166666666666667
    assert mechanism["independent_full_mixed_sign_run_fraction"] == 0.4166666666666667
    assert mechanism["original_initial_trait_off_mixed_sign_run_fraction"] == 0.0
    assert mechanism["independent_initial_trait_off_mixed_sign_run_fraction"] == 0.0
    assert mechanism["trait_adjustment_original_paired_sign_changes"] == 2
    assert mechanism["trait_adjustment_independent_paired_sign_changes"] == 5
    assert mechanism["network_context_sign_rescue_count"] == 16
    assert mechanism["network_context_worsening_count"] == 11
    assert mechanism["assurance_attenuation_count"] == 207
    assert mechanism["assurance_sign_rescue_count_independent"] == 0
    assert mechanism["universal_post_establishment_island_syndrome_supported"] is False

    hypotheses = state["hypothesis_status"]
    assert hypotheses["H1_universal_post_establishment_response"] == "observed_model_capability_5_of_12_not_prevalence_estimate"
    assert hypotheses["H2_state_dependent_branching"] == "demoted_to_model_specific_sensitivity_and_response_geometry_problem"
    assert "bidirectional_local_context_filtering" in hypotheses["H3_context_dependent_branch_allocation"]
    assert "structural_parameter_distinction" in hypotheses["H4_autonomous_assurance_buffering"]
    assert hypotheses["H5_cross_island_response_architecture_recurrence"] == "demoted_from_validation_to_comparative_grounding"


def test_external_set_is_retained_as_grounding_not_validation():
    state = json.loads(STATE.read_text(encoding="utf-8"))
    current = state["current_state"]
    assert current["strict_external_systems"] == 13
    assert current["generative_state_challenges"] == 11
    assert current["generative_state_covered_or_sign_compatible"] == 11
    assert current["coverage_count_role"] == "historical_state_mapping_not_validation"
    assert current["retained_falsifications"] == 1
    assert state["protected_boundaries"]["dominica_heliconia"] == "retained_failed_frozen_signed_position_projection_no_retuning"
    assert state["protected_boundaries"]["external_set"] == "strict_comparative_grounding_set_not_prevalence_or_validation_sample"


def test_submission_is_blocked_until_new_scientific_gate_is_closed():
    state = json.loads(STATE.read_text(encoding="utf-8"))
    submission = state["submission_logic"]
    assert submission["primary_scientific_hypotheses_closed"] is False
    assert submission["research_article_submission_ready"] is False
    assert submission["new_simulation_required"] is True
    assert submission["new_simulation_role"] == "response_geometry_and_parameter_robustness_not_story_cleanup"
    assert submission["new_field_data_required"] is False
    assert submission["new_external_system_search_required"] is False
    assert submission["submission_bundle_blocked"] is True
    assert submission["title_page_metadata"] == "deferred_not_active_blocker"
    assert submission["external_research_programmes_part_of_paper"] is False

    required = state["active_gate"]["required_outputs"]
    assert "response_sign_geometry_across_plant_starting_position" in required
    assert "parameter_sweep_over_pollinator_trait_dispersion_generalism_replacement_partner_loss_arrival_and_saturation" in required
    assert "local_context_sign_change_robustness_map" in required
    assert "assurance_sign_rescue_threshold_map" in required
    assert state["next_executable_task"].startswith("build_response_geometry_and_parameter_robustness")


def test_pre_reassessment_submission_claims_are_explicitly_not_mainline():
    state = json.loads(STATE.read_text(encoding="utf-8"))
    not_mainline = set(state["not_mainline"])
    for item in [
        "submitting_v2_or_v3_as_current_research_article",
        "replicated_minimal_generator_as_headline_discovery",
        "eleven_of_eleven_state_coverage_as_validation",
        "assurance_attenuation_as_emergent_discovery",
        "local_support_on_as_added_beneficial_support",
        "zero_point_four_one_six_seven_as_precise_ecological_frequency",
    ]:
        assert item in not_mainline
    assert state["archived_alternative_framings"]["journal_of_ecology_v2_v3_status"] == "pre_reassessment_not_submission_ready"
    assert state["completed_gates"][-1] == {
        "name": "previous_chapter2_scientific_closure",
        "status": "superseded_by_20260826_reassessment",
    }
