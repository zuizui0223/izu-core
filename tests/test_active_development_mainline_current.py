import json
from pathlib import Path


def load_mainline():
    return json.loads(
        Path("data/design/active_development_mainline.json").read_text(encoding="utf-8")
    )


def workstream(mainline, workstream_id):
    return next(row for row in mainline["workstreams"] if row["id"] == workstream_id)


def test_p1_is_island_system_response_and_propagation_matrix_gate():
    mainline = load_mainline()
    p1 = workstream(mainline, "P1")
    assert p1["name"] == "island_system_response_matrix"
    assert p1["status"] == "active"
    assert "system_by_response_axis_evidence_matrix" in p1["required_outputs"]
    assert "heterogeneous_branching_summary" in p1["required_outputs"]
    assert "propagation_boundary_summary" in p1["required_outputs"]
    assert mainline["comparison_contract"]["propagation_failure_is_a_result"] is True


def test_izu_field_bundle_is_preserved_as_mechanistic_anchor_not_programme_center():
    mainline = load_mainline()
    p3 = workstream(mainline, "P3")
    assert p3["issue"] == 91
    assert p3["status"] == "implementation_ready_field_data_missing"
    assert p3["role"] == "mechanistic_anchor_and_future_direct_dependency_calibration_not_programme_center"
    assert "first_real_six_channel_bundle_passes_preflight" in p3["required_outputs"]
    assert "pilot_variance_coverage_loss_estimates" in p3["required_outputs"]
    assert "direct_izu_signed_position_without_source_native_pollinator_trait_and_weight_data" in p3["blocked_claims"]


def test_stage_c_reflects_six_partial_bridges_and_route_a_closure():
    mainline = load_mainline()
    p2 = workstream(mainline, "P2")
    stage_c = next(row for row in p2["stages"] if row["stage"] == "C")
    assert stage_c["current_state"] == "six_independent_biological_partial_bridges_one_near_complete_zero_complete_route_A_closed"
    assert "source-triggered only" in stage_c["priority_rule"]


def test_mainline_preserves_abm_failures_hawaii_buffering_and_ogasawara_access_bridge():
    mainline = load_mainline()
    state = mainline["protected_scientific_state"]["abm_mechanism_state"]
    assert state["v12_minimal_synthetic_generator"] == "preexisting_lineage_position_in_functional_trait_space"
    assert state["v12_dominica_projection"].startswith("failed_")
    assert "high_reproductive_performance" in state["hawaii_2026_boundary"]
    assert "directional_pollen_transfer" in state["ogasawara_psychotria_bridge"]


def test_formal_fit_and_source_reopen_boundaries_stay_closed():
    mainline = load_mainline()
    protected = mainline["protected_scientific_state"]
    bridge = protected["external_mechanism_bridge_state"]
    assert bridge["independent_partial_systems"] == 6
    assert bridge["complete_systems"] == 0
    assert bridge["hawaii_lobelioid_adds_new_geographic_stratum"] is False
    assert bridge["ogasawara_psychotria_adds_new_geographic_stratum"] is True
    assert bridge["newest_source_triggered_bridge"] == "ogasawara_psychotria_homalosperma_pollinator_replacement"
    assert bridge["stage_c_search_state"] == "route_A_complete_unconstrained_search_closed"
    assert protected["formal_cross_system_fit_ready"] is False

    p5 = workstream(mainline, "P5")
    assert p5["status"] == "wait_for_new_admissible_source_material"
    issue_100_gate = next(row for row in p5["gates"] if row.get("issue") == 100)
    assert "hawaii_and_ogasawara_named_source_triggers" in issue_100_gate["state"]
    hawaii_gate = next(row for row in p5["gates"] if row.get("target") == "hawaii_lobelioid_functional_ecology_raw_csv")
    assert "file_stream_403" in hawaii_gate["state"]
    assert "package_api_401" in hawaii_gate["state"]
    ogasawara_gate = next(row for row in p5["gates"] if row.get("target") == "ogasawara_psychotria_numeric_signed_access_position")
    assert "numeric_signed_mismatch_not_recovered" in ogasawara_gate["state"]


def test_next_executable_task_is_issue91_prediction_freeze_not_another_abm_layer():
    mainline = load_mainline()
    assert mainline["next_executable_task"].startswith(
        "freeze_issue91_propagation_vs_buffering_predictions_before_first_real_field_bundle"
    )
    assert mainline["comparison_contract"]["izu_role"] == "calibration_and_mechanistic_anchor_system_not_programme_center"
    assert "another_generic_abm_layer_before_a_new_empirical_discriminator" in mainline["not_mainline"]
    assert "retuning_the_failed_dominica_signed_position_mapping" in mainline["not_mainline"]
    assert "invent_numeric_signed_position_for_ogasawara_psychotria_from_secondary_proboscis_or_corolla_values" in mainline["not_mainline"]
