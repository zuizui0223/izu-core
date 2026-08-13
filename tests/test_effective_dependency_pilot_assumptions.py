from channel_id.effective_dependency_pilot_assumptions import build_pilot_assumption_audit


def test_pilot_assumption_audit_separates_coverage_loss_and_reliability():
    plants = (
        {"population_id": "p1", "plant_id": "a"},
        {"population_id": "p1", "plant_id": "b"},
        {"population_id": "p1", "plant_id": "c"},
    )
    svd = (
        {"population_id": "p1", "plant_id": "a", "record_type": "single_visit", "visitor_group": "Bombus"},
        {"population_id": "p1", "plant_id": "a", "record_type": "single_visit", "visitor_group": "Bombus"},
        {"population_id": "p1", "plant_id": "b", "record_type": "single_visit", "visitor_group": "Bombus"},
        {"population_id": "p1", "plant_id": "a", "record_type": "exposed_no_visit_control", "visitor_group": ""},
    )
    treatments = []
    for plant in ("a", "b"):
        for treatment in ("open_pollinated", "bagged_autonomous", "supplemental_outcross"):
            treatments.append({
                "population_id": "p1",
                "plant_id": plant,
                "treatment_type": treatment,
                "outcome_status": "mature_fruit",
            })
    treatments.extend((
        {
            "population_id": "p1",
            "plant_id": "c",
            "treatment_type": "open_pollinated",
            "outcome_status": "lost",
        },
        {
            "population_id": "p1",
            "plant_id": "c",
            "treatment_type": "bagged_autonomous",
            "outcome_status": "pending",
        },
    ))

    result = build_pilot_assumption_audit(plants, svd, tuple(treatments))
    pop = result["populations"][0]
    assert pop["registered_independent_plants"] == 3
    assert pop["plants_with_controlled_svd_any_group"] == 2
    assert pop["controlled_svd_registered_plant_coverage_fraction"] == 2 / 3
    assert pop["plants_with_terminal_outcomes_all_core_treatments"] == 2
    assert pop["joint_panel_registered_plant_coverage_fraction"] == 2 / 3

    by_treatment = {row["treatment_type"]: row for row in pop["treatments"]}
    assert by_treatment["open_pollinated"]["assigned_flowers"] == 3
    assert by_treatment["open_pollinated"]["terminal_analyzable_flowers"] == 2
    assert by_treatment["open_pollinated"]["lost_or_damaged_flowers"] == 1
    assert by_treatment["open_pollinated"]["loss_damage_fraction"] == 1 / 3
    assert by_treatment["bagged_autonomous"]["pending_fraction"] == 1 / 3

    group = pop["visitor_group_svd"][0]
    assert group["single_visit_events"] == 3
    assert group["independent_plants"] == 2
    assert group["plants_with_two_or_more_svd_events"] == 1
    assert group["controlled_svd_available"] is True

    replacement = result["synthetic_assumption_replacement"]
    assert replacement["coverage"]["status"] == "empirically_summarized_when_pilot_rows_exist"
    assert replacement["loss"]["status"] == "empirically_summarized_when_treatment_rows_exist"
    assert replacement["dependency_reliability"]["status"] == "not_identified_from_current_pilot_schema"
    assert replacement["all_synthetic_assumptions_replaced"] is False
    assert result["automatic_design_simulation_injection_allowed"] is False


def test_no_control_prevents_controlled_svd_coverage():
    plants = ({"population_id": "p1", "plant_id": "a"},)
    svd = ({
        "population_id": "p1",
        "plant_id": "a",
        "record_type": "single_visit",
        "visitor_group": "Bombus",
    },)
    result = build_pilot_assumption_audit(plants, svd, ())
    pop = result["populations"][0]
    assert pop["plants_with_controlled_svd_any_group"] == 0
    assert pop["controlled_svd_registered_plant_coverage_fraction"] == 0.0
    assert pop["visitor_group_svd"][0]["controlled_svd_available"] is False
