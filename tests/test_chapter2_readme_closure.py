from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


def test_readme_routes_to_current_bridge_gated_unified_model3_state():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()

    assert "core chapter 2 mechanism is now defined" in lower
    assert "full equivalence to the original chapter 2 control suite is still open" in lower
    assert "two prospective bridge gates" in lower
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


def test_readme_keeps_legacy_model2_controls_without_restoring_second_mechanism():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert "exact-richness and synthetic-`k` remain active benchmarks until the model 3 bridge gates close" in lower
    assert "supporting information" in lower
    assert "transitional two-model integration provenance" in lower
    assert "separate biological mechanism" not in lower or "not a separate biological mechanism" in lower
