import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VNEXT = ROOT / "docs/CHAPTER2_MANUSCRIPT_VNEXT_SYNDROME_20261002.md"
ACTIVE = ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260927.json"
VNEXT_LOCK = ROOT / "data/design/chapter2_vnext_syndrome_integration_lock_20261002.json"
AUDIT = ROOT / "docs/CHAPTER2_VNEXT_ESTABLISHMENT_AUDIT_20261002.md"


def _text() -> str:
    return VNEXT.read_text(encoding="utf-8")


def test_vnext_is_explicitly_separate_from_locked_submission() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["active_manuscript"] == "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
    assert ACTIVE.exists()
    assert VNEXT.exists()
    assert "vNext integration candidate" in _text()
    assert "does not replace the locked Oikos submission surface" in _text()
    lock = json.loads(VNEXT_LOCK.read_text(encoding="utf-8"))
    assert lock["status"] == "vnext_established_not_active_submission"
    assert lock["active_submission_unchanged"] is True
    assert lock["active_manuscript"] == manifest["active_manuscript"]


def test_vnext_abstract_carries_stable_stage_decomposition_claim() -> None:
    text = _text()
    abstract = text.split("## Abstract", 1)[1].split("## Keywords", 1)[0]
    lower = abstract.lower()
    words = abstract.split()
    assert 180 <= len(words) <= 300
    assert "stage-by-stage causal decomposition" in lower
    assert "failed a preregistered robustness test" in lower
    assert "standing variation" in lower
    assert "1% of initial additive variance" in lower
    assert "no equilibrium ranking is inferred" in lower
    assert "finite realization" in lower


def test_vnext_retains_negative_results_and_qualifications() -> None:
    lower = _text().lower()
    for phrase in (
        "conditional model mechanism",
        "mirror-symmetric",
        "did not meet its success criteria",
        "earlier 9.4% mutation-rescue/standing-variation ratio is not retained",
        "quantitative transfer is outside the present claim",
        "stage decomposition, not syndrome criticism",
    ):
        assert phrase in lower
    assert "restoring investment standing variation increased absolute investment response by 0.14777" not in lower


def test_vnext_lock_records_establishment_decisions() -> None:
    lock = json.loads(VNEXT_LOCK.read_text(encoding="utf-8"))
    assert lock["establishment_decisions"]["route_A_headline"] == "dropped_after_failed_robustness_rule"
    assert lock["establishment_decisions"]["standing_vs_mutation"] == "retained_only_as_finite_horizon_ranking_at_VM_over_VG0_0_01"
    assert lock["establishment_decisions"]["natural_quantitative_transfer"].startswith("out_of_scope")
    assert lock["retained_negative_results"]["route_A_robustness"]["supported"] is False
    assert AUDIT.exists()


def test_vnext_has_one_coherent_figure_plan() -> None:
    text = _text()
    assert text.count("# Figure captions") == 1
    assert text.count("**Figure 1.") == 1
    assert text.count("**Figure 2.") == 1
    assert text.count("**Figure 3.") == 1
    assert text.count("**Figure 4.") == 1
    assert text.count("**Figure 5.") == 1
