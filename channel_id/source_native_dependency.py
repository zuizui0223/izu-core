"""Validate source-native pollinator-dependency classifications.

Dependency is classified from explicit pollination evidence, not floral syndrome.
The registry distinguishes a resolved dependency class from whether the same
lineage has a clean mainland/island comparator for the focal regime test.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ALLOWED_CLASSES = {
    "generalist",
    "unresolved",
    "bombus_dependent",
    "non_bombus_scoliid",
    "lepidoptera_specialized",
}
ALLOWED_STRENGTH = {"low", "medium", "high"}
ALLOWED_ROLES = {
    "negative_control_candidate",
    "directional_candidate",
    "heterogeneity_candidate",
    "mechanism_context",
    "dependency_control",
    "alternative_mechanism_context",
}


@dataclass(frozen=True)
class DependencyEvidence:
    dependency_id: str
    source_id: str
    doi: str
    taxon: str
    lineage_id: str
    geographic_scope: str
    dependency_class: str
    evidence_basis: str
    evidence_strength: str
    within_lineage_regime_test_eligible: bool
    analysis_role: str
    pollinator_evidence: str
    source_locator: str
    claim_boundary: str


def _as_bool(value: str) -> bool:
    text = value.strip().lower()
    if text in {"true", "1", "yes"}:
        return True
    if text in {"false", "0", "no", ""}:
        return False
    raise ValueError(f"invalid boolean: {value}")


def load_dependency_evidence(path: str | Path) -> tuple[DependencyEvidence, ...]:
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {
        "dependency_id", "source_id", "doi", "taxon", "lineage_id", "geographic_scope",
        "dependency_class", "evidence_basis", "evidence_strength",
        "within_lineage_regime_test_eligible", "analysis_role", "pollinator_evidence",
        "source_locator", "claim_boundary",
    }
    if not rows:
        raise ValueError("dependency evidence registry is empty")
    missing = sorted(required.difference(rows[0]))
    if missing:
        raise ValueError("dependency evidence registry missing columns: " + ", ".join(missing))

    output: list[DependencyEvidence] = []
    seen: set[str] = set()
    for raw in rows:
        dependency_id = raw["dependency_id"].strip()
        if not dependency_id or dependency_id in seen:
            raise ValueError("dependency_id values must be non-empty and unique")
        seen.add(dependency_id)
        dependency_class = raw["dependency_class"].strip()
        strength = raw["evidence_strength"].strip()
        role = raw["analysis_role"].strip()
        eligible = _as_bool(raw["within_lineage_regime_test_eligible"])
        if dependency_class not in ALLOWED_CLASSES:
            raise ValueError(f"{dependency_id}: invalid dependency_class")
        if strength not in ALLOWED_STRENGTH:
            raise ValueError(f"{dependency_id}: invalid evidence_strength")
        if role not in ALLOWED_ROLES:
            raise ValueError(f"{dependency_id}: invalid analysis_role")
        if dependency_class == "unresolved" and eligible:
            raise ValueError(f"{dependency_id}: unresolved dependency cannot be regime-test eligible")
        if role == "negative_control_candidate" and dependency_class != "generalist":
            raise ValueError(f"{dependency_id}: negative-control candidate must be source-classified generalist")
        if role == "dependency_control" and dependency_class.startswith("bombus"):
            raise ValueError(f"{dependency_id}: dependency control cannot be Bombus-dependent")
        if not raw["pollinator_evidence"].strip() or not raw["source_locator"].strip():
            raise ValueError(f"{dependency_id}: source-native pollinator evidence and locator are required")
        output.append(DependencyEvidence(
            dependency_id=dependency_id,
            source_id=raw["source_id"].strip(),
            doi=raw["doi"].strip(),
            taxon=raw["taxon"].strip(),
            lineage_id=raw["lineage_id"].strip(),
            geographic_scope=raw["geographic_scope"].strip(),
            dependency_class=dependency_class,
            evidence_basis=raw["evidence_basis"].strip(),
            evidence_strength=strength,
            within_lineage_regime_test_eligible=eligible,
            analysis_role=role,
            pollinator_evidence=raw["pollinator_evidence"].strip(),
            source_locator=raw["source_locator"].strip(),
            claim_boundary=raw["claim_boundary"].strip(),
        ))
    return tuple(output)


def summarize(records: Iterable[DependencyEvidence]) -> dict[str, object]:
    rows = tuple(records)
    unresolved = sorted({row.lineage_id for row in rows if row.dependency_class == "unresolved"})
    generalists = sorted({row.lineage_id for row in rows if row.dependency_class == "generalist"})
    bombus = sorted({row.lineage_id for row in rows if row.dependency_class == "bombus_dependent"})
    eligible = sorted({row.lineage_id for row in rows if row.within_lineage_regime_test_eligible})
    eligible_bombus = sorted({
        row.lineage_id for row in rows
        if row.within_lineage_regime_test_eligible and row.dependency_class == "bombus_dependent"
    })
    controls = sorted({row.lineage_id for row in rows if row.analysis_role == "dependency_control"})
    return {
        "n_records": len(rows),
        "unresolved_dependency_lineages": unresolved,
        "source_classified_generalist_lineages": generalists,
        "source_classified_bombus_dependent_lineages": bombus,
        "within_lineage_regime_test_eligible_lineages": eligible,
        "eligible_bombus_dependent_lineages": eligible_bombus,
        "dependency_control_lineages": controls,
        "independent_bombus_holdout_status": (
            "open" if eligible_bombus else "blocked_no_clean_source_resolved_bombus_lineage"
        ),
        "interpretation": (
            "A dependency class and a clean regime comparator are separate gates. Direct Bombus dependence "
            "in Goodyera henryi does not open the focal holdout because the island comparator is hybrid; "
            "Weigela and Hosta remain unresolved; Ligustrum is the source-labelled generalist control candidate."
        ),
    }
