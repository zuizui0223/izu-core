import csv
from pathlib import Path

import pytest

from channel_id.field_flower_geometry import (
    GEOMETRY_COLUMNS,
    read_field_geometry_manifest,
    summarize_field_geometry,
    write_field_geometry_summary,
)


def _row(**changes: str) -> dict[str, str]:
    row = {
        "field_event_id": "izu_20260704",
        "island_id": "Oshima",
        "site_id": "OSH_01",
        "plant_id": "P001",
        "flower_id": "F001",
        "measurement_id": "G001",
        "flower_stage": "open",
        "flower_orientation": "downward",
        "corolla_length_mm": "35",
        "corolla_mouth_diameter_mm": "18",
        "corolla_inner_depth_mm": "28",
        "measurement_method": "caliper",
        "photo_id": "IMG001",
        "measurement_date": "2026-07-04",
        "measurer_id": "observer_1",
        "notes": "",
    }
    row.update(changes)
    return row


def _write(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=GEOMETRY_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def test_geometry_summary_averages_flowers_within_tagged_plant_before_island_summary(tmp_path: Path) -> None:
    path = tmp_path / "geometry.csv"
    rows = [
        _row(),
        _row(flower_id="F002", measurement_id="G002", corolla_length_mm="37", corolla_mouth_diameter_mm="20", corolla_inner_depth_mm="30", photo_id="IMG002"),
        _row(plant_id="P002", flower_id="F001", measurement_id="G003", corolla_length_mm="41", corolla_mouth_diameter_mm="24", corolla_inner_depth_mm="34", photo_id="IMG003"),
    ]
    _write(path, rows)

    summary = summarize_field_geometry(read_field_geometry_manifest(path))

    assert len(summary.plant_rows) == 2
    first = next(row for row in summary.plant_rows if row["plant_id"] == "P001")
    assert first["measured_flowers"] == "2"
    assert float(first["mean_corolla_length_mm"]) == pytest.approx(36.0)
    island = summary.island_rows[0]
    # Island mean is average of plant means: (36 + 41) / 2, not all three flowers.
    assert island["plants"] == "2"
    assert float(island["mean_plant_corolla_length_mm"]) == pytest.approx(38.5)
    assert float(island["sd_plant_corolla_length_mm"]) == pytest.approx(2.5)

    out = tmp_path / "summary"
    write_field_geometry_summary(out, summary)
    assert (out / "field_geometry_plant_summary.csv").exists()
    assert (out / "field_geometry_island_summary.csv").exists()


def test_geometry_manifest_rejects_duplicate_tagged_flower(tmp_path: Path) -> None:
    path = tmp_path / "geometry.csv"
    _write(path, [_row(), _row(measurement_id="G002")])

    with pytest.raises(ValueError, match="duplicate final geometry"):
        read_field_geometry_manifest(path)


def test_geometry_manifest_rejects_invalid_value_and_island(tmp_path: Path) -> None:
    path = tmp_path / "geometry.csv"
    _write(path, [_row(corolla_length_mm="0")])
    with pytest.raises(ValueError, match="must be positive"):
        read_field_geometry_manifest(path)

    _write(path, [_row(island_id="NotAnIsland")])
    with pytest.raises(ValueError, match="invalid island_id"):
        read_field_geometry_manifest(path)
