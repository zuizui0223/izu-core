from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIVE = ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
EL = ROOT / "docs/CHAPTER2_ECOLOGY_LETTERS_POSITIONING_20260912.md"
NEE = ROOT / "docs/CHAPTER2_NEE_STAGE1_READINESS_20260912.md"
FIREWALL = ROOT / "docs/CHAPTER2_SUBMISSION_ROUTE_FIREWALL_20260927.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_current_manuscript_remains_unified_model3_not_el_or_field_completion_surface():
    text = _read(ACTIVE)
    lower = text.lower()
    first_line = text.splitlines()[0]
    assert "Conditional island responses: from functional matching to finite-population evolutionary realization" in first_line
    assert "Effective independence is a second-order coordinate" not in text
    assert "fixed-state reproductive assay" in lower
    assert "deterministic genotype-density counterpart" in lower
    assert "annual response-blind richness matching" in lower
    assert "pooling eight independent visitor histories" in lower
    assert "real islands occupy different stages of the same response architecture" in lower


def test_el_lane_keeps_explicit_nonlinear_reduction_boundary():
    text = _read(EL)
    lower = text.lower()
    assert "variance-equivalent coordinate" in lower
    assert "not a sufficient statistic" in lower
    assert "c-versus-i reversal" in lower
    assert "interaction-dominated intermediate phase" in lower
    assert "does not reopen or delay" in lower
    assert "natural threshold" in lower


def test_nee_lane_does_not_reopen_current_oikos_scientific_closure():
    text = _read(NEE)
    assert "Current Oikos paper remains scientifically closed" in text
    assert "The second prospective context is not optional for the NEE route" in text
    assert "do not weaken h5" in text.lower()
    assert "source mechanism | CLOSED" in text


def test_route_firewall_names_three_distinct_submission_objects_and_closed_bridge():
    text = _read(FIREWALL)
    lower = text.lower()
    for token in (
        "## Lane A — current Oikos paper",
        "## Lane B — analytical / Ecology Letters companion",
        "## Lane C — prospective natural A → B → C transport/falsification",
        "one nested Model 3 + layer-specific real-island confrontation",
        "core biological mechanism: **DEFINED",
        "original-Chapter-2 control equivalence: **CLOSED",
        "submission package: **OPEN for unified figures, SI and fail-closed QA",
        "old Model 2 as a second required biological mechanism",
    ):
        assert token.lower() in lower
