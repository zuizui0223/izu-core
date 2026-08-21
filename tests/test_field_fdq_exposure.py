import csv
from pathlib import Path

import pytest

from channel_id.field_fdq_exposure import audit_field_fdq_from_files

ROOT = Path(__file__).resolve().parents[1]
ISLAND = "Oshima"


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


PLANT_FIELDS = [
    "population_id", "field_event_id", "island_id", "site_id", "taxon", "plant_id",
    "analysis_role", "tagged_at", "notes",
]
EFFORT_FIELDS = [
    "field_event_id", "island_id", "site_id", "effort_id", "plant_id", "flower_id",
    "start_time", "end_time", "monitored_open_flower_count", "method", "video_id",
    "recording_status", "usable_observation", "observer_id", "notes",
]
VISIT_FIELDS = [
    "visit_id", "field_event_id", "island_id", "site_id", "effort_id", "plant_id",
    "flower_id", "source_video_id", "visit_start_offset_s", "visit_end_offset_s",
    "individual_track_id", "detection_source", "visitor_group", "visitor_taxon_id",
    "body_size_class", "identification_confidence", "corolla_entry", "anther_contact",
    "stigma_contact", "contact_visibility", "contact_evidence", "scorer_id", "scored_at", "notes",
]
TRAIT_FIELDS = [
    "visitor_taxon_id", "source_taxon_name", "site_id", "proboscis_length_mm", "measurement_n",
    "measurement_source", "source_locator", "trait_status", "source_bundle_sha256", "notes",
]


def base_files(tmp_path: Path, visits: list[dict[str, str]], traits: list[dict[str, str]]):
    plants = tmp_path / "plants.csv"
    effort = tmp_path / "effort.csv"
    visit_path = tmp_path / "visits.csv"
    trait_path = tmp_path / "traits.csv"
    write_csv(plants, PLANT_FIELDS, [{
        "population_id": "pop1", "field_event_id": "event1", "island_id": ISLAND,
        "site_id": "site1", "taxon": "Campanula microdonta", "plant_id": "plant1",
        "analysis_role": "focal_anchor", "tagged_at": "2026-06-01T08:00:00+09:00", "notes": "",
    }])
    write_csv(effort, EFFORT_FIELDS, [{
        "field_event_id": "event1", "island_id": ISLAND, "site_id": "site1",
        "effort_id": "effort1", "plant_id": "plant1", "flower_id": "flower1",
        "start_time": "2026-06-01T09:00:00+09:00", "end_time": "2026-06-01T10:00:00+09:00",
        "monitored_open_flower_count": "1", "method": "live", "video_id": "",
        "recording_status": "complete", "usable_observation": "yes", "observer_id": "obs1", "notes": "",
    }])
    write_csv(visit_path, VISIT_FIELDS, visits)
    write_csv(trait_path, TRAIT_FIELDS, traits)
    return plants, effort, visit_path, trait_path


def visit(visit_id: str, group: str, taxon: str, confidence: str, start: str = "10") -> dict[str, str]:
    return {
        "visit_id": visit_id, "field_event_id": "event1", "island_id": ISLAND, "site_id": "site1",
        "effort_id": "effort1", "plant_id": "plant1", "flower_id": "flower1", "source_video_id": "",
        "visit_start_offset_s": start, "visit_end_offset_s": str(float(start) + 2),
        "individual_track_id": visit_id, "detection_source": "live", "visitor_group": group,
        "visitor_taxon_id": taxon, "body_size_class": "large" if "bombus" in group else "small",
        "identification_confidence": confidence, "corolla_entry": "entered", "anther_contact": "confirmed",
        "stigma_contact": "confirmed", "contact_visibility": "clear", "contact_evidence": "live_direct",
        "scorer_id": "obs1", "scored_at": "2026-06-01T10:01:00+09:00", "notes": "",
    }


def trait(taxon: str, mm: str) -> dict[str, str]:
    return {
        "visitor_taxon_id": taxon, "source_taxon_name": taxon, "site_id": "site1",
        "proboscis_length_mm": mm, "measurement_n": "5", "measurement_source": "source_table_s2",
        "source_locator": "Table S2", "trait_status": "source_exact_site", "source_bundle_sha256": "abc", "notes": "",
    }


def test_repo_visitor_template_carries_optional_taxon_id_for_fdq() -> None:
    header = (ROOT / "templates/field_visitor_contact_manifest_template.csv").read_text(encoding="utf-8").splitlines()[0]
    columns = header.split(",")
    assert "visitor_group" in columns
    assert "visitor_taxon_id" in columns
    assert columns.index("visitor_taxon_id") == columns.index("visitor_group") + 1


