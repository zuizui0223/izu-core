from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


def test_readme_routes_to_current_unified_model3_closure():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()

    assert "Chapter 2 is scientifically closed without new focal field data" in text
    assert "one nested Model 3 + layer-specific real-island confrontation" in text
    assert "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md" in text
    assert "docs/CHAPTER2_CANONICAL_STORY_20260927.md" in text
    assert "docs/CHAPTER1_CHAPTER2_CANONICAL_BRIDGE_20260927.md" in text
    assert "data/design/chapter2_unified_model3_lock_20260927.json" in text
    assert "data/design/chapter2_oikos_submission_manifest_20260927.json" in text
    assert "fixed-state reproductive assay" in lower
    assert "deterministic genotype-density" in lower
    assert "finite-population abm" in lower
    assert "real-island a/b/c confrontation" in lower
    assert "inherited longitudinal layer mostly missing" in lower
    assert "42 research entries / 37 exact geographic labels" in text
    assert "complete A → B → C contracts **0/25**" in text
    assert "post-Chapter-2 transport/falsification" in text


def test_readme_keeps_legacy_model2_as_provenance_not_active_mechanism():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert "legacy model 2 exact-richness / synthetic-`k` / response-rule analyses retained only as supporting information robustness" in lower
    assert "transitional two-model integration provenance" in lower
    assert "pre-model-3 provenance" in lower
