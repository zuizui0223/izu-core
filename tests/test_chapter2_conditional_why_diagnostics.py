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
    assert design["retuning_after_result"] is False
    assert design["empirical_calibration"] is False
    assert all(row["match"] for row in verify_inputs(design).values())


def test_two_way_decomposition_recovers_an_additive_matrix():
    result = two_way_decomposition([[0.0, 1.0, 2.0], [1.0, 2.0, 3.0]])
    fractions = result["sum_of_squares_fraction"]
    assert fractions["starting_position_by_community_nonadditivity"] == pytest.approx(0.0)
    assert sum(fractions.values()) == pytest.approx(1.0)


def test_parameter_scaling_uses_declared_ranges_without_sample_tuning():
    low = {name: bounds[0] for name, bounds in PARAMETER_RANGES.items()}
    high = {name: bounds[1] for name, bounds in PARAMETER_RANGES.items()}
    scaled = scaled_parameters([low, high])
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


def test_frozen_result_passes_identity_and_claim_boundaries():
    payload = json.loads(FROZEN.read_text(encoding="utf-8"))
    assert payload["status"] == "frozen_complete_20260827"
    assert all(payload["frozen_identity_checks"].values())
    assert payload["starting_position_by_community_realization"]["baseline_realization_class_counts"]["mixed_sign"] == 41


def test_thesis_positioning_preserves_how_proximal_why_ultimate_why_boundary():
    positioning = THESIS_POSITIONING.read_text(encoding="utf-8")
    assert "**HOW**" in positioning
    assert "**Proximal WHY**" in positioning
    assert "**Ultimate WHY**" in positioning
    assert "Not tested." in positioning
    assert "The numerical synthetic crossover is not transferred to nature" in positioning


def test_generated_tables_include_current_supporting_material_contract():
    text = TABLES.read_text(encoding="utf-8")
    assert text.rstrip("\n") == build_tables().rstrip("\n")
    assert "## Table S4. Conditional-WHY and relational-robustness diagnostics" in text
    assert "## Table S6. Frozen external-prediction readiness" in text
    assert "Full outcome-independent contracts | 0/25" in text
