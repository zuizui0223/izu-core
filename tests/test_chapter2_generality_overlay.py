from pathlib import Path

from scripts.generate_chapter2_manuscript_tables import build as build_tables
from scripts.render_chapter2_realized_richness_reframe import render_submission_manuscript

ROOT = Path(__file__).resolve().parents[1]
MATERIAL_MAP = ROOT / "docs/CHAPTER2_MAIN_SUPP_MATERIAL_MAP_20260907.md"


def test_joint_structural_crosscheck_is_integrated_without_reopening_modeling():
    manuscript = render_submission_manuscript()
    lower = manuscript.lower()
    assert "75/96 community realizations mixed" in lower
    assert "240-step horizon and zero trait adjustment simultaneously" in lower
    assert "without adding a new calibrated scenario" in lower
    assert "figure 2. result 1 baseline conditional response geometry" in lower
    assert "joint existing-harness cross-check" in lower

    tables = build_tables()
    assert "Joint 240-step + trait adjustment = 0 mixed count | 75/96" in tables
    assert "no new parameter values" in tables

    material = MATERIAL_MAP.read_text(encoding="utf-8")
    assert "replace(BASE, steps=240, trait_adjustment=0.0)" in material
    assert "75/96" in material