def test_complete_taxon_and_trait_coverage_produces_source_formula_fdq(tmp_path: Path) -> None:
    visits = [
        visit("v1", "bombus_ardens_confirmed", "Bombus ardens ardens", "confirmed", "10"),
        visit("v2", "bombus_ardens_confirmed", "Bombus ardens ardens", "confirmed", "20"),
        visit("v3", "small_bee_non_bombus", "Apis mellifera", "confirmed", "30"),
    ]
    paths = base_files(tmp_path, visits, [trait("Bombus ardens ardens", "10"), trait("Apis mellifera", "4")])
    audit = audit_field_fdq_from_files(plants_path=paths[0], effort_path=paths[1], visits_path=paths[2], traits_path=paths[3])
    row = audit.exposure_rows[0]
    assert row["fdq_status"] == "ready"
    assert float(row["fdq"]) == pytest.approx(8 / 3)
    assert float(row["taxon_resolution_fraction"]) == pytest.approx(1.0)
    assert float(row["trait_coverage_fraction"]) == pytest.approx(1.0)
    assert audit.summary["fdq_ready_units"] == 1


def test_zero_visit_usable_effort_remains_explicit_without_inventing_fdq_zero(tmp_path: Path) -> None:
    paths = base_files(tmp_path, [], [])
    audit = audit_field_fdq_from_files(plants_path=paths[0], effort_path=paths[1], visits_path=paths[2], traits_path=paths[3])
    assert len(audit.exposure_rows) == 1
    row = audit.exposure_rows[0]
    assert row["total_visit_bouts"] == "0"
    assert row["fdq"] == ""
    assert row["fdq_status"] == "withheld_no_visit_bouts"
    assert row["taxon_resolution_fraction"] == ""
    assert row["trait_coverage_fraction"] == ""
    assert audit.summary["zero_visit_units"] == 1


def test_group_level_visit_is_retained_and_withholds_fdq(tmp_path: Path) -> None:
    visits = [
        visit("v1", "bombus_ardens_confirmed", "Bombus ardens ardens", "confirmed", "10"),
        visit("v2", "small_bee_non_bombus", "", "group_level", "20"),
    ]
    paths = base_files(tmp_path, visits, [trait("Bombus ardens ardens", "10")])
    audit = audit_field_fdq_from_files(plants_path=paths[0], effort_path=paths[1], visits_path=paths[2], traits_path=paths[3])
    row = audit.exposure_rows[0]
    assert row["fdq"] == ""
    assert row["fdq_status"] == "withheld_incomplete_taxon_or_trait_coverage"
    assert row["total_visit_bouts"] == "2"
    assert row["taxon_resolved_visit_bouts"] == "1"
    assert float(row["taxon_resolution_fraction"]) == pytest.approx(0.5)
    assert row["unresolved_visit_ids"] == "v2"
    assert audit.summary["group_level_service_still_allowed"] is True


def test_confirmed_taxon_with_missing_trait_is_not_dropped_or_renormalized(tmp_path: Path) -> None:
    visits = [
        visit("v1", "bombus_ardens_confirmed", "Bombus ardens ardens", "confirmed", "10"),
        visit("v2", "small_bee_non_bombus", "Apis mellifera", "confirmed", "20"),
    ]
    paths = base_files(tmp_path, visits, [trait("Bombus ardens ardens", "10")])
    audit = audit_field_fdq_from_files(plants_path=paths[0], effort_path=paths[1], visits_path=paths[2], traits_path=paths[3])
    row = audit.exposure_rows[0]
    assert row["fdq"] == ""
    assert row["missing_trait_taxa"] == "Apis mellifera"
    assert float(row["taxon_resolution_fraction"]) == pytest.approx(1.0)
    assert float(row["trait_coverage_fraction"]) == pytest.approx(0.5)


def test_fdq_visit_requires_taxon_column_but_existing_service_manifest_logic_remains_separate(tmp_path: Path) -> None:
    visits = [visit("v1", "bombus_ardens_confirmed", "Bombus ardens ardens", "confirmed")]
    paths = base_files(tmp_path, visits, [trait("Bombus ardens ardens", "10")])
    old_fields = [field for field in VISIT_FIELDS if field != "visitor_taxon_id"]
    write_csv(paths[2], old_fields, [{key: value for key, value in visits[0].items() if key != "visitor_taxon_id"}])
    with pytest.raises(ValueError, match="FDQ visit manifest missing columns: visitor_taxon_id"):
        audit_field_fdq_from_files(plants_path=paths[0], effort_path=paths[1], visits_path=paths[2], traits_path=paths[3])
