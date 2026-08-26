from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


def test_readme_declares_scientific_reassessment_before_submission():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert text.startswith("# Izu Core — island plant response architecture under reassessment")
    assert "chapter 2 has been reopened for scientific reassessment" in lower
    assert "do not submit the current journal of ecology research article yet" in lower
    assert "docs/SCIENTIFIC_REASSESSMENT_AFTER_CRITIQUE_20260826.md" in text
    assert "data/design/manuscript_reassessment_gate_20260826.json" in text
    assert "response geometry / parameter robustness" in text


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
    assert "h2 — demoted from headline discovery" in lower
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
    assert "availability/filtering stress parameter" in lower
    assert "5 of 12" in text
    assert "0.4167" in text
    assert "do not use `0.4167`" in text
    assert "16/96" in text
    assert "11/96" in text
    assert "dominica" in lower
    assert "was not retuned" in lower


def test_readme_keeps_external_programmes_outside_current_paper():
    lower = README.read_text(encoding="utf-8").lower()
    assert "microdonta" not in lower
    assert "issue #91" not in lower
    assert "future empirical translation" not in lower
