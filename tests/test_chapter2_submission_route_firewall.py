from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIVE = ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
EL = ROOT / "docs/CHAPTER2_ECOLOGY_LETTERS_POSITIONING_20260912.md"
NEE = ROOT / "docs/CHAPTER2_NEE_STAGE1_READINESS_20260912.md"
FIREWALL = ROOT / "docs/CHAPTER2_SUBMISSION_ROUTE_FIREWALL_20260912.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_current_manuscript_remains_current_paper_not_el_or_field_completion_surface():
    text = _read(ACTIVE)
    lower = text.lower()
    first_line = text.splitlines()[0]
    assert "Response geometry under community reorganization" in first_line
    assert "Community averaging reverses the hierarchy of ecological response determinants" not in text
    assert "metadata confrontation supports biological ingredients while bounding attribution" in lower
    assert "post-chapter-2 transport/falsification" in lower
    assert "not a completion gate for the present manuscript" in lower


def test_el_lane_keeps_explicit_admission_gate_before_title_promotion():
    text = _read(EL)
    assert "## Admission gate before changing the manuscript title" in text
    assert "The numerical crossover near `k=4` remains model-specific" in text
    assert "correlated-community countercondition" in text


def test_nee_lane_does_not_reopen_current_oikos_scientific_closure():
    text = _read(NEE)
    assert "current Oikos paper = submission-ready scientific fallback" in text
    assert "NEE promotion lane = prospective future study" in text
    assert "The correct action is **not** to reopen simulation" in text


def test_route_firewall_names_three_distinct_submission_objects():
    text = _read(FIREWALL)
    for token in (
        "## Lane A — current Oikos paper",
        "## Lane B — Ecology Letters candidate",
        "## Lane C — prospective natural validation / NEE lane",
        "synthetic `k≈4` being presented as a natural threshold",
        "author-supplied metadata / confirmations only",
    ):
        assert token in text
