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
    assert admission["prediction_ledger"] == "data/design/cross_system_buffer_prediction_ledger.json"
    assert admission["candidate_count"] == 3
    assert admission["candidate_only_count"] == 3
    assert admission["mapping_ready_count"] == 0
    assert admission["empirically_admitted_count"] == 0
    assert admission["generic_hidden_buffer_allowed"] is False
    assert admission["posthoc_target_fitting_allowed"] is False


def test_hawaii_candidate_is_narrowed_without_empirical_admission():
    mainline = load_mainline()
    state = mainline["protected_scientific_state"]["abm_mechanism_state"]
    assert "Clermontia_lindseyana_and_C_pyrularia" in state["hawaii_historical_exact_taxon_assurance"]
    discriminator = mainline["protected_scientific_state"]["propagation_buffering_discriminator"]
    assert discriminator["hawaii_autonomous_assurance_candidate_source_supported"] is True
    assert discriminator["autonomous_assurance_universal_buffer"] is False
    assert discriminator["one_common_buffering_mechanism_identified"] is False
    admission = mainline["protected_scientific_state"]["buffer_mechanism_admission"]
    assert admission["hawaii_assurance_result"] == "data/results/hawaii_autonomous_assurance_abm_admission_frozen.json"


def test_stage_h_freezes_common_admission_before_synthetic_assurance_diagnostic():
    mainline = load_mainline()
    p2 = workstream(mainline, "P2")
    stage_h = next(row for row in p2["stages"] if row["stage"] == "H")
    assert stage_h["name"] == "buffer_mechanism_admission_and_synthetic_capability"
    assert "common_admission_interface_and_prediction_ledger_frozen" in stage_h["current_state"]
    assert stage_h["interface"] == "data/design/buffer_mechanism_abm_admission_interface.json"
    assert stage_h["portfolio_result"] == "data/results/buffer_candidate_portfolio_admission_frozen.json"
    assert "cannot be called empirical validation" in stage_h["rule"]


def test_next_task_is_assurance_route_ablation_without_new_parameter():
    mainline = load_mainline()
    assert mainline["next_executable_task"].startswith(
        "freeze_and_run_a_matched_assurance_route_ablation_in_the_existing_abm"
    )
    assert "generic_buffer_parameter_before_source_identification" in mainline["not_mainline"]
    assert "calling_synthetic_buffering_capability_empirical_validation" in mainline["not_mainline"]
    assert "using_hawaii_2026_outcomes_to_choose_assurance_parameter_values" in mainline["not_mainline"]
    assert "making_issue91_campanula_field_data_a_programme_wide_blocker" in mainline["not_mainline"]
    assert "another_generic_abm_layer_before_a_new_empirical_discriminator" in mainline["not_mainline"]
