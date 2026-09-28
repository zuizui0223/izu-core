from __future__ import annotations

from scripts.render_chapter2_oikos_generality_overlay import NEW_TITLE, render_submission_manuscript


def test_oikos_title_matches_model3_scope():
    text = render_submission_manuscript()
    first_line = text.splitlines()[0]
    assert NEW_TITLE in first_line
    assert "pollination ecology" in first_line.lower()


def test_model3_ecological_mainline_is_explicit():
    lower = render_submission_manuscript().lower()
    assert "reproductive selection before demographic change" in lower
    assert "expected inherited evolution without demographic sampling" in lower
    assert "realized evolution in finite populations" in lower
    assert "24,576-case bridge" in lower
    assert "128 independent visitor histories" in lower
    assert "principal natural-data gap" in lower


def test_island_syndrome_interpretation_is_ecological_not_legacy_geometry():
    lower = render_submission_manuscript().lower()
    assert "repeated ecological function to variable phenotypic realization" in lower
    assert "ecological function can be more repeatable than phenotypic form" in lower
    assert "synthetic k" not in lower
