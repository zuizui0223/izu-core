from __future__ import annotations

from scripts.render_chapter2_oikos_generality_overlay import (
    NEW_TITLE,
    build_supporting_tables,
    render_submission_manuscript,
)


def test_oikos_title_is_not_island_scoped():
    text = render_submission_manuscript()
    first_line = text.splitlines()[0]
    assert NEW_TITLE in text
    assert "in island plant–pollinator systems" not in first_line.lower()


def test_equal_turnover_generality_is_in_manuscript_and_fig2_caption():
    text = render_submission_manuscript()
    lower = text.lower()
    assert "70/96" in text
    assert "65.61%" in text
    assert "equalizing the baseline mainland–island partner-arrival and partner-loss rates" in text
    assert "does not make the two scenarios identical" in lower
    figure2 = text.split("**Figure 2.", 1)[1].split("**Figure 3.", 1)[0]
    assert "equal-turnover control" in figure2.lower()
    assert "70/96" in figure2


def test_equal_turnover_row_is_in_table_s4():
    tables = build_supporting_tables()
    table_s4 = tables.split("## Table S4.", 1)[1].split("## Table S5.", 1)[0]
    assert "Equal turnover rates: mixed count / state × community non-additivity" in table_s4
    assert "70/96 / 65.61%" in table_s4
    assert "all other scenario differences retained" in table_s4
