import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "docs/CHAPTER2_EL_LETTER_DRAFT_V0_3_20260913.md"
COVER = ROOT / "docs/CHAPTER2_EL_COVER_LETTER_DRAFT_20260913.md"


def _word_count(text: str) -> int:
    return len(re.findall(r"\b[\w]+(?:[-'][\w]+)*\b", text))


def _contains_citation(text: str, author: str, year: int) -> bool:
    return re.search(rf"\b{re.escape(author)}\s+et\s+al\.?(?:\s*\(|\s+){year}\)?", text, re.I) is not None


def test_el_v03_meets_letter_surface_and_novelty_boundary():
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
    assert "**References:** 9" in text

    # Literature boundary: effective-unit scaling and aggregation/synchrony
    # precede this paper, while the nonlinear-decomposition claim remains narrow.
    assert _contains_citation(text, "Keitt", 2002)
    assert _contains_citation(text, "Townsend", 2025)
    for concept in ("variance-equivalent", "effective independence", "nonlinear", "response decomposition"):
        assert concept in lower
    assert "sufficient statistic" not in lower
    assert re.search(r"\bnot\b.{0,25}\ba natural richness threshold\b", lower, re.S)

    # Submission availability must promise an immutable/persistent archive and DOI
    # without pinning the manuscript to one exact sentence.
    availability_lower = availability.lower()
    assert re.search(r"\b(permanent|persistent|immutable)\b", availability_lower)
    assert re.search(r"\barchiv\w*\b", availability_lower)
    assert re.search(r"\bdoi\b", availability_lower)
    assert "before submission" in availability_lower


def test_el_cover_letter_states_narrow_novelty_and_leaves_human_declarations_open():
    text = COVER.read_text(encoding="utf-8")
    lower = text.lower()

    for concept in ("variance-equivalent", "effective independence", "sufficient descriptor"):
        assert concept in lower
    assert _contains_citation(text, "Keitt", 2002)
    assert _contains_citation(text, "Townsend", 2025)
    assert "post-hoc" in lower and "structural generalization" in lower
    assert "[corresponding author name]" in lower
    assert re.search(r"\b(permanent|persistent|immutable)\b.{0,40}\barchive\b.{0,30}\bdoi\b", lower, re.S)
    assert "- [ ] all authors have approved submission" in lower
    assert "- [ ] the manuscript is not under consideration elsewhere" in lower
