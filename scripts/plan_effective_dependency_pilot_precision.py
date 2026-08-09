#!/usr/bin/env python3
"""Summarize pilot dispersion and convert locked precision goals to plant n.

No precision target is supplied by default.  A first pilot can therefore be run
without a goal file to obtain plant-level SVD and treatment dispersion.  Once an
absolute CI half-width is scientifically locked, pass a goal CSV and the command
will calculate a normal-approximation number of independent plants.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from channel_id.effective_dependency_precision import (
    PilotPrecisionAudit,
    build_precision_recommendations,
    read_precision_goals,
    summarize_svd_pilot,
    summarize_treatment_pilot,
    write_pilot_precision_audit,
)
from channel_id.effective_pollinator_dependency import read_pollination_treatments, read_svd_manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--svd", type=Path, required=True)
    parser.add_argument("--treatments", type=Path, required=True)
    parser.add_argument("--goals", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    try:
        svd_rows = read_svd_manifest(args.svd)
        treatment_rows = read_pollination_treatments(args.treatments)
        svd_plants, svd_summary = summarize_svd_pilot(svd_rows)
        treatment_plants, treatment_summary = summarize_treatment_pilot(treatment_rows)
        goals = read_precision_goals(args.goals) if args.goals else ()
        recommendations = build_precision_recommendations(goals, svd_summary, treatment_summary)
        audit = PilotPrecisionAudit(
            svd_plant_rows=svd_plants,
            svd_summary_rows=svd_summary,
            treatment_plant_rows=treatment_plants,
            treatment_summary_rows=treatment_summary,
            precision_rows=recommendations,
        )
        write_pilot_precision_audit(args.output_dir, audit)
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
