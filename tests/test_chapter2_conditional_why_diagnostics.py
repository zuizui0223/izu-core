import json
from pathlib import Path

import pytest

from scripts.run_chapter2_conditional_why_diagnostics import (
    DESIGN,
    PARAMETER_RANGES,
    cliff_delta,
    frozen_input_sha256,
    scaled_parameters,
    two_way_decomposition,
    verify_inputs,
)
from scripts.generate_chapter2_manuscript_tables import build as build_tables

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "data/results/chapter2_conditional_why_diagnostics_frozen_20260827.json"
MANUSCRIPT = ROOT / "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_ACTIVE_DRAFT_V2_20260827.md"
SUPPORTING_INFORMATION = ROOT / "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_SUPPORTING_INFORMATION_20260827.md"
TABLES = ROOT / "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_TABLES_20260827.md"
THESIS_POSITIONING = ROOT / "THESIS_CHAPTER_POSITIONING.md"


def test_design_freeze_preserves_parent_execution_and_prohibits_retuning():
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    assert design["status"] == "fixed_before_execution"
    assert design["locked_execution"]["seed"] == 20260826
    assert design["locked_execution"]["baseline_matched_community_realizations"] == 96
    assert design["locked_execution"]["joint_transition_surface"] == {
        "sampling": "fixed_seed_latin_hypercube",
        "points": 48,
        "matched_community_realizations_per_point": 24,
        "parameters": 10,
        "parameter_ranges_source": "scripts/run_joint_response_transition_surface.py:PARAMETER_RANGES",
    }
    assert design["retuning_after_result"] is False
    assert design["empirical_calibration"] is False
    assert "design-point frequencies as natural ecological prevalence" in design["prohibited_interpretations"]
    assert all(row["match"] for row in verify_inputs(design).values())


def test_two_way_decomposition_recovers_an_additive_matrix():
    result = two_way_decomposition([
        [0.0, 1.0, 2.0],
        [1.0, 2.0, 3.0],
    ])
    fractions = result["sum_of_squares_fraction"]
    assert fractions["starting_position_by_community_nonadditivity"] == pytest.approx(0.0)
    assert sum(fractions.values()) == pytest.approx(1.0)
    assert result["additive_sign_mismatch_cells"] == 0


def test_parameter_scaling_uses_declared_ranges_without_sample_tuning():
    low = {name: bounds[0] for name, bounds in PARAMETER_RANGES.items()}
    high = {name: bounds[1] for name, bounds in PARAMETER_RANGES.items()}
    scaled = scaled_parameters([low, high])
    assert scaled.shape == (2, len(PARAMETER_RANGES))
    assert scaled[0].tolist() == pytest.approx([-0.5] * len(PARAMETER_RANGES))
    assert scaled[1].tolist() == pytest.approx([0.5] * len(PARAMETER_RANGES))


def test_frozen_input_hash_is_checkout_newline_invariant(tmp_path: Path):
    lf = tmp_path / "lf.py"
    crlf = tmp_path / "crlf.py"
    lf.write_bytes(b"first\nsecond\n")
    crlf.write_bytes(b"first\r\nsecond\r\n")
    assert frozen_input_sha256(lf) == frozen_input_sha256(crlf)


def test_cliffs_delta_direction_is_destination_minus_source():
    assert cliff_delta([2.0, 3.0], [0.0, 1.0]) == 1.0
    assert cliff_delta([0.0, 1.0], [2.0, 3.0]) == -1.0
    assert cliff_delta([0.0, 1.0], [0.0, 1.0]) == 0.0


def test_frozen_result_passes_identity_and_claim_boundaries():
    payload = json.loads(FROZEN.read_text(encoding="utf-8"))
    assert payload["status"] == "frozen_complete_20260827"
    assert all(payload["frozen_identity_checks"].values())
    counts = payload["starting_position_by_community_realization"]["baseline_realization_class_counts"]
    assert counts == {"mixed_sign": 41, "all_positive": 42, "all_negative": 13, "other": 0}
    filtering = payload["local_filtering_directionality"]
    assert filtering["baseline_sign_denominators"]["total"] == 864
    assert "not estimates from independent biological replicates" in filtering["claim_boundary"]
    assert "No seed, parameter range, grid, replicate count" in payload["claim_boundary"]


def test_active_manuscript_and_thesis_positioning_preserve_how_why_boundary():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    manuscript_lower = manuscript.lower()
    supplement = SUPPORTING_INFORMATION.read_text(encoding="utf-8")
    positioning = THESIS_POSITIONING.read_text(encoding="utf-8")
    for token in [
        "80.17%",
        "partner-loss multiplier",
        "positive baselines crossed to non-positive",
        "proximal why",
    ]:
        assert token in manuscript_lower
    assert "mechanistic" in manuscript_lower
    assert "# Appendix S10. Starting-position × community-realization decomposition" in supplement
    assert "# Appendix S11. Direction-specific local-filtering transitions" in supplement
    assert "**Ultimate WHY:**" in positioning
    assert "remains outside the Chapter 2 test" in positioning
    assert "Not tested." in positioning


def test_generated_tables_include_conditional_why_and_izu_audit():
    text = TABLES.read_text(encoding="utf-8")
    assert text == build_tables()
    assert "## Table 4. Conditional-WHY diagnostics" in text
    assert "Community-realization SS fraction | 80.2%" in text
    assert "Strength 0.40: positive → non-positive | 56.5%" in text
    assert "## Table 5. Focal Izu empirical triangulation and structural audit" in text
    assert "null-corrected `delta_TM_sp_z`" in text
    assert "no support for beyond-composition non-random matching" in text
