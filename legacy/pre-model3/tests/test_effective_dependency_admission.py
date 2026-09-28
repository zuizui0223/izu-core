from scripts.audit_effective_dependency_admission import build_admission


def _plant(pop, plant):
    return {"population_id": pop, "plant_id": plant}


def _svd(pop, plant, record_type, group=""):
    return {
        "population_id": pop,
        "plant_id": plant,
        "record_type": record_type,
        "visitor_group": group,
    }


def _treatment(pop, plant, treatment, outcome="mature_fruit"):
    return {
        "population_id": pop,
        "plant_id": plant,
        "treatment_type": treatment,
        "outcome_status": outcome,
    }


def test_one_plant_can_be_structural_but_not_dispersion_ready():
    plants = (_plant("p1", "a"),)
    svd = (
        _svd("p1", "a", "single_visit", "Bombus"),
        _svd("p1", "a", "exposed_no_visit_control"),
    )
    treatments = tuple(_treatment("p1", "a", t) for t in (
        "open_pollinated", "bagged_autonomous", "supplemental_outcross"
    ))
    result = build_admission(plants, svd, treatments)
    row = result["populations"][0]
    assert row["pilot_dispersion_gate_pass"] is False
    assert row["controlled_svd_between_plant_dispersion_estimable"] is False
    assert row["core_treatment_between_plant_dispersion_estimable"] is False
    assert row["confirmatory_adequacy"] is False


def test_two_independent_plants_make_variance_defined_not_confirmatory():
    plants = (_plant("p1", "a"), _plant("p1", "b"))
    svd = (
        _svd("p1", "a", "single_visit", "Bombus"),
        _svd("p1", "b", "single_visit", "Bombus"),
        _svd("p1", "a", "bagged_unvisited_control"),
    )
    treatments = tuple(
        _treatment("p1", plant, treatment)
        for plant in ("a", "b")
        for treatment in ("open_pollinated", "bagged_autonomous", "supplemental_outcross")
    )
    result = build_admission(plants, svd, treatments)
    row = result["populations"][0]
    assert row["pilot_dispersion_gate_pass"] is True
    assert row["svd_groups_with_between_plant_dispersion_estimable"] == ["Bombus"]
    assert row["confirmatory_adequacy"] is False
    assert result["confirmatory_adequacy_inferred"] is False


def test_pending_lost_and_damaged_do_not_create_treatment_replication():
    plants = (_plant("p1", "a"), _plant("p1", "b"))
    svd = (
        _svd("p1", "a", "single_visit", "Bombus"),
        _svd("p1", "b", "single_visit", "Bombus"),
        _svd("p1", "a", "exposed_no_visit_control"),
    )
    treatments = (
        _treatment("p1", "a", "open_pollinated", "mature_fruit"),
        _treatment("p1", "b", "open_pollinated", "pending"),
        _treatment("p1", "a", "bagged_autonomous", "aborted"),
        _treatment("p1", "b", "bagged_autonomous", "lost"),
        _treatment("p1", "a", "supplemental_outcross", "mature_fruit"),
        _treatment("p1", "b", "supplemental_outcross", "damaged"),
    )
    row = build_admission(plants, svd, treatments)["populations"][0]
    assert row["core_treatment_distinct_plants_with_terminal_outcome"] == {
        "open_pollinated": 1,
        "bagged_autonomous": 1,
        "supplemental_outcross": 1,
    }
    assert row["pilot_dispersion_gate_pass"] is False


def test_controls_do_not_become_visitor_specific_svd_replicates():
    plants = (_plant("p1", "a"), _plant("p1", "b"))
    svd = (
        _svd("p1", "a", "single_visit", "Bombus"),
        _svd("p1", "a", "exposed_no_visit_control"),
        _svd("p1", "b", "bagged_unvisited_control"),
    )
    treatments = tuple(
        _treatment("p1", plant, treatment)
        for plant in ("a", "b")
        for treatment in ("open_pollinated", "bagged_autonomous", "supplemental_outcross")
    )
    row = build_admission(plants, svd, treatments)["populations"][0]
    assert row["single_visit_svd_distinct_plants_by_group"] == {"Bombus": 1}
    assert row["controlled_svd_between_plant_dispersion_estimable"] is False
    assert row["pilot_dispersion_gate_pass"] is False
