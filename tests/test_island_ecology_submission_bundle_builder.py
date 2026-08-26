import json
import zipfile
from pathlib import Path

import pytest

import scripts.build_island_ecology_submission_bundle as bundle

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "data/design/island_ecology_submission_metadata_template.json"
V3 = "docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V3_20260826.md"


def completed_metadata() -> dict:
    metadata = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    metadata["authors"] = [
        {
            "full_name": "Example Author",
            "affiliations": ["Example Institute, Example University, Example City, Example Country"],
            "email": "example@example.org",
            "postal_address": "Example Institute, Example City, Example Country",
        }
    ]
    metadata["corresponding_author_index"] = 0
    metadata["acknowledgements"] = "None"
    metadata["funding"] = "None"
    metadata["author_contributions"] = "Example Author conceived the study, performed the analyses and wrote the manuscript."
    metadata["inclusion_statement"] = "This study used secondary literature and simulation data and involved no new local field data collection."
    metadata["conflict_of_interest"] = "The author declares no conflict of interest."
    for key in metadata["submission_declarations"]:
        metadata["submission_declarations"][key] = True
    return metadata


def test_submission_bundle_is_blocked_by_open_scientific_reassessment_gate(tmp_path: Path):
    metadata_path = tmp_path / "metadata.json"
    metadata_path.write_text(json.dumps(completed_metadata()), encoding="utf-8")
    with pytest.raises(ValueError, match="scientific reassessment gate is open"):
        bundle.build_submission_bundle(metadata_path, tmp_path / "bundle.zip")


def test_submission_bundle_still_fails_closed_on_unresolved_metadata_after_gate_closure(tmp_path: Path, monkeypatch):
    gate = tmp_path / "gate.json"
    gate.write_text(json.dumps({"current_research_article_submission_ready": True}), encoding="utf-8")
    monkeypatch.setattr(bundle, "REASSESSMENT_GATE", gate)
    with pytest.raises(ValueError, match="submission metadata incomplete"):
        bundle.build_submission_bundle(TEMPLATE, tmp_path / "bundle.zip")


def test_submission_bundle_functionality_remains_available_after_scientific_gate_closure(tmp_path: Path, monkeypatch):
    gate = tmp_path / "gate.json"
    gate.write_text(json.dumps({"current_research_article_submission_ready": True}), encoding="utf-8")
    monkeypatch.setattr(bundle, "REASSESSMENT_GATE", gate)

    metadata_path = tmp_path / "metadata.json"
    metadata_path.write_text(json.dumps(completed_metadata()), encoding="utf-8")
    output = bundle.build_submission_bundle(metadata_path, tmp_path / "bundle.zip")
    assert output.exists()
    with zipfile.ZipFile(output) as archive:
        names = set(archive.namelist())
        assert "ISLAND_ECOLOGY_TITLE_PAGE.md" in names
        assert "ISLAND_ECOLOGY_COVER_LETTER.md" in names
        assert "island_ecology_anonymous_review_archive.zip" in names
        assert "SUBMISSION_BUNDLE_MANIFEST.json" in names
        assert V3 in names
        title = archive.read("ISLAND_ECOLOGY_TITLE_PAGE.md").decode("utf-8")
        assert "Example Author" in title
        nested = archive.read("island_ecology_anonymous_review_archive.zip")
        nested_path = tmp_path / "nested.zip"
        nested_path.write_bytes(nested)
        with zipfile.ZipFile(nested_path) as review:
            review_names = set(review.namelist())
            assert V3 in review_names
            assert not any("TITLE_PAGE" in name.upper() for name in review_names)
            assert not any("COVER_LETTER" in name.upper() for name in review_names)
