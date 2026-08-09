from channel_id.effective_pollinator_dependency import audit_effective_pollinator_dependency
from scripts.audit_effective_pollinator_dependency import mask_uncontrolled_effective_service


def plant_registry():
    return [
        {
            "population_id": "pop-oshima-camp",
            "field_event_id": "event-1",
            "island_id": "Oshima",
            "site_id": "site-1",
            "taxon": "Campanula microdonta",
            "plant_id": "plant-1",
            "analysis_role": "focal_anchor",
            "tagged_at": "2026-07-07T08:00:00+09:00",
            "notes": "",
        }
    ]


def effort_rows():
    return [
        {
            "field_event_id": "event-1", "island_id": "Oshima", "site_id": "site-1",
            "effort_id": "eff-1", "plant_id": "plant-1", "flower_id": "svd-flower-1",
            "start_time": "2026-07-07T09:00:00+09:00", "end_time": "2026-07-07T10:00:00+09:00",
            "monitored_open_flower_count": "1", "method": "video", "video_id": "vid-1",
            "recording_status": "complete", "usable_observation": "yes", "observer_id": "obs", "notes": "",
        },
        {
            "field_event_id": "event-1", "island_id": "Oshima", "site_id": "site-1",
            "effort_id": "eff-2", "plant_id": "plant-1", "flower_id": "svd-flower-2",
            "start_time": "2026-07-07T10:00:00+09:00", "end_time": "2026-07-07T11:00:00+09:00",
            "monitored_open_flower_count": "1", "method": "video", "video_id": "vid-2",
            "recording_status": "complete", "usable_observation": "yes", "observer_id": "obs", "notes": "",
        },
    ]


def visit_rows():
    common = {
        "field_event_id": "event-1", "island_id": "Oshima", "site_id": "site-1", "plant_id": "plant-1",
        "visit_start_offset_s": "60", "visit_end_offset_s": "80", "individual_track_id": "",
        "detection_source": "video", "body_size_class": "large", "identification_confidence": "group_level",
        "corolla_entry": "entered", "anther_contact": "confirmed", "stigma_contact": "confirmed",
        "contact_visibility": "clear", "contact_evidence": "video_direct", "scorer_id": "scorer",
        "scored_at": "2026-07-07T12:00:00+09:00", "notes": "",
    }
    first = dict(common)
    first.update({
        "visit_id": "visit-bombus", "effort_id": "eff-1", "flower_id": "svd-flower-1",
        "source_video_id": "vid-1", "visitor_group": "bombus_ardens_confirmed",
        "identification_confidence": "confirmed",
    })
    second = dict(common)
    second.update({
        "visit_id": "visit-small", "effort_id": "eff-2", "flower_id": "svd-flower-2",
        "source_video_id": "vid-2", "visitor_group": "small_bee_non_bombus", "body_size_class": "small",
    })
    return [first, second]


def svd_rows():
    base = {
        "population_id": "pop-oshima-camp", "field_event_id": "event-1", "island_id": "Oshima",
        "site_id": "site-1", "taxon": "Campanula microdonta", "plant_id": "plant-1",
        "bag_on_time": "2026-07-06T18:00:00+09:00", "bag_off_time": "2026-07-07T08:50:00+09:00",
        "stigma_collected_time": "2026-07-07T10:10:00+09:00", "pollen_count_method": "light_microscopy",
        "heterospecific_pollen_grains": "0", "unclassified_pollen_grains": "0", "counter_id": "counter-1", "notes": "",
    }
    bombus = dict(base)
    bombus.update({
        "svd_id": "svd-bombus", "flower_id": "svd-flower-1", "record_type": "single_visit",
        "effort_id": "eff-1", "visit_id": "visit-bombus", "visitor_group": "bombus_ardens_confirmed",
        "identification_confidence": "confirmed", "first_visit_confirmed": "yes",
        "total_pollen_grains": "20", "conspecific_pollen_grains": "20",
    })
    small = dict(base)
    small.update({
        "svd_id": "svd-small", "flower_id": "svd-flower-2", "record_type": "single_visit",
        "effort_id": "eff-2", "visit_id": "visit-small", "visitor_group": "small_bee_non_bombus",
        "identification_confidence": "group_level", "first_visit_confirmed": "yes",
        "total_pollen_grains": "5", "conspecific_pollen_grains": "5",
    })
    control = dict(base)
    control.update({
        "svd_id": "svd-control", "flower_id": "control-flower", "record_type": "exposed_no_visit_control",
        "effort_id": "", "visit_id": "", "visitor_group": "", "identification_confidence": "not_applicable",
        "first_visit_confirmed": "not_applicable", "total_pollen_grains": "2", "conspecific_pollen_grains": "2",
    })
    return [bombus, small, control]


