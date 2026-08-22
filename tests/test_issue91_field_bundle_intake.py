import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_TEMPLATE_TO_BUNDLE = {
    "field_dependency_plant_registry_template.csv": "field_dependency_plant_registry.csv",
    "field_observation_effort_template.csv": "field_observation_effort.csv",
    "field_visitor_contact_manifest_template.csv": "field_visitor_contact_manifest.csv",
    "field_single_visit_pollen_deposition_template.csv": "field_single_visit_pollen_deposition.csv",
    "field_pollination_treatment_template.csv": "field_pollination_treatments.csv",
    "field_mature_fruit_template.csv": "field_mature_fruit.csv",
}


def test_empty_header_only_bundle_runs_full_core_intake_without_inventing_admission(tmp_path):
    bundle = tmp_path / "bundle"
    output = tmp_path / "out"
    bundle.mkdir()
    for template_name, bundle_name in REQUIRED_TEMPLATE_TO_BUNDLE.items():
        shutil.copyfile(ROOT / "templates" / template_name, bundle / bundle_name)

    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/intake_issue91_field_bundle.py"),
            "--bundle-dir",
            str(bundle),
            "--output-dir",
            str(output),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr

    summary = json.loads((output / "intake_summary.json").read_text(encoding="utf-8"))
    assert summary["status"] == "raw_frozen_structural_incomplete"
    assert summary["structural_summary"]["populations"] == 0
    assert summary["admission_summary"]["n_populations_passing_dispersion_gate"] == 0
    assert summary["precision_thresholds_locked"] is False
    assert summary["confirmatory_adequacy_inferred"] is False
    assert summary["optional_reports"]["fdq"]["requested"] is False
    assert summary["optional_reports"]["parentage"]["requested"] is False

    assert (output / "freeze/effective_dependency_raw_v1.json").is_file()
    assert (output / "structural/summary.json").is_file()
    assert (output / "admission/admission.json").is_file()


def test_prediction_freeze_is_recorded_as_pre_outcome_provenance(tmp_path):
    bundle = tmp_path / "bundle"
    output = tmp_path / "out"
    bundle.mkdir()
    for template_name, bundle_name in REQUIRED_TEMPLATE_TO_BUNDLE.items():
        shutil.copyfile(ROOT / "templates" / template_name, bundle / bundle_name)

    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/intake_issue91_field_bundle.py"),
            "--bundle-dir",
            str(bundle),
            "--output-dir",
            str(output),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    summary = json.loads((output / "intake_summary.json").read_text(encoding="utf-8"))
    freeze = summary["prediction_freeze"]
    assert freeze["status"] == "prediction_structure_frozen_before_real_field_bundle_no_decision_thresholds_locked"
    assert freeze["real_issue91_field_rows_inspected_before_freeze"] is False
    assert len(freeze["sha256"]) == 64


def test_optional_fdq_and_parentage_are_nonblocking_by_contract():
    script = (ROOT / "scripts/intake_issue91_field_bundle.py").read_text(encoding="utf-8")
    assert '"blocking_for_core_dependency": False' in script
    assert "optional_strict_fdq_audit" in script
    assert "optional_parentage_audit" in script
