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
    assert "docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md" in CORE_REVIEW_FILES
    assert "docs/CHAPTER2_THREE_RESULT_NARRATIVE_LOCK_20260908.md" in CORE_REVIEW_FILES


def test_review_archive_source_files_pass_default_identity_scan():
    records = validate_files(CORE_REVIEW_FILES, DEFAULT_DENY_TOKENS)
    assert len(records) == len(CORE_REVIEW_FILES)
    assert all(len(record["sha256"]) == 64 for record in records)


def test_review_archive_builds_with_unified_model3_claim_boundary(tmp_path: Path):
    output = tmp_path / "review.zip"
    path = build_archive(output)
    assert path == output and output.exists()

    with zipfile.ZipFile(output) as archive:
        names = set(archive.namelist())
        assert "REVIEW_ARCHIVE_MANIFEST.json" in names
        assert "README_REVIEW_ARCHIVE.md" in names
        assert ANONYMOUS_MANUSCRIPT_NAME in names
        assert ANONYMOUS_SI_NAME in names
        assert SOURCE_MANUSCRIPT not in names

        manuscript = archive.read(ANONYMOUS_MANUSCRIPT_NAME).decode("utf-8")
        lower = manuscript.lower()
        assert "fixed-state reproductive assay" in lower
        assert "deterministic genotype-density counterpart" in lower
        assert "finite-population abm" in lower
        assert "real islands occupy different stages of the same response architecture" in lower
        assert "the main natural-data gap" in lower
        assert "result 1—mechanistic prediction" not in lower

        supporting = archive.read(ANONYMOUS_SI_NAME).decode("utf-8")
        support_lower = supporting.lower()
        assert "unified model 3 projection onto real-island evidence" in support_lower
        assert "exact realized-richness matching hard control" in support_lower
        assert "cell-level simulation variation" not in support_lower

        manifest = json.loads(archive.read("REVIEW_ARCHIVE_MANIFEST.json"))
        assert manifest["scientific_state"] == "unified_model3_nested_ecoevolutionary_response_with_real_island_layer_confrontation"
        assert manifest["mechanism_mainline_included_fail_closed"] is True
        assert manifest["three_result_reframe_active"] is False
        assert manifest["field_e3_e4_required_for_current_paper"] is False
        boundary = manifest["claim_boundary"].lower()
        assert "nested model 3" in boundary
        assert "inherited longitudinal b layer" in boundary

        readme = archive.read("README_REVIEW_ARCHIVE.md").decode("utf-8").lower()
        assert "fixed-state reproductive selection" in readme
        assert "deterministic genotype-density inheritance" in readme
        assert "inherited longitudinal b layer" in readme

def test_identity_scan_detects_explicit_token(tmp_path: Path):
    path = tmp_path / "identity.txt"
    path.write_text("author handle: ExampleSecretToken", encoding="utf-8")
    assert find_denied_tokens(path, ("examplesecrettoken",)) == ("examplesecrettoken",)


def test_archive_builder_rejects_additional_identity_token_present_in_review_file(tmp_path: Path):
    with pytest.raises(ValueError):
        build_archive(tmp_path / "should-not-build.zip", extra_deny_tokens=("Oikos",))
