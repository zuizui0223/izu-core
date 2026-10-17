"""Strict manuscript-scoping and word-limit regression; no biological runs."""
from pathlib import Path

import pytest

from scripts.validate_chapter2_reconciled_manuscript_20261017 import (
    ROOT, SOURCE, anonymous_review_text, audit, lengths, verify_source,
)


def test_final_reconciled_source_and_anonymous_word_limits():
    source = SOURCE.read_text(encoding="utf-8")
    counts = verify_source(source)
    assert 100 <= counts["abstract"] <= 150
    assert 2000 <= counts["main_text"] <= 5000
    assert counts["abstract"] == 142
    assert counts["main_text"] == 4995
    blind = anonymous_review_text(source)
    blind_counts = lengths(blind)
    assert blind_counts["abstract"] == 142
    assert blind_counts["main_text"] <= 5000
    assert not any(s in blind.lower() for s in ("zuizui0223", "github.com/", "issue #436"))
    assert "Supporting Information" in blind
    assert "Permanent, independently downloadable DOI-backed" in blind
    assert "Figure4.svg" in blind
    assert "## Evidence hierarchy and study-origin record" not in blind
    assert "# References" in blind
    assert blind.startswith("# Temporal precedence is not evolutionary necessity:")


def test_manuscript_fails_if_word_limit_exceeded():
    source = SOURCE.read_text(encoding="utf-8")
    oversized = source.replace("# Results\n", "# Results\n" + ("unregistered-word " * 15), 1)
    with pytest.raises(ValueError, match="letter limits"):
        verify_source(oversized)


def test_manuscript_fails_if_registered_null_is_promoted():
    source = SOURCE.read_text(encoding="utf-8")
    invalid = source.replace("Both co-primary intervals included zero",
                             "Both co-primary intervals excluded zero", 1)
    with pytest.raises(ValueError, match="Critical ecological"):
        verify_source(invalid)


def test_manuscript_fails_if_fresh_founder_inconclusive_is_erased():
    source = SOURCE.read_text(encoding="utf-8")
    invalid = source.replace("assurance-cost interval crossed zero",
                             "assurance-cost interval excluded zero")
    with pytest.raises(ValueError, match="Fresh-founder"):
        verify_source(invalid)


def test_anonymous_review_blocks_project_internal_path():
    source = SOURCE.read_text(encoding="utf-8")
    invalid = source.replace("# Discussion\n", "# Discussion\nextra docs/private/new_unverified.json\n")
    with pytest.raises(ValueError, match="Unmapped project path"):
        anonymous_review_text(invalid)


def test_audit_is_clear_about_unfinished_data_deposit_and_figure_bytes():
    result = audit()
    assert result["status"] == "WORD_COUNT_AND_ANONYMITY_PASS_NOT_SUBMITTED"
    assert result["source_word_counts"]["main_text"] == 4995
    assert result["anonymous_word_counts"]["main_text"] <= 5000
    assert result["anonymous_preview_matches_reconciled_source"] is True
    assert result["registered_results_modified"] is False
    assert result["figure_bytes_reverified_in_this_audit"] is False
    assert result["external_doi_deposited"] is False
    assert result["original_manuscript_overwritten"] is False
    assert len(result["figure_roster"]) == 7


def test_saved_anonymous_preview_drift_is_rejected(tmp_path):
    import shutil
    for name in ("CHAPTER2_MANUSCRIPT_RECONCILED_20261017.md",
                 "CHAPTER2_ANONYMOUS_REVIEW_20261017.md"):
        to = tmp_path / "docs" / name
        to.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / "docs" / name, to)
    preview = tmp_path / "docs" / "CHAPTER2_ANONYMOUS_REVIEW_20261017.md"
    preview.write_text(preview.read_text(encoding="utf-8") + "quiet untracked addition\n", encoding="utf-8")
    with pytest.raises(ValueError, match="preview differs"):
        audit(tmp_path)
