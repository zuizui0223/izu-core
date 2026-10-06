from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIVE = ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
FIREWALL = ROOT / "docs/CHAPTER2_SUBMISSION_ROUTE_FIREWALL_20260927.md"


def test_current_manuscript_is_model3_ecological_surface():
    lower = ACTIVE.read_text(encoding="utf-8").lower()
    assert "how island isolation generates floral change" in lower
    assert "temporal precedence is not causal necessity" in lower
    assert "51/64" in lower
    assert "fixed-assurance replication" in lower
    assert "prior selfing with positive mutation did not show an assurance-first majority" in lower
    assert "not calibrated reconstructions of natural island histories" in lower


def test_route_firewall_keeps_retired_routes_in_legacy():
    text = FIREWALL.read_text(encoding="utf-8")
    lower = text.lower()
    assert "the only active chapter 2 manuscript" in lower
    assert "2026-10-05 process paper" in lower
    assert "legacy/model2/" in text
    assert "legacy/routes/nee/" in text
    assert "legacy/routes/ecology-letters/" in text
    assert "legacy/submission-history/" in text
    assert "none of these directories defines the current manuscript" in lower
    assert "future field outcomes to retune the frozen chapter 2 simulation" in lower
