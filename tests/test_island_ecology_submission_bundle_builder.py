import json
import zipfile
from pathlib import Path

import pytest

import scripts.build_island_ecology_submission_bundle as bundle

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "data/design/island_ecology_submission_metadata_template.json"
SOURCE_MANUSCRIPT = "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
SUBMISSION_MANUSCRIPT = "MANUSCRIPT.rtf"
SUBMISSION_SI = "SUPPORTING_INFORMATION.rtf"


def completed_metadata() -> dict:
    metadata = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    metadata["authors"] = [{
        "full_name": "Example Author",
        "affiliations": ["Example Institute, Example University, Example City, Example Country"],
        "email": "example@example.org",
        "postal_address": "Example Institute, Example City, Example Country",
        "orcid": "0000-0000-0000-0000",
    }]
    metadata["corresponding_author_index"] = 0
    metadata["significance_prior_work_context"] = "This manuscript extends prior work by the submitting author and independent published work on island interaction reorganization."
    metadata["planned_public_repository"] = "Dryad Digital Repository"
    metadata["acknowledgements"] = "None"
    metadata["funding"] = "None"
    metadata["author_contributions"] = "Example Author conceived the study, performed the analyses and wrote the manuscript."
    metadata["inclusion_statement"] = "This study used secondary literature and simulation data and involved no new local field data collection."
    metadata["conflict_of_interest"] = "The author declares no conflict of interest."
    metadata["ethics_statement_confirmed"] = True
    for key in metadata["submission_declarations"]:
        metadata["submission_declarations"][key] = True
    return metadata


def test_current_scientific_gate_uses_unified_model3_lock():
    gate = bundle.validate_scientific_gate()
    assert gate["status"] == "active_chapter2_unified_model3_with_bridge_gates"
    assert gate["unification_audit"]["conclusion"] == "success"
    assert gate["unification_audit"]["decision"] == "model2_not_required_as_independent_biological_mechanism_but_not_yet_redundant_for_all_original_controls"
    assert gate["submission_state"]["new_field_data_required"] is False
    assert gate["submission_state"]["model3_bridge_campaign_required_for_full_original_ch2_equivalence"] is True


def test_submission_bundle_fails_closed_when_scientific_gate_is_missing(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(bundle, "UNIFIED_MODEL3_LOCK", tmp_path / "missing-gate.json")
    with pytest.raises(ValueError, match="unified Model 3 scientific lock is missing"):
        bundle.validate_scientific_gate()


def test_submission_bundle_prioritizes_open_bridge_gate_before_metadata(tmp_path: Path):
    with pytest.raises(ValueError, match="original-Chapter-2 bridge controls are not complete"):
        bundle.build_submission_bundle(TEMPLATE, tmp_path / "bundle.zip")


def test_submission_bundle_rejects_non_oikos_route(tmp_path: Path):
    metadata = completed_metadata()
    metadata["journal"] = "Journal of Ecology"
    metadata_path = tmp_path / "metadata.json"
    metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
    with pytest.raises(ValueError, match="original-Chapter-2 bridge controls are not complete"):
        bundle.build_submission_bundle(metadata_path, tmp_path / "bundle.zip")


def test_submission_bundle_refuses_while_original_ch2_bridge_controls_are_open(tmp_path: Path):
    metadata_path = tmp_path / "metadata.json"
    metadata_path.write_text(json.dumps(completed_metadata()), encoding="utf-8")
    with pytest.raises(ValueError, match="original-Chapter-2 bridge controls are not complete"):
        bundle.build_submission_bundle(metadata_path, tmp_path / "bundle.zip")
