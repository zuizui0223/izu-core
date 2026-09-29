"""Validate and summarize first-party flower geometry by plant before island summaries.

Multiple flowers can be measured on a tagged plant, but flowers are not treated
as independent plants. Island-level summaries therefore use plant means and
report site and plant coverage explicitly. These are descriptive field data,
not common-garden estimates or evidence of adaptation by themselves.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, pstdev
from typing import Iterable, Sequence

from channel_id.guide_photo_review import VALID_ISLANDS

GEOMETRY_COLUMNS = (
    "field_event_id", "island_id", "site_id", "plant_id", "flower_id", "measurement_id",
    "flower_stage", "flower_orientation", "corolla_length_mm", "corolla_mouth_diameter_mm",
    "corolla_inner_depth_mm", "measurement_method", "photo_id", "measurement_date",
    "measurer_id", "notes",
)
PLANT_SUMMARY_COLUMNS = (
    "field_event_id", "island_id", "site_id", "plant_id", "measured_flowers",
    "mean_corolla_length_mm", "mean_corolla_mouth_diameter_mm", "mean_corolla_inner_depth_mm",
    "measurement_methods", "photo_ids", "boundary",
)
ISLAND_SUMMARY_COLUMNS = (
    "field_event_id", "island_id", "sites", "plants", "mean_plant_corolla_length_mm",
    "sd_plant_corolla_length_mm", "mean_plant_corolla_mouth_diameter_mm",
    "sd_plant_corolla_mouth_diameter_mm", "mean_plant_corolla_inner_depth_mm",
    "sd_plant_corolla_inner_depth_mm", "boundary",
)

FLOWER_STAGES = frozenset({"early_open", "open", "late_open"})
FLOWER_ORIENTATIONS = frozenset({"upward", "horizontal", "downward", "unknown"})
MEASUREMENT_METHODS = frozenset({"caliper", "ruler_photo", "calibrated_photo"})

BOUNDARY = (
    "Descriptive first-party field geometry summarized by tagged plant. It is not a common-garden "
    "estimate, a random island-wide sample, or evidence of adaptation without linked ecological and reproductive data."
)


@dataclass(frozen=True)
class FieldGeometrySummary:
    plant_rows: tuple[dict[str, str], ...]
    island_rows: tuple[dict[str, str], ...]


def _text(row: dict[str, str], field: str) -> str:
    return str(row.get(field, "")).strip()


def _require_columns(fieldnames: Iterable[str]) -> None:
    missing = set(GEOMETRY_COLUMNS) - set(fieldnames)
    if missing:
        raise ValueError("field geometry manifest missing columns: " + ", ".join(sorted(missing)))


def _positive(row: dict[str, str], field: str, measurement_id: str) -> float:
    try:
        value = float(_text(row, field))
    except ValueError as error:
        raise ValueError(f"{field} must be numeric for measurement_id={measurement_id!r}") from error
    if value <= 0.0:
        raise ValueError(f"{field} must be positive for measurement_id={measurement_id!r}")
    return value


def _choice(row: dict[str, str], field: str, allowed: frozenset[str], measurement_id: str) -> None:
    value = _text(row, field)
    if value not in allowed:
        raise ValueError(f"invalid {field} for measurement_id={measurement_id!r}: {value!r}")


def read_field_geometry_manifest(path: Path) -> tuple[dict[str, str], ...]:
    """Read one final geometry measurement per tagged flower."""
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        _require_columns(reader.fieldnames or ())
        rows = tuple(reader)
    seen_measurements: set[str] = set()
    seen_flowers: set[tuple[str, str, str, str, str]] = set()
    for row in rows:
        measurement_id = _text(row, "measurement_id")
        if not measurement_id:
            raise ValueError("blank measurement_id")
        if measurement_id in seen_measurements:
            raise ValueError(f"duplicate measurement_id {measurement_id!r}")
        seen_measurements.add(measurement_id)
        for field in (
            "field_event_id", "island_id", "site_id", "plant_id", "flower_id", "flower_stage",
            "flower_orientation", "measurement_method", "measurement_date", "measurer_id",
        ):
            if not _text(row, field):
                raise ValueError(f"blank {field} for measurement_id={measurement_id!r}")
        if _text(row, "island_id") not in VALID_ISLANDS:
            raise ValueError(f"invalid island_id for measurement_id={measurement_id!r}")
        _choice(row, "flower_stage", FLOWER_STAGES, measurement_id)
        _choice(row, "flower_orientation", FLOWER_ORIENTATIONS, measurement_id)
        _choice(row, "measurement_method", MEASUREMENT_METHODS, measurement_id)
        for field in ("corolla_length_mm", "corolla_mouth_diameter_mm", "corolla_inner_depth_mm"):
            _positive(row, field, measurement_id)
        flower_key = tuple(_text(row, field) for field in ("field_event_id", "island_id", "site_id", "plant_id", "flower_id"))
        if flower_key in seen_flowers:
            raise ValueError("duplicate final geometry record for tagged flower: " + "/".join(flower_key))
        seen_flowers.add(flower_key)
    return rows


def _join_unique(rows: Sequence[dict[str, str]], field: str) -> str:
    values: list[str] = []
    seen: set[str] = set()
    for row in rows:
        value = _text(row, field)
        if value and value not in seen:
            seen.add(value)
            values.append(value)
    return ";".join(values)


def _format_mean(values: Sequence[float]) -> str:
    return f"{mean(values):.8f}"


def _format_sd(values: Sequence[float]) -> str:
    return "" if len(values) < 2 else f"{pstdev(values):.8f}"


def summarize_field_geometry(rows: Sequence[dict[str, str]]) -> FieldGeometrySummary:
    """Produce plant-first and island-second descriptive geometry summaries."""
    by_plant: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_plant[tuple(_text(row, field) for field in ("field_event_id", "island_id", "site_id", "plant_id"))].append(row)
    plant_rows: list[dict[str, str]] = []
    plant_numeric: dict[tuple[str, str], list[dict[str, float | str]]] = defaultdict(list)
    for (event, island, site, plant), flower_rows in sorted(by_plant.items()):
        lengths = [_positive(row, "corolla_length_mm", _text(row, "measurement_id")) for row in flower_rows]
        mouths = [_positive(row, "corolla_mouth_diameter_mm", _text(row, "measurement_id")) for row in flower_rows]
        depths = [_positive(row, "corolla_inner_depth_mm", _text(row, "measurement_id")) for row in flower_rows]
        plant_rows.append({
            "field_event_id": event,
            "island_id": island,
            "site_id": site,
            "plant_id": plant,
            "measured_flowers": str(len(flower_rows)),
            "mean_corolla_length_mm": _format_mean(lengths),
            "mean_corolla_mouth_diameter_mm": _format_mean(mouths),
            "mean_corolla_inner_depth_mm": _format_mean(depths),
            "measurement_methods": _join_unique(flower_rows, "measurement_method"),
            "photo_ids": _join_unique(flower_rows, "photo_id"),
            "boundary": BOUNDARY,
        })
        plant_numeric[(event, island)].append({
            "site": site,
            "length": mean(lengths),
            "mouth": mean(mouths),
            "depth": mean(depths),
        })
    island_rows: list[dict[str, str]] = []
    for (event, island), values in sorted(plant_numeric.items()):
        lengths = [float(row["length"]) for row in values]
        mouths = [float(row["mouth"]) for row in values]
        depths = [float(row["depth"]) for row in values]
        island_rows.append({
            "field_event_id": event,
            "island_id": island,
            "sites": str(len({str(row["site"]) for row in values})),
            "plants": str(len(values)),
            "mean_plant_corolla_length_mm": _format_mean(lengths),
            "sd_plant_corolla_length_mm": _format_sd(lengths),
            "mean_plant_corolla_mouth_diameter_mm": _format_mean(mouths),
            "sd_plant_corolla_mouth_diameter_mm": _format_sd(mouths),
            "mean_plant_corolla_inner_depth_mm": _format_mean(depths),
            "sd_plant_corolla_inner_depth_mm": _format_sd(depths),
            "boundary": BOUNDARY,
        })
    return FieldGeometrySummary(tuple(plant_rows), tuple(island_rows))


def _write(path: Path, fields: Sequence[str], rows: Sequence[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_field_geometry_summary(output_dir: Path, summary: FieldGeometrySummary) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write(output_dir / "field_geometry_plant_summary.csv", PLANT_SUMMARY_COLUMNS, summary.plant_rows)
    _write(output_dir / "field_geometry_island_summary.csv", ISLAND_SUMMARY_COLUMNS, summary.island_rows)
    lines = [
        "# Field flower geometry summary",
        "",
        f"Tagged plant summaries: {len(summary.plant_rows)}",
        f"Island-event summaries: {len(summary.island_rows)}",
        "",
        "Several flowers from one tagged plant are averaged before island summaries. The resulting field comparison remains descriptive and must not be presented as a common-garden or causal estimate.",
    ]
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
