from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


def test_readme_is_model3_first():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert text.startswith("# Izu Core — Model 3 island pollination-to-evolution")
    assert "positive-mutation genotype-grid fidelity remains unresolved" in lower
    assert "the older oikos bridge submission is a historical snapshot" in lower
    assert "13 rates at fixed plant capacity 48" in lower
    assert "reproductive contributions and local selection" in lower
    assert "shared reproduction and inheritance" in lower
    assert "the abm and deterministic genotype model are parallel implementations" in lower


def test_readme_routes_to_current_submission_surface():
    text = README.read_text(encoding="utf-8")
    for token in (
        "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md",
        "docs/CHAPTER2_PROCESS_MAINLINE_20261005.md",
        "docs/CHAPTER2_CANONICAL_STORY_20260927.md",
        "docs/CHAPTER2_MODEL_UNIFICATION_DECISION_20260927.md",
        "data/design/chapter2_unified_model3_lock_20260927.json",
        "data/design/chapter2_oikos_submission_manifest_20260927.json",
        "scripts/model3_island/",
        "scripts/render_chapter2_oikos_generality_overlay.py",
        "scripts/render_chapter2_process_manuscript.py",
    ):
        assert token in text


def test_readme_preserves_claim_ceiling_and_natural_gap():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert "128 independent visitor histories" in lower
    assert "stable latent branch prevalence" in lower
    assert "principal natural-data gap" in lower
    assert "42 research entries / 37 exact geographic labels" in text
    assert "0/25 complete A → B → C contracts" in text
    assert "chapter 3 phenotype values are **not** used to tune, rescue, validate or retroactively prove" in lower


def test_readme_routes_retired_work_to_legacy():
    text = README.read_text(encoding="utf-8")
    for path in (
        "legacy/model2/",
        "legacy/routes/nee/",
        "legacy/routes/ecology-letters/",
        "legacy/submission-history/",
        "legacy/model3-development/",
        "legacy/pre-model3/",
    ):
        assert path in text
