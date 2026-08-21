"""Build strict Issue #91 FDQ exposure units from linked field visitor records.

This is intentionally separate from visitor-group SVD/effective-service analysis.
Group-level visitor identities remain usable for service summaries, but Izu-compatible
FDQ is withheld unless every scored visit in an exposure unit has a confirmed taxon
identity and every positive-abundance taxon has an admitted numeric proboscis trait.
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


def audit_field_fdq(
    plant_rows: Sequence[dict[str, str]],
    effort_rows: Sequence[dict[str, str]],
    visit_rows: Sequence[dict[str, str]],
    trait_lookup: Mapping[tuple[str, str], Mapping[str, str]],
) -> FieldFDQAudit:
    """Aggregate confirmed taxon identities and calculate strict Rao-Q by population-event-site.

    All visit bouts linked to usable effort contribute to the exposure denominator. A
    group-level/uncertain visit is not silently discarded: it increases the unresolved
    count and blocks official FDQ for that exposure unit. Similarly, a confirmed taxon
    lacking an admitted site-specific numeric trait blocks FDQ.
    """
    # Reuse the established validators and effort-linkage checks.
    audit_field_contacts(effort_rows, visit_rows)
    plant_map = _plant_population_map(plant_rows)

    grouped: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for visit in visit_rows:
        plant_id = _text(visit, "plant_id")
        if not plant_id:
            raise ValueError(f"FDQ visit_id={_text(visit, 'visit_id')!r} requires plant_id linkage")
        population_key = plant_map.get(plant_id)
        if population_key is None:
            raise ValueError(
                f"FDQ visit_id={_text(visit, 'visit_id')!r} references plant_id={plant_id!r} "
                "outside dependency plant registry"
            )
        visit_key = (
            _text(visit, "field_event_id"),
            _text(visit, "island_id"),
            _text(visit, "site_id"),
        )
        if visit_key != population_key[1:]:
            raise ValueError(
                f"FDQ visit_id={_text(visit, 'visit_id')!r} field_event/island/site does not match plant registry"
            )
        grouped[population_key].append(visit)

    exposure_rows: list[dict[str, str]] = []
    ready_units = 0
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

        taxon_resolution_fraction = resolved_visits / total_visits if total_visits else 0.0
        trait_coverage_fraction = trait_covered_visits / total_visits if total_visits else 0.0
        strict_ready = not unresolved_visit_ids and not missing_trait_taxa and total_visits > 0
        fdq_value = ""
        if strict_ready:
            result = abundance_weighted_rao_q(resolved_counts, trait_values)
            fdq_value = f"{result.fdq:.12g}"
            ready_units += 1

        exposure_rows.append(
            {
                "population_id": population_id,
                "field_event_id": field_event_id,
                "island_id": island_id,
                "site_id": site_id,
                "total_visit_bouts": str(total_visits),
                "taxon_resolved_visit_bouts": str(resolved_visits),
                "trait_covered_visit_bouts": str(trait_covered_visits),
                "taxon_resolution_fraction": f"{taxon_resolution_fraction:.12g}",
                "trait_coverage_fraction": f"{trait_coverage_fraction:.12g}",
                "resolved_taxa": "|".join(sorted(resolved_counts)),
                "missing_trait_taxa": "|".join(missing_trait_taxa),
                "unresolved_visitor_groups": "|".join(sorted(unresolved_groups)),
                "unresolved_visit_ids": "|".join(sorted(unresolved_visit_ids)),
                "fdq": fdq_value,
                "fdq_status": "ready" if strict_ready else "withheld_incomplete_taxon_or_trait_coverage",
                "boundary": (
                    "FDQ uses all positive-abundance visit bouts only when taxon identity and site-specific "
                    "numeric proboscis trait coverage are complete; missing visits/taxa are not dropped and "
                    "remaining abundances are not renormalized."
                ),
            }
        )

    summary = {
        "exposure_units": len(exposure_rows),
        "fdq_ready_units": ready_units,
        "fdq_withheld_units": len(exposure_rows) - ready_units,
        "primary_exposure_unit": "population_id x field_event_id x island_id x site_id",
        "official_fdq_requires": (
            "all scored visit bouts taxon-resolved at confirmed confidence and every positive-abundance taxon "
            "linked to an admitted site-specific numeric proboscis trait"
        ),
        "group_level_service_still_allowed": True,
        "claim_boundary": (
            "Failure of FDQ readiness does not invalidate group-level SVD/effective-service records. It only "
            "withholds the harmonized functional-exposure metric."
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
