"""Build strict Issue #91 FDQ exposure units from linked field visitor records.

This is intentionally separate from visitor-group SVD/effective-service analysis.
Group-level visitor identities remain usable for service summaries, but Izu-compatible
FDQ is withheld unless every scored visit in an exposure unit has a confirmed taxon
identity and every positive-abundance taxon has an admitted numeric proboscis trait.
Usable zero-visit effort is retained explicitly rather than disappearing from the
exposure table.
"""
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

from channel_id.effective_pollinator_dependency import read_dependency_plant_registry
from channel_id.fdq_exposure import abundance_weighted_rao_q
from channel_id.field_legitimate_contact import (
    audit_field_contacts,
    read_effort_manifest,
    read_visit_manifest,
)
from channel_id.proboscis_trait_recovery import validate_trait_lookup

TRAIT_COLUMNS = (
    "visitor_taxon_id",
    "source_taxon_name",
    "site_id",
    "proboscis_length_mm",
    "measurement_n",
    "measurement_source",
    "source_locator",
    "trait_status",
    "source_bundle_sha256",
    "notes",
)
REQUIRED_FDQ_VISIT_COLUMNS = ("visitor_taxon_id",)


@dataclass(frozen=True)
class FieldFDQAudit:
    exposure_rows: tuple[dict[str, str], ...]
    summary: Mapping[str, object]


def _text(row: Mapping[str, object], field: str) -> str:
    return str(row.get(field, "") or "").strip()


def _read_raw_csv(path: Path) -> tuple[list[str], tuple[dict[str, str], ...]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or ()), tuple(reader)


def read_trait_lookup(path: Path) -> dict[tuple[str, str], dict[str, str]]:
    """Read exact target taxon × site trait rows after generic lookup validation."""
    validate_trait_lookup(path)
    fields, rows = _read_raw_csv(path)
    missing = set(TRAIT_COLUMNS) - set(fields)
    if missing:
        raise ValueError("trait lookup missing columns: " + ", ".join(sorted(missing)))
    lookup: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        taxon = _text(row, "visitor_taxon_id")
        site = _text(row, "site_id")
        if not taxon or not site:
            raise ValueError("trait lookup requires visitor_taxon_id and site_id on every row")
        key = (taxon, site)
        if key in lookup:
            raise ValueError(f"duplicate trait lookup key {key!r}")
        lookup[key] = row
    return lookup


def _plant_population_map(plants: Sequence[dict[str, str]]) -> dict[str, tuple[str, str, str, str]]:
    mapping: dict[str, tuple[str, str, str, str]] = {}
    for row in plants:
        plant_id = _text(row, "plant_id")
        mapping[plant_id] = (
            _text(row, "population_id"),
            _text(row, "field_event_id"),
            _text(row, "island_id"),
            _text(row, "site_id"),
        )
    return mapping


def _population_key_for_linked_row(
    row: Mapping[str, object],
    *,
    row_label: str,
    plant_map: Mapping[str, tuple[str, str, str, str]],
) -> tuple[str, str, str, str]:
    plant_id = _text(row, "plant_id")
    if not plant_id:
        raise ValueError(f"FDQ {row_label} requires plant_id linkage")
    population_key = plant_map.get(plant_id)
    if population_key is None:
        raise ValueError(f"FDQ {row_label} references plant_id={plant_id!r} outside dependency plant registry")
    row_key = (_text(row, "field_event_id"), _text(row, "island_id"), _text(row, "site_id"))
    if row_key != population_key[1:]:
        raise ValueError(f"FDQ {row_label} field_event/island/site does not match plant registry")
    return population_key