def treatment_rows():
    base = {
        "population_id": "pop-oshima-camp", "field_event_id": "event-1", "island_id": "Oshima",
        "site_id": "site-1", "taxon": "Campanula microdonta", "plant_id": "plant-1",
        "assigned_at": "2026-07-07T08:00:00+09:00", "bag_on_time": "", "bag_off_time": "",
        "hand_pollen_source_site_id": "", "hand_pollen_source_plant_id": "", "notes": "",
    }
    open_row = dict(base)
    open_row.update({
        "treatment_id": "tr-open", "flower_id": "tr-flower-open", "treatment_type": "open_pollinated",
        "outcome_status": "mature_fruit", "fruit_id": "fruit-open",
    })
    bagged = dict(base)
    bagged.update({
        "treatment_id": "tr-bag", "flower_id": "tr-flower-bag", "treatment_type": "bagged_autonomous",
        "bag_on_time": "2026-07-06T18:00:00+09:00", "outcome_status": "aborted", "fruit_id": "",
    })
    supplemental = dict(base)
    supplemental.update({
        "treatment_id": "tr-cross", "flower_id": "tr-flower-cross", "treatment_type": "supplemental_outcross",
        "hand_pollen_source_site_id": "site-1", "hand_pollen_source_plant_id": "donor-2",
        "outcome_status": "mature_fruit", "fruit_id": "fruit-cross",
    })
    return [open_row, bagged, supplemental]


def fruit_rows():
    return [
        {
            "fruit_id": "fruit-open", "site_id": "site-1", "maternal_id": "plant-1",
            "collection_date": "2026-08-01", "mature_seed_count": "10", "genotyped_seed_target": "0",
            "genotyped_seed_count": "0", "fruit_notes": "",
        },
        {
            "fruit_id": "fruit-cross", "site_id": "site-1", "maternal_id": "plant-1",
            "collection_date": "2026-08-01", "mature_seed_count": "20", "genotyped_seed_target": "0",
            "genotyped_seed_count": "0", "fruit_notes": "",
        },
    ]


def test_effective_dependency_links_visit_rate_svd_and_reproductive_panel():
    audit = audit_effective_pollinator_dependency(
        plant_registry(), effort_rows(), visit_rows(), svd_rows(), treatment_rows(), fruit_rows()
    )
    service = {row["visitor_group"]: row for row in audit.effective_service_rows}
    assert float(service["bombus_ardens_confirmed"]["mean_background_adjusted_svd"]) == 18.0
    assert float(service["small_bee_non_bombus"]["mean_background_adjusted_svd"]) == 3.0
    assert abs(float(service["bombus_ardens_confirmed"]["effective_service_share"]) - 0.85714286) < 1e-7
    readiness = audit.population_readiness_rows[0]
    assert readiness["effective_service_structurally_estimable"] == "yes"
    assert readiness["core_reproductive_panel_structurally_complete"] == "yes"
    assert readiness["dependency_panel_structurally_complete"] == "yes"
    assert float(readiness["autonomous_to_supplemental_capsule_ratio"]) == 0.0
    assert float(readiness["open_to_supplemental_capsule_ratio"]) == 1.0
    treatment = {row["treatment_type"]: row for row in audit.treatment_rows}
    assert float(treatment["supplemental_outcross"]["mean_mature_seeds_per_analyzable_flower"]) == 20.0
    assert float(treatment["bagged_autonomous"]["mean_mature_seeds_per_analyzable_flower"]) == 0.0


def test_structural_completion_is_explicitly_not_a_power_or_selfing_claim():
    audit = audit_effective_pollinator_dependency(
        plant_registry(), effort_rows(), visit_rows(), svd_rows(), treatment_rows(), fruit_rows()
    )
    boundary = audit.population_readiness_rows[0]["boundary"].lower()
    assert "not evidence of adequate power" in boundary
    assert "self-compatibility" in boundary
    assert "realized selfing" in boundary
    assert "evolutionary selection" in boundary


def test_missing_no_visit_control_keeps_effective_service_readiness_closed():
    audit = audit_effective_pollinator_dependency(
        plant_registry(), effort_rows(), visit_rows(), svd_rows()[:2], treatment_rows(), fruit_rows()
    )
    readiness = audit.population_readiness_rows[0]
    assert readiness["effective_service_structurally_estimable"] == "no"
    assert readiness["dependency_panel_structurally_complete"] == "no"


def test_cli_mask_withholds_uncontrolled_service_values_and_shares():
    raw = audit_effective_pollinator_dependency(
        plant_registry(), effort_rows(), visit_rows(), svd_rows()[:2], treatment_rows(), fruit_rows()
    )
    masked = mask_uncontrolled_effective_service(raw)
    assert len(masked.effective_service_rows) == 2
    for row in masked.effective_service_rows:
        assert row["mean_background_adjusted_svd"] == ""
        assert row["effective_pollen_delivery_per_flower_hour"] == ""
        assert row["effective_service_share"] == ""
        assert "withheld" in row["boundary"].lower()


def test_supplemental_outcross_cannot_use_same_maternal_plant_as_donor(tmp_path):
    # Reader-level validation is tested by writing one minimal invalid manifest.
    from channel_id.effective_pollinator_dependency import TREATMENT_COLUMNS, read_pollination_treatments
    import csv

    row = treatment_rows()[2]
    row = dict(row)
    row["hand_pollen_source_plant_id"] = "plant-1"
    path = tmp_path / "treatments.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=TREATMENT_COLUMNS)
        writer.writeheader(); writer.writerow(row)
    try:
        read_pollination_treatments(path)
    except ValueError as error:
        assert "donor must differ" in str(error)
    else:
        raise AssertionError("same-plant supplemental outcross donor should be rejected")
