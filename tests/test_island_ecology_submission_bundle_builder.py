import json
import zipfile
from pathlib import Path

import pytest

import scripts.build_island_ecology_submission_bundle as bundle

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "data/design/island_ecology_submission_metadata_template.json"
SOURCE_MANUSCRIPT = "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_ACTIVE_DRAFT_V2_20260827.md"
SUBMISSION_MANUSCRIPT = "MANUSCRIPT.md"


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


def test_current_scientific_gate_accepts_conditional_response_geometry_route():
    gate = bundle.validate_scientific_gate()
    assert gate["scientific_model_gate_complete"] is True
    assert gate["research_article_route"] == "candidate_conditional_response_geometry"


def test_submission_bundle_fails_closed_when_scientific_gate_is_missing(tmp_path: Path, monkeypatch):
    missing_gate = tmp_path / "missing-gate.json"
    monkeypatch.setattr(bundle, "REASSESSMENT_GATE", missing_gate)
    with pytest.raises(ValueError, match="scientific reassessment gate is missing"):
        bundle.validate_scientific_gate()


def test_submission_bundle_fails_closed_when_scientific_gate_is_unreadable(tmp_path: Path, monkeypatch):
    gate = tmp_path / "gate.json"
    gate.write_text("{not-json", encoding="utf-8")
    monkeypatch.setattr(bundle, "REASSESSMENT_GATE", gate)
    with pytest.raises(ValueError, match="scientific reassessment gate is unreadable"):
        bundle.validate_scientific_gate()


def test_submission_bundle_rejects_incomplete_scientific_gate(tmp_path: Path, monkeypatch):
    gate = tmp_path / "gate.json"
    gate.write_text(json.dumps({"scientific_model_gate_complete": False}), encoding="utf-8")
    monkeypatch.setattr(bundle, "REASSESSMENT_GATE", gate)
    with pytest.raises(ValueError, match="scientific model gate is not complete"):
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


def test_submission_bundle_routes_oikos_clean_manuscript_after_gate_closure(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(bundle, "build_figures", lambda: {"figure_outputs": []})

    def fake_review_archive(path: Path) -> Path:
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("README_REVIEW_ARCHIVE.md", "anonymous conditional-response review archive\n")
        return path

    monkeypatch.setattr(bundle, "build_review_archive", fake_review_archive)
    metadata_path = tmp_path / "metadata.json"
    metadata_path.write_text(json.dumps(completed_metadata()), encoding="utf-8")
    output = bundle.build_submission_bundle(metadata_path, tmp_path / "bundle.zip")
    assert output.exists()
    with zipfile.ZipFile(output) as archive:
        names = set(archive.namelist())
        assert "TITLE_PAGE.md" in names
        assert "COVER_LETTER.md" in names
        assert "SIGNIFICANCE_STATEMENT.md" in names
        assert "anonymous_review_archive.zip" in names
        assert "SUBMISSION_BUNDLE_MANIFEST.json" in names
        assert "data/design/chapter2_oikos_submission_manifest_20260831.json" in names
        assert SUBMISSION_MANUSCRIPT in names
        assert SOURCE_MANUSCRIPT not in names
        title = archive.read("TITLE_PAGE.md").decode("utf-8")
        cover = archive.read("COVER_LETTER.md").decode("utf-8")
        significance = archive.read("SIGNIFICANCE_STATEMENT.md").decode("utf-8")
        assert "Title page — Oikos" in title
        assert "Example Author" in title
        assert "publication in *Oikos*" in cover
        assert "Significance statement — Oikos" in significance
        manuscript = archive.read(SUBMISSION_MANUSCRIPT).decode("utf-8")
        lower = manuscript.lower()
        assert "null-corrected matching" in lower
        assert "mechanistic resolution" in lower
        assert "dissertation" not in lower
        assert "chapter 1" not in lower
        assert "chapter 2" not in lower
        assert "chapter 3" not in lower
        assert "campanula microdonta" not in lower
        manifest = json.loads(archive.read("SUBMISSION_BUNDLE_MANIFEST.json"))
        assert manifest["journal"] == "Oikos"
        assert manifest["article_type"] == "Research Paper"
        assert manifest["scientific_state"] == "model_gate_closed_mechanistic_response_geometry_with_world_identifiability_and_izu_resolution"
        assert manifest["manuscript_state"] == "active_v2_source_rendered_to_oikos_clean_submission"
        assert manifest["source_manuscript"] == SOURCE_MANUSCRIPT
        assert manifest["submission_manuscript"] == SUBMISSION_MANUSCRIPT
        assert manifest["oikos_significance_statement_included"] is True
        assert manifest["oikos_data_code_ready_for_first_submission"] is True
        assert manifest["submission_manuscript_internal_thesis_language_removed_fail_closed"] is True
        assert manifest["figures_regenerated_fail_closed"] is True
