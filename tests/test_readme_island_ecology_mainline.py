from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


def test_readme_declares_closed_scientific_gate_and_metadata_blocker():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert text.startswith("# Izu Core — conditional island plant response geometry")
    assert "synthetic scientific gate is closed" in lower
    assert "actual submission remains blocked by author metadata and declarations" in lower
    assert "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_ACTIVE_DRAFT_20260827.md" in text
    assert "data/results/chapter2_conditional_why_diagnostics_frozen_20260827.json" in text
    assert "mechanistic **how** plus **proximal why**" in lower
    assert "ultimate why" in lower


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
    assert "11/11 covered or sign-compatible" in text
    assert "no longer used as validation" in lower


def test_readme_corrects_local_support_semantics_and_precision():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert "support_strength" in text
    assert "local context / availability filtering" in lower
    assert "not extra beneficial support" in lower
    assert "5 of 12" in text
    assert "0.4167" in text
    assert "do not use `0.4167`" in lower
    assert "41/96" in text
    assert "16/48" in text
    assert "737" in text
    assert "directionally asymmetric" in lower
    assert "dominica" in lower
    assert "was not retuned" in lower


def test_readme_keeps_external_programmes_outside_current_paper():
    lower = README.read_text(encoding="utf-8").lower()
    assert "microdonta" not in lower
    assert "issue #91" not in lower
    assert "future empirical translation" not in lower
