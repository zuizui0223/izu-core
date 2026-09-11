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


def test_current_scientific_gate_accepts_conditional_response_geometry_route():
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


def test_submission_bundle_routes_mechanism_mainline_oikos_rtf_after_gate_closure(tmp_path: Path, monkeypatch):
    relational_inputs = tmp_path / "chapter2_manuscript_figure_inputs_relational_20260831.json"

    def fake_build_figures() -> dict:
        relational_inputs.write_text(json.dumps({"status": "test-generated"}), encoding="utf-8")
        return {"figure_outputs": []}

    monkeypatch.setattr(bundle, "RELATIONAL_FIGURE_INPUTS", relational_inputs)
    monkeypatch.setattr(bundle, "build_figures", fake_build_figures)

    def fake_review_archive(path: Path) -> Path:
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("README_REVIEW_ARCHIVE.md", "anonymous mechanism-mainline review archive\n")
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
        assert "docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md" in names
        assert "docs/CHAPTER2_THREE_RESULT_NARRATIVE_LOCK_20260908.md" in names
        assert "data/design/chapter2_oikos_submission_manifest_20260831.json" in names
        assert bundle.RELATIONAL_FIGURE_INPUTS_ARCNAME in names
        assert SOURCE_MANUSCRIPT not in names

        manuscript = archive.read(SUBMISSION_MANUSCRIPT).decode("utf-8")
        assert manuscript.startswith("{\\rtf1")
        assert "\\sl480\\slmult1" in manuscript
        assert "\\linemod1" in manuscript
        assert "fldinst PAGE" in manuscript
        lower = manuscript.lower()
        assert "conditional response geometry" in lower
        assert "realized richness differences therefore help position the ensemble mean regime" in lower
        assert "ordering of response determinants is itself regime dependent" in lower
        assert "deterministic mean-field kernel contrast was all-positive" in lower
        assert "optional future validation programme" in lower
        assert "55.84%" in manuscript and "12.72%" in manuscript
        assert "result 1—mechanistic prediction" not in lower
        assert "result 2—real-world exposure" not in lower
        assert "result 3—biological consequence" not in lower

        supporting = archive.read(SUBMISSION_SI).decode("utf-8")
        assert supporting.startswith("{\\rtf1")
        support_lower = supporting.lower()
        assert "exact realized-richness matching hard control" in support_lower
        assert "finite-community system-size audit" in support_lower
        assert "regime-dependent response hierarchy" in support_lower
        assert "cell-level simulation variation" not in support_lower

        manifest = json.loads(archive.read("SUBMISSION_BUNDLE_MANIFEST.json"))
        assert manifest["journal"] == "Oikos"
        assert manifest["article_type"] == "Research Paper"
        assert manifest["scientific_state"] == "synthetic_conditional_response_geometry_with_regime_dependent_determinant_ordering"
        assert manifest["manuscript_state"] == "active_20260911_mechanism_mainline_rendered_to_oikos_rtf_submission"
        assert manifest["mechanism_mainline_narrative"] is True
        assert manifest["three_result_narrative"] is False
        assert manifest["field_e3_e4_required_for_submission"] is False
        assert manifest["system_size_rank_crossover"]["starting_exceeds_community_from_k4"] == "6_of_6_seeds"
        assert manifest["system_size_rank_crossover"]["natural_threshold_claimed"] is False
        assert manifest["izu_e3_e4_status"] == "future_optional_validation_not_completion_gate"
        assert manifest["source_manuscript"] == SOURCE_MANUSCRIPT
        assert manifest["submission_manuscript"] == SUBMISSION_MANUSCRIPT
        assert manifest["submission_supporting_information"] == SUBMISSION_SI
        assert manifest["formal_full_contracts"] == "0_of_25"
        assert manifest["realized_richness_mean_geometry"] == "all_positive_in_6_of_6_matching_seeds"
        assert manifest["chapter3_direct_phenotype_used_as_validation"] is False
        assert bundle.RELATIONAL_FIGURE_INPUTS_ARCNAME in manifest["files"]
