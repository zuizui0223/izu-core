from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIVE = ROOT / "docs/CHAPTER2_MANUSCRIPT_ECOLOGY_LETTERS_20261006.md"
LONGFORM = ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
FIREWALL = ROOT / "docs/CHAPTER2_SUBMISSION_ROUTE_FIREWALL_20260927.md"


def test_current_manuscript_is_model3_ecological_surface():
    lower = ACTIVE.read_text(encoding="utf-8").lower()
    assert "reproductive assurance compresses floral-investment divergence" in lower
    assert "temporal sequence is not used as evidence of causal necessity" in lower
    assert "51 of 64 histories" in lower
    assert "assurance evolution is not required for investment decline" in lower
    assert "prior selfing" in lower
    assert "not calibrated to a named island" in lower


def test_longform_is_provenance_not_submission_surface():
    first_block = LONGFORM.read_text(encoding="utf-8").split("## Numerical scope amendment", 1)[0].lower()
    assert "long-form chapter 2 process/provenance manuscript" in first_block
    assert "chapter2_manuscript_ecology_letters_20261006.md" in first_block


def test_route_firewall_keeps_retired_routes_in_legacy():
    text = FIREWALL.read_text(encoding="utf-8")
    lower = text.lower()
    assert "the only active chapter 2 manuscript" in lower
    assert "2026-10-05 process paper" in lower
    assert "chapter2_manuscript_ecology_letters_20261006.md" in lower
    assert "4/4 settings" in lower
    assert "legacy/model2/" in text
    assert "legacy/routes/nee/" in text
    assert "legacy/routes/ecology-letters/" in text
    assert "legacy/submission-history/" in text
    assert "none of these directories defines the current manuscript" in lower
    assert "future field outcomes to retune the frozen chapter 2 simulation" in lower
