import csv
from pathlib import Path

import pytest

from channel_id.proboscis_measurement import (
    MEASUREMENT_COLUMNS,
    read_proboscis_measurements,
    summarize_proboscis_measurements,
)
from channel_id.proboscis_trait_recovery import validate_trait_lookup


def _row(i: int, *, method: str = "digital_caliper", all_available: str = "no", length: float | None = None):
    return {
        "measurement_id": f"m{i}",
        "specimen_id": f"sp{i}",
        "visitor_taxon_id": "Bombus_ardens_ardens",
        "source_taxon_name": "Bombus ardens ardens",
        "field_event_id": "evt1",
        "island_id": "Oshima",
        "site_id": "site1",
        "proboscis_length_mm": str(length if length is not None else 4 + i),
        "measurement_method": method,
        "instrument_resolution_mm": "0.01",
        "measurer_id": "observer1",
        "measured_at": "2026-08-22T10:00:00+09:00",
        "all_available_at_site": all_available,
        "voucher_id": f"v{i}",
        "notes": "",
    }


def _write(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=MEASUREMENT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def test_five_source_matched_specimens_are_promoted_to_measured_new(tmp_path: Path) -> None:
    rows = [_row(i, length=value) for i, value in enumerate([5, 6, 7, 8, 9], start=1)]
    path = tmp_path / "measurements.csv"
    _write(path, rows)
    parsed = read_proboscis_measurements(path)
    summaries, lookup = summarize_proboscis_measurements(parsed)
    assert summaries[0]["admission_state"] == "ready_target_reached"
    assert summaries[0]["measurement_n"] == 5
    assert summaries[0]["mean_proboscis_length_mm"] == pytest.approx(7.0)
    assert lookup[0]["trait_status"] == "measured_new"
    assert lookup[0]["measurement_n"] == "5"

    lookup_path = tmp_path / "lookup.csv"
    with lookup_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=lookup[0].keys())
        writer.writeheader()
        writer.writerows(lookup)
    counts = validate_trait_lookup(lookup_path)
    assert counts["measured_new"] == 1


def test_all_available_below_five_can_be_admitted_explicitly() -> None:
    rows = [_row(i, all_available="yes") for i in range(1, 4)]
    summaries, lookup = summarize_proboscis_measurements(rows)
    assert summaries[0]["admission_state"] == "ready_all_available_below_target"
    assert summaries[0]["trait_lookup_ready"] is True
    assert len(lookup) == 1


def test_incomplete_sample_is_not_promoted() -> None:
    rows = [_row(i, all_available="no") for i in range(1, 4)]
    summaries, lookup = summarize_proboscis_measurements(rows)
    assert summaries[0]["admission_state"] == "blocked_incomplete_specimen_sample"
    assert summaries[0]["trait_lookup_ready"] is False
    assert lookup == ()


def test_non_source_matched_method_is_not_promoted() -> None:
    rows = [_row(i, method="other_prespecified") for i in range(1, 6)]
    summaries, lookup = summarize_proboscis_measurements(rows)
    assert summaries[0]["admission_state"] == "blocked_non_source_matched_method"
    assert lookup == ()


def test_duplicate_specimen_is_rejected(tmp_path: Path) -> None:
    rows = [_row(1), _row(2)]
    rows[1]["specimen_id"] = rows[0]["specimen_id"]
    path = tmp_path / "measurements.csv"
    _write(path, rows)
    with pytest.raises(ValueError, match="duplicate specimen_id"):
        read_proboscis_measurements(path)


def test_measurement_time_requires_timezone(tmp_path: Path) -> None:
    row = _row(1)
    row["measured_at"] = "2026-08-22T10:00:00"
    path = tmp_path / "measurements.csv"
    _write(path, [row])
    with pytest.raises(ValueError, match="timezone"):
        read_proboscis_measurements(path)
