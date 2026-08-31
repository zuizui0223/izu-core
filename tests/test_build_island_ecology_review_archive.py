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


def test_review_archive_file_list_excludes_identity_files_and_retired_manuscripts():
    assert "docs/ISLAND_ECOLOGY_TITLE_PAGE_TEMPLATE_20260824.md" not in CORE_REVIEW_FILES
    assert "docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V2_20260824.md" not in CORE_REVIEW_FILES
    assert SOURCE_MANUSCRIPT not in CORE_REVIEW_FILES
    assert all("TITLE_PAGE" not in path.upper() for path in CORE_REVIEW_FILES)
    assert "zuizui0223" in DEFAULT_DENY_TOKENS
    assert SOURCE_MANUSCRIPT == "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
    assert ANONYMOUS_MANUSCRIPT_NAME == "MANUSCRIPT.md"
    assert ANONYMOUS_SI_NAME == "SUPPORTING_INFORMATION.md"
    assert "data/design/chapter2_oikos_submission_manifest_20260831.json" in CORE_REVIEW_FILES
    assert "data/design/chapter2_conditional_why_diagnostics_freeze_20260827.json" in CORE_REVIEW_FILES
    assert "data/results/chapter2_conditional_why_diagnostics_frozen_20260827.json" in CORE_REVIEW_FILES
    assert "data/design/chapter2_external_prediction_challenge_freeze_20260828.json" in CORE_REVIEW_FILES
    assert "data/design/chapter2_external_prediction_admission_ledger_20260828.csv" in CORE_REVIEW_FILES
    assert "data/results/chapter2_external_prediction_readiness_frozen_20260828.json" in CORE_REVIEW_FILES
    assert "docs/CHAPTER2_INTERACTION_KERNEL_DERIVATION_20260828.md" in CORE_REVIEW_FILES
    assert "data/results/chapter2_interaction_kernel_audit_frozen_20260828.json" in CORE_REVIEW_FILES
    assert "data/design/chapter2_relational_robustness_audit_freeze_20260831.json" in CORE_REVIEW_FILES
    assert "data/results/chapter2_relational_robustness_audit_frozen_20260831.json" in CORE_REVIEW_FILES


def test_review_archive_source_files_pass_default_identity_scan():
    records = validate_files(CORE_REVIEW_FILES, DEFAULT_DENY_TOKENS)
    assert len(records) == len(CORE_REVIEW_FILES)
    assert all(len(record["sha256"]) == 64 for record in records)


def test_review_archive_builds_with_oikos_claim_boundary(tmp_path: Path):
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
        assert "response direction is therefore relational rather than intrinsic" in lower
        assert "53/96" in manuscript
        assert "null-corrected matching" in lower
        assert "non-random partner sorting" in lower
        assert "dissertation" not in lower
        assert "chapter 1" not in lower
        assert "chapter 2" not in lower
        assert "chapter 3" not in lower
        assert "campanula microdonta" not in lower
        supporting = archive.read(ANONYMOUS_SI_NAME).decode("utf-8")
        support_lower = supporting.lower()
        assert "69.34–80.17%" in supporting
        assert "partner arrival/replacement `2/25`" in supporting
        assert "cell-level simulation variation" not in support_lower
        assert "chapter 3" not in support_lower
        manifest = json.loads(archive.read("REVIEW_ARCHIVE_MANIFEST.json"))
        assert manifest["author_identity_included"] is False
        assert manifest["title_page_included"] is False
        assert manifest["journal_target"] == "Oikos"
        assert manifest["article_type"] == "Research Paper"
        assert manifest["oikos_data_code_review_ready"] is True
        assert manifest["frozen_figures_regenerated_then_relational_overlay"] is True
        assert manifest["relational_robustness_audit_included"] is True
        assert manifest["interaction_kernel_identity_audit_included"] is True
        assert manifest["external_prediction_readiness_audit_included"] is True
        assert manifest["review_manuscript_internal_thesis_language_removed_fail_closed"] is True
        assert manifest["supporting_information_superseded_nonadditivity_wording_removed_fail_closed"] is True
        assert "source-state/community-composition" in manifest["claim_boundary"]
        readme = archive.read("README_REVIEW_ARCHIVE.md").decode("utf-8")
        assert "Oikos double-anonymous review" in readme
        assert "relational-robustness audit" in readme.lower()
        assert "not evaluable" in readme
        assert "reviewer inspection at first submission" in readme


def test_identity_scan_detects_explicit_token(tmp_path: Path):
    path = tmp_path / "identity.txt"
    path.write_text("author handle: ExampleSecretToken", encoding="utf-8")
    assert find_denied_tokens(path, ("examplesecrettoken",)) == ("examplesecrettoken",)


def test_archive_builder_rejects_additional_identity_token_present_in_review_file(tmp_path: Path):
    with pytest.raises(ValueError):
        build_archive(tmp_path / "should-not-build.zip", extra_deny_tokens=("Oikos",))
