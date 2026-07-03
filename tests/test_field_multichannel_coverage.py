from pathlib import Path

from channel_id.field_multichannel_coverage import (
    build_field_multichannel_coverage,
    write_field_multichannel_coverage,
)


def _base(*, plant: str = "P001", island: str = "Oshima", site: str = "OSH_01") -> dict[str, str]:
    return {
        "field_event_id": "izu_20260704",
        "island_id": island,
        "site_id": site,
        "plant_id": plant,
    }


def _guide(**changes: str) -> dict[str, str]:
    row = {
        **_base(),
        "photo_id": "IMG001",
        "inner_corolla_view_field": "yes",
    }
    row.update(changes)
    return row


def _geometry(**changes: str) -> dict[str, str]:
    row = {
        **_base(),
        "flower_id": "F001",
    }
    row.update(changes)
    return row


def _effort(**changes: str) -> dict[str, str]:
    row = {
        **_base(),
        "effort_id": "E001",
        "start_time": "2026-07-04T09:00:00+09:00",
        "end_time": "2026-07-04T09:30:00+09:00",
        "monitored_open_flower_count": "2",
        "usable_observation": "yes",
    }
    row.update(changes)
    return row


def _visit(**changes: str) -> dict[str, str]:
    row = {
        **_base(),
        "visit_id": "V001",
        "anther_contact": "confirmed",
        "stigma_contact": "confirmed",
    }
    row.update(changes)
    return row


def test_coverage_links_complete_tagged_plant_and_retains_contact_counts(tmp_path: Path) -> None:
    coverage = build_field_multichannel_coverage(
        [_guide()], [_geometry()], [_effort()], [_visit()]
    )

    assert len(coverage.plant_rows) == 1
    plant = coverage.plant_rows[0]
    assert plant["guide_capture_status"] == "inner_view_recorded"
    assert plant["geometry_status"] == "geometry_recorded"
    assert plant["usable_plant_effort_windows"] == "1"
    assert plant["scored_plant_visit_bouts"] == "1"
    assert plant["confirmed_both_contact_bouts"] == "1"
    assert plant["coverage_status"] == "linked_multichannel_unit_with_scored_visit"
    assert plant["next_required_action"] == "retain_linkage_and_add_reproductive_outcome_when_feasible"

    output = tmp_path / "coverage"
    write_field_multichannel_coverage(output, coverage)
    assert (output / "field_multichannel_plant_coverage.csv").exists()
    assert (output / "field_multichannel_site_coverage.csv").exists()
    assert (output / "field_multichannel_island_coverage.csv").exists()


def test_coverage_does_not_treat_zero_scored_visits_as_absence() -> None:
    coverage = build_field_multichannel_coverage(
        [_guide()], [_geometry()], [_effort()], []
    )

    plant = coverage.plant_rows[0]
    assert plant["observation_status"] == "usable_effort_no_scored_visit"
    assert plant["coverage_status"] == "linked_multichannel_unit_no_scored_visit"
    assert plant["next_required_action"] == "retain_zero_visit_effort_and_add_comparable_observation_windows"
    assert coverage.site_rows[0]["scored_visit_bouts"] == "0"
    assert coverage.island_rows[0]["coverage_status"] == "multichannel_plant_coverage_present"


def test_coverage_identifies_missing_inner_photo_geometry_and_plant_linked_effort() -> None:
    guide_only = _guide(plant="P002", photo_id="IMG002", inner_corolla_view_field="no")
    geometry_only = _geometry(plant="P003", flower_id="F003")
    coverage = build_field_multichannel_coverage(
        [guide_only], [geometry_only], [], []
    )
    rows = {row["plant_id"]: row for row in coverage.plant_rows}

    assert rows["P002"]["coverage_status"] == "missing_guide_inner_corolla_photo"
    assert rows["P002"]["next_required_action"] == "capture_standardized_inner_corolla_photo"
    assert rows["P003"]["coverage_status"] == "missing_guide_inner_corolla_photo"
    assert rows["P003"]["geometry_status"] == "geometry_recorded"


def test_site_level_effort_without_tagged_plant_is_not_assigned_to_a_plant() -> None:
    unlinked = _effort(plant="", effort_id="E_SITE", monitored_open_flower_count="4")
    coverage = build_field_multichannel_coverage([], [], [unlinked], [])

    assert coverage.plant_rows == ()
    site = coverage.site_rows[0]
    assert site["tagged_plants"] == "0"
    assert site["usable_effort_windows"] == "1"
    assert site["unlinked_usable_effort_windows"] == "1"
    assert site["site_coverage_status"] == "effort_without_tagged_plant_linkage"


def test_coverage_rejects_plant_linked_row_with_missing_site_context() -> None:
    bad = _guide(site="")
    try:
        build_field_multichannel_coverage([bad], [], [], [])
    except ValueError as error:
        assert "missing event, island, or site" in str(error)
    else:
        raise AssertionError("invalid plant-linked row was accepted")
