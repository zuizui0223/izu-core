"""Prospective proboscis-length measurement admission for Issue #91.

This module mirrors the source-native Hiraiwa & Ushimaru trait hierarchy without
inventing historical Table-S2 values.  One row is one measured visitor specimen.
A taxon x site mean is promoted to ``measured_new`` only when the measurement
method is source-matched (digital caliper, mm) and either five independent
specimens are measured or the field record explicitly states that all available
specimens at that taxon x site were measured when fewer than five existed.
"""
from __future__ import annotations

import csv
import math
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean, stdev
from typing import Iterable, Mapping, Sequence

from channel_id.guide_photo_review import VALID_ISLANDS

MEASUREMENT_COLUMNS = (
    "measurement_id",
    "specimen_id",
    "visitor_taxon_id",
    "source_taxon_name",
    "field_event_id",
    "island_id",
    "site_id",
    "proboscis_length_mm",
    "measurement_method",
    "instrument_resolution_mm",
    "measurer_id",
    "measured_at",
    "all_available_at_site",
    "voucher_id",
    "notes",
)
ALL_AVAILABLE_STATES = frozenset({"yes", "no", "unknown"})
MEASUREMENT_METHODS = frozenset({"digital_caliper", "other_prespecified"})
SOURCE_MATCHED_METHOD = "digital_caliper"
SOURCE_TARGET_N = 5


def _text(row: Mapping[str, object], field: str) -> str:
    return str(row.get(field, "") or "").strip()


def _require_columns(fieldnames: Iterable[str], required: Sequence[str], label: str) -> None:
    missing = set(required) - set(fieldnames)
    if missing:
        raise ValueError(f"{label} missing columns: " + ", ".join(sorted(missing)))


def _positive_float(row: Mapping[str, object], field: str, label: str) -> float:
    try:
        value = float(_text(row, field))
    except ValueError as exc:
        raise ValueError(f"{field} must be numeric for {label}") from exc
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{field} must be finite and positive for {label}")
    return value


def _parse_time(value: str, *, label: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"measured_at must be ISO-8601 for {label}") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"measured_at requires timezone offset for {label}")
    return parsed


def read_proboscis_measurements(path: Path) -> tuple[dict[str, str], ...]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        _require_columns(reader.fieldnames or (), MEASUREMENT_COLUMNS, "proboscis measurement file")
        rows = tuple(reader)

    measurement_ids: set[str] = set()
    specimen_ids: set[str] = set()
    for row in rows:
        measurement_id = _text(row, "measurement_id")
        specimen_id = _text(row, "specimen_id")
        label = f"measurement_id={measurement_id!r}"
        for field in (
            "measurement_id", "specimen_id", "visitor_taxon_id", "source_taxon_name",
            "field_event_id", "island_id", "site_id", "proboscis_length_mm",
            "measurement_method", "instrument_resolution_mm", "measurer_id", "measured_at",
            "all_available_at_site",
        ):
            if not _text(row, field):
                raise ValueError(f"blank {field} for {label}")
        if measurement_id in measurement_ids:
            raise ValueError(f"duplicate measurement_id {measurement_id!r}")
        if specimen_id in specimen_ids:
            raise ValueError(f"duplicate specimen_id {specimen_id!r}")
        measurement_ids.add(measurement_id)
        specimen_ids.add(specimen_id)
        if _text(row, "island_id") not in VALID_ISLANDS:
            raise ValueError(f"invalid island_id for {label}")
        if _text(row, "measurement_method") not in MEASUREMENT_METHODS:
            raise ValueError(f"invalid measurement_method for {label}")
        if _text(row, "all_available_at_site") not in ALL_AVAILABLE_STATES:
            raise ValueError(f"invalid all_available_at_site for {label}")
        _positive_float(row, "proboscis_length_mm", label)
        _positive_float(row, "instrument_resolution_mm", label)
        _parse_time(_text(row, "measured_at"), label=label)
    return rows


def summarize_proboscis_measurements(
    rows: Sequence[Mapping[str, object]],
    *,
    target_n: int = SOURCE_TARGET_N,
) -> tuple[tuple[dict[str, object], ...], tuple[dict[str, str], ...]]:
    if target_n <= 0:
        raise ValueError("target_n must be positive")
    groups: dict[tuple[str, str], list[Mapping[str, object]]] = defaultdict(list)
    for row in rows:
        groups[(_text(row, "visitor_taxon_id"), _text(row, "site_id"))].append(row)

    summaries: list[dict[str, object]] = []
    lookup_rows: list[dict[str, str]] = []
    for (taxon_id, site_id), subset in sorted(groups.items()):
        source_names = {_text(row, "source_taxon_name") for row in subset}
        methods = {_text(row, "measurement_method") for row in subset}
        availability = {_text(row, "all_available_at_site") for row in subset}
        islands = {_text(row, "island_id") for row in subset}
        if len(source_names) != 1:
            raise ValueError(f"inconsistent source_taxon_name for {taxon_id} x {site_id}")
        if len(availability) != 1:
            raise ValueError(f"inconsistent all_available_at_site for {taxon_id} x {site_id}")
        if len(islands) != 1:
            raise ValueError(f"inconsistent island_id for {taxon_id} x {site_id}")

        values = [float(_text(row, "proboscis_length_mm")) for row in subset]
        n = len({ _text(row, "specimen_id") for row in subset })
        all_available = next(iter(availability))
        source_matched = methods == {SOURCE_MATCHED_METHOD}
        sample_complete = n >= target_n or (n < target_n and all_available == "yes")
        ready = source_matched and sample_complete
        if not source_matched:
            state = "blocked_non_source_matched_method"
        elif not sample_complete:
            state = "blocked_incomplete_specimen_sample"
        elif n < target_n:
            state = "ready_all_available_below_target"
        else:
            state = "ready_target_reached"

        summary = {
            "visitor_taxon_id": taxon_id,
            "source_taxon_name": next(iter(source_names)),
            "island_id": next(iter(islands)),
            "site_id": site_id,
            "measurement_n": n,
            "mean_proboscis_length_mm": mean(values),
            "sd_proboscis_length_mm": stdev(values) if len(values) >= 2 else None,
            "measurement_methods": "|".join(sorted(methods)),
            "all_available_at_site": all_available,
            "source_target_n": target_n,
            "admission_state": state,
            "trait_lookup_ready": ready,
        }
        summaries.append(summary)

        if ready:
            lookup_rows.append({
                "visitor_taxon_id": taxon_id,
                "source_taxon_name": next(iter(source_names)),
                "site_id": site_id,
                "proboscis_length_mm": f"{mean(values):.12g}",
                "measurement_n": str(n),
                "measurement_source": "Issue #91 prospective source-matched specimen measurements",
                "source_locator": f"field_proboscis_measurement:{site_id}:{taxon_id}",
                "trait_status": "measured_new",
                "source_bundle_sha256": "",
                "notes": (
                    "digital-caliper site mean; source target n reached"
                    if n >= target_n
                    else "digital-caliper site mean; all available specimens measured below source target n"
                ),
            })
    return tuple(summaries), tuple(lookup_rows)
