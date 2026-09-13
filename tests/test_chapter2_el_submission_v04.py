import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "docs/CHAPTER2_EL_LETTER_DRAFT_V0_4_20260913.md"
COVER = ROOT / "docs/CHAPTER2_EL_COVER_LETTER_DRAFT_V0_4_20260913.md"


def _word_count(text: str) -> int:
    return len(re.findall(r"\b[\w]+(?:[-'][\w]+)*\b", text))


def test_el_v04_meets_letter_surface_and_contains_the_analytic_upgrade() -> None:
    text = DRAFT.read_text(encoding="utf-8")
    lower = text.lower()
    abstract = re.search(r"## Abstract\n\n(.*?)\n\n\*\*Keywords:", text, re.S).group(1)
    main = re.search(r"## Introduction\n\n(.*?)\n\n## Data and code availability", text, re.S).group(1)
    availability = re.search(r"## Data and code availability\n\n(.*?)\n\n## Figure legends", text, re.S).group(1)
    running = re.search(r"\*\*Running title:\*\* (.*?)\s*$", text, re.M).group(1).strip()
    keywords = re.search(r"\*\*Keywords:\*\* (.*?)\n", text).group(1).split(";")

    assert _word_count(abstract) <= 150
    assert _word_count(main) <= 5000
    assert len(running) < 45
    assert len(keywords) <= 10
    assert text.count("**Figure ") == 4
    assert "**References:** 11" in text

    for concept in (
        "third cumulant",
        "fourth cumulant",
        "mixed state–community",
        "scalar saturation curvature",
        "fresh seeds",
        "phase topology",
    ):
        assert concept.lower() in lower
    assert re.search(r"e\^2\s*b\^2\s*-\s*c\^2\s*d\^2", lower)

    # Protect the scientific content while allowing Markdown emphasis to change.
    assert re.search(r"alpha=0.{0,40}(?:produced\s+)?\*{0,2}0\*{0,2}.{0,20}c/i reversals", lower, re.S)
    assert re.search(r"alpha=0\.15.{0,40}(?:produced\s+)?\*{0,2}52\*{0,2}", lower, re.S)
    assert re.search(r"18 matched.{0,80}increased in\s+0 blocks.{0,40}unchanged in\s+16.{0,40}decreased in\s+2", lower, re.S)
    assert "effective population size" in lower
    assert "effective numbers of species" in lower
    assert "do **not** argue that effective numbers are generally misleading" in lower

    availability_lower = availability.lower()
    assert "failed and successful prediction receipts" in availability_lower
    assert "doi" in availability_lower
    assert "before submission" in availability_lower


def test_el_v04_cover_letter_discloses_companion_and_shared_model_surface() -> None:
    text = COVER.read_text(encoding="utf-8")
    lower = text.lower()

    assert "companion manuscript and overlap disclosure" in lower
    assert "oikos" in lower
    assert "response geometry under community reorganization" in lower
    assert "reuses that frozen model and scaling output" in lower
    assert "those shared quantities are not claimed as new here" in lower
    assert "higher-cumulant common-factor derivation" in lower
    assert "exact quadratic mixed-response condition" in lower
    assert "fresh-seed feedback intervention" in lower
    assert "we will disclose the companion manuscript" in lower
    assert "[corresponding author name]" in lower
    assert "- [ ] lane a / *oikos* manuscript has been submitted first" in lower


def test_v04_does_not_erase_the_failed_prediction() -> None:
    manuscript = DRAFT.read_text(encoding="utf-8").lower()
    cover = COVER.read_text(encoding="utf-8").lower()
    for text in (manuscript, cover):
        assert "failed" in text
        assert re.search(r"41.{0,30}38.{0,30}32", text, re.S)
