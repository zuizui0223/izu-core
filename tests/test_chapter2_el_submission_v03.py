import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "docs/CHAPTER2_EL_LETTER_DRAFT_V0_3_20260913.md"
COVER = ROOT / "docs/CHAPTER2_EL_COVER_LETTER_DRAFT_20260913.md"


def _word_count(text: str) -> int:
    return len(re.findall(r"\b[\w]+(?:[-'][\w]+)*\b", text))


def test_el_v03_meets_letter_surface_and_novelty_boundary():
    text = DRAFT.read_text(encoding="utf-8")
    lower = text.lower()
    abstract = re.search(r"## Abstract\n\n(.*?)\n\n\*\*Keywords:", text, re.S).group(1)
    main = re.search(r"## Introduction\n\n(.*?)\n\n## Data and code availability", text, re.S).group(1)
    running = re.search(r"\*\*Running title:\*\* (.*?)\s*$", text, re.M).group(1).strip()
    keywords = re.search(r"\*\*Keywords:\*\* (.*?)\n", text).group(1).split(";")

    assert _word_count(abstract) <= 150
    assert _word_count(main) <= 5000
    assert len(running) < 45
    assert len(keywords) <= 10
    assert text.count("**Figure ") == 4
    assert "**References:** 9" in text
    assert "Keitt et al. 2002" in text
    assert "Townsend et al. 2025" in text
    assert "These precedents motivate, rather than answer, our question" in text
    assert "sufficient statistic" not in lower
    assert "natural richness threshold" in lower
    assert "permanent archived release and DOI" in lower


def test_el_cover_letter_states_narrow_novelty_and_leaves_human_declarations_open():
    text = COVER.read_text(encoding="utf-8")
    lower = text.lower()

    assert "variance-equivalent effective independence is not, by itself, a sufficient descriptor" in lower
    assert "keitt et al. (2002)" in lower
    assert "townsend et al. (2025)" in lower
    assert "post-hoc structural generalization" in lower
    assert "[corresponding author name]" in lower
    assert "permanent public archive doi will be inserted" in lower
    assert "- [ ] all authors have approved submission" in lower
    assert "- [ ] the manuscript is not under consideration elsewhere" in lower
