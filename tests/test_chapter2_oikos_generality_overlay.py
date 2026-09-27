
from __future__ import annotations

from scripts.render_chapter2_oikos_generality_overlay import (
    NEW_TITLE,
    build_supporting_tables,
    render_submission_manuscript,
)


def test_oikos_title_matches_unified_model3_scope():
    text = render_submission_manuscript()
    assert text.splitlines()[0] == f"# {NEW_TITLE}"
    assert "conditional island responses" in NEW_TITLE.lower()


def test_unified_model3_reduction_is_explicit():
    text = render_submission_manuscript()
    lower = text.lower()
    assert "fixed-state reproductive assay" in lower
    assert "deterministic genotype-density counterpart" in lower
    assert "finite-population abm" in lower
    assert "demographic stochasticity is therefore not necessary for response branching" in lower
    assert "2.3768" in text
    assert "0.1891" in text
    assert "1.78e-15" in lower


def test_history_assurance_and_connectivity_are_integrated():
    text = render_submission_manuscript()
    lower = text.lower()
    assert "early visitor absence" in lower
    assert "reproductive assurance changed whether an endpoint existed" in lower
    assert "seed immigration modifies demographic and genetic input" in lower


def test_real_island_layer_confrontation_is_integrated():
    text = render_submission_manuscript()
    lower = text.lower()
    assert "real islands occupy different stages of the same response architecture" in lower
    assert "all eight shared oshima-to-post targets" in lower
    assert "same-direction propagation case" in lower
    assert "counterdirectional case" in lower
    assert "the main natural-data gap" in lower


def test_legacy_structural_generality_rows_remain_in_supporting_table_s4():
    tables = build_supporting_tables()
    table_s4 = tables.split("## Table S4.", 1)[1].split("## Table S5.", 1)[0]
    assert "Equal turnover rates: mixed count / state × community non-additivity" in table_s4
    assert "Finite-community system-size pooling, k=1 → 16" in table_s4
    assert "Exact finite-k moments + Gaussian limit" in table_s4
    assert "Active-adjustment system-size rank crossover" in table_s4
