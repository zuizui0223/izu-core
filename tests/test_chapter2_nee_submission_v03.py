import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/CHAPTER2_NEE_ARTICLE_DRAFT_V0_3_SUBMISSION_20260915.md"
COVER = ROOT / "docs/CHAPTER2_NEE_COVER_LETTER_DRAFT_V0_3_SUBMISSION_20260915.md"

WORD_RE = re.compile(r"\b[\w]+(?:[-'’][\w]+)*\b")


def wc(text: str) -> int:
    return len(WORD_RE.findall(text))


def manuscript_sections(text: str) -> tuple[str, str, str]:
    after = text.split("## Abstract", 1)[1].lstrip()
    abstract, remainder = re.split(r"\n\s*\n", after, maxsplit=1)
    main = remainder.split("## Methods", 1)[0].strip()
    discussion = text.split("## Discussion", 1)[1].split("## Methods", 1)[0]
    return abstract.strip(), main, discussion


def test_submission_clean_nee_article_format_and_claims() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    lower = text.lower()
    abstract, main, discussion = manuscript_sections(text)

    assert wc(abstract) <= 200, wc(abstract)
    assert wc(main) <= 3500, wc(main)
    assert "### " not in discussion
    assert text.count("**Figure ") == 4

    # Submission surface must not expose internal journal-routing governance.
    for forbidden in (
        "nee_candidate",
        "promotion threshold",
        "journal-routing",
        "claim ceiling",
        "figure plan",
    ):
        assert forbidden not in lower

    # Core evidence and limitations must remain visible.
    for required in (
        "42 systems from six studies and five island or archipelago groups",
        "**52/108**",
        "**0/108**",
        "**21/25**",
        "**2/25**",
        "**0/25**",
        "removing england reduces the source-balanced `phi` span to **0.162**",
        "removing martinique lowers interior occupancy to **18.75%**",
        "do not validate the synthetic `c/i` crossover",
        "natural hill `d1` is not synthetic `k`",
        "analysis-design rules, not biological thresholds",
    ):
        assert required in lower

    # Source-verified primary bibliography and corrected Tenerife DOI.
    for doi in (
        "10.1002/ajb2.1233",
        "10.1111/ecog.06112",
        "10.1111/jbi.13615",
        "10.1111/2041-210x.70165",
        "10.25666/dataubfc-2025-03-28",
        "10.1111/ele.12657",
        "10.1111/geb.70000",
    ):
        assert doi in lower
    assert "10.1111/jbi.13625" not in lower


def test_submission_clean_cover_letter_matches_manuscript_ceiling() -> None:
    text = COVER.read_text(encoding="utf-8")
    lower = text.lower()

    assert "nature ecology & evolution" in lower
    assert "52 community-to-interaction rank reversals in 108" in lower
    assert "42 island interaction systems from six studies and five island or archipelago groups" in lower
    assert "removing england step reduces synchrony dispersion" in lower
    assert "removing martinique reduces interior occupancy" in lower
    assert "0/25 with the complete outcome-independent determinant–response contract" in lower
    assert "do not claim that the synthetic determinant crossover has already been observed in nature" in lower
    assert "great britain retains a source compilation’s pre-existing island-study classification" in lower
    assert "[corresponding author]" in lower

    for forbidden in ("nee_candidate", "promotion threshold", "journal-routing"):
        assert forbidden not in lower
