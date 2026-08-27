import json
import zipfile
from pathlib import Path

import pytest

from scripts.build_island_ecology_review_archive import (
    CORE_REVIEW_FILES,
    DEFAULT_DENY_TOKENS,
    MANUSCRIPT,
    build_archive,
    find_denied_tokens,
    validate_files,
)


def test_review_archive_file_list_excludes_identity_files_and_retired_manuscripts():
    assert "docs/ISLAND_ECOLOGY_TITLE_PAGE_TEMPLATE_20260824.md" not in CORE_REVIEW_FILES
    assert "docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V2_20260824.md" not in CORE_REVIEW_FILES
    assert all("TITLE_PAGE" not in path.upper() for path in CORE_REVIEW_FILES)
    assert "zuizui0223" in DEFAULT_DENY_TOKENS
    assert "data/design/chapter2_conditional_why_diagnostics_freeze_20260827.json" in CORE_REVIEW_FILES
    assert "data/results/chapter2_conditional_why_diagnostics_frozen_20260827.json" in CORE_REVIEW_FILES


def test_review_archive_source_files_pass_default_identity_scan():
    records = validate_files(CORE_REVIEW_FILES, DEFAULT_DENY_TOKENS)
    assert len(records) == len(CORE_REVIEW_FILES)
    assert all(len(record["sha256"]) == 64 for record in records)


def test_review_archive_builds_with_frozen_conditional_why_diagnostics(tmp_path: Path):
    output = tmp_path / "review.zip"
    path = build_archive(output)
    assert path == output
    assert output.exists()

    with zipfile.ZipFile(output) as archive:
        names = set(archive.namelist())
        assert "REVIEW_ARCHIVE_MANIFEST.json" in names
        assert "README_REVIEW_ARCHIVE.md" in names
        assert MANUSCRIPT in names
        assert set(CORE_REVIEW_FILES).issubset(names)
        assert "figures/chapter2/figS2_conditional_why_diagnostics.svg" in names
        assert not any("title_page" in name.lower() for name in names)
        manuscript = archive.read(MANUSCRIPT).decode("utf-8")
        assert "community realization for `80.17%`" in manuscript
        manifest = json.loads(archive.read("REVIEW_ARCHIVE_MANIFEST.json"))
        assert manifest["author_identity_included"] is False
        assert manifest["title_page_included"] is False
        assert manifest["journal_target"] == "Journal of Ecology"
        assert manifest["figures_regenerated_fail_closed"] is True
        assert "conditional-WHY diagnostics" in manifest["claim_boundary"]
        readme = archive.read("README_REVIEW_ARCHIVE.md").decode("utf-8")
        assert "same fixed points, seeds, realization counts and filtering strengths" in readme
        assert "not causal field effects" in readme


def test_identity_scan_detects_explicit_token(tmp_path: Path):
    path = tmp_path / "identity.txt"
    path.write_text("author handle: ExampleSecretToken", encoding="utf-8")
    assert find_denied_tokens(path, ("examplesecrettoken",)) == ("examplesecrettoken",)


def test_archive_builder_rejects_additional_identity_token_present_in_review_file(tmp_path: Path):
    with pytest.raises(ValueError):
        build_archive(tmp_path / "should-not-build.zip", extra_deny_tokens=("Journal of Ecology",))
