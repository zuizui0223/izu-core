from pathlib import Path

from scripts import build_chapter2_nee_presubmission_bundle as bundle
from scripts.render_chapter2_nee_v04_submission_figures import render_all

ROOT = Path(__file__).resolve().parents[1]
SUPPLEMENTARY_TABLES = ROOT / "docs/CHAPTER2_NEE_SUPPLEMENTARY_TABLES_20260917.md"
FIGURE_TABLE_MAP = ROOT / "docs/CHAPTER2_NEE_FIGURE_TABLE_RESULT_MAP_20260917.md"


def test_presubmission_bundle_uses_v04_submission_renderer() -> None:
    assert bundle.render_all.__module__ == "scripts.render_chapter2_nee_v04_submission_figures"


def test_nee_v04_submission_figures_render_from_frozen_results(tmp_path: Path) -> None:
    paths = render_all(tmp_path)
    assert len(paths) == 8
    assert len([path for path in paths if path.suffix == ".pdf"]) == 4
    assert len([path for path in paths if path.suffix == ".svg"]) == 4
    assert all(path.is_file() and path.stat().st_size > 0 for path in paths)

    expected_tokens = {
        "figure1_sufficiency_boundary.svg": (
            "Variance equivalence fixes only the second moment",
            "curvature alignment boundary",
            "higher-order variation raises I/C",
            "higher-order variation lowers I/C",
        ),
        "figure2_nonlinear_phase_and_feedback.svg": (
            "Plant-pollinator rank path",
            "18/54",
            "41",
            "38",
            "32",
            "52/108",
            "0/108",
        ),
        "figure3_natural_breadth_synchrony_plane.svg": (
            "42 systems",
            "Leave-one-study-out source leverage",
            "England",
            "0.162",
            "Martinique",
            "0.188",
        ),
        "figure4_measurement_ceiling_and_transport.svg": (
            "21/25",
            "2/25",
            "0/25",
            "42-system regime map estimates context",
            "not evaluable",
        ),
    }
    for filename, tokens in expected_tokens.items():
        text = (tmp_path / filename).read_text(encoding="utf-8")
        for token in tokens:
            assert token in text, f"{filename} missing frozen-result token: {token}"


def test_nee_paper_tables_are_results_backed_and_submission_facing() -> None:
    assert SUPPLEMENTARY_TABLES.is_file()
    text = SUPPLEMENTARY_TABLES.read_text(encoding="utf-8")
    for token in (
        "Supplementary Table 1 | Natural-regime source inventory",
        "Mallorca | Balearic Islands | 19",
        "Supplementary Table 2 | Leave-one-study-out source leverage",
        "England STEP / Great Britain | 39 | 6.199 | 0.162",
        "Martinique (Cyrille 2025) | 32 | 2.883 | 0.352 | 0.188",
        "Supplementary Table 3 | Prospectively frozen source-redundancy challenge",
        "Petanidou Aegean / Cyclades",
        "Supplementary Table 4 | Existing-island measurement ceiling",
        "Comparable plant response | 21/25",
        "Partner arrival/replacement | 2/25",
        "Full outcome-independent contract | 0/25",
        "not_evaluable",
    ):
        assert token in text


def test_nee_figure_table_map_names_the_frozen_result_sources() -> None:
    assert FIGURE_TABLE_MAP.is_file()
    text = FIGURE_TABLE_MAP.read_text(encoding="utf-8")
    for token in (
        "Figure 1",
        "chapter2_el_higher_order_sufficiency_20260913.json",
        "Figure 2",
        "chapter2_el_nonlinear_reduction_audit_20260913.json",
        "Figure 3",
        "chapter2_natural_regime_six_source_checkpoint_20260915.json",
        "chapter2_natural_regime_six_source_all_loo_diagnostic_20260915.json",
        "Figure 4",
        "chapter2_simulation_metadata_completion_lock_20260912.json",
        "Supplementary Table 3",
        "chapter2_natural_regime_source_robustness_challenge_closure_20260915.json",
    ):
        assert token in text
