from pathlib import Path

import scripts.build_chapter2_process_review as builder

ROOT = Path(__file__).resolve().parents[1]


def test_confirmed_review_package_routes_current_four_figures():
    assert builder.MAIN == {
        "Figure1.pdf": "model3_selection_process_20261005/selection_process.pdf",
        "Figure2.pdf": "model3_sequence_necessity_20261005/sequence_necessity.pdf",
        "Figure3.pdf": "model3_return_components_20261005/return_components.pdf",
        "Figure4.pdf": "model3_genetic_realization_20261005/genetic_realization.pdf",
    }


def test_confirmatory_result_and_establishment_docs_are_in_review_contract():
    assert "data/design/chapter2_1005_confirmatory_replication_20261006.json" in builder.FIGURE_INPUTS
    assert "data/results/chapter2_1005_confirmatory_replication_20261006.json" in builder.FIGURE_INPUTS
    assert "data/design/chapter2_1005_ecological_mainline_lock_20261006.json" in builder.FIGURE_INPUTS
    for name in (
        "CHAPTER2_1005_ESTABLISHMENT_CLOSEOUT_20261006.md",
        "CHAPTER2_1005_FIVE_CRITERIA_AUDIT_20261006.md",
        "CHAPTER2_1005_NOVELTY_AND_LITERATURE_POSITION_20261006.md",
        "CHAPTER2_SUBMISSION_ROUTE_FIREWALL_20260927.md",
    ):
        assert name in builder.SUPPORT


def test_figure2_reads_frozen_confirmatory_result():
    text = (ROOT / "scripts/figure_model3_sequence_necessity.py").read_text(encoding="utf-8")
    assert "chapter2_1005_confirmatory_replication_20261006.json" in text
    assert "Independent replication" in text
    assert "Independent fixed-capacity replication" in text


def test_review_archive_is_versioned_after_confirmation():
    build_source = (ROOT / "scripts/build_chapter2_process_review.py").read_text(encoding="utf-8")
    verify_source = (ROOT / "scripts/verify_chapter2_process_review.py").read_text(encoding="utf-8")
    assert "chapter2_process_review_20261006.zip" in build_source
    assert "chapter2_process_review_20261006.zip" in verify_source
    assert "chapter2_process_review_20261005.zip" not in build_source
