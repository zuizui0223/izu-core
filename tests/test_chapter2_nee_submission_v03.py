import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/CHAPTER2_NEE_ARTICLE_DRAFT_V0_4_SUBMISSION_20260915.md"
COVER = ROOT / "docs/CHAPTER2_NEE_COVER_LETTER_DRAFT_V0_4_SUBMISSION_20260915.md"

WORD_RE = re.compile(r"\b[\w]+(?:[-'’][\w]+)*\b")


def wc(text: str) -> int:
    return len(WORD_RE.findall(text))


def manuscript_sections(text: str) -> tuple[str, str, str]:
    after = text.split("## Abstract", 1)[1].lstrip()
    abstract, remainder = re.split(r"\n\s*\n", after, maxsplit=1)
    main = remainder.split("## Methods", 1)[0].strip()
    discussion = text.split("## Discussion", 1)[1].split("## Methods", 1)[0]
    return abstract.strip(), main, discussion


def test_submission_clean_nee_article_format_claims_and_novelty_boundary() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    lower = text.lower()
    abstract, main, discussion = manuscript_sections(text)
    methods = text.split("## Methods", 1)[1].split("## Data availability", 1)[0].lower()

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
        "removing england reduces source-balanced `phi` span to **0.162**",
        "removing martinique lowers interior occupancy to **18.75%**",
        "do not validate the synthetic `c/i` crossover",
        "natural hill `d1` is not synthetic `k`",
        "analysis-design safeguards, not biological thresholds",
        "separate four-candidate robustness challenge",
        "no additional `d1` or `phi` values were opened",
        "no source was added",
    ):
        assert required in lower

    # The natural breadth coordinate must be separated from the synthetic
    # aggregation scale in Methods, before any natural-coordinate formula is used.
    assert "natural `d1` was not treated as an estimator, calibration or proxy for synthetic `k` or `k_eff`" in methods
    assert "outcome-independent coordinate for realized partner breadth" in methods
    assert "estimated no numerical mapping between `d1` and `k` or `k_eff`" in methods
    assert "used no natural threshold corresponding to synthetic `k≈4`" in methods
    assert methods.index("natural `d1` was not treated") < methods.index("`d1 = exp[-sum_j p_j log(p_j)]`")
    assert "post-promotion robustness challenge prospectively froze four previously unresolved candidates" in methods
    assert "none passed to coordinate extraction" in methods

    # Context-dependent importance is prior art; novelty is the sufficiency /
    # transportability boundary after context compression.
    assert "context dependence itself is therefore not the unresolved point" in lower
    assert "the unresolved point is **transportability**" in lower
    assert "exact sufficiency boundary for determinant-rank transport" in lower
    assert "what has to be preserved for a ranking to be transportable across contexts" in lower

    # Source-verified bibliography, prior-art boundary, and corrected Tenerife DOI.
    for doi in (
        "10.1002/ajb2.1233",
        "10.1111/ecog.06112",
        "10.1111/jbi.13615",
        "10.1111/2041-210x.70165",
        "10.25666/dataubfc-2025-03-28",
        "10.1111/ele.12657",
        "10.1111/geb.70000",
        "10.1002/ecm.1646",
        "10.1111/1365-2656.70107",
    ):
        assert doi in lower
    assert "10.1111/jbi.13625" not in lower


def test_submission_clean_cover_letter_matches_transportability_ceiling() -> None:
    text = COVER.read_text(encoding="utf-8")
    lower = text.lower()

    assert "nature ecology & evolution" in lower
    assert "52 community-to-interaction rank reversals in 108 paired comparisons" in lower
    assert "42 island interaction systems from six studies and five island or archipelago groups" in lower
    assert "removing england step reduces synchrony dispersion" in lower
    assert "removing martinique reduces interior occupancy" in lower
    assert "prospectively froze a separate four-candidate robustness challenge" in lower
    assert "no new natural coordinates were opened" in lower
    assert "source-complementarity limitation remains" in lower
    assert "0/25** with the complete outcome-independent determinant–response contract" in lower
    assert "do not claim that the synthetic determinant crossover has already been observed in nature" in lower
    assert "great britain retains euppollnet’s pre-existing island-study classification" in lower
    assert "context dependent" in lower
    assert "when can a determinant ranking estimated in one ecological context be transported to another" in lower
    assert "[corresponding author]" in lower

    for forbidden in ("nee_candidate", "promotion threshold", "journal-routing"):
        assert forbidden not in lower
