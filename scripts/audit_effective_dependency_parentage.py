#!/usr/bin/env python3
"""Audit optional seed-parentage records for the direct dependency pilot.

Parentage is an optional downstream channel.  This audit validates fruit/seed
linkage and genotype-QC state, but it never converts an unresolved or missing
paternal assignment into selfing.  Parentage status is therefore reported
separately from the core open/bagged/supplemental reproductive-dependency panel.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Mapping, Sequence

from scripts.audit_effective_pollinator_dependency import FRUIT_COLUMNS, read_fruits


PARENTAGE_COLUMNS = (
    "parentage_id",
    "fruit_id",
    "seed_id",
    "site_id",
    "maternal_id",
    "paternal_id",
    "parentage_status",
    "posterior_probability",
    "genotype_qc_status",
    "notes",
)
PARENTAGE_STATES = frozenset({"assigned", "unresolved", "failed_qc"})
QC_STATES = frozenset({"pass", "fail", "pending"})


def _text(row: Mapping[str, object], field: str) -> str:
    return str(row.get(field, "") or "").strip()


def read_parentage(path: Path) -> tuple[dict[str, str], ...]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = set(PARENTAGE_COLUMNS) - set(reader.fieldnames or ())
        if missing:
            raise ValueError("parentage manifest missing columns: " + ", ".join(sorted(missing)))
        rows = tuple(reader)

    seen_parentage: set[str] = set()
    seen_seed: set[str] = set()
    for row in rows:
        parentage_id = _text(row, "parentage_id")
        seed_id = _text(row, "seed_id")
        if not parentage_id or parentage_id in seen_parentage:
            raise ValueError("parentage_id values must be non-empty and unique")
        if not seed_id or seed_id in seen_seed:
            raise ValueError("seed_id values must be non-empty and unique")
        seen_parentage.add(parentage_id)
        seen_seed.add(seed_id)

        for field in ("fruit_id", "site_id", "maternal_id", "parentage_status", "genotype_qc_status"):
            if not _text(row, field):
                raise ValueError(f"blank {field} for parentage_id={parentage_id!r}")

        status = _text(row, "parentage_status")
        qc = _text(row, "genotype_qc_status")
        paternal = _text(row, "paternal_id")
        posterior = _text(row, "posterior_probability")
        if status not in PARENTAGE_STATES:
            raise ValueError(f"invalid parentage_status for parentage_id={parentage_id!r}")
        if qc not in QC_STATES:
            raise ValueError(f"invalid genotype_qc_status for parentage_id={parentage_id!r}")

        if status == "assigned":
            if qc != "pass":
                raise ValueError(f"assigned parentage requires genotype_qc_status=pass for parentage_id={parentage_id!r}")
            if not paternal:
                raise ValueError(f"assigned parentage requires paternal_id for parentage_id={parentage_id!r}")
            try:
                probability = float(posterior)
            except ValueError as error:
                raise ValueError(f"assigned parentage requires numeric posterior_probability for parentage_id={parentage_id!r}") from error
            if not 0.0 <= probability <= 1.0:
                raise ValueError(f"posterior_probability must be in [0,1] for parentage_id={parentage_id!r}")
        else:
            if paternal:
                raise ValueError(f"{status} parentage cannot carry paternal_id for parentage_id={parentage_id!r}")
            if posterior:
                raise ValueError(f"{status} parentage cannot carry posterior_probability for parentage_id={parentage_id!r}")
        if status == "failed_qc" and qc != "fail":
            raise ValueError(f"failed_qc parentage requires genotype_qc_status=fail for parentage_id={parentage_id!r}")
    return rows


def audit_parentage(
    fruits: Sequence[Mapping[str, object]],
    parentage_rows: Sequence[Mapping[str, object]],
) -> dict[str, object]:
    fruits_by_id: dict[str, Mapping[str, object]] = {}
    for fruit in fruits:
        fruit_id = _text(fruit, "fruit_id")
        if not fruit_id:
            raise ValueError("fruit_id values must be non-empty")
        if fruit_id in fruits_by_id:
            raise ValueError(f"duplicate fruit_id {fruit_id!r}")
        fruits_by_id[fruit_id] = fruit

    status_counts = {status: 0 for status in sorted(PARENTAGE_STATES)}
    assigned_self_parent = 0
    assigned_outcross_parent = 0
    fruits_with_parentage: set[str] = set()
    for row in parentage_rows:
        parentage_id = _text(row, "parentage_id")
        fruit_id = _text(row, "fruit_id")
        fruit = fruits_by_id.get(fruit_id)
        if fruit is None:
            raise ValueError(f"parentage_id={parentage_id!r} references unknown fruit_id={fruit_id!r}")
        if _text(row, "site_id") != _text(fruit, "site_id"):
            raise ValueError(f"site_id mismatch for parentage_id={parentage_id!r}")
        if _text(row, "maternal_id") != _text(fruit, "maternal_id"):
            raise ValueError(f"maternal_id mismatch for parentage_id={parentage_id!r}")
        fruits_with_parentage.add(fruit_id)
        status = _text(row, "parentage_status")
        status_counts[status] += 1
        if status == "assigned":
            if _text(row, "paternal_id") == _text(row, "maternal_id"):
                assigned_self_parent += 1
            else:
                assigned_outcross_parent += 1

    n_assigned = status_counts["assigned"]
    return {
        "schema_version": "1.0",
        "status": "optional_parentage_linkage_audit_complete",
        "n_fruits": len(fruits_by_id),
        "n_parentage_rows": len(parentage_rows),
        "n_fruits_with_parentage_rows": len(fruits_with_parentage),
        "parentage_status_counts": status_counts,
        "assigned_parent_identity": {
            "maternal_parent_assignment": assigned_self_parent,
            "different_parent_assignment": assigned_outcross_parent,
            "n_assigned": n_assigned,
        },
        "realized_selfing_estimable_from_all_seeds": False,
        "core_dependency_panel_affected_by_missing_parentage": False,
        "claim_boundary": (
            "Only rows with an explicit assigned paternal identity after passing genotype QC can be classified by parent identity. "
            "Unresolved, failed-QC, ungenotyped, or missing parentage is not selfing and is not imputed. "
            "This optional channel does not replace open/bagged/supplemental treatment-based reproductive dependence."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fruits", type=Path, required=True)
    parser.add_argument("--parentage", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        fruits = read_fruits(args.fruits)
        parentage_rows = read_parentage(args.parentage)
        report = audit_parentage(fruits, parentage_rows)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error
    print(args.output)


if __name__ == "__main__":
    main()
