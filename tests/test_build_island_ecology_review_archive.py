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


def test_review_archive_file_list_excludes_identity_files_and_includes_three_result_sources():
    assert "docs/ISLAND_ECOLOGY_TITLE_PAGE_TEMPLATE_20260824.md" not in CORE_REVIEW_FILES
    assert "docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V2_20260824.md" not in CORE_REVIEW_FILES
    assert SOURCE_MANUSCRIPT not in CORE_REVIEW_FILES
    assert all("TITLE_PAGE" not in path.upper() for path in CORE_REVIEW_FILES)
    assert "zuizui0223" in DEFAULT_DENY_TOKENS
    assert SOURCE_MANUSCRIPT == "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
    assert ANONYMOUS_MANUSCRIPT_NAME == "MANUSCRIPT.md"
    assert ANONYMOUS_SI_NAME == "SUPPORTING_INFORMATION.md"
    assert "docs/CHAPTER2_THREE_RESULT_NARRATIVE_LOCK_20260908.md" in CORE_REVIEW_FILES
    assert "data/results/wanshan_yongxing/effect_rows.json" in CORE_REVIEW_FILES
    assert "data/results/ogasawara/context_analysis/effect_rows.json" in CORE_REVIEW_FILES
    assert "data/design/chapter2_oikos_submission_manifest_20260831.json" in CORE_REVIEW_FILES
    assert "data/results/chapter2_realized_richness_matching_decision_20260907.json" in CORE_REVIEW_FILES


def test_review_archive_source_files_pass_default_identity_scan():
    records = validate_files(CORE_REVIEW_FILES, DEFAULT_DENY_TOKENS)
    assert len(records) == len(CORE_REVIEW_FILES)
    assert all(len(record["sha256"]) == 64 for record in records)


def test_review_archive_builds_with_three_result_claim_boundary(tmp_path: Path):
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
        assert "figures/chapter2/figS2_conditional_why_diagnostics.svg" in names
        assert "figures/chapter2/figS3_external_prediction_readiness.svg" in names
        assert "figures/chapter2/fig1_mechanistic_resolution_funnel.svg" in names
        assert "figures/chapter2/fig3_proximal_why_hierarchy.svg" in names
        assert "figures/chapter2/fig4_global_to_izu_resolution.svg" in names
        assert not any("title_page" in name.lower() for name in names)

        manuscript = archive.read(ANONYMOUS_MANUSCRIPT_NAME).decode("utf-8")
        lower = manuscript.lower()
        assert "result 1—mechanistic prediction" in lower
        assert "result 2—real-world exposure" in lower
        assert "result 3—biological consequence" in lower
        assert "real island systems undergo compositional reorganization beyond richness loss" in lower
        assert "pollinator assemblage turnover was 0.9796" in lower
        assert "matched-plant turnover was 0.6817" in lower
        assert "functional community structure in izu" in lower
        assert "response direction is therefore relational rather than intrinsic" not in lower
        assert "richness reduction is not necessary for mixed response geometry" not in lower
        assert "historical boundary check" in lower
        assert "dissertation" not in lower
        assert "chapter 1" not in lower
        assert "chapter 2" not in lower
        assert "chapter 3" not in lower
        assert "campanula microdonta" in lower

        supporting = archive.read(ANONYMOUS_SI_NAME).decode("utf-8")
        support_lower = supporting.lower()
        assert "69.34–80.17%" in supporting
        assert "partner arrival/replacement `2/25`" in supporting
        assert "exact realized-richness matching hard control" in support_lower
        assert "cell-level simulation variation" not in support_lower
        assert "chapter 3" not in support_lower

        manifest = json.loads(archive.read("REVIEW_ARCHIVE_MANIFEST.json"))
        assert manifest["author_identity_included"] is False
        assert manifest["title_page_included"] is False
        assert manifest["journal_target"] == "Oikos"
        assert manifest["article_type"] == "Research Paper"
        assert manifest["oikos_data_code_review_ready"] is True
        assert manifest["scientific_state"] == "three_result_hierarchical_response_architecture_with_bounded_historical_inference"
        assert manifest["three_result_reframe_included_fail_closed"] is True
        assert manifest["realized_richness_reframe_included_fail_closed"] is True
        assert manifest["result2_external_exposure_rows_included"] is True
        assert manifest["frozen_figures_regenerated_then_realized_richness_overlay"] is True
        assert manifest["relational_robustness_audit_included"] is True
        assert manifest["realized_richness_hard_control_included"] is True
        assert manifest["interaction_kernel_identity_audit_included"] is True
        assert manifest["external_prediction_readiness_audit_included"] is True
        assert manifest["review_manuscript_internal_thesis_language_removed_fail_closed"] is True
        assert manifest["supporting_information_superseded_nonadditivity_wording_removed_fail_closed"] is True
        assert "mechanistic prediction" in manifest["claim_boundary"].lower()
        assert "0/25 full-contract" in manifest["claim_boundary"].lower()

        readme = archive.read("README_REVIEW_ARCHIVE.md").decode("utf-8")
        readme_lower = readme.lower()
        assert "oikos double-anonymous review" in readme_lower
        assert "mechanistic prediction -> real-world compositional exposure -> biological consequence" in readme_lower
        assert "wanshan-yongxing" in readme_lower
        assert "ogasawara" in readme_lower
        assert "no entry meets the full joint outcome-independent historical transition contract" in readme_lower
        assert "not a coequal study objective" in readme_lower


def test_identity_scan_detects_explicit_token(tmp_path: Path):
    path = tmp_path / "identity.txt"
    path.write_text("author handle: ExampleSecretToken", encoding="utf-8")
    assert find_denied_tokens(path, ("examplesecrettoken",)) == ("examplesecrettoken",)


def test_archive_builder_rejects_additional_identity_token_present_in_review_file(tmp_path: Path):
    with pytest.raises(ValueError):
        build_archive(tmp_path / "should-not-build.zip", extra_deny_tokens=("Oikos",))
