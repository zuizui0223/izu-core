from __future__ import annotations

from scripts.render_chapter2_oikos_generality_overlay import (
    NEW_TITLE,
    build_supporting_tables,
    render_submission_manuscript,
)


def test_oikos_title_matches_unified_model3_scope():
    text = render_submission_manuscript()
    first_line = text.splitlines()[0]
    assert NEW_TITLE in first_line
    assert "conditional island responses" in first_line.lower()


def test_unified_model3_mainline_is_explicit():
    text = render_submission_manuscript()
    lower = text.lower()
    assert "fixed-state reproductive assay" in lower
    assert "deterministic genotype-density counterpart" in lower
    assert "finite-population abm" in lower
    assert "demographic stochasticity is therefore not necessary for response branching under these controlled visitor compositions" in lower
    assert "real islands occupy different stages of the same response architecture" in lower
    assert "the main natural-data gap" in lower


def test_chapter1_bridge_logic_is_compatible_with_island_syndrome_interpretation():
    text = render_submission_manuscript()
    lower = text.lower()
    assert "functional-and-historical interpretation of island syndromes" in lower
    assert "recurrent functional regime with conditional phenotypic realization" in lower


def test_legacy_structural_generality_rows_remain_in_supporting_table_s4():
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
