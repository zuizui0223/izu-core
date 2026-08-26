import json
import zipfile
from pathlib import Path

import pytest

from scripts.build_island_ecology_review_archive import (
    DEFAULT_DENY_TOKENS,
    MANUSCRIPT_ARCNAME,
    REVIEW_FILES,
    build_archive,
    find_denied_tokens,
    validate_review_files,
)


def test_review_archive_file_list_excludes_identity_files_and_source_v2():
    assert "docs/ISLAND_ECOLOGY_TITLE_PAGE_TEMPLATE_20260824.md" not in REVIEW_FILES
    assert "docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V2_20260824.md" not in REVIEW_FILES
    assert all("TITLE_PAGE" not in path.upper() for path in REVIEW_FILES)
    assert "zuizui0223" in DEFAULT_DENY_TOKENS


def test_review_archive_source_files_pass_default_identity_scan():
    records = validate_review_files(DEFAULT_DENY_TOKENS)
    assert len(records) == len(REVIEW_FILES)
    assert all(len(record["sha256"]) == 64 for record in records)


def test_review_archive_builds_with_v3_manifest_and_no_external_programmes(tmp_path: Path):
    output = tmp_path / "review.zip"
    path = build_archive(output)
    assert path == output
    assert output.exists()

    with zipfile.ZipFile(output) as archive:
        names = set(archive.namelist())
        assert "REVIEW_ARCHIVE_MANIFEST.json" in names
        assert "README_REVIEW_ARCHIVE.md" in names
        assert MANUSCRIPT_ARCNAME in names
        assert set(REVIEW_FILES).issubset(names)
        assert not any("title_page" in name.lower() for name in names)
        manuscript = archive.read(MANUSCRIPT_ARCNAME).decode("utf-8")
        assert "sign(Δ reproduction) = sign(Δ service) = sign(Δ functional opportunity)" in manuscript
        manifest = json.loads(archive.read("REVIEW_ARCHIVE_MANIFEST.json"))
        assert manifest["author_identity_included"] is False
        assert manifest["title_page_included"] is False
        assert manifest["external_research_programmes_included"] is False
        assert manifest["journal_target"] == "Journal of Ecology"
        assert "editorial v3" in manifest["claim_boundary"].lower()
        readme = archive.read("README_REVIEW_ARCHIVE.md").decode("utf-8").lower()
        assert "no external research programme is required" in readme
        assert "editorial v3" in readme
        for token in ["future empirical translation", "issue #91", "microdonta"]:
            assert token not in readme


def test_identity_scan_detects_explicit_token(tmp_path: Path):
    path = tmp_path / "identity.txt"
    path.write_text("author handle: ExampleSecretToken", encoding="utf-8")
    assert find_denied_tokens(path, ("examplesecrettoken",)) == ("examplesecrettoken",)


def test_archive_builder_rejects_additional_identity_token_present_in_review_file():
    with pytest.raises(ValueError):
        build_archive(Path("/tmp/should-not-build.zip"), extra_deny_tokens=("Journal of Ecology",))
