from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


def test_readme_routes_to_current_chapter2_closure():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()

    assert "Chapter 2 is scientifically closed" in text
    assert "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md" in text
    assert "42 research entries across 37 exact geographic labels" in text
    assert "25 research entries across 21 exact geographic labels" in text
    assert "two consecutive zero-novelty tranches" in lower
    assert "measurement continuity across the unresolved chain" in lower
    assert "not focal because it is in japan" in lower
    assert "chapter 3 phenotype validates chapter 2" in lower


def test_readme_does_not_route_historical_v2_as_active_surface():
    text = README.read_text(encoding="utf-8")
    assert "The active manuscript surface is:" not in text
    assert "Chapter 2 v2 adds one empirical layer" not in text
    assert "Izu is the focal empirical triangulation and deep mechanistic anchor" not in text
    assert "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_ACTIVE_DRAFT_V2_20260827.md`](docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_ACTIVE_DRAFT_V2_20260827.md)" not in text
