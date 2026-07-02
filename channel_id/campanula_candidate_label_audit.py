"""Audit public-photo discovery labels without treating labels as taxonomy decisions.

The focal floral-trait workflow needs to distinguish three things that are
normally easy to conflate:

* a focal query label used for ordinary candidate discovery;
* a broader taxon query used to find potentially mislabelled focal flowers;
* a historical label visible in source metadata.

This module turns those roles into a declared registry and audits the raw-photo
proxy queue at *source-record* level. It never resolves a synonymy, assigns a
record to the focal entity, or sends broad/historical-label hits into blinded
trait review automatically.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


VALID_LABEL_ROLES = frozenset({"focal_exact", "broader_aggregate", "historical_record_label"})
VALID_POLICIES = frozenset({
    "eligible_after_manual_taxon_review",
    "candidate_only_until_manual_focal_taxon_confirmation",
})

REGISTRY_COLUMNS = (
    "target_id",
    "query_label",
    "label_role",
    "blind_review_policy",
    "manual_focal_taxon_confirmation_required",
    "registry_basis",
    "notes",
)
RECORD_COLUMNS = (
    "source_type",
    "source_record_unit_id",
    "record_id",
    "discovery_target_ids",
    "query_labels",
    "label_roles",
    "blind_review_policy",
    "manual_focal_taxon_confirmation_required",
    "candidate_ids",
    "photo_urls",
    "observed_taxon_names",
    "observed_on_values",
    "latitude",
    "longitude",
    "positional_accuracy_m",
    "quality_grades",
    "observation_source_url",
    "nearest_declared_proxy",
    "nearest_proxy_distance_km",
    "second_nearest_declared_proxy",
    "second_nearest_proxy_distance_km",
    "nearest_proxy_gap_km",
    "review_route",
    "boundary",
)
SUMMARY_COLUMNS = (
    "target_id",
    "query_label",
    "label_role",
    "blind_review_policy",
    "raw_photo_candidates",
    "source_record_units",
    "source_record_units_nearest_hachijo_proxy",
    "overlap_with_other_registry_target_ids",
    "interpretation_boundary",
)


@dataclass(frozen=True)
class CandidateLabel:
    target_id: str
    query_label: str
    label_role: str
    blind_review_policy: str
    manual_focal_taxon_confirmation_required: bool
    registry_basis: str
    notes: str

    def __post_init__(self) -> None:
        if not self.target_id or not self.query_label:
            raise ValueError("candidate label requires target_id and query_label")
        if self.label_role not in VALID_LABEL_ROLES:
            raise ValueError(f"unknown label_role {self.label_role!r}")
        if self.blind_review_policy not in VALID_POLICIES:
            raise ValueError(f"unknown blind_review_policy {self.blind_review_policy!r}")
        if not self.manual_focal_taxon_confirmation_required:
            raise ValueError("all candidate labels must require manual focal-taxon confirmation")


def _text(row: dict[str, str], field: str) -> str:
    return str(row.get(field, "")).strip()


def _bool_yes(value: str, path: Path, line: int) -> bool:
    normalized = value.strip().casefold()
    if normalized == "yes":
        return True
    if normalized == "no":
        return False
    raise ValueError(f"{path}:{line}: manual_focal_taxon_confirmation_required must be yes or no")


def _require_columns(path: Path, fieldnames: Iterable[str], required: Iterable[str]) -> None:
    missing = set(required) - set(fieldnames)
    if missing:
        raise ValueError(f"{path}: missing columns: " + ", ".join(sorted(missing)))


def load_label_registry(path: Path) -> tuple[CandidateLabel, ...]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        _require_columns(path, tuple(reader.fieldnames or ()), REGISTRY_COLUMNS)
        rows: list[CandidateLabel] = []
        seen: set[str] = set()
        for line, raw in enumerate(reader, start=2):
            target_id = _text(raw, "target_id")
            if target_id in seen:
                raise ValueError(f"{path}:{line}: duplicate target_id {target_id!r}")
            seen.add(target_id)
            rows.append(CandidateLabel(
                target_id=target_id,
                query_label=_text(raw, "query_label"),
                label_role=_text(raw, "label_role"),
                blind_review_policy=_text(raw, "blind_review_policy"),
                manual_focal_taxon_confirmation_required=_bool_yes(_text(raw, "manual_focal_taxon_confirmation_required"), path, line),
                registry_basis=_text(raw, "registry_basis"),
                notes=_text(raw, "notes"),
            ))
    if not rows:
        raise ValueError(f"{path}: registry cannot be empty")
    if sum(row.label_role == "focal_exact" for row in rows) != 1:
        raise ValueError(f"{path}: registry must contain exactly one focal_exact row")
    return tuple(rows)


def load_snapshot_targets(path: Path) -> dict[str, str]:
    config = json.loads(path.read_text(encoding="utf-8"))
    targets = config.get("targets")
    if not isinstance(targets, list):
        raise ValueError(f"{path}: targets must be a list")
    result: dict[str, str] = {}
    for target in targets:
        if not isinstance(target, dict):
            raise ValueError(f"{path}: target is not an object")
        target_id = str(target.get("target_id") or "").strip()
        taxon_name = str(target.get("taxon_name") or "").strip()
        if not target_id or not taxon_name:
            raise ValueError(f"{path}: target needs target_id and taxon_name")
        if target_id in result:
            raise ValueError(f"{path}: duplicate target_id {target_id!r}")
        result[target_id] = taxon_name
    return result


def validate_registry_against_snapshot(registry: Sequence[CandidateLabel], snapshot_targets: dict[str, str]) -> None:
    for label in registry:
        configured = snapshot_targets.get(label.target_id)
        if configured is None:
            raise ValueError(f"registry target {label.target_id!r} is absent from snapshot config")
        if configured != label.query_label:
            raise ValueError(
                f"registry query_label {label.query_label!r} does not match snapshot taxon_name {configured!r} for {label.target_id!r}"
            )


def load_proxy_queue(path: Path) -> list[dict[str, str]]:
    required = {
        "candidate_id", "record_id", "target_id", "query_taxon_name", "observed_taxon_name",
        "photo_url", "observation_source_url", "nearest_declared_proxy", "nearest_proxy_distance_km",
        "second_nearest_declared_proxy", "second_nearest_proxy_distance_km", "nearest_proxy_gap_km",
    }
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        _require_columns(path, tuple(reader.fieldnames or ()), required)
        return list(reader)


def _source_type(row: dict[str, str]) -> str:
    return _text(row, "source_type") or "iNaturalist"


def _source_record_unit_id(source_type: str, record_id: str) -> str:
    slug = "".join(character if character.isalnum() else "_" for character in source_type.casefold()).strip("_") or "source"
    return f"{slug}_record:{record_id}"


def _unique_join(values: Iterable[str]) -> str:
    return ";".join(sorted({value for value in values if value}))


def _policy_for(labels: Sequence[CandidateLabel]) -> str:
    if any(row.label_role == "focal_exact" for row in labels):
        return "eligible_after_manual_taxon_review"
    return "candidate_only_until_manual_focal_taxon_confirmation"


def build_audit_rows(registry: Sequence[CandidateLabel], candidate_rows: Sequence[dict[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Return deduplicated source-record rows and per-search-label summary rows."""
    by_target = {row.target_id: row for row in registry}
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    raw_by_target: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in candidate_rows:
        target_id = _text(row, "target_id")
        if target_id not in by_target:
            continue
        record_id = _text(row, "record_id")
        if not record_id:
            continue
        source_type = _source_type(row)
        grouped[(source_type, record_id)].append(row)
        raw_by_target[target_id].append(row)

    records: list[dict[str, str]] = []
    record_targets: dict[tuple[str, str], set[str]] = {}
    for key, rows in grouped.items():
        record_targets[key] = {_text(row, "target_id") for row in rows}

    boundary = (
        "Query labels are public-record discovery routes, not taxonomic decisions. A broader or historical label remains candidate-only until an independent reviewer accepts focal taxon identity; source-record overlap across labels is deduplicated here."
    )
    for (source_type, record_id), rows in sorted(grouped.items()):
        target_ids = sorted(record_targets[(source_type, record_id)])
        labels = [by_target[target_id] for target_id in target_ids]
        first = rows[0]
        policy = _policy_for(labels)
        review_route = (
            "existing_focal_review_path_after_manual_taxon_confirmation"
            if policy == "eligible_after_manual_taxon_review"
            else "candidate_only_do_not_send_to_focal_blind_review_without_explicit_taxon_promotion"
        )
        records.append({
            "source_type": source_type,
            "source_record_unit_id": _source_record_unit_id(source_type, record_id),
            "record_id": record_id,
            "discovery_target_ids": ";".join(target_ids),
            "query_labels": _unique_join(label.query_label for label in labels),
            "label_roles": _unique_join(label.label_role for label in labels),
            "blind_review_policy": policy,
            "manual_focal_taxon_confirmation_required": "yes",
            "candidate_ids": _unique_join(_text(row, "candidate_id") for row in rows),
            "photo_urls": _unique_join(_text(row, "photo_url") for row in rows),
            "observed_taxon_names": _unique_join(_text(row, "observed_taxon_name") for row in rows),
            "observed_on_values": _unique_join(_text(row, "observed_on") for row in rows),
            "latitude": _text(first, "latitude"),
            "longitude": _text(first, "longitude"),
            "positional_accuracy_m": _text(first, "positional_accuracy_m"),
            "quality_grades": _unique_join(_text(row, "quality_grade") for row in rows),
            "observation_source_url": _text(first, "observation_source_url"),
            "nearest_declared_proxy": _text(first, "nearest_declared_proxy"),
            "nearest_proxy_distance_km": _text(first, "nearest_proxy_distance_km"),
            "second_nearest_declared_proxy": _text(first, "second_nearest_declared_proxy"),
            "second_nearest_proxy_distance_km": _text(first, "second_nearest_proxy_distance_km"),
            "nearest_proxy_gap_km": _text(first, "nearest_proxy_gap_km"),
            "review_route": review_route,
            "boundary": boundary,
        })

    summary: list[dict[str, str]] = []
    for label in registry:
        raw = raw_by_target.get(label.target_id, [])
        source_units = {
            (_source_type(row), _text(row, "record_id"))
            for row in raw
            if _text(row, "record_id")
        }
        hachijo_units = {
            (_source_type(row), _text(row, "record_id"))
            for row in raw
            if _text(row, "record_id") and _text(row, "nearest_declared_proxy") == "Hachijo"
        }
        overlaps: set[str] = set()
        for source_key in source_units:
            overlaps.update(target_id for target_id in record_targets.get(source_key, set()) if target_id != label.target_id)
        summary.append({
            "target_id": label.target_id,
            "query_label": label.query_label,
            "label_role": label.label_role,
            "blind_review_policy": label.blind_review_policy,
            "raw_photo_candidates": str(len(raw)),
            "source_record_units": str(len(source_units)),
            "source_record_units_nearest_hachijo_proxy": str(len(hachijo_units)),
            "overlap_with_other_registry_target_ids": ";".join(sorted(overlaps)),
            "interpretation_boundary": boundary,
        })
    return records, summary


