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


def test_strict_validation_and_buffer_admission_remain_partial():
    mainline = load_mainline()
    gate = mainline["protected_scientific_state"]["system_agnostic_validation_gate"]
    assert gate["status"] == "initial_strict_harness_complete_partial_coverage"
    assert gate["qualitatively_covered_systems"] == 1
    assert gate["sign_class_compatible_but_unmapped_systems"] == 1
    assert gate["buffer_mechanism_coverage_gaps"] == 3
    assert gate["retained_falsifications"] == 1

    admission = mainline["protected_scientific_state"]["buffer_mechanism_admission"]
    assert admission["interface"] == "data/design/buffer_mechanism_abm_admission_interface.json"
    assert admission["candidate_count"] == 3
    assert admission["candidate_only_count"] == 3
    assert admission["mapping_ready_count"] == 0
    assert admission["empirically_admitted_count"] == 0
    assert admission["generic_hidden_buffer_allowed"] is False
    assert admission["posthoc_target_fitting_allowed"] is False


def test_v14_initial_sign_rescue_is_retained_but_independent_robustness_downgrades_claim():
    mainline = load_mainline()
    state = mainline["protected_scientific_state"]["abm_mechanism_state"]
    assert "one_of_202_service_declines_sign_rescued" in state["v14_assurance_initial"]
    assert state["v14_initial_result"] == "data/results/constraint_mechanism_abm_v14_assurance_buffering_frozen.json"
    assert "zero_of_216_sign_rescued_207_magnitude_rescued" in state["v14_assurance_robustness"]
    assert "zero_of_525_sign_rescued_510_attenuated" in state["v14_assurance_robustness"]
    assert state["v14_robustness_result"] == "data/results/constraint_mechanism_abm_v14_assurance_buffering_robustness_frozen.json"
    assert state["v14_broadened_result"] == "data/results/assurance_buffering_capability_ablation_frozen.json"

    admission = mainline["protected_scientific_state"]["buffer_mechanism_admission"]
    assert admission["mapping_ready_count"] == 0
    assert admission["empirically_admitted_count"] == 0


def test_stage_h_records_robust_attenuation_and_nonreplicated_sign_buffering():
    mainline = load_mainline()
    p2 = workstream(mainline, "P2")
    stage_h = next(row for row in p2["stages"] if row["stage"] == "H")
    assert stage_h["name"] == "buffer_mechanism_admission_and_synthetic_capability"
    assert "one_of_202_not_replicated" in stage_h["current_state"]
    assert "zero_of_216" in stage_h["current_state"]
    assert "zero_of_525" in stage_h["current_state"]
    assert stage_h["v14_initial_result"] == "data/results/constraint_mechanism_abm_v14_assurance_buffering_frozen.json"
    assert stage_h["v14_robustness_result"] == "data/results/constraint_mechanism_abm_v14_assurance_buffering_robustness_frozen.json"
    assert "magnitude attenuation" in stage_h["rule"]
    assert "Do not tune assurance" in stage_h["rule"]


def test_next_task_moves_to_next_existing_buffer_route_without_assurance_seed_search():
    mainline = load_mainline()
    assert mainline["next_executable_task"].startswith(
        "test_the_next_already_implemented_source_plausible_buffer_route_service_redundancy_or_network_context"
    )
    assert "calling_one_v14_sign_rescue_a_robust_buffering_frequency" in mainline["not_mainline"]
    assert "tuning_assurance_after_v14_to_increase_sign_rescue" in mainline["not_mainline"]
    assert "seed_searching_until_assurance_sign_rescue_reappears" in mainline["not_mainline"]
    assert "calling_synthetic_buffering_capability_empirical_validation" in mainline["not_mainline"]
    assert "using_hawaii_2026_outcomes_to_choose_assurance_parameter_values" in mainline["not_mainline"]
    assert "making_issue91_campanula_field_data_a_programme_wide_blocker" in mainline["not_mainline"]
