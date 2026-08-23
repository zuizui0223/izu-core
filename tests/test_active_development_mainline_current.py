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


def test_v14_assurance_has_synthetic_sufficiency_but_does_not_change_empirical_admission():
    mainline = load_mainline()
    state = mainline["protected_scientific_state"]["abm_mechanism_state"]
    assert state["v14_assurance_buffering"] == (
        "synthetic_sign_buffering_sufficient_but_sparse_one_of_202_service_declines_"
        "197_magnitude_rescues_empirical_admission_unchanged"
    )
    assert state["v14_result"] == "data/results/constraint_mechanism_abm_v14_assurance_buffering_frozen.json"
    admission = mainline["protected_scientific_state"]["buffer_mechanism_admission"]
    assert admission["mapping_ready_count"] == 0
    assert admission["empirically_admitted_count"] == 0
    assert admission["hawaii_assurance_result"] == "data/results/hawaii_autonomous_assurance_abm_admission_frozen.json"


def test_stage_h_records_sparse_v14_sign_rescue_and_requires_independent_robustness():
    mainline = load_mainline()
    p2 = workstream(mainline, "P2")
    stage_h = next(row for row in p2["stages"] if row["stage"] == "H")
    assert stage_h["name"] == "buffer_mechanism_admission_and_synthetic_capability"
    assert "assurance_sign_rescue_1_of_202" in stage_h["current_state"]
    assert "magnitude_rescue_197_of_202" in stage_h["current_state"]
    assert stage_h["v14_result"] == "data/results/constraint_mechanism_abm_v14_assurance_buffering_frozen.json"
    assert "non-overlapping stochastic block" in stage_h["rule"]


def test_next_task_is_independent_v14_robustness_without_retuning():
    mainline = load_mainline()
    assert mainline["next_executable_task"].startswith(
        "freeze_and_run_an_independent_nonoverlapping_seed_block_robustness_test_of_the_exact_v14_assurance_ablation"
    )
    assert "calling_one_v14_sign_rescue_a_robust_buffering_frequency" in mainline["not_mainline"]
    assert "tuning_assurance_after_v14_to_increase_sign_rescue" in mainline["not_mainline"]
    assert "calling_synthetic_buffering_capability_empirical_validation" in mainline["not_mainline"]
    assert "using_hawaii_2026_outcomes_to_choose_assurance_parameter_values" in mainline["not_mainline"]
    assert "making_issue91_campanula_field_data_a_programme_wide_blocker" in mainline["not_mainline"]
