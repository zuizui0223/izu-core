"""Audit first-party flower-visitor observations at the contact level.

A detection or a visit is not treated as pollination.  This module keeps
observation effort separate from scored visit bouts and reports only a
*potential legitimate-contact proxy*: confirmed anther and stigma contact in
the same scorable visit.  It never infers pollen deposition, seed set, or
pollinator effectiveness.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Sequence

from channel_id.guide_photo_review import VALID_ISLANDS

EFFORT_COLUMNS = (
    "field_event_id", "island_id", "site_id", "effort_id", "plant_id", "flower_id",
    "start_time", "end_time", "monitored_open_flower_count", "method", "video_id",
    "recording_status", "usable_observation", "observer_id", "notes",
)
VISIT_COLUMNS = (
    "visit_id", "field_event_id", "island_id", "site_id", "effort_id", "plant_id",
    "flower_id", "source_video_id", "visit_start_offset_s", "visit_end_offset_s",
    "individual_track_id", "detection_source", "visitor_group", "body_size_class",
    "identification_confidence", "corolla_entry", "anther_contact", "stigma_contact",
    "contact_visibility", "contact_evidence", "scorer_id", "scored_at", "notes",
)
VISIT_LEDGER_COLUMNS = (
    *VISIT_COLUMNS,
    "effort_duration_s", "monitored_flower_hours", "contact_proxy_status", "boundary",
)
RATE_SUMMARY_COLUMNS = (
    "island_id", "visitor_group", "body_size_class", "usable_effort_windows",
    "monitored_flower_hours", "visit_bouts", "corolla_entry_bouts", "scorable_contact_bouts",
    "confirmed_anther_contact_bouts", "confirmed_stigma_contact_bouts",
    "confirmed_both_contact_bouts", "unscorable_contact_bouts", "visit_bouts_per_flower_hour",
    "confirmed_both_per_flower_hour", "confirmed_both_fraction_of_scorable_bouts", "boundary",
)

VISITOR_GROUPS = frozenset({
    "bombus_ardens_confirmed", "bombus_large_other", "bombus_small", "small_bee_non_bombus",
    "other_hymenopteran", "non_bee_insect", "unknown_visitor",
})
BODY_SIZE_CLASSES = frozenset({"large", "small", "unknown"})
IDENTIFICATION_CONFIDENCE = frozenset({"confirmed", "group_level", "uncertain"})
COROLLA_ENTRY = frozenset({"entered", "landed_no_entry", "approached_no_landing", "unknown"})
CONTACT_STATE = frozenset({"confirmed", "not_seen", "not_confirmable"})
CONTACT_VISIBILITY = frozenset({"clear", "partial", "obscured"})
CONTACT_EVIDENCE = frozenset({"video_direct", "live_direct", "still_image", "unknown"})
RECORDING_STATUS = frozenset({"complete", "partial", "failed"})
YES_NO = frozenset({"yes", "no"})

BOUNDARY = (
    "Confirmed both-contact is a handling proxy only. It does not establish pollen deposition, "
    "pollen-tube growth, fruit/seed production, pollinator effectiveness, or evolutionary causality."
)


@dataclass(frozen=True)
class FieldContactAudit:
    visit_ledger_rows: tuple[dict[str, str], ...]
    rate_summary_rows: tuple[dict[str, str], ...]


def _text(row: dict[str, str], field: str) -> str:
    return str(row.get(field, "")).strip()


def _require_columns(fieldnames: Iterable[str], required: Sequence[str], label: str) -> None:
    missing = set(required) - set(fieldnames)
    if missing:
        raise ValueError(f"{label} missing columns: " + ", ".join(sorted(missing)))


def _choice(row: dict[str, str], field: str, choices: frozenset[str], label: str) -> None:
    value = _text(row, field)
    if value not in choices:
        raise ValueError(f"invalid {field} for {label}={_text(row, label)!r}: {value!r}")


def _parse_time(value: str, *, field: str, label: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as error:
        raise ValueError(f"invalid {field} for {label}: {value!r}") from error
    if parsed.tzinfo is None:
        raise ValueError(f"{field} requires an ISO-8601 timezone offset for {label}")
    return parsed


def _positive_float(row: dict[str, str], field: str, label: str, *, allow_zero: bool = False) -> float:
    try:
        value = float(_text(row, field))
    except ValueError as error:
        raise ValueError(f"{field} must be numeric for {label}") from error
    if value < 0.0 or (not allow_zero and value <= 0.0):
        bound = "non-negative" if allow_zero else "positive"
        raise ValueError(f"{field} must be {bound} for {label}")
    return value


def read_effort_manifest(path: Path) -> tuple[dict[str, str], ...]:
    """Read and validate time-bounded observation effort windows."""
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        _require_columns(reader.fieldnames or (), EFFORT_COLUMNS, "effort manifest")
        rows = tuple(reader)
    seen: set[str] = set()
    for row in rows:
        effort_id = _text(row, "effort_id")
        if not effort_id:
            raise ValueError("blank effort_id")
        if effort_id in seen:
            raise ValueError(f"duplicate effort_id {effort_id!r}")
        seen.add(effort_id)
        for field in ("field_event_id", "island_id", "site_id", "start_time", "end_time", "method", "recording_status", "usable_observation"):
            if not _text(row, field):
                raise ValueError(f"blank {field} for effort_id={effort_id!r}")
        if _text(row, "island_id") not in VALID_ISLANDS:
            raise ValueError(f"invalid island_id for effort_id={effort_id!r}")
        _choice(row, "recording_status", RECORDING_STATUS, "effort_id")
        _choice(row, "usable_observation", YES_NO, "effort_id")
        start = _parse_time(_text(row, "start_time"), field="start_time", label=f"effort_id={effort_id!r}")
        end = _parse_time(_text(row, "end_time"), field="end_time", label=f"effort_id={effort_id!r}")
        if end <= start:
            raise ValueError(f"end_time must be after start_time for effort_id={effort_id!r}")
        _positive_float(row, "monitored_open_flower_count", f"effort_id={effort_id!r}")
        if _text(row, "usable_observation") == "yes" and _text(row, "recording_status") == "failed":
            raise ValueError(f"failed effort cannot be usable for effort_id={effort_id!r}")
    return rows


def read_visit_manifest(path: Path) -> tuple[dict[str, str], ...]:
    """Read manual bout-level contact scores; rows are not individual video frames."""
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        _require_columns(reader.fieldnames or (), VISIT_COLUMNS, "visit manifest")
        rows = tuple(reader)
    seen: set[str] = set()
    for row in rows:
        visit_id = _text(row, "visit_id")
        if not visit_id:
            raise ValueError("blank visit_id")
        if visit_id in seen:
            raise ValueError(f"duplicate visit_id {visit_id!r}")
        seen.add(visit_id)
        for field in (
            "field_event_id", "island_id", "site_id", "effort_id", "visit_start_offset_s",
            "visit_end_offset_s", "detection_source", "visitor_group", "body_size_class",
            "identification_confidence", "corolla_entry", "anther_contact", "stigma_contact",
            "contact_visibility", "contact_evidence", "scorer_id", "scored_at",
        ):
            if not _text(row, field):
                raise ValueError(f"blank {field} for visit_id={visit_id!r}")
        if _text(row, "island_id") not in VALID_ISLANDS:
            raise ValueError(f"invalid island_id for visit_id={visit_id!r}")
        _choice(row, "visitor_group", VISITOR_GROUPS, "visit_id")
        _choice(row, "body_size_class", BODY_SIZE_CLASSES, "visit_id")
        _choice(row, "identification_confidence", IDENTIFICATION_CONFIDENCE, "visit_id")
        _choice(row, "corolla_entry", COROLLA_ENTRY, "visit_id")
        _choice(row, "anther_contact", CONTACT_STATE, "visit_id")
        _choice(row, "stigma_contact", CONTACT_STATE, "visit_id")
        _choice(row, "contact_visibility", CONTACT_VISIBILITY, "visit_id")
        _choice(row, "contact_evidence", CONTACT_EVIDENCE, "visit_id")
        start = _positive_float(row, "visit_start_offset_s", f"visit_id={visit_id!r}", allow_zero=True)
        end = _positive_float(row, "visit_end_offset_s", f"visit_id={visit_id!r}", allow_zero=True)
        if end < start:
            raise ValueError(f"visit_end_offset_s must be at or after visit_start_offset_s for visit_id={visit_id!r}")
        _parse_time(_text(row, "scored_at"), field="scored_at", label=f"visit_id={visit_id!r}")
        if _text(row, "corolla_entry") != "entered" and (
            _text(row, "anther_contact") == "confirmed" or _text(row, "stigma_contact") == "confirmed"
        ):
            raise ValueError(f"non-entering visit cannot have confirmed floral contact for visit_id={visit_id!r}")
        if _text(row, "visitor_group") == "bombus_ardens_confirmed" and _text(row, "identification_confidence") != "confirmed":
            raise ValueError(f"confirmed B. ardens label requires confirmed identification for visit_id={visit_id!r}")
    return rows


def _contact_proxy_status(row: dict[str, str]) -> str:
    anther = _text(row, "anther_contact")
    stigma = _text(row, "stigma_contact")
    if anther == "confirmed" and stigma == "confirmed":
        return "confirmed_both_contact"
    if anther == "confirmed" or stigma == "confirmed":
        return "confirmed_partial_contact"
    if anther == "not_seen" and stigma == "not_seen":
        return "no_confirmed_contact"
    return "unscorable_contact"


def _effort_seconds(row: dict[str, str]) -> float:
    start = _parse_time(_text(row, "start_time"), field="start_time", label=f"effort_id={_text(row, 'effort_id')!r}")
    end = _parse_time(_text(row, "end_time"), field="end_time", label=f"effort_id={_text(row, 'effort_id')!r}")
    return (end - start).total_seconds()


def audit_field_contacts(
    effort_rows: Sequence[dict[str, str]],
    visit_rows: Sequence[dict[str, str]],
) -> FieldContactAudit:
    """Join visits to usable effort and calculate descriptive contact-rate summaries."""
    efforts = {row["effort_id"].strip(): row for row in effort_rows}
    ledger: list[dict[str, str]] = []
    for visit in visit_rows:
        visit_id = _text(visit, "visit_id")
        effort = efforts.get(_text(visit, "effort_id"))
        if effort is None:
            raise ValueError(f"visit_id={visit_id!r} references unknown effort_id={_text(visit, 'effort_id')!r}")
        if _text(effort, "usable_observation") != "yes":
            raise ValueError(f"visit_id={visit_id!r} references unusable effort")
        for field in ("field_event_id", "island_id", "site_id"):
            if _text(visit, field) != _text(effort, field):
                raise ValueError(f"visit_id={visit_id!r} does not match effort {field}")
        for field in ("plant_id", "flower_id"):
            effort_value = _text(effort, field)
            visit_value = _text(visit, field)
            if effort_value and visit_value and effort_value != visit_value:
                raise ValueError(f"visit_id={visit_id!r} does not match effort {field}")
        if _text(effort, "video_id") and _text(visit, "source_video_id") and _text(effort, "video_id") != _text(visit, "source_video_id"):
            raise ValueError(f"visit_id={visit_id!r} does not match effort video_id")
        duration_s = _effort_seconds(effort)
        start = _positive_float(visit, "visit_start_offset_s", f"visit_id={visit_id!r}", allow_zero=True)
        end = _positive_float(visit, "visit_end_offset_s", f"visit_id={visit_id!r}", allow_zero=True)
        if end > duration_s + 1e-9:
            raise ValueError(f"visit_id={visit_id!r} extends beyond effort duration")
        flower_hours = duration_s / 3600.0 * _positive_float(effort, "monitored_open_flower_count", f"effort_id={_text(effort, 'effort_id')!r}")
        ledger.append({
            **{field: _text(visit, field) for field in VISIT_COLUMNS},
            "effort_duration_s": f"{duration_s:.6f}",
            "monitored_flower_hours": f"{flower_hours:.8f}",
            "contact_proxy_status": _contact_proxy_status(visit),
            "boundary": BOUNDARY,
        })
    usable_efforts = [row for row in effort_rows if _text(row, "usable_observation") == "yes"]
    # Exposure must include zero-visit effort; group-specific rows inherit island-wide exposure by design.
    island_exposure: dict[str, dict[str, float]] = defaultdict(lambda: {"windows": 0.0, "flower_hours": 0.0})
    for effort in usable_efforts:
        island = _text(effort, "island_id")
        island_exposure[island]["windows"] += 1.0
        island_exposure[island]["flower_hours"] += _effort_seconds(effort) / 3600.0 * _positive_float(effort, "monitored_open_flower_count", f"effort_id={_text(effort, 'effort_id')!r}")
    group_counts: dict[tuple[str, str, str], dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for row in ledger:
        key = (_text(row, "island_id"), _text(row, "visitor_group"), _text(row, "body_size_class"))
        counts = group_counts[key]
        counts["visit"] += 1.0
        if _text(row, "corolla_entry") == "entered":
            counts["entry"] += 1.0
        status = _text(row, "contact_proxy_status")
        if status != "unscorable_contact":
            counts["scorable"] += 1.0
        else:
            counts["unscorable"] += 1.0
        if _text(row, "anther_contact") == "confirmed":
            counts["anther"] += 1.0
        if _text(row, "stigma_contact") == "confirmed":
            counts["stigma"] += 1.0
        if status == "confirmed_both_contact":
            counts["both"] += 1.0
    summaries: list[dict[str, str]] = []
    for (island, group, size), counts in sorted(group_counts.items()):
        exposure = island_exposure[island]
        flower_hours = exposure["flower_hours"]
        scorable = counts["scorable"]
        both_fraction = counts["both"] / scorable if scorable else 0.0
        summaries.append({
            "island_id": island,
            "visitor_group": group,
            "body_size_class": size,
            "usable_effort_windows": str(int(exposure["windows"])),
            "monitored_flower_hours": f"{flower_hours:.8f}",
            "visit_bouts": str(int(counts["visit"])),
            "corolla_entry_bouts": str(int(counts["entry"])),
            "scorable_contact_bouts": str(int(scorable)),
            "confirmed_anther_contact_bouts": str(int(counts["anther"])),
            "confirmed_stigma_contact_bouts": str(int(counts["stigma"])),
            "confirmed_both_contact_bouts": str(int(counts["both"])),
            "unscorable_contact_bouts": str(int(counts["unscorable"])),
            "visit_bouts_per_flower_hour": f"{counts['visit'] / flower_hours:.8f}" if flower_hours else "",
            "confirmed_both_per_flower_hour": f"{counts['both'] / flower_hours:.8f}" if flower_hours else "",
            "confirmed_both_fraction_of_scorable_bouts": f"{both_fraction:.8f}" if scorable else "",
            "boundary": BOUNDARY,
        })
    return FieldContactAudit(tuple(ledger), tuple(summaries))


def _write(path: Path, fields: Sequence[str], rows: Sequence[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_field_contact_audit(output_dir: Path, audit: FieldContactAudit) -> None:
    """Write traceable visit-level and descriptive rate outputs."""
    output_dir.mkdir(parents=True, exist_ok=True)
    _write(output_dir / "field_contact_visit_ledger.csv", VISIT_LEDGER_COLUMNS, audit.visit_ledger_rows)
    _write(output_dir / "field_contact_rate_summary.csv", RATE_SUMMARY_COLUMNS, audit.rate_summary_rows)
    lines = [
        "# Field visitor-contact audit",
        "",
        f"Validated visit bouts: {len(audit.visit_ledger_rows)}",
        f"Island × visitor-group × body-size rows: {len(audit.rate_summary_rows)}",
        "",
        "Visit rates use total usable island-level monitored flower-hours as the denominator, including windows with zero visits. A confirmed both-contact row is a visual handling proxy, not evidence of actual pollen transfer or fitness.",
    ]
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
