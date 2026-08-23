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


def test_strict_validation_and_buffer_gate_remain_partial():
    mainline = load_mainline()
    gate = mainline["protected_scientific_state"]["system_agnostic_validation_gate"]
    assert gate["status"] == "initial_strict_harness_complete_partial_coverage"
    assert gate["qualitatively_covered_systems"] == 1
    assert gate["sign_class_compatible_but_unmapped_systems"] == 1
    assert gate["buffer_mechanism_coverage_gaps"] == 3
    assert gate["retained_falsifications"] == 1
    assert gate["campanula_specific_tuning_allowed"] is False

    bridge = mainline["protected_scientific_state"]["external_mechanism_bridge_state"]
    assert bridge["independent_partial_systems"] == 6
    assert bridge["complete_systems"] == 0
    assert bridge["buffer_mechanism_ready_for_abm_admission"] == 0
    assert bridge["hawaii_exact_taxon_assurance_candidate_found"] is True
    assert bridge["hawaii_named_dependency_source_check"] == "data/results/hawaii_lobelioid_controlled_dependency_named_source_check.json"


def test_hawaii_candidate_is_narrowed_without_abm_admission():
    mainline = load_mainline()
    state = mainline["protected_scientific_state"]["abm_mechanism_state"]
    assert "Clermontia_lindseyana_and_C_pyrularia" in state["hawaii_historical_exact_taxon_assurance"]
    discriminator = mainline["protected_scientific_state"]["propagation_buffering_discriminator"]
    assert discriminator["hawaii_autonomous_assurance_candidate_source_supported"] is True
    assert discriminator["autonomous_assurance_universal_buffer"] is False
    assert discriminator["one_common_buffering_mechanism_identified"] is False


def test_source_reopen_gates_do_not_repeat_exhausted_hawaii_or_cordia_searches():
    mainline = load_mainline()
    p5 = workstream(mainline, "P5")
    hawaii = next(row for row in p5["gates"] if row.get("target") == "hawaii_lobelioid_controlled_dependency_same_context")
    assert "named_historical_exact_taxon_assurance_found" in hawaii["state"]
    assert "same_context_numeric_dependency_still_missing" in hawaii["state"]
    cordia = next(row for row in p5["gates"] if row.get("target") == "cordia_dong_single_visit_effectiveness_and_dependency")
    assert "targeted_followup_exhausted" in cordia["state"]
    assert "reopen_only_on_new_named_source_native_or_prospective_matched_measurement" in cordia["state"]
    assert "repeat_broad_hawaii_historical_assurance_search_after_exact_taxon_candidate_found" in mainline["not_mainline"]
    assert "repeat_cordia_dong_search_without_new_named_source_trigger" in mainline["not_mainline"]


def test_next_internal_task_is_buffer_admission_interface_not_generic_parameter():
    mainline = load_mainline()
    assert mainline["next_executable_task"].startswith(
        "freeze_a_source_agnostic_buffer_mechanism_admission_interface_and_cross_system_prediction_ledger"
    )
    assert "generic_buffer_parameter_before_source_identification" in mainline["not_mainline"]
    assert "making_issue91_campanula_field_data_a_programme_wide_blocker" in mainline["not_mainline"]
    assert "another_generic_abm_layer_before_a_new_empirical_discriminator" in mainline["not_mainline"]
