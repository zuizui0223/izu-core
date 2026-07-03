"""Screen candidate flowering-plant taxa for an Izu comparative programme.

This is a feasibility and evidence-map tool, *not* a meta-analysis engine.
A taxon is only an independent mainland--Izu contrast after its taxonomy,
mainland reference, multiple-island coverage, and shared measurable channels
have each been documented. Discovery candidates remain visible, but cannot be
silently promoted to comparative replicates.
"""

from __future__ import annotations

import csv
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


TAXON_SCREEN_COLUMNS = (
    "taxon_id", "scientific_name", "common_name_ja", "comparison_role",
    "taxonomy_status", "mainland_reference_status", "izu_coverage_status",
    "known_izu_islands_or_scope", "phenology_window", "shared_channel_status",
    "pollination_evidence_status", "source_status", "screen_outcome",
    "next_required_action", "source_citation_or_record", "notes", "boundary",
)
SUMMARY_COLUMNS = ("dimension", "value", "taxa", "boundary")

COMPARISON_ROLES = frozenset({
    "focal_mainland_to_island", "izu_only_within_archipelago", "prospective_mainland_to_island",
})
TAXONOMY_STATUS = frozenset({"reviewed_project_scope", "needs_taxonomic_audit", "unreviewed_discovery"})
MAINLAND_STATUS = frozenset({"documented_known_data", "documented_external_source", "not_applicable_izu_endemic", "unverified"})
IZU_COVERAGE_STATUS = frozenset({"documented_source_scope", "documented_multiple_islands", "unverified"})
CHANNEL_STATUS = frozenset({"ready_existing_protocol", "feasible_later_phenology", "needs_field_reconnaissance"})
POLLINATION_STATUS = frozenset({"structured_known_data", "literature_lead_only", "none_verified"})
SOURCE_STATUS = frozenset({"locked_source", "partial_source", "discovery_only"})
SCREEN_OUTCOMES = frozenset({"core_focal_ready", "auxiliary_after_distribution_audit", "discovery_only"})

BOUNDARY = (
    "The screen reports candidate evidence readiness, not occurrence prevalence, pollinator absence, "
    "effectiveness, repeated evolutionary transitions, or meta-analytic effect sizes. A discovery taxon is "
    "not evidence that it occurs on a focal island or forms an independent comparative replicate."
)


@dataclass(frozen=True)
class IzuComparativeTaxonScreen:
    rows: tuple[dict[str, str], ...]
    summary_rows: tuple[dict[str, str], ...]
    independent_mainland_to_island_ready: int
    meta_analysis_status: str


def _text(row: dict[str, str], field: str) -> str:
    return str(row.get(field, "")).strip()


def _require_columns(fieldnames: Iterable[str]) -> None:
    missing = set(TAXON_SCREEN_COLUMNS) - set(fieldnames)
    if missing:
        raise ValueError("taxon screen missing columns: " + ", ".join(sorted(missing)))


def _choice(row: dict[str, str], field: str, allowed: frozenset[str], taxon_id: str) -> None:
    value = _text(row, field)
    if value not in allowed:
        raise ValueError(f"invalid {field} for taxon_id={taxon_id!r}: {value!r}")


def _validate_logic(row: dict[str, str]) -> None:
    taxon_id = _text(row, "taxon_id")
    role = _text(row, "comparison_role")
    outcome = _text(row, "screen_outcome")
    mainland = _text(row, "mainland_reference_status")
    izu = _text(row, "izu_coverage_status")
    taxonomy = _text(row, "taxonomy_status")
    channels = _text(row, "shared_channel_status")
    pollination = _text(row, "pollination_evidence_status")
    source = _text(row, "source_status")
    if role == "izu_only_within_archipelago" and mainland != "not_applicable_izu_endemic":
        raise ValueError(f"{taxon_id}: Izu-only role requires not_applicable_izu_endemic mainland status")
    if role != "izu_only_within_archipelago" and mainland == "not_applicable_izu_endemic":
        raise ValueError(f"{taxon_id}: mainland-to-island role cannot be Izu endemic")
    if outcome == "core_focal_ready":
        required = {
            "comparison_role": "focal_mainland_to_island",
            "taxonomy_status": "reviewed_project_scope",
            "mainland_reference_status": "documented_known_data",
            "izu_coverage_status": "documented_source_scope",
            "shared_channel_status": "ready_existing_protocol",
            "pollination_evidence_status": "structured_known_data",
            "source_status": "locked_source",
        }
        for field, expected in required.items():
            if _text(row, field) != expected:
                raise ValueError(f"{taxon_id}: core_focal_ready requires {field}={expected!r}")
    if outcome == "auxiliary_after_distribution_audit":
        if role != "izu_only_within_archipelago":
            raise ValueError(f"{taxon_id}: auxiliary outcome is reserved for Izu-only taxa")
        if izu != "unverified":
            raise ValueError(f"{taxon_id}: auxiliary pre-audit status must retain unverified island coverage")
        if source == "locked_source":
            raise ValueError(f"{taxon_id}: auxiliary pre-audit taxon cannot claim locked source status")
    if outcome == "discovery_only":
        if source != "discovery_only" or taxonomy != "unreviewed_discovery":
            raise ValueError(f"{taxon_id}: discovery-only requires discovery source and unreviewed taxonomy")
        if mainland != "unverified" or izu != "unverified":
            raise ValueError(f"{taxon_id}: discovery-only cannot claim mainland or Izu coverage")
        if channels != "needs_field_reconnaissance" or pollination != "none_verified":
            raise ValueError(f"{taxon_id}: discovery-only cannot claim field or pollination readiness")


