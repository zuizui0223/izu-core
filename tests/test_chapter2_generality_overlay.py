from pathlib import Path

from scripts.generate_chapter2_manuscript_tables import build as build_tables
from scripts.render_chapter2_realized_richness_reframe import render_submission_manuscript

ROOT = Path(__file__).resolve().parents[1]
MATERIAL_MAP = ROOT / "docs/CHAPTER2_MAIN_SUPP_MATERIAL_MAP_20260907.md"


def test_unified_model3_is_mainline_and_legacy_generality_remains_supporting_evidence():
    manuscript = render_submission_manuscript()
    lower = manuscript.lower()

    assert "fixed-state reproductive assay" in lower
    assert "deterministic genotype-density counterpart" in lower
    assert "finite-population abm" in lower
    assert "real islands occupy different stages of the same response architecture" in lower

    # Historical generality checks remain auditable in SI/tables rather than defining
    # the active biological mechanism.
    tables = build_tables()
    assert "Joint 240-step + trait adjustment = 0 mixed count | 75/96" in tables
    assert "no new parameter values" in tables

    material = MATERIAL_MAP.read_text(encoding="utf-8")
    assert "replace(BASE, steps=240, trait_adjustment=0.0)" in material
    assert "75/96" in material
