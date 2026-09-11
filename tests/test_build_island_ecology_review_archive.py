import json
import zipfile
from pathlib import Path

import pytest

from scripts.build_island_ecology_review_archive import (
    ANONYMOUS_MANUSCRIPT_NAME,
    ANONYMOUS_SI_NAME,
    CORE_REVIEW_FILES,
    DEFAULT_DENY_TOKENS,
    SOURCE_MANUSCRIPT,
    build_archive,
    find_denied_tokens,
    validate_files,
)


def test_review_archive_file_list_excludes_identity_files_and_includes_active_and_historical_locks():
    assert "docs/ISLAND_ECOLOGY_TITLE_PAGE_TEMPLATE_20260824.md" not in CORE_REVIEW_FILES
    assert SOURCE_MANUSCRIPT not in CORE_REVIEW_FILES
    assert all("TITLE_PAGE" not in path.upper() for path in CORE_REVIEW_FILES)
    assert "zuizui0223" in DEFAULT_DENY_TOKENS
    assert SOURCE_MANUSCRIPT == "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
    assert ANONYMOUS_MANUSCRIPT_NAME == "MANUSCRIPT.md"
    assert ANONYMOUS_SI_NAME == "SUPPORTING_INFORMATION.md"
    assert "docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md" in CORE_REVIEW_FILES
    assert "docs/CHAPTER2_THREE_RESULT_NARRATIVE_LOCK_20260908.md" in CORE_REVIEW_FILES
    assert "data/results/wanshan_yongxing/effect_rows.json" in CORE_REVIEW_FILES
    assert "data/results/ogasawara/context_analysis/effect_rows.json" in CORE_REVIEW_FILES
    assert "data/design/chapter2_oikos_submission_manifest_20260831.json" in CORE_REVIEW_FILES
    assert "data/results/chapter2_realized_richness_matching_decision_20260907.json" in CORE_REVIEW_FILES


def test_review_archive_source_files_pass_default_identity_scan():
    records = validate_files(CORE_REVIEW_FILES, DEFAULT_DENY_TOKENS)
    assert len(records) == len(CORE_REVIEW_FILES)
    assert all(len(record["sha256"]) == 64 for record in records)


def test_review_archive_builds_with_mechanism_mainline_claim_boundary(tmp_path: Path):
    output = tmp_path / "review.zip"
    path = build_archive(output)
    assert path == output
    assert output.exists()

    with zipfile.ZipFile(output) as archive:
        names = set(archive.namelist())
        assert "REVIEW_ARCHIVE_MANIFEST.json" in names
        assert "README_REVIEW_ARCHIVE.md" in names
        assert ANONYMOUS_MANUSCRIPT_NAME in names
        assert ANONYMOUS_SI_NAME in names
        assert SOURCE_MANUSCRIPT not in names
        assert set(CORE_REVIEW_FILES).issubset(names)
        assert not any("title_page" in name.lower() for name in names)

        manuscript = archive.read(ANONYMOUS_MANUSCRIPT_NAME).decode("utf-8")
        lower = manuscript.lower()
        assert "conditional response geometry" in lower
        assert "realized richness differences therefore help position the ensemble mean regime" in lower
        assert "ordering of response determinants is itself regime dependent" in lower
        assert "deterministic mean-field kernel contrast was all-positive" in lower
        assert "55.84%" in manuscript and "12.72%" in manuscript
        assert "optional future validation programme" in lower
        assert "result 1—mechanistic prediction" not in lower
        assert "result 2—real-world exposure" not in lower
        assert "result 3—biological consequence" not in lower

        supporting = archive.read(ANONYMOUS_SI_NAME).decode("utf-8")
        support_lower = supporting.lower()
        assert "69.34–80.17%" in supporting
        assert "partner arrival/replacement `2/25`" in supporting
        assert "exact realized-richness matching hard control" in support_lower
        assert "cell-level simulation variation" not in support_lower

        manifest = json.loads(archive.read("REVIEW_ARCHIVE_MANIFEST.json"))
        assert manifest["author_identity_included"] is False
        assert manifest["title_page_included"] is False
        assert manifest["journal_target"] == "Oikos"
        assert manifest["article_type"] == "Research Paper"
        assert manifest["oikos_data_code_review_ready"] is True
        assert manifest["scientific_state"] == "synthetic_conditional_response_geometry_with_regime_dependent_determinant_ordering"
        assert manifest["mechanism_mainline_included_fail_closed"] is True
        assert manifest["three_result_reframe_active"] is False
        assert manifest["realized_richness_reframe_included_fail_closed"] is True
        assert manifest["field_e3_e4_required_for_current_paper"] is False
        assert manifest["relational_robustness_audit_included"] is True
        assert manifest["realized_richness_hard_control_included"] is True
        assert manifest["interaction_kernel_identity_audit_included"] is True
        assert manifest["external_prediction_readiness_audit_included"] is True
        assert "system-size" in manifest["claim_boundary"].lower()
        assert "not required validation" in manifest["claim_boundary"].lower()

        readme = archive.read("README_REVIEW_ARCHIVE.md").decode("utf-8")
        readme_lower = readme.lower()
        assert "oikos double-anonymous review" in readme_lower
        assert "conditional response geometry" in readme_lower
        assert "scale-dependent determinant ordering" in readme_lower
        assert "55.84%" in readme and "12.72%" in readme
        assert "optional future validation programme" in readme_lower
        assert "no entry meets the full joint outcome-independent historical transition contract" in readme_lower


def test_identity_scan_detects_explicit_token(tmp_path: Path):
    path = tmp_path / "identity.txt"
    path.write_text("author handle: ExampleSecretToken", encoding="utf-8")
    assert find_denied_tokens(path, ("examplesecrettoken",)) == ("examplesecrettoken",)


def test_archive_builder_rejects_additional_identity_token_present_in_review_file(tmp_path: Path):
    with pytest.raises(ValueError):
        build_archive(tmp_path / "should-not-build.zip", extra_deny_tokens=("Oikos",))
