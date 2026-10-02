import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VNEXT = ROOT / "docs/CHAPTER2_MANUSCRIPT_VNEXT_SYNDROME_20261002.md"
ACTIVE = ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260927.json"


def _text() -> str:
    return VNEXT.read_text(encoding="utf-8")


def test_vnext_is_explicitly_separate_from_locked_submission() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["active_manuscript"] == "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
    assert ACTIVE.exists()
    assert VNEXT.exists()
    assert "vNext integration candidate" in _text()
    assert "does not replace the locked Oikos submission surface" in _text()


def test_vnext_abstract_carries_syndrome_as_outcome_claim() -> None:
    text = _text()
    abstract = text.split("## Abstract", 1)[1].split("## Keywords", 1)[0]
    lower = abstract.lower()
    words = abstract.split()
    assert 180 <= len(words) <= 300
    assert "syndromes summarize recurrent combinations" in lower
    assert "reproductive assurance and investment cost were both present" in lower
    assert "standing variation" in lower
    assert "de novo mutation" in lower
    assert "negative result" in lower
    assert "emergent outcomes" in lower


def test_vnext_preserves_positive_and_negative_prospective_results() -> None:
    lower = _text().lower()
    for phrase in (
        "adaptive-reduction route",
        "functional rematching",
        "standing genetic variation filters",
        "did not support its success criteria",
        "restoring investment standing variation increased absolute investment response by 0.14777",
        "increasing de novo investment mutation supply added 0.01389",
        "strengthened that mutation rescue by a further 0.00102",
        "syndromes are outcomes, not mechanisms",
    ):
        assert phrase in lower


def test_vnext_has_one_coherent_figure_plan() -> None:
    text = _text()
    assert text.count("# Figure captions") == 1
    assert text.count("**Figure 1.") == 1
    assert text.count("**Figure 2.") == 1
    assert text.count("**Figure 3.") == 1
    assert text.count("**Figure 4.") == 1
    assert text.count("**Figure 5.") == 1
