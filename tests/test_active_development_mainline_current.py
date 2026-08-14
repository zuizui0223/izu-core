import json
from pathlib import Path


def load_mainline():
    return json.loads(
        Path("data/design/active_development_mainline.json").read_text(encoding="utf-8")
    )


def workstream(mainline, workstream_id):
    return next(row for row in mainline["workstreams"] if row["id"] == workstream_id)


def test_p1_is_first_real_field_bundle_gate():
    mainline = load_mainline()
    p1 = workstream(mainline, "P1")
    assert p1["issue"] == 91
    assert p1["status"] == "implementation_ready_field_data_missing"
    assert "first_real_six_channel_bundle_passes_preflight" in p1["required_outputs"]


def test_p1_does_not_relabel_focal_pilot_as_final_dependency_reliability():
    p1 = workstream(load_mainline(), "P1")
    outputs = p1["required_outputs"]
    assert "pilot_variance_coverage_loss_estimates" in outputs
    assert "final_dependency_reliability_remains_separate_repeated_final_estimand_gate" in outputs
    assert "pilot_variance_reliability_coverage_loss_estimates" not in outputs
    assert "final_dependency_reliability_from_single_focal_pilot" in p1["blocked_claims"]


def test_stage_c_reflects_three_partial_bridges_and_cordia_gap():
    mainline = load_mainline()
    p3 = workstream(mainline, "P3")
    stage_c = next(row for row in p3["stages"] if row["stage"] == "C")
    assert stage_c["current_state"] == "three_independent_partial_bridges_one_near_complete_zero_complete"
    assert stage_c["current_best_bridge"] == "xisha_cordia_subcordata_two_island_system"
    assert stage_c["missing_best_bridge_links"] == [
        "Dong_direct_single_visit_effectiveness",
        "Dong_controlled_reproductive_dependency",
    ]


def test_formal_fit_and_source_reopen_boundaries_stay_closed():
    mainline = load_mainline()
    protected = mainline["protected_scientific_state"]
    assert protected["external_mechanism_bridge_state"]["independent_partial_systems"] == 3
    assert protected["external_mechanism_bridge_state"]["complete_systems"] == 0
    assert protected["formal_cross_system_fit_ready"] is False

    p4 = workstream(mainline, "P4")
    assert p4["status"] == "wait_for_new_admissible_source_material"


def test_next_executable_task_keeps_issue_91_first():
    mainline = load_mainline()
    assert mainline["next_executable_task"].startswith("Issue_91_first_real_field_bundle")
