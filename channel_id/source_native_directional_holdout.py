"""Audit B-grade source-native directional evidence without inventing effect sizes.

This layer exists because original articles can contain useful response-shape
information even when population means, uncertainty, n, or exact locality tables
are not publicly recoverable. It is deliberately separate from the A-grade
numeric holdout.

A source may support a shared Oshima-to-Toshima second step only when the source
itself localizes the comparison across that boundary. Broad phrases such as
"Izu Islands", "southern Izu", a gradual mainland-distance decline, or a Hachijo
endpoint do not satisfy that rule.
"""
from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence


ALLOWED_GROUPS = {"specialist", "generalist", "uncertain"}
ALLOWED_GRADES = {"B"}
ALLOWED_BOUNDARY = {
    "explicit_oshima_postboundary",
    "exact_island_sequence_missing",
    "southern_izu_aggregate_only",
}
ALLOWED_STEP_EVIDENCE = {"supports", "does_not_demonstrate", "unresolved"}


@dataclass(frozen=True)
class DirectionalEvidence:
    directional_id: str
    source_id: str
    doi: str
    taxon: str
    lineage_id: str
    analysis_group: str
    dependency_status: str
    evidence_grade: str
    response_domain: str
    source_reported_pattern: str
    boundary_localization: str
    shared_second_step_evidence: str
    generalist_change_observed: bool
    eligible_for_numeric_holdout: bool
    source_locator: str
    claim_boundary: str
    next_required_evidence: str


def _as_bool(value: str) -> bool:
    text = value.strip().lower()
    if text in {"true", "1", "yes"}:
        return True
    if text in {"false", "0", "no", ""}:
        return False
    raise ValueError(f"invalid boolean: {value}")


def load_directional_evidence(path: str | Path) -> tuple[DirectionalEvidence, ...]:
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {
        "directional_id", "source_id", "doi", "taxon", "lineage_id", "analysis_group",
        "dependency_status", "evidence_grade", "response_domain", "source_reported_pattern",
        "boundary_localization", "shared_second_step_evidence", "generalist_change_observed",
        "eligible_for_numeric_holdout", "source_locator", "claim_boundary", "next_required_evidence",
    }
    if not rows:
        raise ValueError("directional evidence registry is empty")
    missing = sorted(required.difference(rows[0]))
    if missing:
        raise ValueError("directional evidence registry missing columns: " + ", ".join(missing))

    output: list[DirectionalEvidence] = []
    seen: set[str] = set()
    for raw in rows:
        directional_id = raw["directional_id"].strip()
        if not directional_id or directional_id in seen:
            raise ValueError("directional_id values must be non-empty and unique")
        seen.add(directional_id)
        group = raw["analysis_group"].strip().lower()
        grade = raw["evidence_grade"].strip().upper()
        boundary = raw["boundary_localization"].strip()
        step_evidence = raw["shared_second_step_evidence"].strip()
        numeric_eligible = _as_bool(raw["eligible_for_numeric_holdout"])
        generalist_change = _as_bool(raw["generalist_change_observed"])
        dependency_status = raw["dependency_status"].strip()

        if group not in ALLOWED_GROUPS:
            raise ValueError(f"{directional_id}: invalid analysis_group")
        if grade not in ALLOWED_GRADES:
            raise ValueError(f"{directional_id}: directional layer must remain grade B")
        if boundary not in ALLOWED_BOUNDARY:
            raise ValueError(f"{directional_id}: invalid boundary_localization")
        if step_evidence not in ALLOWED_STEP_EVIDENCE:
            raise ValueError(f"{directional_id}: invalid shared_second_step_evidence")
        if numeric_eligible:
            raise ValueError(f"{directional_id}: B-grade directional evidence cannot enter numeric holdout")
        if group == "uncertain" and dependency_status != "unresolved_dependency":
            raise ValueError(f"{directional_id}: uncertain group requires unresolved_dependency")
        if group != "generalist" and generalist_change:
            raise ValueError(f"{directional_id}: generalist_change_observed requires generalist group")
        if step_evidence == "supports" and boundary != "explicit_oshima_postboundary":
            raise ValueError(
                f"{directional_id}: shared second-step support requires explicit Oshima/post-boundary localization"
            )
        if not raw["source_locator"].strip() or not raw["claim_boundary"].strip():
            raise ValueError(f"{directional_id}: source_locator and claim_boundary are required")

        output.append(DirectionalEvidence(
            directional_id=directional_id,
            source_id=raw["source_id"].strip(),
            doi=raw["doi"].strip(),
            taxon=raw["taxon"].strip(),
            lineage_id=raw["lineage_id"].strip(),
            analysis_group=group,
            dependency_status=dependency_status,
            evidence_grade=grade,
            response_domain=raw["response_domain"].strip(),
            source_reported_pattern=raw["source_reported_pattern"].strip(),
            boundary_localization=boundary,
            shared_second_step_evidence=step_evidence,
            generalist_change_observed=generalist_change,
            eligible_for_numeric_holdout=numeric_eligible,
            source_locator=raw["source_locator"].strip(),
            claim_boundary=raw["claim_boundary"].strip(),
            next_required_evidence=raw["next_required_evidence"].strip(),
        ))
    return tuple(output)


