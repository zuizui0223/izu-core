import json
from pathlib import Path


def load_mainline():
    return json.loads(Path("data/design/active_development_mainline.json").read_text(encoding="utf-8"))


def workstream(mainline, workstream_id):
    return next(row for row in mainline["workstreams"] if row["id"] == workstream_id)


def test_programme_stays_system_agnostic_and_issue91_is_parallel():
    mainline = load_mainline()
    assert mainline["comparison_contract"]["programme_can_progress_without_issue91_field_data"] is True
    assert mainline["comparison_contract"]["no_single_focal_taxon_can_block_programme"] is True
    assert mainline["comparison_contract"]["izu_role"] == "calibration_and_mechanistic_anchor_system_not_programme_center"
    assert mainline["comparison_contract"]["axis_specific_reproductive_responses_must_not_be_collapsed"] is True
    p3 = workstream(mainline, "P3")
    assert p3["issue"] == 91
    assert p3["status"] == "implementation_ready_field_data_missing"
    assert mainline["protected_scientific_state"]["issue91_prediction_freeze"]["programme_blocker"] is False


def test_empirical_buffer_portfolio_has_two_true_candidates_and_guaiacum_is_reference_only():
    mainline = load_mainline()
    admission = mainline["protected_scientific_state"]["buffer_mechanism_admission"]
    assert admission["candidate_count"] == 2
    assert set(admission["candidate_systems"]) == {
        "hawaii_lobelioid_post_extinction_pollination_2026",
        "california_channel_islands_nicotiana_glauca",
    }
    assert admission["candidate_only_count"] == 2
    assert admission["mapping_ready_count"] == 0
    assert admission["empirically_admitted_count"] == 0
    assert admission["guaiacum_removed_from_buffer_portfolio"] is True
    assert admission["guaiacum_current_role"] == "network_context_service_mapping_and_reproductive_axis_decoupling_reference"
    assert admission["guaiacum_correction"] == "data/results/guaiacum_propagation_state_correction.json"
    assert admission["generic_hidden_buffer_allowed"] is False


def test_synthetic_mechanism_roles_remain_decomposed():
    mainline = load_mainline()
    decomp = mainline["protected_scientific_state"]["mechanism_decomposition"]
    assert decomp["branch_generator"] == "preexisting_lineage_position_in_functional_trait_space"
    assert decomp["replicated_strong_buffer_or_branch_allocator"] == "local_support_and_network_context"
    assert decomp["replicated_weak_attenuator"] == "autonomous_assurance_route"
    assert decomp["branch_identity_modifier"] == "partner_effectiveness"
    assert decomp["empirically_identified_universal_buffer"] is False
    assert "both rescue and worsen" in decomp["interpretation"]


def test_assurance_and_network_context_robustness_are_both_preserved():
    mainline = load_mainline()
    state = mainline["protected_scientific_state"]["abm_mechanism_state"]
    assert "zero_of_216" in state["v14_assurance_robustness"]
    assert "zero_of_525" in state["v14_assurance_robustness"]
    assert "2_of_89" in state["network_context_initial"]
    assert "16_of_96" in state["network_context_robustness"]
    assert state["network_context_robustness_result"] == "data/results/network_context_buffering_capability_robustness_frozen.json"


def test_updated_validation_has_two_unmapped_buffer_cases_one_axis_decoupling_and_one_failure():
    mainline = load_mainline()
    gate = mainline["protected_scientific_state"]["system_agnostic_validation_gate"]
    assert gate["status"] == "strict_harness_updated_after_network_buffer_replication_and_guaiacum_axis_correction"
    assert gate["branching_cases_covered"] == 1
    assert gate["same_direction_sign_compatible"] == 1
    assert gate["buffering_state_class_available_but_empirical_mechanism_unmapped"] == 2
    assert gate["reproductive_axis_decoupling_constraints"] == 1
    assert gate["retained_falsifications"] == 1


def test_empirical_network_context_mapping_readiness_is_zero_of_five():
    mainline = load_mainline()
    assert mainline["comparison_contract"]["network_context_empirical_prediction_freeze"] == "data/design/network_context_empirical_prediction_freeze.json"
    assert mainline["comparison_contract"]["network_context_mapping_candidate_registry"] == "data/design/network_context_mapping_candidate_registry.json"
    assert mainline["comparison_contract"]["network_context_mapping_readiness"] == "data/results/network_context_mapping_readiness_frozen.json"
    assert mainline["comparison_contract"]["guaiacum_network_mapping_preflight"] == "data/design/guaiacum_network_context_mapping_preflight.json"

    readiness = mainline["protected_scientific_state"]["network_context_mapping_readiness"]
    assert readiness["systems_screened"] == 5
    assert readiness["mapping_ready_count"] == 0
    assert readiness["closest_structural_candidate"] == "puerto_rico_mona_guaiacum"
    assert readiness["closest_missing_gate"] == "visitor_specific_direct_effectiveness"
    assert readiness["guaiacum_named_source_route_exhausted"] is True
    assert readiness["campanula_programme_blocker"] is False
    assert readiness["derived_estimand"] == "rate_weighted_effective_service = sum_k(V_k * E_k)"
    assert readiness["required_gate_sequence"] == [
        "matched_transition_unit",
        "repeated_local_context_support",
        "visitor_specific_rate",
        "visitor_specific_direct_effectiveness",
        "reproductive_outcome",
    ]

    p2 = workstream(mainline, "P2")
    stage_i = next(row for row in p2["stages"] if row["stage"] == "I")
    assert stage_i["name"] == "empirical_network_context_mapping"
    assert "zero_of_five_mapping_ready" in stage_i["current_state"]
    assert stage_i["candidate_registry"] == "data/design/network_context_mapping_candidate_registry.json"
    assert stage_i["readiness_result"] == "data/results/network_context_mapping_readiness_frozen.json"
    assert "V_k" in stage_i["rule"]
    assert "E_k" in stage_i["rule"]
    assert "Partial or one-sided links do not pass" in stage_i["rule"]


def test_next_task_waits_for_first_five_gate_system_not_specific_taxon_or_exhausted_search():
    mainline = load_mainline()
    assert mainline["next_executable_task"].startswith(
        "accept_the_first_named_source_or_prospective_island_system_that_closes_all_five_network_context_mapping_gates"
    )
    assert "whole_reproduction_buffer_label_from_stable_breeding_system_index_alone" in mainline["not_mainline"]
    assert "restoring_guaiacum_to_buffer_portfolio_without_new_reproductive_buffer_evidence" in mainline["not_mainline"]
    assert "visitor_assemblage_difference_as_service_redundancy_without_per_visit_effectiveness" in mainline["not_mainline"]
    assert "calling_synthetic_network_buffering_empirical_validation" in mainline["not_mainline"]
    assert "tuning_local_support_strength_to_match_observed_outcomes" in mainline["not_mainline"]
    assert "making_issue91_campanula_field_data_a_programme_wide_blocker" in mainline["not_mainline"]
    assert "repeating_guaiacum_Ek_search_without_new_named_trigger" in mainline["not_mainline"]
    assert "repeating_nicotiana_primary_artifact_transport_without_new_route" in mainline["not_mainline"]
    assert "declaring_mapping_ready_from_partial_or_one_sided_links" in mainline["not_mainline"]
