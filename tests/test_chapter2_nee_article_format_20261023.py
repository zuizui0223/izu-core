"""NEE Article formatting proof: only headings and internal lead are changed."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.format_chapter2_nee_article_20261023 import (
    ROOT, MASTER, STATUS, publish, render, words,
)


def source():
    return (ROOT / MASTER).read_text(encoding="utf8")


def test_current_nee_article_format_source_locked_and_science_unchanged():
    master = source()
    out, report = render(master, "f" * 40)
    assert report["status"] == STATUS
    assert 100 <= report["abstract_words"] <= 200
    assert 400 <= report["intro_words"] <= 650
    assert report["main_words"] <= 3500
    assert report["results_topical_headings"] == 5
    assert report["figure_legends"] == 6
    assert report["discussion_subheadings"] == 0
    assert out.startswith("# Founding constraints and the predictability")
    assert "Completed-evidence editorial extract" not in out.split("## Abstract",1)[0]
    assert not any(line.strip() == "## Introduction" for line in out.splitlines())
    assert "## Discussion\n" in out
    assert "### Arrival:" not in out
    assert "### Scope and limitations" not in out
    assert "### R1 — " in out and "### R5 — " in out
    assert "post-outcome" in out
    assert "registered" in out
    assert out.split("## Results\n")[1].split("## Discussion\n")[0] == (
        master.split("## Results\n")[1].split("## Discussion\n")[0])
    assert "## References\n" in out
    assert "## References — preliminary" in master
    assert report["references_formatted_and_verified_by_author"] is False
    assert report["data_code_external_deposit_doi_verified"] is False
    assert report["article_formally_submitted"] is False
    assert report["new_biological_simulations"] == 0
    assert report["new_scientific_inference"] is False
    assert report["registered_G_S_unchanged"] is True


def test_preserves_discussion_prose_without_reordering():
    master = source()
    original = master.split("## Discussion\n",1)[1].split("## Online Methods",1)[0]
    original_paragraphs = [
        s.strip() for s in original.split("\n\n")
        if s.strip() and not s.startswith("### ")]
    formatted, _ = render(master)
    d = formatted.split("## Discussion\n",1)[1].split("## Online Methods\n",1)[0]
    new_paragraphs = [s.strip() for s in d.split("\n\n") if s.strip()]
    assert new_paragraphs == original_paragraphs
    assert len(new_paragraphs) >= 10


def test_reject_changed_scientific_boundaries():
    m = source()
    with pytest.raises(ValueError, match="title"):
        render(m.replace("Founding constraints and the predictability",
                         "Irreversible floral evolution",1))
    with pytest.raises(ValueError, match="post-outcome result not visibly qualified"):
        render(m.replace("post-outcome", "POSTHOC", 1).replace(
            "post-outcome", "POSTHOC"))
    with pytest.raises(ValueError, match="seven Discussion"):
        render(m.replace("### Scope and limitations\n", ""))
    with pytest.raises(ValueError, match="section heading"):
        render(m.replace("## Results\n", "## Results REPLACED\n",1))


def test_emit_deterministic_outputs_and_refuse_overwrite(tmp_path):
    s = source()
    a, d = render(s, "b"*40)
    b, e = render(s, "b"*40)
    assert a == b and d == e
    preview = tmp_path / "NEE_ARTICLE_AUTHOR_PREVIEW.md"
    report = tmp_path / "PROOF.json"
    x = publish(ROOT, preview, report, "b"*40)
    assert preview.read_text(encoding="utf8") == a
    assert json.loads(report.read_text(encoding="utf8")) == x
    with pytest.raises(ValueError, match="refuse overwriting"):
        publish(ROOT, preview, report, "b"*40)
