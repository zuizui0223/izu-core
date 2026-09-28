from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


def test_readme_routes_to_bridge_complete_unified_model3_state():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()

    assert "chapter 2 is scientifically closed at the declared synthetic claim ceiling" in lower
    assert "completed 24,576-case isolation bridge" in lower
    assert "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md" in text
    assert "docs/CHAPTER2_CANONICAL_STORY_20260927.md" in text
    assert "docs/CHAPTER1_CHAPTER2_CANONICAL_BRIDGE_20260927.md" in text
    assert "data/design/chapter2_unified_model3_lock_20260927.json" in text
    assert "data/design/chapter2_oikos_submission_manifest_20260927.json" in text
    assert "fixed-state reproductive assay" in lower
    assert "deterministic genotype-density" in lower
    assert "finite-population abm" in lower
    assert "real-island a/b/c confrontation" in lower
    assert "principal natural-data gap is **b**" in lower
    assert "42 research entries / 37 exact geographic labels" in text
    assert "complete A → B → C contracts **0/25**" in text


def test_readme_demotes_legacy_model2_after_bridge_completion():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert "legacy model 2 exact-richness / synthetic-`k` / response-rule / s/c/i analyses retained as historical provenance only" in lower
    assert "legacy/model2" in lower
    assert "transitional two-model integration provenance" in lower
    assert "active benchmarks until the model 3 bridge gates close" not in lower
