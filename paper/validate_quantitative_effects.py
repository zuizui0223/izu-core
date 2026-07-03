"""Validate numeric effect extraction before evidence is promoted to rank A.

The repository uses a two-table gate:

* ``primary_source_extraction_queue.csv`` declares each source, its current
  scope, and the exact information still needed from primary text.
* ``quantitative_effects.csv`` may contain a numeric effect only after the
  source is marked ``source_locked`` or ``numeric_extracted`` and every field
  necessary to audit the comparison and compute its uncertainty is present.

This validator deliberately accepts an empty effect table. Absence of recovered
numbers is an honest state; invented or incompletely sourced values are not.
"""
from __future__ import annotations

import csv
import math
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
SCREENING = HERE / "evidence_screening"
QUEUE = SCREENING / "primary_source_extraction_queue.csv"
SCHEMA = SCREENING / "quantitative_effects.schema.csv"
EFFECTS = SCREENING / "quantitative_effects.csv"

VALID_SOURCE_STATES = {"awaiting_full_text", "not_transcribed", "source_locked", "numeric_extracted"}
NUMERIC_READY_STATES = {"source_locked", "numeric_extracted"}
VALID_ROLES = {"primary_geographic", "pending_scope_check", "comparative_context"}
VALID_VARIANCE_TYPES = {"sd", "se", "variance", "ci95"}
YES = {"yes"}


def load(path: pathlib.Path) -> list[dict[str, str]]:
    if not path.exists():
        raise ValueError(f"MISSING required file: {path}")
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def header(path: pathlib.Path) -> list[str]:
    if not path.exists():
        raise ValueError(f"MISSING required file: {path}")
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        return next(reader, [])


def finite_number(value: str, field: str, effect_id: str, *, positive: bool = False, nonnegative: bool = False) -> float:
    try:
        numeric = float(value)
    except ValueError as error:
        raise ValueError(f"effect {effect_id}: {field} must be numeric, got {value!r}") from error
    if not math.isfinite(numeric):
        raise ValueError(f"effect {effect_id}: {field} must be finite")
    if positive and numeric <= 0:
        raise ValueError(f"effect {effect_id}: {field} must be > 0")
    if nonnegative and numeric < 0:
        raise ValueError(f"effect {effect_id}: {field} must be >= 0")
    return numeric


def validate(queue_path: pathlib.Path = QUEUE, schema_path: pathlib.Path = SCHEMA, effects_path: pathlib.Path = EFFECTS) -> dict[str, int]:
    schema_fields = header(schema_path)
    effect_fields = header(effects_path)
    if effect_fields != schema_fields:
        raise ValueError("quantitative_effects.csv header must exactly match quantitative_effects.schema.csv")

    queue = load(queue_path)
    if not queue:
        raise ValueError("primary_source_extraction_queue.csv is empty")
    queue_by_source = {row["source_id"]: row for row in queue}
    if len(queue_by_source) != len(queue):
        raise ValueError("duplicate source_id in primary_source_extraction_queue.csv")
    for source_id, row in queue_by_source.items():
        state = row.get("status", "")
        if state not in VALID_SOURCE_STATES:
            raise ValueError(f"source {source_id}: invalid status {state!r}")
        if not row.get("current_synthesis_role"):
            raise ValueError(f"source {source_id}: missing current_synthesis_role")

    effects = load(effects_path)
    effect_ids = [row["effect_id"] for row in effects]
    if any(not effect_id for effect_id in effect_ids):
        raise ValueError("quantitative_effects.csv contains blank effect_id")
    if len(effect_ids) != len(set(effect_ids)):
        raise ValueError("duplicate effect_id in quantitative_effects.csv")

    nonempty = {
        "effect_id", "source_id", "synthesis_role", "taxon_as_reported", "accepted_taxon_concept",
        "trait_id", "trait_definition", "comparison_id", "comparison_scope", "mainland_or_reference_unit",
        "island_or_focal_unit", "island_order", "variance_type", "effect_metric", "page_table_figure",
        "extraction_method", "unit_compatibility", "taxonomy_verified", "geography_verified",
        "wild_status_verified", "source_verification_status",
    }
    numeric_positive = {"mean_reference", "mean_focal", "n_reference", "n_focal"}
    numeric_nonnegative = {"variance_reference", "variance_focal", "effect_variance"}

    for row in effects:
        effect_id = row["effect_id"]
        missing = sorted(field for field in nonempty if not row.get(field, "").strip())
        if missing:
            raise ValueError(f"effect {effect_id}: missing required fields: {', '.join(missing)}")
        source_id = row["source_id"]
        if source_id not in queue_by_source:
            raise ValueError(f"effect {effect_id}: source_id {source_id!r} is absent from extraction queue")
        source_state = queue_by_source[source_id]["status"]
        if source_state not in NUMERIC_READY_STATES:
            raise ValueError(f"effect {effect_id}: source {source_id} is {source_state!r}; lock primary source before numeric extraction")
        if row["synthesis_role"] not in VALID_ROLES:
            raise ValueError(f"effect {effect_id}: invalid synthesis_role {row['synthesis_role']!r}")
        if row["variance_type"] not in VALID_VARIANCE_TYPES:
            raise ValueError(f"effect {effect_id}: invalid variance_type {row['variance_type']!r}")
        if row["source_verification_status"] != "source_locked":
            raise ValueError(f"effect {effect_id}: source_verification_status must be 'source_locked'")
        for boolean in ("taxonomy_verified", "geography_verified", "wild_status_verified"):
            if row[boolean] not in YES:
                raise ValueError(f"effect {effect_id}: {boolean} must be 'yes'")
        for field in numeric_positive:
            finite_number(row[field], field, effect_id, positive=True)
        for field in numeric_nonnegative:
            finite_number(row[field], field, effect_id, nonnegative=True)
        finite_number(row["effect_value"], "effect_value", effect_id)

    return {"sources": len(queue), "numeric_effects": len(effects)}


def main() -> None:
    try:
        summary = validate()
    except ValueError as error:
        sys.exit(str(error))
    print(f"OK: {summary['sources']} source-recovery records, {summary['numeric_effects']} source-locked numeric effects")


if __name__ == "__main__":
    main()
