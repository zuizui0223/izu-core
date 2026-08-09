import math

from channel_id.effective_dependency_precision import (
    build_precision_recommendations,
    recommend_independent_plants,
    summarize_svd_pilot,
    summarize_treatment_pilot,
)


def svd_rows():
    common = {
        "population_id": "pop-1",
        "field_event_id": "event-1",
        "island_id": "Oshima",
        "site_id": "site-1",
        "taxon": "Campanula microdonta",
        "record_type": "single_visit",
        "visitor_group": "bombus_ardens_confirmed",
        "conspecific_pollen_grains": "0",
    }
    rows = []
    for plant, values in (("p1", (10, 14)), ("p2", (20, 24))):
        for index, value in enumerate(values, start=1):
            row = dict(common)
            row.update({
                "svd_id": f"svd-{plant}-{index}",
                "plant_id": plant,
                "conspecific_pollen_grains": str(value),
            })
            rows.append(row)
    rows.append({
        **common,
        "svd_id": "control-1",
        "plant_id": "p1",
        "record_type": "exposed_no_visit_control",
        "visitor_group": "",
        "conspecific_pollen_grains": "2",
    })
    return rows


def treatment_rows():
    rows = []
    # p1: 1/2 capsules; p2: 2/2 capsules.
    outcomes = {"p1": ("mature_fruit", "aborted"), "p2": ("mature_fruit", "mature_fruit")}
    for plant, plant_outcomes in outcomes.items():
        for index, outcome in enumerate(plant_outcomes, start=1):
            rows.append({
                "population_id": "pop-1",
                "treatment_type": "open_pollinated",
                "plant_id": plant,
                "outcome_status": outcome,
            })
    return rows


def test_svd_pilot_summarizes_events_within_plant_before_between_plant_sd():
    plant_rows, summaries = summarize_svd_pilot(svd_rows())
    assert len(plant_rows) == 2
    by_plant = {row["plant_id"]: row for row in plant_rows}
    assert float(by_plant["p1"]["background_adjusted_plant_mean_svd"]) == 10.0
    assert float(by_plant["p2"]["background_adjusted_plant_mean_svd"]) == 20.0
    summary = summaries[0]
    assert summary["independent_plants_with_controlled_svd"] == "2"
    assert summary["total_single_visit_events"] == "4"
    assert float(summary["mean_of_plant_means"]) == 15.0
    assert math.isclose(float(summary["between_plant_sd"]), math.sqrt(50.0), rel_tol=1e-7)
    assert summary["pilot_status"] == "dispersion_estimable"


def test_treatment_pilot_uses_plant_level_capsule_proportions():
    plant_rows, summaries = summarize_treatment_pilot(treatment_rows())
    by_plant = {row["plant_id"]: row for row in plant_rows}
    assert float(by_plant["p1"]["plant_capsule_set_proportion"]) == 0.5
    assert float(by_plant["p2"]["plant_capsule_set_proportion"]) == 1.0
    summary = summaries[0]
    assert summary["independent_plants_with_analyzable_outcomes"] == "2"
    assert summary["total_analyzable_flowers"] == "4"
    assert float(summary["mean_of_plant_proportions"]) == 0.75
    assert summary["pilot_status"] == "dispersion_estimable"


def test_locked_absolute_half_width_generates_independent_plant_recommendation():
    _, svd_summary = summarize_svd_pilot(svd_rows())
    _, treatment_summary = summarize_treatment_pilot(treatment_rows())
    goals = [
        {
            "goal_id": "g-svd",
            "metric": "background_adjusted_svd",
            "population_id": "pop-1",
            "group_label": "bombus_ardens_confirmed",
            "absolute_half_width": "5",
            "confidence": "0.95",
            "status": "locked",
            "notes": "synthetic",
        },
        {
            "goal_id": "g-open",
            "metric": "capsule_set_proportion",
            "population_id": "pop-1",
            "group_label": "open_pollinated",
            "absolute_half_width": "0.20",
            "confidence": "0.95",
            "status": "locked",
            "notes": "synthetic",
        },
    ]
    rows = build_precision_recommendations(goals, svd_summary, treatment_summary)
    assert len(rows) == 2
    indexed = {row["goal_id"]: row for row in rows}
    svd_sd = float(indexed["g-svd"]["pilot_between_plant_sd"])
    expected = recommend_independent_plants(
        between_plant_sd=svd_sd,
        absolute_half_width=5.0,
        confidence=0.95,
    )
    assert int(indexed["g-svd"]["recommended_independent_plants_normal_approx"]) == expected
    assert indexed["g-svd"]["pilot_independent_plants"] == "2"
    assert indexed["g-open"]["status"] == "approximate_n_available"
    assert int(indexed["g-open"]["recommended_independent_plants_normal_approx"]) > 2
    assert "flowers within a plant are not independent n" in indexed["g-open"]["boundary"]


def test_draft_precision_goal_is_not_turned_into_a_sample_size():
    _, svd_summary = summarize_svd_pilot(svd_rows())
    rows = build_precision_recommendations(
        [{
            "goal_id": "draft",
            "metric": "background_adjusted_svd",
            "population_id": "pop-1",
            "group_label": "bombus_ardens_confirmed",
            "absolute_half_width": "",
            "confidence": "",
            "status": "draft",
            "notes": "not locked",
        }],
        svd_summary,
        (),
    )
    assert rows == ()


def test_missing_background_control_does_not_produce_svd_dispersion():
    no_control = [row for row in svd_rows() if row["record_type"] == "single_visit"]
    plants, summaries = summarize_svd_pilot(no_control)
    assert len(plants) == 2
    assert all(row["background_adjusted_plant_mean_svd"] == "" for row in plants)
    assert summaries[0]["independent_plants_with_controlled_svd"] == "0"
    assert summaries[0]["between_plant_sd"] == ""
    assert summaries[0]["pilot_status"] == "needs_more_independent_plants"
