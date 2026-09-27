from pathlib import Path

import pytest

from scripts.render_island_ecology_submission_manuscript import (
    FINAL_TITLE,
    FORBIDDEN_SUBMISSION_TOKENS,
    SOURCE,
    render_submission_manuscript,
    render_to_path,
)


def test_renderer_delegates_to_canonical_mechanism_mainline():
    text = render_submission_manuscript()
    lower = text.lower()
    assert text.startswith(f"# {FINAL_TITLE}")
    assert "fixed-state reproductive assay" in lower
    assert "deterministic genotype-density counterpart" in lower
    assert "real islands occupy different stages of the same response architecture" in lower
    assert "2.3768" in text and "0.1891" in text
    for token in FORBIDDEN_SUBMISSION_TOKENS:
        assert token.lower() not in lower


def test_renderer_writes_current_canonical_file(tmp_path: Path):
    output = tmp_path / "manuscript.md"
    assert render_to_path(output) == output
    text = output.read_text(encoding="utf-8")
    assert text == render_submission_manuscript()


def test_renderer_fails_closed_for_noncanonical_override(tmp_path: Path):
    broken = tmp_path / "broken.md"
    source = SOURCE.read_text(encoding="utf-8")
    broken.write_text(source.replace("deterministic genotype-density counterpart", "deterministic comparator", 1), encoding="utf-8")
    with pytest.raises(ValueError, match="canonical mechanism-mainline contract changed"):
        render_submission_manuscript(broken)
