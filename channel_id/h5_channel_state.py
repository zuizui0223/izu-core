from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

REQUIRED_FIELDS = [
    "island_id",
    "site_id",
    "field_event_id",
    "channel_id",
    "survey_method",
    "survey_effort_hours",
    "independent_channel_detections",
    "detection_model_id",
    "estimated_detection_probability_if_present",
    "source_state",
    "source_evidence_id",
]

SOURCE_STATES = {"available", "structurally_absent", "unresolved"}
DISRUPTION_DETECTION_PROBABILITY = 0.95


@dataclass(frozen=True)
class ChannelStateAudit:
    rows: list[dict[str, str]]
    summary: dict[str, object]


def _float(value: str, label: str) -> float:
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(f"{label} must be numeric") from exc


def _int(value: str, label: str) -> int:
    numeric = _float(value, label)
    if not numeric.is_integer():
        raise ValueError(f"{label} must be integer-valued")
    return int(numeric)


def classify_channel_state(row: dict[str, str]) -> tuple[str, str]:
    source_state = row["source_state"].strip()
    if source_state not in SOURCE_STATES:
        raise ValueError(f"invalid source_state: {source_state}")
    if source_state in {"available", "structurally_absent"} and not row[
        "source_evidence_id"
    ].strip():
        raise ValueError("resolved source_state requires source_evidence_id")

    if source_state == "structurally_absent":
        return "structurally_absent", "source_channel_not_available"
    if source_state == "unresolved":
        return "unresolved", "source_state_unresolved"

    effort = _float(row["survey_effort_hours"].strip(), "survey_effort_hours")
    detections = _int(
        row["independent_channel_detections"].strip(),
        "independent_channel_detections",
    )
    detection_probability = _float(
        row["estimated_detection_probability_if_present"].strip(),
        "estimated_detection_probability_if_present",
    )
    if effort < 0:
        raise ValueError("survey_effort_hours must be non-negative")
    if detections < 0:
        raise ValueError("independent_channel_detections must be non-negative")
    if not 0 <= detection_probability <= 1:
        raise ValueError("estimated_detection_probability_if_present must be in [0, 1]")

    if detections > 0:
        if effort <= 0:
            raise ValueError("positive detections require positive survey effort")
        return "retained", "independent_detection"
    if effort <= 0:
        return "unresolved", "no_usable_survey_effort"
    if not row["detection_model_id"].strip():
        return "unresolved", "detection_model_missing"
    if detection_probability >= DISRUPTION_DETECTION_PROBABILITY:
        return "disrupted", "adequate_independent_non_detection"
    return "unresolved", "non_detection_below_detection_probability_gate"


def audit_channel_state_rows(rows: list[dict[str, str]]) -> ChannelStateAudit:
    output: list[dict[str, str]] = []
    seen: set[tuple[str, str, str, str]] = set()
    for row in rows:
        missing = [field for field in REQUIRED_FIELDS if field not in row]
        if missing:
            raise ValueError(f"channel-state row missing fields: {', '.join(missing)}")
        key = tuple(
            row[field].strip()
            for field in ("island_id", "site_id", "field_event_id", "channel_id")
        )
        if any(not value for value in key):
            raise ValueError("channel-state row contains blank unit key")
        if key in seen:
            raise ValueError("duplicate channel-state survey unit")
        seen.add(key)
        state, basis = classify_channel_state(row)
        out = dict(row)
        out["strict_H5_channel_state"] = state
        out["classification_basis"] = basis
        output.append(out)

    counts = {
        state: sum(row["strict_H5_channel_state"] == state for row in output)
        for state in ("retained", "disrupted", "structurally_absent", "unresolved")
    }
    summary: dict[str, object] = {
        "schema_version": "1.0",
        "detection_probability_gate": DISRUPTION_DETECTION_PROBABILITY,
        "n_units": len(output),
        "counts": counts,
        "retained_disrupted_contrast_present": bool(
            counts["retained"] > 0 and counts["disrupted"] > 0
        ),
        "claim_boundary": (
            "Contemporary channel state is independent occurrence/abundance evidence; "
            "it is not historical loss, effective service or floral selection."
        ),
    }
    return ChannelStateAudit(rows=output, summary=summary)


def audit_channel_state_file(path: Path) -> ChannelStateAudit:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("channel-state CSV has no header")
        missing = [field for field in REQUIRED_FIELDS if field not in reader.fieldnames]
        if missing:
            raise ValueError(f"channel-state CSV missing columns: {', '.join(missing)}")
        rows = [dict(row) for row in reader]
    return audit_channel_state_rows(rows)
