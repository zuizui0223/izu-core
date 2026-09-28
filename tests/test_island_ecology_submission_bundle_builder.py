import json
import zipfile
import hashlib
from pathlib import Path

import pytest

import scripts.build_island_ecology_submission_bundle as bundle

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "data/design/island_ecology_submission_metadata_template.json"


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


def test_current_scientific_gate_uses_bridge_complete_unified_model3_lock():
    gate = bundle.validate_scientific_gate()
    assert gate["status"] == "active_chapter2_unified_model3_bridge_complete"
    assert gate["unification_audit"]["conclusion"] == "success"
    assert gate["unification_audit"]["decision"] == "model2_not_required_as_active_scientific_model_or_control_gate"
    assert gate["prospective_bridge"]["status"] == "complete"
    assert gate["prospective_bridge"]["cases_verified"] == 24576
    assert gate["submission_state"]["original_chapter2_controls_closed"] is True
    assert gate["submission_state"]["new_field_data_required"] is False


def test_submission_bundle_fails_closed_when_scientific_gate_is_missing(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(bundle, "UNIFIED_MODEL3_LOCK", tmp_path / "missing-gate.json")
    with pytest.raises(ValueError, match="unified Model 3 scientific lock is missing"):
        bundle.validate_scientific_gate()


def test_submission_bundle_still_fails_closed_on_unresolved_metadata(tmp_path: Path):
    with pytest.raises(ValueError, match="submission metadata incomplete"):
        bundle.build_submission_bundle(TEMPLATE, tmp_path / "bundle.zip")


def test_submission_bundle_rejects_non_oikos_route(tmp_path: Path):
    metadata = completed_metadata()
    metadata["journal"] = "Journal of Ecology"
    metadata_path = tmp_path / "metadata.json"
    metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
    with pytest.raises(ValueError, match="Oikos Research Paper"):
        bundle.build_submission_bundle(metadata_path, tmp_path / "bundle.zip")


def test_submission_bundle_includes_reproducible_natural_atlas(tmp_path: Path, monkeypatch):
    # The unrelated full source archive is already covered separately.
    def small_archive(path):
        with zipfile.ZipFile(path, 'w') as archive:
            archive.writestr('test-fixture.txt', 'test only')
        return path
    monkeypatch.setattr(bundle, 'build_review_archive', small_archive)
    metadata = tmp_path / 'test-only-metadata.json'
    metadata.write_text(json.dumps(completed_metadata()), encoding='utf-8')
    target = bundle.build_submission_bundle(metadata, tmp_path / 'test-only-bundle.zip')
    with zipfile.ZipFile(target) as archive:
        provenance = json.loads(archive.read('natural_island_atlas/provenance.json'))
        atlas = json.loads(archive.read('natural_island_atlas/atlas.json'))
        assert atlas['units']['network_observations'] == 42
        for name, expected in provenance['outputs'].items():
            assert hashlib.sha256(archive.read('natural_island_atlas/' + name)).hexdigest() == expected
