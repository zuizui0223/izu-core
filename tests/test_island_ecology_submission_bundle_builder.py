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
REFERENCE_LIST = "REFERENCE_LIST.rtf"


def completed_metadata() -> dict:
    metadata = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    metadata["authors"] = [
        {
            "full_name": "Example Author",
            "affiliations": ["Example Institute, Example University, Example City, Example Country"],
            "email": "example@example.org",
            "postal_address": "Example Institute, Example City, Example Country",
            "orcid": "0000-0000-0000-0000",
        }
    ]
    metadata["corresponding_author_index"] = 0
    metadata["significance_prior_work_context"] = "This manuscript extends prior work by the submitting author and independent published work on island interaction reorganization."
    metadata["planned_public_repository"] = "Dryad Digital Repository"
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


def test_submission_bundle_routes_upload_ready_oikos_rtf_after_gate_closure(tmp_path: Path, monkeypatch):
    relational_inputs = tmp_path / "chapter2_manuscript_figure_inputs_relational_20260831.json"

    def fake_build_figures() -> dict:
        relational_inputs.write_text(json.dumps({"status": "test-generated"}), encoding="utf-8")
        return {"figure_outputs": []}

    monkeypatch.setattr(bundle, "RELATIONAL_FIGURE_INPUTS", relational_inputs)
    monkeypatch.setattr(bundle, "build_figures", fake_build_figures)

    def fake_review_archive(path: Path) -> Path:
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("README_REVIEW_ARCHIVE.md", "anonymous relational-response review archive\n")
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
            "REFERENCE_LIST.rtf",
            "TITLE_PAGE.rtf",
            "COVER_LETTER.rtf",
            "SIGNIFICANCE_STATEMENT.rtf",
            "SUBMISSION_STATEMENTS.rtf",
            "anonymous_review_archive.zip",
            "SUBMISSION_BUNDLE_MANIFEST.json",
        ):
            assert name in names
        assert "MANUSCRIPT.md" not in names
        assert "TITLE_PAGE.md" not in names
        assert "data/design/chapter2_oikos_submission_manifest_20260831.json" in names
        assert "data/results/chapter2_relational_robustness_audit_frozen_20260831.json" in names
        assert bundle.RELATIONAL_FIGURE_INPUTS_ARCNAME in names
        assert SOURCE_MANUSCRIPT not in names

        manuscript = archive.read(SUBMISSION_MANUSCRIPT).decode("utf-8")
        assert manuscript.startswith("{\\rtf1")
        assert "\\sl480\\slmult1" in manuscript
        assert "\\linemod1" in manuscript
        assert "\\linecont" in manuscript
        assert "fldinst PAGE" in manuscript
        assert "\\page" in manuscript
        lower = manuscript.lower()
        assert "response direction is therefore relational rather than intrinsic" in lower
        assert "53/96" in manuscript
        assert "null-corrected matching" in lower
        assert "supporting information" in lower
        assert "42 research entries across 37 exact geographic labels" in lower
        assert "cyclamen creticum" in lower
        assert "trinidad and tobago" in lower
        assert "campanula uniflora" in lower
        assert "(appendix)" not in lower
        assert "fig. s" not in lower
        assert "dissertation" not in lower
        assert "chapter 1" not in lower
        assert "chapter 2" not in lower
        assert "chapter 3" not in lower
        assert "campanula microdonta" not in lower
        assert "docs/island_ecology_research_article_reference_ledger_20260827.md" not in lower

        supporting = archive.read(SUBMISSION_SI).decode("utf-8")
        assert supporting.startswith("{\\rtf1")
        support_lower = supporting.lower()
        assert "69.34" in supporting and "80.17" in supporting
        assert "partner arrival/replacement" in supporting
        assert "2/25" in supporting
        assert "cell-level simulation variation" not in support_lower
        assert "chapter 3" not in support_lower

        references = archive.read(REFERENCE_LIST).decode("utf-8")
        assert references.startswith("{\\rtf1")
        refs_lower = references.lower()
        assert "affre, l. & thompson, j.d. (1997)" in refs_lower
        assert "feinsinger, p., wolfe, j.a. & swarm, l.a. (1982)" in refs_lower
        assert "ægisdóttir, h.h. & thórhallsdóttir, t.e. (2006)" in refs_lower
        assert "hiraiwa, m.k. & ushimaru, a. (2024)" in refs_lower
        assert "value-selected breadth source boundary" not in refs_lower
        assert "hygiene decisions" not in refs_lower

        title = archive.read("TITLE_PAGE.rtf").decode("utf-8")
        cover = archive.read("COVER_LETTER.rtf").decode("utf-8")
        significance = archive.read("SIGNIFICANCE_STATEMENT.rtf").decode("utf-8")
        statements = archive.read("SUBMISSION_STATEMENTS.rtf").decode("utf-8")
        for rendered in (title, cover, significance, statements):
            assert rendered.startswith("{\\rtf1")
        assert "Example Author" in title
        assert "0000-0000-0000-0000" in title
        assert "publication in Oikos" in cover
        assert "Dryad Digital Repository" in cover
        assert "Relation to previous work" in significance
        assert "Data archiving statement" in statements
        assert "Ethics statement" in statements

        manifest = json.loads(archive.read("SUBMISSION_BUNDLE_MANIFEST.json"))
        assert manifest["journal"] == "Oikos"
        assert manifest["article_type"] == "Research Paper"
        assert manifest["scientific_state"] == "relational_response_geometry_with_structural_robustness_and_bounded_empirical_resolution"
        assert manifest["manuscript_state"] == "active_20260831_relational_source_rendered_to_oikos_rtf_submission"
        assert manifest["source_manuscript"] == SOURCE_MANUSCRIPT
        assert manifest["submission_manuscript"] == SUBMISSION_MANUSCRIPT
        assert manifest["submission_supporting_information"] == SUBMISSION_SI
        assert manifest["submission_reference_list"] == REFERENCE_LIST
        assert manifest["oikos_upload_format"] == "RTF"
        assert manifest["main_text_double_spaced"] is True
        assert manifest["main_text_continuous_line_numbers"] is True
        assert manifest["main_text_page_numbers"] is True
        assert manifest["introduction_forced_to_page_two"] is True
        assert manifest["corresponding_author_orcid_required"] is True
        assert manifest["planned_public_repository_named"] is True
        assert manifest["significance_prior_work_context_included"] is True
        assert bundle.RELATIONAL_FIGURE_INPUTS_ARCNAME in manifest["files"]
        assert REFERENCE_LIST in manifest["files"]
        assert manifest["oikos_significance_statement_included"] is True
        assert manifest["oikos_submission_statements_included"] is True
        assert manifest["oikos_data_code_ready_for_first_submission"] is True
        assert manifest["submission_manuscript_internal_thesis_language_removed_fail_closed"] is True
        assert manifest["submission_reference_list_generated_from_active_reference_ledger"] is True
        assert manifest["supporting_information_superseded_nonadditivity_wording_removed_fail_closed"] is True
        assert manifest["figures_regenerated_from_frozen_gate_then_relational_overlay"] is True
