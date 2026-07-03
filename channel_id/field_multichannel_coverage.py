"""Audit linkage and coverage across first-party field evidence channels.

The module joins the raw field guide-photo, flower-geometry, observation-effort,
and visitor-contact manifests by explicit field event, island, site, and tagged
plant identifiers. It reports missing channels as workflow gaps, never as
biological absences. In particular, a usable video window with no scored visit
is evidence of observation effort, not evidence that a visitor group is absent.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from channel_id.field_legitimate_contact import _effort_seconds


PLANT_COVERAGE_COLUMNS = (
    "field_event_id", "island_id", "site_id", "plant_id",
    "guide_photo_rows", "guide_inner_corolla_view_rows", "guide_capture_status",
    "geometry_flower_records", "geometry_status",
    "usable_plant_effort_windows", "plant_monitored_flower_hours",
    "scored_plant_visit_bouts", "confirmed_both_contact_bouts",
    "observation_status", "coverage_status", "next_required_action", "boundary",
)
SITE_COVERAGE_COLUMNS = (
    "field_event_id", "island_id", "site_id", "tagged_plants",
    "plants_with_inner_corolla_photo", "plants_with_geometry", "plants_with_usable_plant_effort",
    "usable_effort_windows", "monitored_flower_hours", "scored_visit_bouts",
    "confirmed_both_contact_bouts", "unlinked_usable_effort_windows", "site_coverage_status", "boundary",
)
ISLAND_COVERAGE_COLUMNS = (
    "field_event_id", "island_id", "sites", "tagged_plants",
    "plants_with_inner_corolla_photo", "plants_with_geometry", "plants_with_usable_plant_effort",
    "usable_effort_windows", "monitored_flower_hours", "scored_visit_bouts",
    "confirmed_both_contact_bouts", "coverage_status", "boundary",
)

BOUNDARY = (
    "Coverage describes recorded first-party field channels and identifier linkage. It does not quantify "
    "island trait prevalence, visitor absence, pollen transfer, reproductive success, adaptation, or causality."
)


@dataclass(frozen=True)
class FieldMultichannelCoverage:
    plant_rows: tuple[dict[str, str], ...]
    site_rows: tuple[dict[str, str], ...]
    island_rows: tuple[dict[str, str], ...]


def _text(row: dict[str, str], field: str) -> str:
    return str(row.get(field, "")).strip()


def _plant_key(row: dict[str, str]) -> tuple[str, str, str, str] | None:
    values = tuple(_text(row, field) for field in ("field_event_id", "island_id", "site_id", "plant_id"))
    if not values[-1]:
        return None
    if not all(values[:3]):
        raise ValueError("plant-linked row is missing event, island, or site")
    return values


def _site_key(row: dict[str, str]) -> tuple[str, str, str]:
    values = tuple(_text(row, field) for field in ("field_event_id", "island_id", "site_id"))
    if not all(values):
        raise ValueError("row is missing event, island, or site")
    return values


def _flower_hours(effort: dict[str, str]) -> float:
    return _effort_seconds(effort) / 3600.0 * float(_text(effort, "monitored_open_flower_count"))


def _status(guide_inner: int, geometry: int, effort: int, visits: int) -> tuple[str, str]:
    if guide_inner == 0:
        return "missing_guide_inner_corolla_photo", "capture_standardized_inner_corolla_photo"
    if geometry == 0:
        return "missing_flower_geometry", "measure_open_flower_geometry"
    if effort == 0:
        return "missing_usable_plant_effort", "record_usable_video_or_direct_observation_window"
    if visits == 0:
        return "linked_multichannel_unit_no_scored_visit", "retain_zero_visit_effort_and_add_comparable_observation_windows"
    return "linked_multichannel_unit_with_scored_visit", "retain_linkage_and_add_reproductive_outcome_when_feasible"


def build_field_multichannel_coverage(
    guide_rows: Sequence[dict[str, str]],
    geometry_rows: Sequence[dict[str, str]],
    effort_rows: Sequence[dict[str, str]],
    visit_rows: Sequence[dict[str, str]],
) -> FieldMultichannelCoverage:
    """Build field plant, site, and island coverage tables from validated raw manifests.

    The caller should use the existing manifest readers before calling this
    function. Observation effort with a blank plant ID is retained in site and
    island summaries but is intentionally not assigned to a tagged plant.
    """
    plants: set[tuple[str, str, str, str]] = set()
    guide = defaultdict(lambda: {"rows": 0, "inner": 0})
    geometry = defaultdict(int)
    effort = defaultdict(lambda: {"windows": 0, "flower_hours": 0.0})
    visits = defaultdict(lambda: {"bouts": 0, "both": 0})
    site_effort = defaultdict(lambda: {"windows": 0, "flower_hours": 0.0, "unlinked": 0})
    site_visits = defaultdict(lambda: {"bouts": 0, "both": 0})

    for row in guide_rows:
        key = _plant_key(row)
        if key is None:
            continue
        plants.add(key)
        guide[key]["rows"] += 1
        if _text(row, "inner_corolla_view_field").casefold() == "yes":
            guide[key]["inner"] += 1
    for row in geometry_rows:
        key = _plant_key(row)
        if key is None:
            continue
        plants.add(key)
        geometry[key] += 1
    for row in effort_rows:
        if _text(row, "usable_observation").casefold() != "yes":
            continue
        site = _site_key(row)
        flower_hours = _flower_hours(row)
        site_effort[site]["windows"] += 1
        site_effort[site]["flower_hours"] += flower_hours
        key = _plant_key(row)
        if key is None:
            site_effort[site]["unlinked"] += 1
            continue
        plants.add(key)
        effort[key]["windows"] += 1
        effort[key]["flower_hours"] += flower_hours
    for row in visit_rows:
        site = _site_key(row)
        site_visits[site]["bouts"] += 1
        if _text(row, "anther_contact") == "confirmed" and _text(row, "stigma_contact") == "confirmed":
            site_visits[site]["both"] += 1
        key = _plant_key(row)
        if key is None:
            continue
        plants.add(key)
        visits[key]["bouts"] += 1
        if _text(row, "anther_contact") == "confirmed" and _text(row, "stigma_contact") == "confirmed":
            visits[key]["both"] += 1

    plant_rows: list[dict[str, str]] = []
    for event, island, site, plant in sorted(plants):
        key = (event, island, site, plant)
        coverage_status, next_action = _status(
            guide[key]["inner"], geometry[key], effort[key]["windows"], visits[key]["bouts"]
        )
        plant_rows.append({
            "field_event_id": event,
            "island_id": island,
            "site_id": site,
            "plant_id": plant,
            "guide_photo_rows": str(guide[key]["rows"]),
            "guide_inner_corolla_view_rows": str(guide[key]["inner"]),
            "guide_capture_status": "inner_view_recorded" if guide[key]["inner"] else ("photo_without_inner_view" if guide[key]["rows"] else "no_guide_photo"),
            "geometry_flower_records": str(geometry[key]),
            "geometry_status": "geometry_recorded" if geometry[key] else "no_geometry_record",
            "usable_plant_effort_windows": str(effort[key]["windows"]),
            "plant_monitored_flower_hours": f"{effort[key]['flower_hours']:.8f}",
            "scored_plant_visit_bouts": str(visits[key]["bouts"]),
            "confirmed_both_contact_bouts": str(visits[key]["both"]),
            "observation_status": "usable_effort_with_scored_visit" if visits[key]["bouts"] else ("usable_effort_no_scored_visit" if effort[key]["windows"] else "no_usable_plant_effort"),
            "coverage_status": coverage_status,
            "next_required_action": next_action,
            "boundary": BOUNDARY,
        })

    site_plants = defaultdict(list)
    for row in plant_rows:
        site_plants[(row["field_event_id"], row["island_id"], row["site_id"])].append(row)
    site_keys = sorted(set(site_plants) | set(site_effort) | set(site_visits))
    site_rows: list[dict[str, str]] = []
    for event, island, site in site_keys:
        rows = site_plants[(event, island, site)]
        raw_effort = site_effort[(event, island, site)]
        raw_visits = site_visits[(event, island, site)]
        if not rows:
            status = "effort_without_tagged_plant_linkage" if raw_effort["windows"] else "no_tagged_plant_or_usable_effort"
        elif any(row["coverage_status"].startswith("missing_") for row in rows):
            status = "tagged_plant_channel_gap"
        else:
            status = "tagged_plant_multichannel_coverage_present"
        site_rows.append({
            "field_event_id": event,
            "island_id": island,
            "site_id": site,
            "tagged_plants": str(len(rows)),
            "plants_with_inner_corolla_photo": str(sum(row["guide_inner_corolla_view_rows"] != "0" for row in rows)),
            "plants_with_geometry": str(sum(row["geometry_flower_records"] != "0" for row in rows)),
            "plants_with_usable_plant_effort": str(sum(row["usable_plant_effort_windows"] != "0" for row in rows)),
            "usable_effort_windows": str(raw_effort["windows"]),
            "monitored_flower_hours": f"{raw_effort['flower_hours']:.8f}",
            "scored_visit_bouts": str(raw_visits["bouts"]),
            "confirmed_both_contact_bouts": str(raw_visits["both"]),
            "unlinked_usable_effort_windows": str(raw_effort["unlinked"]),
            "site_coverage_status": status,
            "boundary": BOUNDARY,
        })

    island_sites = defaultdict(list)
    for row in site_rows:
        island_sites[(row["field_event_id"], row["island_id"])].append(row)
    island_rows: list[dict[str, str]] = []
    for (event, island), rows in sorted(island_sites.items()):
        plants = sum(int(row["tagged_plants"]) for row in rows)
        field_hours = sum(float(row["monitored_flower_hours"]) for row in rows)
        if plants == 0:
            status = "no_tagged_plant_coverage"
        elif any(row["site_coverage_status"] == "tagged_plant_channel_gap" for row in rows):
            status = "tagged_plant_channel_gap"
        else:
            status = "multichannel_plant_coverage_present"
        island_rows.append({
            "field_event_id": event,
            "island_id": island,
            "sites": str(len(rows)),
            "tagged_plants": str(plants),
            "plants_with_inner_corolla_photo": str(sum(int(row["plants_with_inner_corolla_photo"]) for row in rows)),
            "plants_with_geometry": str(sum(int(row["plants_with_geometry"]) for row in rows)),
            "plants_with_usable_plant_effort": str(sum(int(row["plants_with_usable_plant_effort"]) for row in rows)),
            "usable_effort_windows": str(sum(int(row["usable_effort_windows"]) for row in rows)),
            "monitored_flower_hours": f"{field_hours:.8f}",
            "scored_visit_bouts": str(sum(int(row["scored_visit_bouts"]) for row in rows)),
            "confirmed_both_contact_bouts": str(sum(int(row["confirmed_both_contact_bouts"]) for row in rows)),
            "coverage_status": status,
            "boundary": BOUNDARY,
        })
    return FieldMultichannelCoverage(tuple(plant_rows), tuple(site_rows), tuple(island_rows))


def _write(path: Path, columns: Sequence[str], rows: Sequence[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def write_field_multichannel_coverage(output_dir: Path, coverage: FieldMultichannelCoverage) -> None:
    """Write plant, site, and island workflow-coverage tables."""
    output_dir.mkdir(parents=True, exist_ok=True)
    _write(output_dir / "field_multichannel_plant_coverage.csv", PLANT_COVERAGE_COLUMNS, coverage.plant_rows)
    _write(output_dir / "field_multichannel_site_coverage.csv", SITE_COVERAGE_COLUMNS, coverage.site_rows)
    _write(output_dir / "field_multichannel_island_coverage.csv", ISLAND_COVERAGE_COLUMNS, coverage.island_rows)
    lines = [
        "# Field multichannel coverage audit",
        "",
        f"Tagged plant rows: {len(coverage.plant_rows)}",
        f"Site rows: {len(coverage.site_rows)}",
        f"Island rows: {len(coverage.island_rows)}",
        "",
        "A channel gap is a collection or linkage task, not a biological result. A zero-visit usable effort window remains observational information and is never converted to visitor absence.",
    ]
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
