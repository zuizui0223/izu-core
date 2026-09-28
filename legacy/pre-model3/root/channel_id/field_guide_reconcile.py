"""Reconcile first-party field guide reviews without public-photo labeling or pooling."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Sequence

from channel_id.guide_photo_review import (
    DRAFT_CONSTRAINT_COLUMNS,
    ELIGIBLE_COLUMNS,
    ISLAND_SUMMARY_COLUMNS,
    reconcile_reviews,
)

FIELD_SOURCE_NOTE = "Double-blind ordinal review; first-party field photo; one row per tagged field plant."
FIELD_BOUNDARY = (
    "Ordinal first-party field-photo review summary, not a random island-wide estimate. "
    "A directional model constraint requires manual inspection of source plants, site coverage, "
    "review notes, and independent biological confirmation."
)


def _require_field_source(rows: Sequence[dict[str, str]], label: str) -> None:
    types = {str(row.get("source_type", "")).strip() for row in rows}
    if types != {"field_photo"}:
        raise ValueError(f"{label} must contain only source_type=field_photo, got {sorted(types)!r}")


def reconcile_field_reviews(
    geographic_rows: Sequence[dict[str, str]],
    review_a_rows: Sequence[dict[str, str]],
    review_b_rows: Sequence[dict[str, str]],
    key_rows: Sequence[dict[str, str]],
    *,
    min_units_per_island: int = 3,
    maximum_reviewer_score_difference: int = 1,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    """Reconcile field-only review files and label output as field evidence."""
    _require_field_source(geographic_rows, "field geographic review")
    _require_field_source(key_rows, "field blind key")
    eligible, summaries, drafts = reconcile_reviews(
        geographic_rows,
        review_a_rows,
        review_b_rows,
        key_rows,
        min_units_per_island=min_units_per_island,
        maximum_reviewer_score_difference=maximum_reviewer_score_difference,
    )
    for row in eligible:
        row["source_note"] = FIELD_SOURCE_NOTE
    for row in summaries:
        row["source_boundary"] = FIELD_BOUNDARY
    for row in drafts:
        row["draft_id"] = row["draft_id"].replace("public_photo_ordinal_", "field_photo_ordinal_", 1)
        row["source_boundary"] = FIELD_BOUNDARY
    return eligible, summaries, drafts


def _write(path: Path, fields: Sequence[str], rows: Sequence[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_field_reconciliation(
    output_dir: Path,
    eligible: Sequence[dict[str, str]],
    summaries: Sequence[dict[str, str]],
    drafts: Sequence[dict[str, str]],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write(output_dir / "eligible_field_plant_units.csv", ELIGIBLE_COLUMNS, eligible)
    _write(output_dir / "field_island_ordinal_summary.csv", ISLAND_SUMMARY_COLUMNS, summaries)
    _write(output_dir / "field_guide_direction_constraint_drafts.csv", DRAFT_CONSTRAINT_COLUMNS, drafts)
    lines = [
        "# Field guide-photo review reconciliation",
        "",
        f"Eligible tagged field-plant units: {len(eligible)}",
        f"Island summaries: {len(summaries)}",
        f"Directional drafts requiring scientific confirmation: {len(drafts)}",
        "",
        "This output is field-photo evidence only. Do not concatenate these rows with public-photo reconciliation output or use either output to update model constraints automatically.",
    ]
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
