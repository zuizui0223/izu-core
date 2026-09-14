import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "docs/CHAPTER2_NEE_ARTICLE_DRAFT_V0_2_20260915.md"
COVER = ROOT / "docs/CHAPTER2_NEE_COVER_LETTER_DRAFT_V0_2_20260915.md"
RESOLUTION = ROOT / "docs/CHAPTER2_NEE_ROUTE_RESOLUTION_20260915.md"


def _word_count(text: str) -> int:
    return len(re.findall(r"\b[\w]+(?:[-'’][\w]+)*\b", text))


def test_nee_v02_matches_article_surface_and_current_route() -> None:
    text = DRAFT.read_text(encoding="utf-8")
    lower = text.lower()

    abstract = re.search(r"## Abstract\n\n(.*?)\n\nEcology compares causes", text, re.S).group(1)
    main = re.search(r"Ecology compares causes(.*?)\n\n## Methods", text, re.S).group(0)
    discussion = re.search(r"## Discussion\n\n(.*?)\n\n## Methods", text, re.S).group(1)

    assert _word_count(abstract) <= 200
    assert _word_count(main) <= 3500
    assert "**Article type:** Article" in text
    assert "**Target:** *Nature Ecology & Evolution*" in text
    assert text.count("**Figure ") == 4
    assert "### " not in discussion

    for required in (
        "42 systems from six studies and five island or archipelago groups",
        "d1` q90/q10 ratio was **4.521**",
        "`phi` q90–q10 span was **0.352**",
        "**52/108**",
        "**0/108**",
        "**21/25**",
        "**2/25**",
        "**0/25**",
        "removing england reduces the source-balanced `phi` span to **0.162**",
        "removing martinique lowers interior occupancy to **18.75%**",
    ):
        assert required in lower

    assert "do not test a universal island-syndrome effect" in lower
    assert "natural hill `d1` is not synthetic `k`" in lower
    assert "do not validate the synthetic `c/i` crossover" in lower
    assert "not as evidence that each part of that space is source-invariant" in lower
    assert "reopening candidate hunting" in lower


def test_nee_v02_cover_letter_discloses_scope_and_post_promotion_sensitivity() -> None:
    text = COVER.read_text(encoding="utf-8")
    lower = text.lower()

    assert "nature ecology & evolution" in lower
    assert "42 island interaction systems from six studies and five island or archipelago groups" in lower
    assert "removing the england step source reduces synchrony dispersion" in lower
    assert "removing martinique reduces interior occupancy" in lower
    assert "do not claim that the synthetic determinant crossover has already been observed in nature" in lower
    assert "internal nee promotion thresholds are routing rules rather than biological boundaries" in lower
    assert "great britain retains a source compilation’s pre-existing island-study classification" in lower
    assert "earlier ecology letters and oikos manuscript surfaces remain archived" in lower


def test_nee_route_resolution_preserves_promotion_and_sensitivity_boundaries() -> None:
    text = RESOLUTION.read_text(encoding="utf-8")
    lower = text.lower()

    assert "nature ecology & evolution article candidate" in lower
    assert "journal-selection deferral" in lower
    assert "d1` q90/q10 = 4.5213" in lower
    assert "`phi` q90-q10 span = 0.3516" in lower
    assert "removing england step reduces `phi` span to 0.1619" in lower
    assert "removing martinique reduces joint-interior occupancy to 0.1875" in lower
    assert "do not undo the frozen route decision" in lower
    assert "must not describe the natural plane as robust to removal of every source" in lower
    assert "candidate search is closed" in lower
    assert "0/25 full contracts" in lower
