from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "docs/CHAPTER2_MANUSCRIPT_JOURNAL_OF_ECOLOGY_20261006.md"


def text() -> str:
    return DRAFT.read_text(encoding="utf-8")


def section(source: str, start: str, end: str) -> str:
    return source.split(start, 1)[1].split(end, 1)[0]


def test_journal_of_ecology_initial_submission_shape():
    source = text()
    abstract = section(source, "## Abstract", "## Keywords")
    keywords = section(source, "## Keywords", "# Introduction").strip()
    main = section(source, "# Introduction", "# References")

    assert len(abstract.split()) <= 350
    for number in range(1, 6):
        assert f"\n{number}. " in abstract
    assert "5. **Synthesis.**" in abstract

    keyword_items = [item.strip() for item in keywords.split(";") if item.strip()]
    assert len(keyword_items) <= 8
    assert keyword_items == sorted(keyword_items, key=str.lower)

    assert len(main.split()) <= 8000
    assert source.count("**Figure 1.") == 1
    assert source.count("**Figure 2.") == 1
    assert source.count("**Figure 3.") == 1
    assert "**Figure 4." not in source


def test_journal_draft_keeps_confirmed_claim_and_scope():
    source = text()
    normalized = " ".join(source.split())
    assert "51/64" in normalized
    assert "0.6875–0.8906" in normalized
    assert "−0.3060 [−0.3181, −0.2941]" in normalized
    assert "−0.4354 [−0.4533, −0.4172]" in normalized
    assert "only 30/64 histories were assurance-first" in normalized
    assert "temporal precedence and causal necessity are different biological questions" in normalized.lower()
    assert "fixed assurance blocks assurance evolution but not realized selfing" in normalized.lower()


def test_submission_draft_excludes_repository_routing_language():
    source = text()
    for forbidden in ("MODEL3_", "CHAPTER2_", "Q1", "outputs/", "data/results/"):
        assert forbidden not in source
    assert "DOI-backed public deposit is pending" in source