def read_izu_comparative_taxon_screen(path: Path) -> tuple[dict[str, str], ...]:
    """Read the candidate map and reject unsupported promotion to a replicate."""
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        _require_columns(reader.fieldnames or ())
        rows = tuple(reader)
    if not rows:
        raise ValueError("taxon screen has no rows")
    seen: set[str] = set()
    core_count = 0
    for row in rows:
        taxon_id = _text(row, "taxon_id")
        if not taxon_id:
            raise ValueError("blank taxon_id")
        if taxon_id in seen:
            raise ValueError(f"duplicate taxon_id {taxon_id!r}")
        seen.add(taxon_id)
        for field in ("scientific_name", "common_name_ja", "known_izu_islands_or_scope", "phenology_window", "next_required_action", "source_citation_or_record", "boundary"):
            if not _text(row, field):
                raise ValueError(f"blank {field} for taxon_id={taxon_id!r}")
        _choice(row, "comparison_role", COMPARISON_ROLES, taxon_id)
        _choice(row, "taxonomy_status", TAXONOMY_STATUS, taxon_id)
        _choice(row, "mainland_reference_status", MAINLAND_STATUS, taxon_id)
        _choice(row, "izu_coverage_status", IZU_COVERAGE_STATUS, taxon_id)
        _choice(row, "shared_channel_status", CHANNEL_STATUS, taxon_id)
        _choice(row, "pollination_evidence_status", POLLINATION_STATUS, taxon_id)
        _choice(row, "source_status", SOURCE_STATUS, taxon_id)
        _choice(row, "screen_outcome", SCREEN_OUTCOMES, taxon_id)
        _validate_logic(row)
        if _text(row, "screen_outcome") == "core_focal_ready":
            core_count += 1
    if core_count != 1:
        raise ValueError("the pre-field Izu screen must identify exactly one core focal taxon")
    return rows


def build_izu_comparative_taxon_screen(rows: Sequence[dict[str, str]]) -> IzuComparativeTaxonScreen:
    """Summarize readiness and make the non-meta-analysis stopping rule explicit."""
    counts = Counter(_text(row, "screen_outcome") for row in rows)
    roles = Counter(_text(row, "comparison_role") for row in rows)
    ready = sum(
        _text(row, "comparison_role") == "focal_mainland_to_island"
        and _text(row, "taxonomy_status") == "reviewed_project_scope"
        and _text(row, "mainland_reference_status") in {"documented_known_data", "documented_external_source"}
        and _text(row, "izu_coverage_status") in {"documented_source_scope", "documented_multiple_islands"}
        and _text(row, "shared_channel_status") == "ready_existing_protocol"
        for row in rows
    )
    meta_status = (
        "not_ready_requires_at_least_three_independent_ready_mainland_to_island_lineages"
        if ready < 3 else "screen_only_requires_effect_size_and_phylogenetic_design_review"
    )
    summary_rows: list[dict[str, str]] = []
    for outcome, count in sorted(counts.items()):
        summary_rows.append({"dimension": "screen_outcome", "value": outcome, "taxa": str(count), "boundary": BOUNDARY})
    for role, count in sorted(roles.items()):
        summary_rows.append({"dimension": "comparison_role", "value": role, "taxa": str(count), "boundary": BOUNDARY})
    summary_rows.append({
        "dimension": "independent_mainland_to_island_ready",
        "value": meta_status,
        "taxa": str(ready),
        "boundary": BOUNDARY,
    })
    return IzuComparativeTaxonScreen(tuple(rows), tuple(summary_rows), ready, meta_status)


def _write(path: Path, fields: Sequence[str], rows: Sequence[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_izu_comparative_taxon_screen(output_dir: Path, screen: IzuComparativeTaxonScreen) -> None:
    """Write the candidate map summary and a human-readable next-action report."""
    output_dir.mkdir(parents=True, exist_ok=True)
    _write(output_dir / "izu_comparative_taxon_screen_summary.csv", SUMMARY_COLUMNS, screen.summary_rows)
    lines = [
        "# Izu comparative taxon screen", "",
        f"Candidate taxa: {len(screen.rows)}", 
        f"Independent mainland-to-Izu lineages ready for a shared field pilot: {screen.independent_mainland_to_island_ready}",
        f"Meta-analysis status: `{screen.meta_analysis_status}`", "",
        "## Candidate map", "",
        "| taxon | role | screen outcome | mainland reference | Izu coverage | shared field channels | next action |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in screen.rows:
        lines.append(
            f"| {row['scientific_name']} ({row['common_name_ja']}) | {row['comparison_role']} | {row['screen_outcome']} | "
            f"{row['mainland_reference_status']} | {row['izu_coverage_status']} | {row['shared_channel_status']} | "
            f"{row['next_required_action']} |"
        )
    lines.extend((
        "", "## Interpretation boundary", "", BOUNDARY, "",
        "A formal meta-analysis is not started by this screen. It requires multiple genuinely independent ready lineages, comparable effect sizes, site replication, direct observation channels, and a model that addresses lineage/phylogenetic and shared-island dependence.",
    ))
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
