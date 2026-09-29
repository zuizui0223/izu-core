from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/CHAPTER2_NEE_ARTICLE_DRAFT_V0_4_SUBMISSION_20260915.md"
COVER = ROOT / "docs/CHAPTER2_NEE_COVER_LETTER_DRAFT_V0_4_SUBMISSION_20260915.md"
CHECKLIST = ROOT / "docs/CHAPTER2_NEE_INITIAL_SUBMISSION_CHECKLIST_20260915.md"


def test_nee_methods_discloses_llm_assistance_without_authorship_or_evidence_claims() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    methods = text.split("## Methods", 1)[1].split("## Data availability", 1)[0].lower()

    assert "### ai-assisted development and writing" in methods
    assert "openai chatgpt" in methods
    assert "code drafting and review" in methods
    assert "source-provenance organization" in methods
    assert "language editing" in methods
    assert "not treated as empirical evidence" in methods
    assert "not treated" in methods and "authority for source qualification" in methods
    assert "subject to human review" in methods
    assert "responsibility for study design, analysis choices, interpretation and the final manuscript remains with the authors" in methods
    assert "no large language model is listed as an author" in methods


def test_initial_submission_checklist_marks_llm_disclosure_closed() -> None:
    text = CHECKLIST.read_text(encoding="utf-8").lower()
    assert "author-controlled fields pending" in text
    assert "ai/llm-use disclosure is present in methods" in text
    assert "llm output was not treated as empirical evidence or source authority" in text
    assert "does not list an llm as an author" in text


def test_cover_letter_fails_closed_on_unconfirmed_author_declarations() -> None:
    text = COVER.read_text(encoding="utf-8")
    lower = text.lower()

    assert "author confirmation required — related manuscripts" in lower
    assert "author confirmation required — editor contact" in lower
    assert "[corresponding author]" in lower
    assert "this work is original and is not under consideration elsewhere" not in lower
