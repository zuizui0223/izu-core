from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


def test_readme_declares_closed_scientific_gate_and_metadata_only_blocker():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert text.startswith("# Izu Core — conditional island plant response geometry")
    assert "synthetic gate is closed" in lower
    assert "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_ACTIVE_DRAFT_V2_20260827.md" in text
    assert "data/results/chapter2_conditional_why_diagnostics_frozen_20260827.json" in text
    assert "mechanistic **how** plus model-conditional **proximal why**" in lower
    assert "ultimate why" in lower
    assert "source-locked implementation/source gate/structural audit are part of the active paper branch" in lower
    assert "only author-supplied identity metadata and submission declarations remain unresolved" in lower


def test_readme_preserves_three_layer_island_syndrome_core():
    text = README.read_text(encoding="utf-8")
    for token in [
        "Colonization / assembly filtering",
        "In-situ evolutionary change",
        "Post-establishment interaction response",
    ]:
        assert token in text
    assert "three-layer decomposition" in text.lower()


def test_readme_demotes_overstated_h2_h4_h5_claims():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert "h2 — reassigned to conditional response geometry" in lower
    assert "not a pure algebraic tautology" in lower
    assert "replicated_minimal_generator" in text
    assert "no longer a main-paper claim" in lower
    assert "h4 — retained as a structural distinction, not a discovery" in lower
    assert "h5 — demoted from validation" in lower
    assert "not used as validation" in lower


def test_readme_corrects_local_support_semantics_and_precision():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert "support_strength" in text
    assert "local context / availability filtering" in lower
    assert "not extra beneficial support" in lower
    assert "5 of 12" in text
    assert "0.4167" in text
    assert "do not use `0.4167`" in lower
    assert "41 of 96" in text or "41/96" in text
    assert "16 points are mixed" in lower or "16/48" in text
    assert "737" in text
    assert "directionally asymmetric" in lower


def test_readme_registers_izu_empirical_claim_ceiling():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert "focal empirical depth: izu islands" in lower
    assert "raw realized trait matching" in lower
    assert "null-corrected trait matching" in lower
    assert "does **not** explain" in text
    assert "beyond-composition" in lower
    assert "validation of the synthetic" in lower


def test_readme_keeps_external_programmes_outside_current_paper():
    lower = README.read_text(encoding="utf-8").lower()
    assert "microdonta" not in lower
    assert "future empirical translation" not in lower
