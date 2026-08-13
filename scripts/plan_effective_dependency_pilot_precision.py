#!/usr/bin/env python3
"""Summarize pilot dispersion and convert locked precision goals to plant n.

No precision target is supplied by default. A first pilot can therefore be run
without a goal file to obtain plant-level SVD and treatment dispersion. Once an
absolute CI half-width is scientifically locked, precision planning additionally
requires a frozen raw bundle and a passed pilot-dispersion admission state for
every population referenced by a locked goal.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Mapping, Sequence

from channel_id.effective_dependency_precision import (
    PilotPrecisionAudit,
    build_precision_recommendations,
    read_precision_goals,
    summarize_svd_pilot,
    summarize_treatment_pilot,
    write_pilot_precision_audit,
)
from channel_id.effective_pollinator_dependency import read_pollination_treatments, read_svd_manifest


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _locked_goal_populations(goals: Sequence[Mapping[str, object]]) -> set[str]:
    return {
        str(row.get("population_id", "") or "").strip()
        for row in goals
        if str(row.get("status", "") or "").strip() == "locked"
    }


def validate_precision_inputs(
    *,
    goals: Sequence[Mapping[str, object]],
    svd_path: Path,
    treatments_path: Path,
    freeze_manifest_path: Path | None,
    admission_path: Path | None,
) -> None:
    """Require frozen bytes and a passed pilot gate before locked-goal planning."""
    locked_populations = _locked_goal_populations(goals)
    if not locked_populations:
        return
    if freeze_manifest_path is None:
        raise ValueError("locked precision goals require --freeze-manifest")
    if admission_path is None:
        raise ValueError("locked precision goals require --admission")

    freeze = json.loads(freeze_manifest_path.read_text(encoding="utf-8"))
    if freeze.get("status") != "effective_dependency_raw_field_bundle_frozen":
        raise ValueError("freeze manifest has unexpected status")
    required = set(freeze.get("required_channels") or ())
    if not {"plants", "effort", "visits", "svd", "treatments", "fruits"}.issubset(required):
        raise ValueError("freeze manifest does not declare all required field channels")
    channels = {
        str(row.get("channel", "")): row
        for row in freeze.get("channels", ())
        if isinstance(row, dict)
    }
    for name, path in (("svd", svd_path), ("treatments", treatments_path)):
        frozen = channels.get(name)
        if frozen is None:
            raise ValueError(f"freeze manifest is missing channel {name}")
        observed = _sha256_file(path)
        if observed != frozen.get("sha256"):
            raise ValueError(f"{name} bytes do not match the frozen raw bundle")

    admission = json.loads(admission_path.read_text(encoding="utf-8"))
    if admission.get("schema_version") != "effective_dependency_admission_v1":
        raise ValueError("admission artifact has unexpected schema")
    populations = {
        str(row.get("population_id", "")): row
        for row in admission.get("populations", ())
        if isinstance(row, dict)
    }
    for population_id in sorted(locked_populations):
        row = populations.get(population_id)
        if row is None:
            raise ValueError(
                f"locked precision goal population {population_id!r} is absent from admission artifact"
            )
        if row.get("pilot_dispersion_gate_pass") is not True:
            raise ValueError(
                f"locked precision goal population {population_id!r} has not passed the pilot-dispersion gate"
            )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--svd", type=Path, required=True)
    parser.add_argument("--treatments", type=Path, required=True)
    parser.add_argument("--goals", type=Path)
    parser.add_argument("--freeze-manifest", type=Path)
    parser.add_argument("--admission", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    try:
        svd_rows = read_svd_manifest(args.svd)
        treatment_rows = read_pollination_treatments(args.treatments)
        svd_plants, svd_summary = summarize_svd_pilot(svd_rows)
        treatment_plants, treatment_summary = summarize_treatment_pilot(treatment_rows)
        goals = read_precision_goals(args.goals) if args.goals else ()
        validate_precision_inputs(
            goals=goals,
            svd_path=args.svd,
            treatments_path=args.treatments,
            freeze_manifest_path=args.freeze_manifest,
            admission_path=args.admission,
        )
        recommendations = build_precision_recommendations(goals, svd_summary, treatment_summary)
        audit = PilotPrecisionAudit(
            svd_plant_rows=svd_plants,
            svd_summary_rows=svd_summary,
            treatment_plant_rows=treatment_plants,
            treatment_summary_rows=treatment_summary,
            precision_rows=recommendations,
        )
        write_pilot_precision_audit(args.output_dir, audit)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
