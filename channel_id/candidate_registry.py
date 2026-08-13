"""Audit candidate lineages before they enter the negative-control analysis."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

ALLOWED_GROUPS = {"specialist", "generalist", "uncertain"}
ALLOWED_GRADES = {"A", "B", "C", "U"}
ALLOWED_STATUSES = {"candidate", "extracting", "ready", "excluded"}


@dataclass(frozen=True)
class Candidate:
    lineage: str
    group: str
    growth_form: str
    flowering_season: str
    mainland_coverage: str
    island_coverage: str
    trait_channel: str
    evidence_grade: str
    quantitative_ready: bool
    specialization_source: str
    trait_source: str
    matched_set: str
    status: str
    next_action: str


def _as_bool(value: str) -> bool:
    text = value.strip().lower()
    if text in {"1", "true", "yes", "y"}:
        return True
    if text in {"0", "false", "no", "n", ""}:
        return False
    raise ValueError(f"invalid boolean: {value}")


def load_candidates(path: str | Path) -> tuple[Candidate, ...]:
    required = {
        "lineage", "group", "growth_form", "flowering_season",
        "mainland_coverage", "island_coverage", "trait_channel",
        "evidence_grade", "quantitative_ready", "specialization_source",
        "trait_source", "matched_set", "status", "next_action",
    }
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("candidate registry is empty")
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"missing columns: {sorted(missing)}")
    out = []
    for row in rows:
        item = Candidate(
            lineage=row["lineage"].strip(),
            group=row["group"].strip().lower(),
            growth_form=row["growth_form"].strip(),
            flowering_season=row["flowering_season"].strip(),
            mainland_coverage=row["mainland_coverage"].strip(),
            island_coverage=row["island_coverage"].strip(),
            trait_channel=row["trait_channel"].strip(),
            evidence_grade=row["evidence_grade"].strip().upper(),
            quantitative_ready=_as_bool(row["quantitative_ready"]),
            specialization_source=row["specialization_source"].strip(),
            trait_source=row["trait_source"].strip(),
            matched_set=row["matched_set"].strip(),
            status=row["status"].strip().lower(),
            next_action=row["next_action"].strip(),
        )
        if not item.lineage:
            raise ValueError("lineage is required")
        if item.group not in ALLOWED_GROUPS:
            raise ValueError(f"unknown group: {item.group}")
        if item.evidence_grade not in ALLOWED_GRADES:
            raise ValueError(f"unknown evidence grade: {item.evidence_grade}")
        if item.status not in ALLOWED_STATUSES:
            raise ValueError(f"unknown status: {item.status}")
        if item.quantitative_ready:
            if item.evidence_grade != "A":
                raise ValueError(f"quantitative-ready row must be grade A: {item.lineage}")
            if not item.trait_source:
                raise ValueError(f"quantitative-ready row requires trait_source: {item.lineage}")
            if item.group == "uncertain":
                raise ValueError(f"quantitative-ready row requires resolved group: {item.lineage}")
        out.append(item)
    return tuple(out)


def audit_candidates(candidates: Sequence[Candidate]) -> dict[str, object]:
    ready = [x for x in candidates if x.quantitative_ready and x.status == "ready"]
    unresolved = [x for x in candidates if x.group == "uncertain"]
    missing_specialization = [x for x in candidates if x.group != "uncertain" and not x.specialization_source]
    missing_trait_source = [x for x in candidates if x.evidence_grade in {"A", "B"} and not x.trait_source]

    matched: dict[str, set[str]] = {}
    for item in candidates:
        if item.matched_set:
            matched.setdefault(item.matched_set, set()).add(item.group)
    complete_sets = sorted(k for k, groups in matched.items() if {"specialist", "generalist"} <= groups)
    incomplete_sets = sorted(k for k, groups in matched.items() if not {"specialist", "generalist"} <= groups)

    actions: dict[str, list[str]] = {}
    for item in candidates:
        if item.next_action:
            actions.setdefault(item.next_action, []).append(item.lineage)

    return {
        "n_candidates": len(candidates),
        "n_quantitative_ready": len(ready),
        "ready_lineages": sorted(x.lineage for x in ready),
        "unresolved_group": sorted(x.lineage for x in unresolved),
        "missing_specialization_source": sorted(x.lineage for x in missing_specialization),
        "missing_trait_source": sorted(x.lineage for x in missing_trait_source),
        "complete_matched_sets": complete_sets,
        "incomplete_matched_sets": incomplete_sets,
        "next_actions": {k: sorted(v) for k, v in sorted(actions.items())},
        "analysis_gate": {
            "open": len(ready) >= 4 and len(complete_sets) >= 2,
            "rule": "Open only with at least four quantitative-ready lineages and two complete specialist-generalist matched sets.",
        },
    }
