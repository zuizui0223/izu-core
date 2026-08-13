import hashlib
import json
import math

import pytest

from channel_id.effective_dependency_precision import (
    build_precision_recommendations,
    recommend_independent_plants,
    summarize_svd_pilot,
    summarize_treatment_pilot,
)
from scripts.plan_effective_dependency_pilot_precision import validate_precision_inputs


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


def locked_goal():
    return {
        "goal_id": "g-svd",
        "metric": "background_adjusted_svd",
        "population_id": "pop-1",
        "group_label": "bombus_ardens_confirmed",
        "absolute_half_width": "5",
        "confidence": "0.95",
        "status": "locked",
        "notes": "synthetic",
    }


def _sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_freeze(path, svd, treatments):
    path.write_text(json.dumps({
        "status": "effective_dependency_raw_field_bundle_frozen",
        "required_channels": ["plants", "effort", "visits", "svd", "treatments", "fruits"],
        "channels": [
            {"channel": "svd", "sha256": _sha(svd)},
            {"channel": "treatments", "sha256": _sha(treatments)},
        ],
    }), encoding="utf-8")


def _write_admission(path, svd, treatments, *, svd_sha=None, pass_gate=True):
    path.write_text(json.dumps({
        "schema_version": "effective_dependency_admission_v1",
        "input_sha256": {
            "plants": "synthetic-plants-sha",
            "svd": svd_sha or _sha(svd),
            "treatments": _sha(treatments),
        },
        "populations": [{"population_id": "pop-1", "pilot_dispersion_gate_pass": pass_gate}],
    }), encoding="utf-8")


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
        locked_goal(),
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


def test_draft_goal_does_not_require_freeze_or_admission(tmp_path):
    svd = tmp_path / "svd.csv"
    treatments = tmp_path / "treatments.csv"
    svd.write_text("svd\n", encoding="utf-8")
    treatments.write_text("treatments\n", encoding="utf-8")
    validate_precision_inputs(
        goals=[{**locked_goal(), "status": "draft"}],
        svd_path=svd,
        treatments_path=treatments,
        freeze_manifest_path=None,
        admission_path=None,
    )


def test_locked_goal_requires_freeze_manifest(tmp_path):
    svd = tmp_path / "svd.csv"
    treatments = tmp_path / "treatments.csv"
    svd.write_text("svd\n", encoding="utf-8")
    treatments.write_text("treatments\n", encoding="utf-8")
    with pytest.raises(ValueError, match="--freeze-manifest"):
        validate_precision_inputs(
            goals=[locked_goal()],
            svd_path=svd,
            treatments_path=treatments,
            freeze_manifest_path=None,
            admission_path=tmp_path / "admission.json",
        )


def test_locked_goal_rejects_bytes_changed_after_freeze(tmp_path):
    svd = tmp_path / "svd.csv"
    treatments = tmp_path / "treatments.csv"
    svd.write_text("original-svd\n", encoding="utf-8")
    treatments.write_text("treatments\n", encoding="utf-8")
    freeze = tmp_path / "freeze.json"
    admission = tmp_path / "admission.json"
    _write_freeze(freeze, svd, treatments)
    _write_admission(admission, svd, treatments)
    svd.write_text("changed-svd\n", encoding="utf-8")
    with pytest.raises(ValueError, match="svd bytes do not match"):
        validate_precision_inputs(
            goals=[locked_goal()],
            svd_path=svd,
            treatments_path=treatments,
            freeze_manifest_path=freeze,
            admission_path=admission,
        )


def test_locked_goal_rejects_stale_admission_even_when_freeze_matches(tmp_path):
    svd = tmp_path / "svd.csv"
    treatments = tmp_path / "treatments.csv"
    svd.write_text("svd\n", encoding="utf-8")
    treatments.write_text("treatments\n", encoding="utf-8")
    freeze = tmp_path / "freeze.json"
    admission = tmp_path / "admission.json"
    _write_freeze(freeze, svd, treatments)
    _write_admission(admission, svd, treatments, svd_sha="stale-admission-sha")
    with pytest.raises(ValueError, match="admission artifact was not built from the current svd bytes"):
        validate_precision_inputs(
            goals=[locked_goal()],
            svd_path=svd,
            treatments_path=treatments,
            freeze_manifest_path=freeze,
            admission_path=admission,
        )


def test_locked_goal_accepts_frozen_bytes_after_matching_admission_pass(tmp_path):
    svd = tmp_path / "svd.csv"
    treatments = tmp_path / "treatments.csv"
    svd.write_text("svd\n", encoding="utf-8")
    treatments.write_text("treatments\n", encoding="utf-8")
    freeze = tmp_path / "freeze.json"
    admission = tmp_path / "admission.json"
    _write_freeze(freeze, svd, treatments)
    _write_admission(admission, svd, treatments)
    validate_precision_inputs(
        goals=[locked_goal()],
        svd_path=svd,
        treatments_path=treatments,
        freeze_manifest_path=freeze,
        admission_path=admission,
    )
