from pathlib import Path

import pytest

from scripts.render_island_ecology_submission_manuscript import (
    FINAL_TITLE,
    FORBIDDEN_SUBMISSION_TOKENS,
    SOURCE,
    render_submission_manuscript,
    render_to_path,
)


def test_renderer_removes_internal_thesis_routing_and_preserves_science():
    text = render_submission_manuscript()
    lower = text.lower()
    assert text.startswith(f"# {FINAL_TITLE}\n")
    for token in FORBIDDEN_SUBMISSION_TOKENS:
        assert token.lower() not in lower
    assert "dissertation" not in lower
    assert "campanula microdonta" not in lower
    assert "80.17%" in text
    assert "41" in text and "96" in text
    assert "null-corrected matching" in lower
    assert "non-random partner sorting" in lower
    assert "Izu Islands" in text


def test_renderer_writes_clean_submission_file(tmp_path: Path):
    output = tmp_path / "manuscript.md"
    assert render_to_path(output) == output
    text = output.read_text(encoding="utf-8")
    assert text.startswith(f"# {FINAL_TITLE}\n")
    assert "At the dissertation scale" not in text
    assert "## From Chapter 1 to Chapter 3" not in text


def test_renderer_fails_closed_if_source_header_contract_changes(tmp_path: Path):
    broken = tmp_path / "broken.md"
    source = SOURCE.read_text(encoding="utf-8")
    broken.write_text(source.replace("**Status:** active working manuscript v2 — not submission-ready", "**Status:** changed"), encoding="utf-8")
    with pytest.raises(ValueError, match="header changed"):
        render_submission_manuscript(broken)


def test_renderer_fails_closed_if_thesis_bridge_contract_changes(tmp_path: Path):
    broken = tmp_path / "broken.md"
    source = SOURCE.read_text(encoding="utf-8")
    broken.write_text(source.replace("At the dissertation scale", "At another scale", 1), encoding="utf-8")
    with pytest.raises(ValueError, match="Introduction bridge changed"):
        render_submission_manuscript(broken)