def write_audit(output_records_csv: Path, output_summary_csv: Path, output_markdown: Path, records: Sequence[dict[str, str]], summary: Sequence[dict[str, str]]) -> None:
    for path in (output_records_csv, output_summary_csv, output_markdown):
        path.parent.mkdir(parents=True, exist_ok=True)
    with output_records_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=RECORD_COLUMNS)
        writer.writeheader()
        writer.writerows(records)
    with output_summary_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=SUMMARY_COLUMNS)
        writer.writeheader()
        writer.writerows(summary)
    lines = [
        "# Campanula candidate-label audit",
        "",
        "This audit tracks public-photo discovery labels separately from focal taxonomic acceptance. It does not resolve synonymy or promote a broader/historical-label record into the focal trait channel.",
        "",
        "## Query-label coverage",
        "",
        "| target | query label | role | photo rows | unique source records | Hachijo-proxy source records | review policy | overlaps |",
        "|---|---|---|---:|---:|---:|---|---|",
    ]
    for row in summary:
        lines.append(
            f"| {row['target_id']} | {row['query_label']} | {row['label_role']} | {row['raw_photo_candidates']} | "
            f"{row['source_record_units']} | {row['source_record_units_nearest_hachijo_proxy']} | "
            f"{row['blind_review_policy']} | {row['overlap_with_other_registry_target_ids'] or 'none'} |"
        )
    candidate_only = [row for row in records if row["blind_review_policy"] != "eligible_after_manual_taxon_review"]
    lines.extend([
        "",
        "## Routing rule",
        "",
        f"Deduplicated source-record units across all registered discovery labels: {len(records)}.",
        f"Candidate-only units requiring explicit focal-taxon promotion before any blinded trait review: {len(candidate_only)}.",
        "",
        "A zero Hachijo-proxy count under a given query label is a result of that named public-record query and proxy triage, not evidence of absence. A positive broader/historical label is only a lead until geography and focal taxon identity are manually accepted.",
    ])
    output_markdown.write_text("\n".join(lines) + "\n", encoding="utf-8")
