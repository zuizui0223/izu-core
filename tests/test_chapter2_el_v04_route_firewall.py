from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANE_A = ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
FIREWALL = ROOT / "docs/CHAPTER2_SUBMISSION_ROUTE_FIREWALL_20260912.md"
V04 = ROOT / "docs/CHAPTER2_EL_LETTER_DRAFT_V0_4_20260913.md"
COVER = ROOT / "docs/CHAPTER2_EL_COVER_LETTER_DRAFT_V0_4_20260913.md"
RESULT = ROOT / "data/results/chapter2_el_higher_order_sufficiency_20260913.json"


def test_lane_a_remains_the_closed_oikos_manuscript() -> None:
    text = LANE_A.read_text(encoding="utf-8")
    assert text.splitlines()[0] == "# Response geometry under community reorganization: richness-sensitive regimes and state-dependent branching"
    assert "Effective independence is a second-order coordinate" not in text


def test_firewall_promotes_v04_only_inside_lane_b() -> None:
    text = FIREWALL.read_text(encoding="utf-8")
    lower = text.lower()
    assert "scientific analysis = CLOSED" in text
    assert "submission surface = CLOSED" in text
    assert "docs/CHAPTER2_EL_LETTER_DRAFT_V0_4_20260913.md" in text
    assert "docs/CHAPTER2_EL_COVER_LETTER_DRAFT_V0_4_20260913.md" in text
    assert "data/results/chapter2_el_higher_order_sufficiency_20260913.json" in text
    assert "failed lane b scalar-curvature prediction" in lower
    assert "preferred routing remains **lane a first, lane b second**" in lower
    assert "shared lane a scaling output being presented as newly generated el evidence" in lower


def test_v04_surfaces_and_result_receipt_exist() -> None:
    for path in (V04, COVER, RESULT):
        assert path.is_file()
        assert path.stat().st_size > 1000
