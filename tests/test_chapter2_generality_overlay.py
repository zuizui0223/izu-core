from pathlib import Path

from scripts.generate_chapter2_manuscript_tables import build as build_tables
from scripts.render_chapter2_realized_richness_reframe import render_submission_manuscript

ROOT = Path(__file__).resolve().parents[1]
MATERIAL_MAP = ROOT / "docs/CHAPTER2_MAIN_SUPP_MATERIAL_MAP_20260907.md"


def test_joint_structural_crosscheck_remains_supporting_evidence_not_mainline():
    manuscript = render_submission_manuscript()
    lower = manuscript.lower()

    # The active paper now centers the prespecified system-size rank crossover.
    assert "ordering of response determinants is itself regime dependent" in lower
    assert "55.84%" in manuscript and "12.72%" in manuscript
    assert "numerical crossover is model-specific" in lower

    # The older joint 240-step + zero-adjustment check remains auditable in SI/tables,
    # but no longer has to be narrated in the main manuscript.
    tables = build_tables()
    assert "Joint 240-step + trait adjustment = 0 mixed count | 75/96" in tables
    assert "no new parameter values" in tables

    material = MATERIAL_MAP.read_text(encoding="utf-8")
    assert "replace(BASE, steps=240, trait_adjustment=0.0)" in material
    assert "75/96" in material
