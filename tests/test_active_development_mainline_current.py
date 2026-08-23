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
    p3 = workstream(mainline, "P3")
    assert p3["issue"] == 91
    assert p3["status"] == "implementation_ready_field_data_missing"
    assert mainline["protected_scientific_state"]["issue91_prediction_freeze"]["programme_blocker"] is False


def test_empirical_buffer_admission_remains_closed_despite_synthetic_capability():
    mainline = load_mainline()
    admission = mainline["protected_scientific_state"]["buffer_mechanism_admission"]
    assert admission["candidate_count"] == 3
    assert admission["candidate_only_count"] == 3
    assert admission["mapping_ready_count"] == 0
    assert admission["empirically_admitted_count"] == 0
    assert admission["generic_hidden_buffer_allowed"] is False
    assert admission["posthoc_target_fitting_allowed"] is False


def test_mechanism_decomposition_separates_branch_generation_buffering_and_attenuation():
    mainline = load_mainline()
    decomp = mainline["protected_scientific_state"]["mechanism_decomposition"]
    assert decomp["branch_generator"] == "preexisting_lineage_position_in_functional_trait_space"
    assert decomp["replicated_strong_buffer_or_branch_allocator"] == "local_support_and_network_context"
    assert decomp["replicated_weak_attenuator"] == "autonomous_assurance_route"
    assert decomp["branch_identity_modifier"] == "partner_effectiveness"
    assert decomp["empirically_identified_universal_buffer"] is False
    assert "both rescue and worsen" in decomp["interpretation"]


def test_assurance_sign_rescue_remains_nonreplicated():
    mainline = load_mainline()
    state = mainline["protected_scientific_state"]["abm_mechanism_state"]
    assert "one_of_202_service_declines_sign_rescued" in state["v14_assurance_initial"]
    assert "zero_of_216" in state["v14_assurance_robustness"]
    assert "zero_of_525" in state["v14_assurance_robustness"]
    assert state["v14_robustness_result"] == "data/results/constraint_mechanism_abm_v14_assurance_buffering_robustness_frozen.json"


def test_network_context_sign_buffering_replicates_but_is_bidirectional():
    mainline = load_mainline()
    state = mainline["protected_scientific_state"]["abm_mechanism_state"]
    assert "2_of_89" in state["network_context_initial"]
    assert "worsened_37" in state["network_context_initial"]
    assert state["network_context_initial_result"] == "data/results/network_context_buffering_capability_ablation_frozen.json"
    assert "16_of_96" in state["network_context_robustness"]
    assert "worsened_11" in state["network_context_robustness"]
    assert state["network_context_robustness_result"] == "data/results/network_context_buffering_capability_robustness_frozen.json"

    p2 = workstream(mainline, "P2")
    stage_i = next(row for row in p2["stages"] if row["stage"] == "I")
    assert stage_i["name"] == "network_context_buffering_capability"
    assert "sign_rescue_replicated" in stage_i["current_state"]
    assert "worsening_also_occurs" in stage_i["current_state"]
    assert "Do not call it Guaiacum" in stage_i["rule"]


def test_next_task_is_empirical_network_context_mapping_not_parameter_tuning():
    mainline = load_mainline()
    assert mainline["next_executable_task"].startswith(
        "freeze_empirical_network_context_buffer_predictions_and_apply_the_common_admission_interface"
    )
    assert "calling_network_context_a_universal_buffer" in mainline["not_mainline"]
    assert "calling_network_context_guaiacum_service_redundancy_without_source_native_mapping" in mainline["not_mainline"]
    assert "tuning_local_support_strength_to_match_observed_buffering" in mainline["not_mainline"]
    assert "seed_searching_until_more_network_context_sign_rescues_appear" in mainline["not_mainline"]
    assert "calling_synthetic_buffering_capability_empirical_validation" in mainline["not_mainline"]
    assert "making_issue91_campanula_field_data_a_programme_wide_blocker" in mainline["not_mainline"]
