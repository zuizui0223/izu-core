from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


def test_readme_routes_to_current_chapter2_closure():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()

    assert "Chapter 2 is scientifically closed without new focal field data" in text
    assert "simulation + source-audited metadata/secondary-data confrontation" in text
    assert "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md" in text
    assert "docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md" in text
    assert "data/design/chapter2_simulation_metadata_completion_lock_20260912.json" in text
    assert "conditional response geometry" in lower
    assert "exact realized-richness control" in lower
    assert "finite-community / system-size determinant hierarchy" in lower
    assert "metadata confrontation" in lower
    assert "55.84%" in text and "12.72%" in text
    assert "25 research entries across 21 exact geographic labels" in text
    assert "42 research entries across 37 exact geographic labels" in text
    assert "not full validation" in lower
    assert "post-chapter-2 transport/falsification" in lower
    assert "chapter 3 phenotype validates chapter 2" in lower


def test_readme_does_not_route_historical_v2_or_world_izu_cascade_as_active_surface():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert "The active manuscript surface is:" not in text
    assert "Chapter 2 v2 adds one empirical layer" not in text
    assert "Izu is the focal empirical triangulation and deep mechanistic anchor" not in text
    assert "geography-first world confrontation\n        -> transition-measurement identifiability bottleneck" not in lower
