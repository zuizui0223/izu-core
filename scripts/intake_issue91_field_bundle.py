#!/usr/bin/env python3
"""Run the frozen Issue #91 field-bundle intake in the required gate order.

This is orchestration only. It does not redefine any scientific estimand or
admission rule. The command validates that the prospective prediction freeze is
still pre-outcome, freezes the raw six-channel bundle, runs the existing
structural dependency audit, runs the existing plant-level admission/dispersion
audit, and optionally audits parentage and strict FDQ when those inputs exist.

Core dependency intake is intentionally independent of optional FDQ/parentage
success. Optional-channel failures are reported but do not manufacture a core
failure or silently repair missing data.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Mapping

ROOT = Path(__file__).resolve().parents[1]
PREDICTION_FREEZE = ROOT / "data/design/issue91_propagation_buffering_prediction_freeze.json"

REQUIRED_FILES = {
    "plants": "field_dependency_plant_registry.csv",
    "effort": "field_observation_effort.csv",
    "visits": "field_visitor_contact_manifest.csv",
    "svd": "field_single_visit_pollen_deposition.csv",
    "treatments": "field_pollination_treatments.csv",
    "fruits": "field_mature_fruit.csv",
}
OPTIONAL_DEFAULT_FILES = {
    "seeds_parentage": "field_seed_parentage.csv",
    "traits": "field_pollinator_trait_lookup.csv",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def validate_prediction_freeze(path: Path = PREDICTION_FREEZE) -> dict[str, object]:
    payload = load_json(path)
    inspected = payload.get("inputs_inspected_before_freeze")
    boundary = payload.get("pilot_vs_confirmatory_boundary")
    if not isinstance(inspected, dict) or not isinstance(boundary, dict):
        raise ValueError("Issue #91 prediction freeze lacks required gate sections")
    if inspected.get("real_issue91_field_rows") is not False:
        raise ValueError("prediction freeze is not certified as preceding real Issue #91 field rows")
    if inspected.get("pilot_dispersion") is not False:
        raise ValueError("prediction freeze is not certified as preceding pilot dispersion")
    if boundary.get("decision_thresholds_locked_now") is not False:
        raise ValueError("prediction freeze unexpectedly locks decision thresholds before pilot dispersion")
    expected_status = "prediction_structure_frozen_before_real_field_bundle_no_decision_thresholds_locked"
    if payload.get("status") != expected_status:
        raise ValueError(f"unexpected prediction-freeze status: {payload.get('status')!r}")
    return payload


def resolve_paths(
    bundle_dir: Path,
    *,
    seeds_parentage: Path | None = None,
    traits: Path | None = None,
    geometry: Path | None = None,
    calibration: Path | None = None,
) -> dict[str, Path | None]:
    paths: dict[str, Path | None] = {
        key: bundle_dir / name for key, name in REQUIRED_FILES.items()
    }
    for key, supplied in (("seeds_parentage", seeds_parentage), ("traits", traits)):
        if supplied is not None:
            paths[key] = supplied
        else:
            candidate = bundle_dir / OPTIONAL_DEFAULT_FILES[key]
            paths[key] = candidate if candidate.is_file() else None
    paths["geometry"] = geometry
    paths["calibration"] = calibration
    return paths


def run_step(label: str, command: list[str]) -> dict[str, object]:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "label": label,
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "success": completed.returncode == 0,
    }


def core_status(structural: Mapping[str, object], admission: Mapping[str, object]) -> str:
    structurally_complete = int(structural.get("structurally_complete_populations", 0) or 0)
    dispersion_complete = int(admission.get("n_populations_passing_dispersion_gate", 0) or 0)
    if structurally_complete <= 0:
        return "raw_frozen_structural_incomplete"
    if dispersion_complete <= 0:
        return "structural_complete_pilot_dispersion_not_yet_estimable"
    return "pilot_dispersion_estimable_precision_thresholds_still_unlocked"


def write_summary(output_dir: Path, summary: Mapping[str, object]) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "intake_summary.json"
    path.write_text(json.dumps(dict(summary), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--seeds-parentage", type=Path)
    parser.add_argument("--traits", type=Path)
    parser.add_argument("--geometry", type=Path)
    parser.add_argument("--calibration", type=Path)
    args = parser.parse_args()

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    steps: list[dict[str, object]] = []

    try:
        prediction = validate_prediction_freeze()
    except (OSError, ValueError, json.JSONDecodeError) as error:
        summary = {
            "schema_version": "1.0",
            "status": "prediction_freeze_validation_failed",
            "failed_step": "prediction_freeze",
            "error": str(error),
            "precision_thresholds_locked": False,
            "confirmatory_adequacy_inferred": False,
        }
        print(write_summary(output_dir, summary))
        raise SystemExit(2) from error

    paths = resolve_paths(
        args.bundle_dir,
        seeds_parentage=args.seeds_parentage,
        traits=args.traits,
        geometry=args.geometry,
        calibration=args.calibration,
    )

    freeze_path = output_dir / "freeze/effective_dependency_raw_v1.json"
    freeze_cmd = [
        sys.executable,
        str(ROOT / "scripts/freeze_effective_dependency_field_bundle.py"),
    ]
    for key in ("plants", "effort", "visits", "svd", "treatments", "fruits"):
        freeze_cmd.extend(["--" + key.replace("_", "-"), str(paths[key])])
    for key in ("seeds_parentage", "geometry", "calibration"):
        path = paths.get(key)
        if path is not None:
            freeze_cmd.extend(["--" + key.replace("_", "-"), str(path)])
    freeze_cmd.extend(["--output", str(freeze_path)])
    freeze_step = run_step("raw_freeze", freeze_cmd)
    steps.append(freeze_step)
    if not freeze_step["success"]:
        summary = {
            "schema_version": "1.0",
            "status": "raw_freeze_failed",
            "failed_step": "raw_freeze",
            "prediction_freeze": {
                "path": str(PREDICTION_FREEZE),
                "sha256": sha256_file(PREDICTION_FREEZE),
                "status": prediction["status"],
            },
            "steps": steps,
            "precision_thresholds_locked": False,
            "confirmatory_adequacy_inferred": False,
        }
        print(write_summary(output_dir, summary))
        raise SystemExit(3)

    structural_dir = output_dir / "structural"
    structural_cmd = [
        sys.executable,
        str(ROOT / "scripts/audit_effective_pollinator_dependency.py"),
        "--plants", str(paths["plants"]),
        "--effort", str(paths["effort"]),
        "--visits", str(paths["visits"]),
        "--svd", str(paths["svd"]),
        "--treatments", str(paths["treatments"]),
        "--fruits", str(paths["fruits"]),
        "--output-dir", str(structural_dir),
    ]
    structural_step = run_step("structural_dependency_audit", structural_cmd)
    steps.append(structural_step)
    if not structural_step["success"]:
        summary = {
            "schema_version": "1.0",
            "status": "structural_dependency_audit_failed",
            "failed_step": "structural_dependency_audit",
            "prediction_freeze": {
                "path": str(PREDICTION_FREEZE),
                "sha256": sha256_file(PREDICTION_FREEZE),
                "status": prediction["status"],
            },
            "freeze_manifest": str(freeze_path),
            "steps": steps,
            "precision_thresholds_locked": False,
            "confirmatory_adequacy_inferred": False,
        }
        print(write_summary(output_dir, summary))
        raise SystemExit(4)

    admission_path = output_dir / "admission/admission.json"
    admission_cmd = [
        sys.executable,
        str(ROOT / "scripts/audit_effective_dependency_admission.py"),
        "--plants", str(paths["plants"]),
        "--svd", str(paths["svd"]),
        "--treatments", str(paths["treatments"]),
        "--output", str(admission_path),
    ]
    admission_step = run_step("pilot_dispersion_admission_audit", admission_cmd)
    steps.append(admission_step)
    if not admission_step["success"]:
        summary = {
            "schema_version": "1.0",
            "status": "pilot_dispersion_admission_audit_failed",
            "failed_step": "pilot_dispersion_admission_audit",
            "prediction_freeze": {
                "path": str(PREDICTION_FREEZE),
                "sha256": sha256_file(PREDICTION_FREEZE),
                "status": prediction["status"],
            },
            "freeze_manifest": str(freeze_path),
            "structural_summary": str(structural_dir / "summary.json"),
            "steps": steps,
            "precision_thresholds_locked": False,
            "confirmatory_adequacy_inferred": False,
        }
        print(write_summary(output_dir, summary))
        raise SystemExit(5)

    optional_reports: dict[str, object] = {}
    parentage = paths.get("seeds_parentage")
    if parentage is not None:
        parentage_path = output_dir / "parentage/summary.json"
        step = run_step(
            "optional_parentage_audit",
            [
                sys.executable,
                str(ROOT / "scripts/audit_effective_dependency_parentage.py"),
                "--fruits", str(paths["fruits"]),
                "--parentage", str(parentage),
                "--output", str(parentage_path),
            ],
        )
        steps.append(step)
        optional_reports["parentage"] = {
            "requested": True,
            "success": step["success"],
            "path": str(parentage_path) if step["success"] else None,
            "blocking_for_core_dependency": False,
        }
    else:
        optional_reports["parentage"] = {
            "requested": False,
            "success": None,
            "path": None,
            "blocking_for_core_dependency": False,
        }

    traits = paths.get("traits")
    if traits is not None:
        fdq_dir = output_dir / "fdq"
        step = run_step(
            "optional_strict_fdq_audit",
            [
                sys.executable,
                str(ROOT / "scripts/audit_field_fdq_exposure.py"),
                "--plants", str(paths["plants"]),
                "--effort", str(paths["effort"]),
                "--visits", str(paths["visits"]),
                "--traits", str(traits),
                "--output-dir", str(fdq_dir),
            ],
        )
        steps.append(step)
        optional_reports["fdq"] = {
            "requested": True,
            "success": step["success"],
            "path": str(fdq_dir / "summary.json") if step["success"] else None,
            "blocking_for_core_dependency": False,
        }
    else:
        optional_reports["fdq"] = {
            "requested": False,
            "success": None,
            "path": None,
            "blocking_for_core_dependency": False,
        }

    freeze = load_json(freeze_path)
    structural = load_json(structural_dir / "summary.json")
    admission = load_json(admission_path)
    status = core_status(structural, admission)
    summary = {
        "schema_version": "1.0",
        "status": status,
        "bundle_dir": str(args.bundle_dir),
        "prediction_freeze": {
            "path": str(PREDICTION_FREEZE),
            "sha256": sha256_file(PREDICTION_FREEZE),
            "status": prediction["status"],
            "real_issue91_field_rows_inspected_before_freeze": prediction["inputs_inspected_before_freeze"]["real_issue91_field_rows"],
        },
        "raw_freeze": {
            "path": str(freeze_path),
            "bundle_fingerprint_sha256": freeze["bundle_fingerprint_sha256"],
        },
        "structural_summary": structural,
        "admission_summary": admission,
        "optional_reports": optional_reports,
        "steps": steps,
        "precision_thresholds_locked": False,
        "confirmatory_adequacy_inferred": False,
        "next_gate": (
            "If pilot between-plant dispersion is not estimable, collect additional independent-plant records without changing the frozen interpretation rules. "
            "If dispersion is estimable, use pilot variance/coverage/loss to lock a biologically meaningful precision target before confirmatory planning."
        ),
        "claim_boundary": (
            "Successful intake establishes raw provenance and applies existing structural/dispersion gates only. "
            "It does not identify historical pollinator-loss causation, final predictor reliability, a universal buffering mechanism, or a confirmatory sample size."
        ),
    }
    summary_path = write_summary(output_dir, summary)
    print(summary_path)


if __name__ == "__main__":
    main()
