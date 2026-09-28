import csv
from pathlib import Path

import pytest

from channel_id.field_legitimate_contact import (
    EFFORT_COLUMNS,
    VISIT_COLUMNS,
    audit_field_contacts,
    read_effort_manifest,
    read_visit_manifest,
    write_field_contact_audit,
)


def _effort(**changes: str) -> dict[str, str]:
    row = {
        "field_event_id": "izu_20260704",
        "island_id": "Oshima",
        "site_id": "OSH_01",
        "effort_id": "E001",
        "plant_id": "P001",
        "flower_id": "F001",
        "start_time": "2026-07-04T09:00:00+09:00",
        "end_time": "2026-07-04T09:10:00+09:00",
        "monitored_open_flower_count": "2",
        "method": "fixed_video",
        "video_id": "VID001",
        "recording_status": "complete",
        "usable_observation": "yes",
        "observer_id": "observer_1",
        "notes": "",
    }
    row.update(changes)
    return row


def _visit(**changes: str) -> dict[str, str]:
    row = {
        "visit_id": "V001",
        "field_event_id": "izu_20260704",
        "island_id": "Oshima",
        "site_id": "OSH_01",
        "effort_id": "E001",
        "plant_id": "P001",
        "flower_id": "F001",
        "source_video_id": "VID001",
        "visit_start_offset_s": "20",
        "visit_end_offset_s": "28",
        "individual_track_id": "track_1",
        "detection_source": "manual_video_review",
        "visitor_group": "small_bee_non_bombus",
        "body_size_class": "small",
        "identification_confidence": "group_level",
        "corolla_entry": "entered",
        "anther_contact": "confirmed",
        "stigma_contact": "confirmed",
        "contact_visibility": "clear",
        "contact_evidence": "video_direct",
        "scorer_id": "scorer_A",
        "scored_at": "2026-07-05T10:00:00+09:00",
        "notes": "",
    }
    row.update(changes)
    return row


def _write(path: Path, fields: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def test_field_contact_audit_keeps_zero_visit_effort_in_flower_hour_denominator(tmp_path: Path) -> None:
    effort_path = tmp_path / "effort.csv"
    visit_path = tmp_path / "visits.csv"
    # The second usable window has no visit but contributes 20 flower-minutes.
    second = _effort(
        effort_id="E002",
        plant_id="P002",
        flower_id="F002",
        start_time="2026-07-04T10:00:00+09:00",
        end_time="2026-07-04T10:20:00+09:00",
        monitored_open_flower_count="1",
        video_id="VID002",
    )
    _write(effort_path, EFFORT_COLUMNS, [_effort(), second])
    _write(visit_path, VISIT_COLUMNS, [_visit()])

    efforts = read_effort_manifest(effort_path)
    visits = read_visit_manifest(visit_path)
    audit = audit_field_contacts(efforts, visits)

    assert len(audit.visit_ledger_rows) == 1
    ledger = audit.visit_ledger_rows[0]
    assert ledger["contact_proxy_status"] == "confirmed_both_contact"
    summary = audit.rate_summary_rows[0]
    # 2 flowers x 10 min + 1 flower x 20 min = 40 flower-minutes = 2/3 flower-hour.
    assert summary["usable_effort_windows"] == "2"
    assert float(summary["monitored_flower_hours"]) == pytest.approx(2.0 / 3.0)
    assert summary["visit_bouts"] == "1"
    assert summary["confirmed_both_contact_bouts"] == "1"
    assert float(summary["visit_bouts_per_flower_hour"]) == pytest.approx(1.5)
    assert float(summary["confirmed_both_fraction_of_scorable_bouts"]) == pytest.approx(1.0)

    output = tmp_path / "audit"
    write_field_contact_audit(output, audit)
    assert (output / "field_contact_visit_ledger.csv").exists()
    assert (output / "field_contact_rate_summary.csv").exists()


def test_contact_validation_rejects_non_entry_confirmed_contact(tmp_path: Path) -> None:
    path = tmp_path / "visits.csv"
    _write(path, VISIT_COLUMNS, [_visit(corolla_entry="landed_no_entry")])

    with pytest.raises(ValueError, match="non-entering visit"):
        read_visit_manifest(path)


def test_audit_rejects_visit_outside_effort_or_unusable_effort() -> None:
    effort = _effort(usable_observation="no")
    with pytest.raises(ValueError, match="unusable effort"):
        audit_field_contacts([effort], [_visit()])

    valid_effort = _effort()
    outside = _visit(visit_end_offset_s="601")
    with pytest.raises(ValueError, match="beyond effort duration"):
        audit_field_contacts([valid_effort], [outside])


def test_bombus_ardens_label_requires_confirmed_identification(tmp_path: Path) -> None:
    path = tmp_path / "visits.csv"
    _write(path, VISIT_COLUMNS, [_visit(visitor_group="bombus_ardens_confirmed", identification_confidence="group_level")])

    with pytest.raises(ValueError, match="requires confirmed identification"):
        read_visit_manifest(path)


def test_visit_effort_identity_mismatch_is_rejected() -> None:
    effort = _effort(site_id="OSH_01")
    visit = _visit(site_id="OSH_02")
    with pytest.raises(ValueError, match="does not match effort site_id"):
        audit_field_contacts([effort], [visit])
