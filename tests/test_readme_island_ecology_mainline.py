from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


def test_readme_declares_closed_science_and_current_unified_surface():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert text.startswith("# Izu Core — conditional island plant response and evolutionary realization")
    assert "chapter 2 is scientifically closed without new focal field data" in lower
    assert "one nested model 3 + layer-specific real-island confrontation" in lower
    assert "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md" in text
    assert "docs/CHAPTER2_CANONICAL_STORY_20260927.md" in text
    assert "docs/CHAPTER1_CHAPTER2_CANONICAL_BRIDGE_20260927.md" in text
    assert "data/design/chapter2_unified_model3_lock_20260927.json" in text
    assert "data/design/chapter2_oikos_submission_manifest_20260927.json" in text
    assert "historical v2 manuscripts" in lower
    assert "must not be treated as the current manuscript surface" in lower


def test_readme_preserves_three_distinct_island_processes():
    text = README.read_text(encoding="utf-8")
    for token in [
        "Colonization / assembly filtering",
        "In-situ evolutionary change",
        "Post-establishment interaction response",
    ]:
        assert token in text
    assert "three distinct processes" in text.lower()


def test_readme_centers_unified_model3_not_legacy_rank_crossover():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert "fixed-state reproductive assay" in lower
    assert "deterministic genotype-density propagation" in lower
    assert "finite-population abm" in lower
    assert "selection-gradient branching" in lower
    assert "inherited branching persists" in lower
    assert "legacy model 2 exact-richness / synthetic-`k` / response-rule analyses retained only as supporting information robustness" in lower


def test_readme_routes_real_island_confrontation_and_chapter1_bridge():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert "real-island a/b/c confrontation" in lower
    assert "same-direction propagation case" in lower
    assert "counterdirectional case" in lower
    assert "principal natural-data gap is **b**" in lower
    assert "chapter1_chapter2_canonical_bridge_20260927.md" in lower
    assert "42 research entries / 37 exact geographic labels" in text
    assert "complete A → B → C contracts **0/25**" in text


def test_readme_blocks_retroactive_chapter3_validation():
    lower = README.read_text(encoding="utf-8").lower()
    assert "chapter 3 phenotype values are **not** used to tune, rescue, validate or retroactively prove" in lower
    assert "chapter 3 phenotype validates chapter 2" in lower
    assert "prospective izu e3/e4 chain is required for chapter 2 completion" in lower
