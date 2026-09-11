from __future__ import annotations

from scripts.render_chapter2_oikos_generality_overlay import (
    NEW_TITLE,
    build_supporting_tables,
    render_submission_manuscript,
)


def test_oikos_title_is_not_island_scoped():
    text = render_submission_manuscript()
    first_line = text.splitlines()[0]
    assert NEW_TITLE in first_line
    assert "in island plant–pollinator systems" not in first_line.lower()


def test_island_syndrome_novelty_is_explicit_without_becoming_title_scope():
    text = render_submission_manuscript()
    lower = text.lower()
    assert "ensemble-level regime shifts rather than deterministic lineage-level trait rules" in lower
    assert "how a coherent island-level tendency can coexist with opposing lineage-level responses" in lower
    assert "scale-dependent response architecture" in lower
    assert "dominant source of response variation need not be fixed" in lower
    assert "the syndrome is therefore the shifted response regime and its variance architecture" in lower
    discussion = text.split("# Discussion", 1)[1].lower()
    assert "single island syndrome" in discussion
    assert "ensemble-level" in discussion


def test_equal_turnover_generality_is_in_manuscript_and_fig2_caption():
    text = render_submission_manuscript()
    lower = text.lower()
    assert "70/96" in text and "65.61%" in text
    assert "equalizing the baseline mainland–island partner-arrival and partner-loss rates" in lower
    assert "does not make the two scenarios identical" in lower
    figure2 = text.split("**Figure 2.", 1)[1].split("**Figure 3.", 1)[0]
    assert "equal-turnover control" in figure2.lower()


def test_finite_community_model_rationale_and_size_audit_are_in_manuscript():
    text = render_submission_manuscript()
    lower = text.lower()
    assert "finite-community stochastic formulation" in lower
    assert "deterministic mean-field reduction would average over community-realization variation" in lower
    assert "44–60/96" in text
    assert "0.575–0.691" in text and "0.134–0.172" in text
    assert "finite-community sampling contributes materially to realization variance" in lower


def test_finite_n_gaussian_limit_is_bounded_and_integrated():
    text = render_submission_manuscript()
    lower = text.lower().replace("`", "")
    assert "deterministic mean-field kernel contrast was all-positive" in lower
    assert "minimum contrast 0.0208" in lower
    assert "absolute error fell from 0.0689 at k=1 to 0.00654 at k=16" in lower
    assert "finite-community in the asymptotic sense" in lower
    assert "not a rare-extinction or n≈2 artifact" in lower
    assert "not presented as an exact fokker–planck or full linear-noise solution" in lower


def test_active_adjustment_rank_crossover_is_in_result_discussion_and_figures():
    text = render_submission_manuscript()
    lower = text.lower().replace("`", "")
    assert "ordering of response determinants is itself regime dependent" in lower
    assert "2.55% at k=1" in lower
    assert "55.84% at k=16" in lower
    assert "72.98%" in text and "12.72%" in text
    assert "6/6 seeds at k=4" in lower
    assert "28–42/96" in text
    assert "numerical crossover is model-specific" in lower


def test_structural_generality_rows_are_in_table_s4():
    tables = build_supporting_tables()
    table_s4 = tables.split("## Table S4.", 1)[1].split("## Table S5.", 1)[0]
    assert "Equal turnover rates: mixed count / state × community non-additivity" in table_s4
    assert "70/96 / 65.61%" in table_s4
    assert "Finite-community system-size pooling, k=1 → 16" in table_s4
    assert "44–60/96" in table_s4
    assert "Exact finite-k moments + Gaussian limit" in table_s4
    assert "0.0689 → 0.00654" in table_s4
    assert "Active-adjustment system-size rank crossover" in table_s4
    assert "55.84%/12.72%" in table_s4
