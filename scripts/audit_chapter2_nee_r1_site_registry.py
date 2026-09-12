#!/usr/bin/env python3
"""Fail-closed audit for the Chapter 2 future NEE R1b site/block registry.

This audit checks prospective scope feasibility only. It does not inspect or accept
reproductive outcomes and it does not calculate empirical power.
"""
from __future__ import annotations

import argparse
import csv
import json
from datetime import date
from pathlib import Path

REQUIRED_COLUMNS = [
    "context_id",
    "taxon",
    "geographic_unit",
    "population_site_id",
    "site_name",
    "planned_block_id",
    "planned_start_date",
    "planned_end_date",
    "eligible_flowering_plants_screen",
    "block_independence_basis",
    "independence_review_status",
    "svd_background_feasible",
    "open_pollination_feasible",
    "bagged_autonomous_feasible",
    "supplemental_outcross_feasible",
    "dependence_coordinate_feasible",
    "access_status",
    "permit_status",
    "phenology_status",
    "outcome_blind_exclusion_reason",
    "admission_status",
]

EXPECTED_TAXON = {
    "focal": "Campanula microdonta",
    "transport": "Farfugium japonicum",
}
BOOL_FIELDS = [
    "svd_background_feasible",
    "open_pollination_feasible",
    "bagged_autonomous_feasible",
    "supplemental_outcross_feasible",
    "dependence_coordinate_feasible",
]
ADMISSION = {"candidate", "admitted", "excluded"}
INDEPENDENCE = {"pass", "review", "fail"}
ACCESS = {"confirmed", "pending", "blocked"}
PERMIT = {"not_required", "confirmed", "pending", "blocked"}
PHENOLOGY = {"confirmed", "pending", "failed"}


def _bool(value: str) -> bool | None:
    x = value.strip().lower()
    if x in {"true", "1", "yes"}:
        return True
    if x in {"false", "0", "no"}:
        return False
    return None


def _date(value: str) -> date | None:
    try:
        return date.fromisoformat(value.strip())
    except ValueError:
        return None


def audit(path: Path) -> dict:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames or []
        rows = list(reader)

    errors: list[str] = []
    missing_columns = [c for c in REQUIRED_COLUMNS if c not in columns]
    if missing_columns:
        return {
            "status": "NOT_READY",
            "reason": "schema_failure",
            "missing_columns": missing_columns,
            "errors": [f"missing required column: {c}" for c in missing_columns],
        }

    seen_blocks: set[str] = set()
    admitted = {"focal": [], "transport": []}
    candidate_counts = {"focal": 0, "transport": 0}
    excluded_counts = {"focal": 0, "transport": 0}

    for line_no, row in enumerate(rows, start=2):
        context = row["context_id"].strip().lower()
        prefix = f"line {line_no}"
        if context not in EXPECTED_TAXON:
            errors.append(f"{prefix}: context_id must be focal or transport")
            continue
        if row["taxon"].strip() != EXPECTED_TAXON[context]:
            errors.append(f"{prefix}: taxon does not match frozen {context} taxon")

        block_id = row["planned_block_id"].strip()
        if not block_id:
            errors.append(f"{prefix}: planned_block_id is required")
        elif block_id in seen_blocks:
            errors.append(f"{prefix}: duplicate planned_block_id {block_id}")
        else:
            seen_blocks.add(block_id)

        for field in ("geographic_unit", "population_site_id", "site_name", "block_independence_basis"):
            if not row[field].strip():
                errors.append(f"{prefix}: {field} is required")

        start = _date(row["planned_start_date"])
        end = _date(row["planned_end_date"])
        if start is None or end is None:
            errors.append(f"{prefix}: planned dates must be ISO YYYY-MM-DD")
        elif end < start:
            errors.append(f"{prefix}: planned_end_date precedes planned_start_date")

        try:
            eligible = int(row["eligible_flowering_plants_screen"])
            if eligible < 0:
                raise ValueError
        except ValueError:
            eligible = -1
            errors.append(f"{prefix}: eligible_flowering_plants_screen must be a non-negative integer")

        if row["independence_review_status"].strip().lower() not in INDEPENDENCE:
            errors.append(f"{prefix}: invalid independence_review_status")
        if row["access_status"].strip().lower() not in ACCESS:
            errors.append(f"{prefix}: invalid access_status")
        if row["permit_status"].strip().lower() not in PERMIT:
            errors.append(f"{prefix}: invalid permit_status")
        if row["phenology_status"].strip().lower() not in PHENOLOGY:
            errors.append(f"{prefix}: invalid phenology_status")

        bools = {field: _bool(row[field]) for field in BOOL_FIELDS}
        for field, value in bools.items():
            if value is None:
                errors.append(f"{prefix}: {field} must be true/false")

        status = row["admission_status"].strip().lower()
        if status not in ADMISSION:
            errors.append(f"{prefix}: invalid admission_status")
            continue

        if status == "excluded":
            excluded_counts[context] += 1
            if not row["outcome_blind_exclusion_reason"].strip():
                errors.append(f"{prefix}: excluded rows require an outcome-blind exclusion reason")
            continue

        if status == "candidate":
            candidate_counts[context] += 1
            continue

        # Admitted rows fail closed: every structural feasibility gate must pass.
        admitted_failures = []
        if eligible <= 0:
            admitted_failures.append("eligible flowering plants")
        if row["independence_review_status"].strip().lower() != "pass":
            admitted_failures.append("block independence")
        if not all(value is True for value in bools.values()):
            admitted_failures.append("SVD/treatment/dependence feasibility")
        if row["access_status"].strip().lower() != "confirmed":
            admitted_failures.append("access")
        if row["permit_status"].strip().lower() not in {"not_required", "confirmed"}:
            admitted_failures.append("permit")
        if row["phenology_status"].strip().lower() != "confirmed":
            admitted_failures.append("phenology")
        if admitted_failures:
            errors.append(f"{prefix}: admitted row fails: {', '.join(admitted_failures)}")
        else:
            admitted[context].append(block_id)

    focal_blocks = len(admitted["focal"])
    transport_blocks = len(admitted["transport"])
    scope_complete = focal_blocks > 0 and transport_blocks > 0
    h5_screen_pass = focal_blocks >= 32
    status = "R1B_READY_FOR_R2" if (not errors and scope_complete and h5_screen_pass) else "NOT_READY"

    return {
        "status": status,
        "claim_boundary": "R1b structural/site feasibility only; not empirical power and not confirmatory sample-size justification.",
        "focal_taxon": EXPECTED_TAXON["focal"],
        "transport_taxon": EXPECTED_TAXON["transport"],
        "admitted_focal_blocks": focal_blocks,
        "admitted_transport_blocks": transport_blocks,
        "candidate_counts": candidate_counts,
        "excluded_counts": excluded_counts,
        "scope_complete": scope_complete,
        "h5_r1_screening_floor_blocks": 32,
        "h5_r1_screen_pass": h5_screen_pass,
        "h5_r1_screen_is_empirical_power": False,
        "errors": errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", required=True, type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    result = audit(args.registry)
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    print(text, end="")
    raise SystemExit(0 if result["status"] == "R1B_READY_FOR_R2" else 2)


if __name__ == "__main__":
    main()
