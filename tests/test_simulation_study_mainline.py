import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "data/design/simulation_study_mainline_20260824.json"


def test_island_ecology_primary_claim_has_no_field_blocker():
    state = json.loads(STATE.read_text(encoding="utf-8"))
    assert state["study_type"] == "island_ecology_simulation_with_qualitative_external_island_challenges"
    assert state["field_data_required_for_primary_claim"] is False
    assert state["empirical_mechanism_mapping_required_for_primary_claim"] is False
    assert state["external_system_role"] == "comparative_held_out_island_response_state_challenge_not_parameter_calibration"
    assert state["active_gate"]["name"] == "island_ecology_reference_and_submission_alignment"
    assert state["primary_ecological_contribution"].startswith("a_state_dependent_island_response_model")
    assert state["core_story"] == "docs/ISLAND_ECOLOGY_CORE_STORY_20260824.md"
    assert state["hypothesis_recovery"] == "data/design/island_ecology_hypothesis_recovery_20260824.json"
    assert state["manuscript_reassembly_spec"] == "docs/ISLAND_ECOLOGY_MANUSCRIPT_REASSEMBLY_SPEC_20260824.md"
    assert state["primary_manuscript"] == "docs/ISLAND_ECOLOGY_MANUSCRIPT_DRAFT_20260824.md"
    assert state["legacy_ecology_first_draft"] == "docs/SIMULATION_MANUSCRIPT_DRAFT_20260824.md"
    assert state["reference_map"] == "docs/ISLAND_ECOLOGY_REFERENCE_MAP_20260824.md"
    assert state["figure_captions"] == "docs/ISLAND_ECOLOGY_FIGURE_CAPTIONS_20260824.md"
    assert state["journal_positioning"] == "docs/ISLAND_ECOLOGY_JOURNAL_POSITIONING_20260824.md"

    mechanism = state["ecological_mechanism_readout"]
    assert mechanism["branch_generator_independent_replication"] == "replicated_minimal_generator"
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
    assert hypotheses["H2_state_dependent_branching"] == "supported_within_declared_abm_and_independently_replicated"
    assert hypotheses["H3_context_dependent_branch_allocation"] == "supported_bidirectionally_within_declared_abm"
    assert hypotheses["H4_autonomous_assurance_buffering"] == "partially_supported_magnitude_attenuation_only"
    assert hypotheses["H5_cross_island_response_architecture_recurrence"] == "supported_at_qualitative_state_level"

    submission = state["submission_logic"]
    assert submission["primary_scientific_hypotheses_closed"] is True
    assert submission["unresolved_empirical_sidelines_block_submission"] is False
    assert submission["new_simulation_required"] is False
    assert submission["new_field_data_required"] is False
    assert submission["new_external_system_search_required"] is False
    assert submission["primary_journal_target"] == "Journal of Ecology"
    assert submission["fallback_journals"] == ["Functional Ecology", "Oikos"]
    assert submission["method_first_MEE_is_primary_target"] is False
    assert submission["ecology_figure_routing_complete"] is True
    assert submission["reference_map_complete"] is True
    assert submission["figure_captions_complete"] is True
    assert len(submission["future_empirical_tests"]) == 3

    supporting = state["supporting_method_layer"]
    assert supporting["role"] == "inference_guard_and_supplement_not_primary_scientific_novelty"
    assert state["archived_alternative_framings"]["status"] == "not_current_mainline_method_first_spin_off_only"

    completed = {row["name"]: row["status"] for row in state["completed_gates"]}
    assert completed["island_ecology_H1_H5_primary_manuscript_assembled"] == "complete"
    assert completed["island_ecology_main_figure_routing"].startswith("ecology_first_main_Fig1_to_Fig4")
    assert completed["island_ecology_reference_map_and_figure_captions"] == "complete"

    assert "method_first_MEE_framing_as_primary_story" in state["not_mainline"]
    assert "MEE_as_primary_journal_target" in state["not_mainline"]
    assert "inverse_problem_as_primary_discussion_result" in state["not_mainline"]
    assert "state_separability_metrics_as_primary_abstract_conclusion" in state["not_mainline"]
    assert "claim_that_all_islands_follow_one_post_establishment_reproductive_syndrome" in state["not_mainline"]
    assert "claim_that_all_thirteen_systems_share_one_empirical_mechanism" in state["not_mainline"]
    assert "treating_thirteen_strict_systems_as_a_prevalence_sample" in state["not_mainline"]
    assert "collecting_field_data_before_the_primary_simulation_manuscript_is_resolved" in state["not_mainline"]
    assert "unresolved_empirical_translation_sidelines_as_submission_blockers" in state["not_mainline"]
    assert "retuning_dominica_signed_position_mapping" in state["not_mainline"]
    assert "forcing_a_cross_system_meta_analytic_coefficient_from_noncommensurate_estimands" in state["not_mainline"]
    assert state["next_executable_task"].startswith("integrate_source_controlled_citations")
