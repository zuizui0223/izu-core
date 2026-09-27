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


def test_current_scientific_gate_retains_legacy_gate_provenance():
    gate = bundle.validate_scientific_gate()
    assert gate["scientific_model_gate_complete"] is True
    assert gate["research_article_route"] == "candidate_conditional_response_geometry"
    assert gate["realized_richness_reframe_complete"] is True


def test_submission_bundle_fails_closed_when_scientific_gate_is_missing(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(bundle, "REASSESSMENT_GATE", tmp_path / "missing-gate.json")
    with pytest.raises(ValueError, match="scientific reassessment gate is missing"):
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


def test_submission_bundle_routes_unified_model3_oikos_rtf_after_gate_closure(tmp_path: Path, monkeypatch):
    relational_inputs = tmp_path / "chapter2_manuscript_figure_inputs_relational_20260831.json"

    def fake_build_figures() -> dict:
        relational_inputs.write_text(json.dumps({"status": "test-generated"}), encoding="utf-8")
        return {"figure_outputs": []}

    monkeypatch.setattr(bundle, "RELATIONAL_FIGURE_INPUTS", relational_inputs)
    monkeypatch.setattr(bundle, "build_figures", fake_build_figures)

    def fake_review_archive(path: Path) -> Path:
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("README_REVIEW_ARCHIVE.md", "anonymous unified Model 3 review archive\n")
        return path

    monkeypatch.setattr(bundle, "build_review_archive", fake_review_archive)
    metadata_path = tmp_path / "metadata.json"
    metadata_path.write_text(json.dumps(completed_metadata()), encoding="utf-8")
    output = bundle.build_submission_bundle(metadata_path, tmp_path / "bundle.zip")
    assert output.exists()

    with zipfile.ZipFile(output) as archive:
        names = set(archive.namelist())
        for name in (
            "MANUSCRIPT.rtf",
            "SUPPORTING_INFORMATION.rtf",
            "TITLE_PAGE.rtf",
            "COVER_LETTER.rtf",
            "SIGNIFICANCE_STATEMENT.rtf",
            "SUBMISSION_STATEMENTS.rtf",
            "anonymous_review_archive.zip",
            "SUBMISSION_BUNDLE_MANIFEST.json",
        ):
            assert name in names

        manuscript = archive.read(SUBMISSION_MANUSCRIPT).decode("utf-8")
        lower = manuscript.lower()
        assert "fixed-state reproductive assay" in lower
        assert "deterministic genotype-density counterpart" in lower
        assert "finite-population abm" in lower
        assert "real islands occupy different stages of the same response architecture" in lower
        assert "result 1—mechanistic prediction" not in lower

        supporting = archive.read(SUBMISSION_SI).decode("utf-8").lower()
        assert "unified model 3 projection onto real-island evidence" in supporting
        assert "exact realized-richness matching hard control" in supporting

        manifest = json.loads(archive.read("SUBMISSION_BUNDLE_MANIFEST.json"))
        assert manifest["scientific_state"] == "unified_model3_nested_ecoevolutionary_response_with_real_island_layer_confrontation"
        assert manifest["manuscript_state"] == "active_20260927_unified_model3_rendered_to_oikos_rtf_submission"
        assert manifest["mechanism_mainline_narrative"] is True
        assert manifest["three_result_narrative"] is False
        assert manifest["field_e3_e4_required_for_submission"] is False
        assert manifest["real_island_abc_projection_included"] is True
        assert manifest["unified_model3_reduction_audit_complete"] is True
        assert manifest["formal_full_contracts"] == "0_of_25"
        assert manifest["chapter3_direct_phenotype_used_as_validation"] is False
