#!/usr/bin/env python3
"""Audit direct effective-pollinator dependency field records.

This command links:

* tagged focal plants;
* camera/direct-observation effort and visitor bouts;
* single-visit pollen deposition (SVD);
* flower-level pollination treatments; and
* optional mature-fruit records from the existing raw-record protocol.

It writes descriptive population-level readiness and service summaries. A
structurally complete panel is not a power or causal-identification claim.

Official CLI output is conservative about background correction: if a visitor
group has no no-visit SVD control, raw SVD may remain in the SVD audit table but
background-adjusted SVD, rate-weighted effective service and service share are
withheld. Shares are then recomputed only among visitor groups with controlled
SVD estimates.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

from channel_id.effective_pollinator_dependency import (
    EffectiveDependencyAudit,
    audit_effective_pollinator_dependency,
    read_dependency_plant_registry,
    read_pollination_treatments,
    read_svd_manifest,
    write_effective_dependency_audit,
)
from channel_id.field_legitimate_contact import read_effort_manifest, read_visit_manifest


FRUIT_COLUMNS = (
    "fruit_id", "site_id", "maternal_id", "collection_date", "mature_seed_count",
    "genotyped_seed_target", "genotyped_seed_count", "fruit_notes",
)


def read_fruits(path: Path) -> tuple[dict[str, str], ...]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = set(FRUIT_COLUMNS) - set(reader.fieldnames or ())
        if missing:
            raise ValueError("fruit manifest missing columns: " + ", ".join(sorted(missing)))
        return tuple(reader)


def mask_uncontrolled_effective_service(audit: EffectiveDependencyAudit) -> EffectiveDependencyAudit:
    """Withhold adjusted service values when no SVD background control exists.

    The core audit intentionally retains raw rows for troubleshooting, but the
    field-facing output must never imply a background-adjusted service estimate
    when the corresponding SVD group has neither an exposed-no-visit nor a
    bagged-unvisited control.  Controlled groups keep their rate-weighted service
    value and their shares are recomputed after uncontrolled groups are removed.
    """
    uncontrolled = {
        (row["population_id"], row["visitor_group"])
        for row in audit.svd_group_rows
        if row["background_control_basis"] == "missing_no_visit_control"
    }

    rows = [dict(row) for row in audit.effective_service_rows]
    totals: dict[str, float] = defaultdict(float)
    for row in rows:
        key = (row["population_id"], row["visitor_group"])
        if key in uncontrolled:
            row["mean_background_adjusted_svd"] = ""
            row["effective_pollen_delivery_per_flower_hour"] = ""
            row["effective_service_share"] = ""
            row["boundary"] = (
                "Effective service withheld because this visitor group lacks a no-visit SVD background control. "
                "Raw visit rate and raw SVD remain audit information only."
            )
            continue
        value = row["effective_pollen_delivery_per_flower_hour"].strip()
        if value:
            totals[row["population_id"]] += float(value)

    for row in rows:
        key = (row["population_id"], row["visitor_group"])
        if key in uncontrolled:
            continue
        value = row["effective_pollen_delivery_per_flower_hour"].strip()
        total = totals.get(row["population_id"], 0.0)
        row["effective_service_share"] = f"{float(value) / total:.8f}" if value and total > 0 else ""

    return EffectiveDependencyAudit(
        svd_group_rows=audit.svd_group_rows,
        effective_service_rows=tuple(rows),
        treatment_rows=audit.treatment_rows,
        population_readiness_rows=audit.population_readiness_rows,
        summary=audit.summary,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plants", type=Path, required=True)
    parser.add_argument("--effort", type=Path, required=True)
    parser.add_argument("--visits", type=Path, required=True)
    parser.add_argument("--svd", type=Path, required=True)
    parser.add_argument("--treatments", type=Path, required=True)
    parser.add_argument("--fruits", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    try:
        plants = read_dependency_plant_registry(args.plants)
        effort = read_effort_manifest(args.effort)
        visits = read_visit_manifest(args.visits)
        svd = read_svd_manifest(args.svd)
        treatments = read_pollination_treatments(args.treatments)
        fruits = read_fruits(args.fruits) if args.fruits else None
        audit = audit_effective_pollinator_dependency(
            plants,
            effort,
            visits,
            svd,
            treatments,
            fruit_rows=fruits,
        )
        audit = mask_uncontrolled_effective_service(audit)
        write_effective_dependency_audit(args.output_dir, audit)
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
