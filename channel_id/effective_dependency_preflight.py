"""File-level preflight for the direct effective-dependency field bundle."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Mapping

CHANNEL_TEMPLATES = {
    "plants": "field_dependency_plant_registry_template.csv",
    "effort": "field_observation_effort_template.csv",
    "visits": "field_visitor_contact_manifest_template.csv",
    "svd": "field_single_visit_pollen_deposition_template.csv",
    "treatments": "field_pollination_treatment_template.csv",
    "fruits": "field_mature_fruit_template.csv",
}


def _shape(path: Path) -> tuple[list[str], int]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        if not header or any(not cell.strip() for cell in header):
            raise ValueError(f"invalid header: {path}")
        rows = sum(1 for row in reader if any(cell.strip() for cell in row))
    return header, rows


def build_preflight(paths: Mapping[str, Path], templates_dir: Path) -> dict[str, object]:
    channels = []
    for name, template_name in CHANNEL_TEMPLATES.items():
        path = paths[name]
        if not path.is_file():
            channels.append({"channel": name, "status": "missing_file", "n_data_rows": None})
            continue
        try:
            observed, n_rows = _shape(path)
            expected, _ = _shape(templates_dir / template_name)
        except (OSError, ValueError, StopIteration) as error:
            channels.append({"channel": name, "status": "invalid_csv", "n_data_rows": None, "error": str(error)})
            continue
        missing = [column for column in expected if column not in observed]
        channels.append({
            "channel": name,
            "status": "schema_invalid" if missing else ("header_only" if n_rows == 0 else "rows_present"),
            "n_data_rows": n_rows,
            "missing_required_columns": missing,
            "extra_columns": [column for column in observed if column not in expected],
        })

    states = [row["status"] for row in channels]
    if "missing_file" in states:
        status = "required_files_missing"
    elif any(state in {"invalid_csv", "schema_invalid"} for state in states):
        status = "schema_invalid"
    elif all(state == "header_only" for state in states):
        status = "template_only_no_field_rows"
    elif "header_only" in states:
        status = "partial_required_channels"
    else:
        status = "candidate_real_field_bundle_present"
    return {
        "schema_version": "effective_dependency_field_preflight_v1",
        "status": status,
        "channels": channels,
        "freeze_recommended": status in {"partial_required_channels", "candidate_real_field_bundle_present"},
        "structural_audit_recommended": status == "candidate_real_field_bundle_present",
        "analysis_admission_opened": False,
        "pilot_dispersion_opened": False,
        "confirmatory_adequacy_opened": False,
        "claim_boundary": "Row presence alone is not linkage, validity, independence, control adequacy, effectiveness, dependency, precision, or causation.",
    }