def native_source_ids(path: str | Path) -> set[str]:
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or "source_id" not in rows[0]:
        raise ValueError("source-native evidence registry must contain source_id")
    return {row["source_id"].strip() for row in rows if row["source_id"].strip()}


def validate_source_links(records: Sequence[DirectionalEvidence], native_path: str | Path) -> None:
    available = native_source_ids(native_path)
    missing = sorted({row.source_id for row in records} - available)
    if missing:
        raise ValueError("directional sources missing from source-native registry: " + ", ".join(missing))


def summarize(records: Iterable[DirectionalEvidence]) -> dict[str, object]:
    rows = tuple(records)
    lineages = sorted({row.lineage_id for row in rows})
    support = sorted({row.lineage_id for row in rows if row.shared_second_step_evidence == "supports"})
    not_demonstrated = sorted({
        row.lineage_id for row in rows if row.shared_second_step_evidence == "does_not_demonstrate"
    })
    unresolved = sorted({row.lineage_id for row in rows if row.shared_second_step_evidence == "unresolved"})
    generalist_change = sorted({
        row.lineage_id for row in rows if row.analysis_group == "generalist" and row.generalist_change_observed
    })
    unresolved_dependency = sorted({row.lineage_id for row in rows if row.analysis_group == "uncertain"})
    return {
        "n_directional_records": len(rows),
        "n_lineages": len(lineages),
        "lineages": lineages,
        "shared_second_step_support_lineages": support,
        "shared_second_step_not_demonstrated_lineages": not_demonstrated,
        "shared_second_step_unresolved_lineages": unresolved,
        "generalist_change_observed_lineages": generalist_change,
        "unresolved_dependency_lineages": unresolved_dependency,
        "numeric_holdout_rows": sum(row.eligible_for_numeric_holdout for row in rows),
        "universal_shared_second_step_status": (
            "supported_by_directional_layer" if support and len(support) == len(lineages)
            else "not_supported_by_current_directional_layer"
        ),
        "interpretation": (
            "Current B-grade sources document heterogeneous island responses, but none independently "
            "localizes an Oshima-to-Toshima shared second step. This is absence of directional support, "
            "not a statistical falsification of the pollinator-regime hypothesis. Generalist geographic "
            "change is allowed; the negative control concerns a repeated shared breakpoint, not zero change."
        ),
    }


def run_audit(
    directional_path: str | Path,
    native_path: str | Path,
) -> dict[str, object]:
    rows = load_directional_evidence(directional_path)
    validate_source_links(rows, native_path)
    return {
        "records": [asdict(row) for row in rows],
        "summary": summarize(rows),
        "claim_boundary": (
            "B-grade directional evidence can constrain response shapes but cannot supply effect sizes, "
            "equivalence claims, exact regime breakpoints, or causal attribution unless the original source "
            "explicitly supplies the required localities and measurements."
        ),
    }


def write_report(path: str | Path, report: dict[str, object]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