def audit_field_fdq(
    plant_rows: Sequence[dict[str, str]],
    effort_rows: Sequence[dict[str, str]],
    visit_rows: Sequence[dict[str, str]],
    trait_lookup: Mapping[tuple[str, str], Mapping[str, str]],
) -> FieldFDQAudit:
    """Aggregate confirmed taxon identities and calculate strict Rao-Q by population-event-site.

    Every usable effort unit is represented, including units with zero scored visits.
    All visit bouts linked to usable effort contribute to the exposure denominator. A
    group-level/uncertain visit is not silently discarded: it increases the unresolved
    count and blocks official FDQ for that exposure unit. Similarly, a confirmed taxon
    lacking an admitted site-specific numeric trait blocks FDQ.
    """
    audit_field_contacts(effort_rows, visit_rows)
    plant_map = _plant_population_map(plant_rows)

    grouped: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    # Seed the table from usable effort so zero-visit windows remain visible.
    for effort in effort_rows:
        if _text(effort, "usable_observation") != "yes":
            continue
        key = _population_key_for_linked_row(
            effort,
            row_label=f"effort_id={_text(effort, 'effort_id')!r}",
            plant_map=plant_map,
        )
        grouped[key]  # create empty exposure unit if no visit is scored

    for visit in visit_rows:
        key = _population_key_for_linked_row(
            visit,
            row_label=f"visit_id={_text(visit, 'visit_id')!r}",
            plant_map=plant_map,
        )
        grouped[key].append(visit)

    exposure_rows: list[dict[str, str]] = []
    ready_units = 0
    zero_visit_units = 0
    for (population_id, field_event_id, island_id, site_id), rows in sorted(grouped.items()):
        total_visits = len(rows)
        resolved_counts: Counter[str] = Counter()
        unresolved_visit_ids: list[str] = []
        unresolved_groups: Counter[str] = Counter()
        for row in rows:
            taxon = _text(row, "visitor_taxon_id")
            confidence = _text(row, "identification_confidence")
            if confidence == "confirmed" and taxon:
                resolved_counts[taxon] += 1
            else:
                unresolved_visit_ids.append(_text(row, "visit_id"))
                unresolved_groups[_text(row, "visitor_group")] += 1

        resolved_visits = sum(resolved_counts.values())
        trait_values: dict[str, float] = {}
        missing_trait_taxa: list[str] = []
        trait_covered_visits = 0
        for taxon, count in sorted(resolved_counts.items()):
            trait_row = trait_lookup.get((taxon, site_id))
            status = _text(trait_row or {}, "trait_status")
            value = _text(trait_row or {}, "proboscis_length_mm")
            if status in {"source_exact_site", "source_transfer_prespecified", "measured_new"} and value:
                trait_values[taxon] = float(value)
                trait_covered_visits += count
            else:
                missing_trait_taxa.append(taxon)

        if total_visits == 0:
            taxon_resolution_fraction = ""
            trait_coverage_fraction = ""
            fdq_status = "withheld_no_visit_bouts"
            fdq_value = ""
            zero_visit_units += 1
        else:
            taxon_resolution_fraction = f"{resolved_visits / total_visits:.12g}"
            trait_coverage_fraction = f"{trait_covered_visits / total_visits:.12g}"
            strict_ready = not unresolved_visit_ids and not missing_trait_taxa
            fdq_value = ""
            if strict_ready:
                result = abundance_weighted_rao_q(resolved_counts, trait_values)
                fdq_value = f"{result.fdq:.12g}"
                ready_units += 1
            fdq_status = "ready" if strict_ready else "withheld_incomplete_taxon_or_trait_coverage"

        exposure_rows.append(
            {
                "population_id": population_id,
                "field_event_id": field_event_id,
                "island_id": island_id,
                "site_id": site_id,
                "total_visit_bouts": str(total_visits),
                "taxon_resolved_visit_bouts": str(resolved_visits),
                "trait_covered_visit_bouts": str(trait_covered_visits),
                "taxon_resolution_fraction": taxon_resolution_fraction,
                "trait_coverage_fraction": trait_coverage_fraction,
                "resolved_taxa": "|".join(sorted(resolved_counts)),
                "missing_trait_taxa": "|".join(missing_trait_taxa),
                "unresolved_visitor_groups": "|".join(sorted(unresolved_groups)),
                "unresolved_visit_ids": "|".join(sorted(unresolved_visit_ids)),
                "fdq": fdq_value,
                "fdq_status": fdq_status,
                "boundary": (
                    "Usable zero-visit effort remains explicit. For positive-abundance units, FDQ is reported only "
                    "when taxon identity and site-specific numeric proboscis trait coverage are complete; missing "
                    "visits/taxa are not dropped and remaining abundances are not renormalized."
                ),
            }
        )

    summary = {
        "exposure_units": len(exposure_rows),
        "zero_visit_units": zero_visit_units,
        "fdq_ready_units": ready_units,
        "fdq_withheld_units": len(exposure_rows) - ready_units,
        "primary_exposure_unit": "population_id x field_event_id x island_id x site_id",
        "official_fdq_requires": (
            "positive visitor abundance plus all scored visit bouts taxon-resolved at confirmed confidence and every "
            "positive-abundance taxon linked to an admitted site-specific numeric proboscis trait"
        ),
        "group_level_service_still_allowed": True,
        "claim_boundary": (
            "Zero visits are retained as zero-visit exposure, not converted to FDQ=0. Failure of FDQ readiness does "
            "not invalidate group-level SVD/effective-service records; it only withholds the harmonized exposure metric."
        ),
    }
    return FieldFDQAudit(tuple(exposure_rows), summary)


def audit_field_fdq_from_files(
    *,
    plants_path: Path,
    effort_path: Path,
    visits_path: Path,
    traits_path: Path,
) -> FieldFDQAudit:
    visit_fields, _ = _read_raw_csv(visits_path)
    missing = set(REQUIRED_FDQ_VISIT_COLUMNS) - set(visit_fields)
    if missing:
        raise ValueError("FDQ visit manifest missing columns: " + ", ".join(sorted(missing)))
    plants = read_dependency_plant_registry(plants_path)
    efforts = read_effort_manifest(effort_path)
    visits = read_visit_manifest(visits_path)
    traits = read_trait_lookup(traits_path)
    return audit_field_fdq(plants, efforts, visits, traits)
