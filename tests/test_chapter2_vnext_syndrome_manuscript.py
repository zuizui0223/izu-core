import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VNEXT = ROOT / "docs/CHAPTER2_MANUSCRIPT_VNEXT_SYNDROME_20261002.md"
ACTIVE = ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260927.json"
VNEXT_LOCK = ROOT / "data/design/chapter2_vnext_syndrome_integration_lock_20261002.json"
AUDIT = ROOT / "docs/CHAPTER2_VNEXT_ESTABLISHMENT_AUDIT_20261002.md"
BACKBONE = ROOT / "data/results/chapter2_deterministic_backbone_depression_sensitivity_20261002.json"


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


def test_vnext_abstract_locates_where_repeatability_is_lost() -> None:
    text = _text()
    abstract = text.split("## Abstract", 1)[1].split("## Keywords", 1)[0]
    lower = abstract.lower()
    words = abstract.split()
    assert 180 <= len(words) <= 300
    assert "where repeatability is retained or lost" in lower
    assert "failed a preregistered robustness test" in lower
    assert "standing genetic variation" in lower
    assert "116/128" in lower
    assert "11 were mixed" in lower
    assert "one was positive-only" in lower
    assert "locate where syndrome-component repeatability is retained, redirected or lost" in lower
    assert "rather than merely to show that the pathway can be partitioned into modules" in lower


def test_vnext_propagates_backbone_qualification() -> None:
    lower = _text().lower()
    for phrase in (
        "negative mean backbone but not uniform history-level direction",
        "overall far-minus-near deterministic effects were -0.3506, -0.4510 and -0.4142",
        "116/128 remained negative-only",
        "11/128 were mixed",
        "1/128 was positive-only",
        "where repeatability is retained and lost",
        "the same perturbation is carried through them",
    ):
        assert phrase in lower
    assert "natural deterministic density is one-directional" not in lower
    assert "uniformly one-directional across all 128 histories" not in lower


def test_vnext_retains_other_negative_results_and_qualifications() -> None:
    lower = _text().lower()
    for phrase in (
        "conditional model mechanism",
        "mirror-symmetric",
        "did not meet its success criteria",
        "earlier 9.4% mutation-rescue/standing-variation ratio is not retained",
        "quantitative transfer is outside the present claim",
    ):
        assert phrase in lower
    assert "restoring investment standing variation increased absolute investment response by 0.14777" not in lower


def test_vnext_lock_records_final_establishment_decisions() -> None:
    lock = json.loads(VNEXT_LOCK.read_text(encoding="utf-8"))
    backbone = json.loads(BACKBONE.read_text(encoding="utf-8"))
    assert lock["establishment_decisions"]["route_A_headline"] == "dropped_after_failed_robustness_rule"
    assert lock["establishment_decisions"]["standing_vs_mutation"] == "retained_only_as_finite_horizon_ranking_at_VM_over_VG0_0_01"
    assert lock["establishment_decisions"]["natural_quantitative_transfer"].startswith("out_of_scope")
    assert lock["establishment_decisions"]["deterministic_backbone"] == "negative_mean_robust_across_depression_0_25_to_0_75_but_uniform_history_direction_fails_at_0_75"
    assert lock["retained_negative_results"]["route_A_robustness"]["supported"] is False
    assert lock["retained_negative_results"]["deterministic_backbone_uniformity"]["supported"] is False
    assert lock["establishment_status"] == "five_criteria_plus_backbone_propagation_plus_full_clean_reproduction_closed"
    assert backbone["backbone_mean_direction_robust"] is True
    assert backbone["uniform_history_direction_robust"] is False
    assert backbone["reports"][2]["mixed_histories_eps0"] == 11
    assert backbone["reports"][2]["positive_only_histories_eps0"] == 1
    assert AUDIT.exists()



def test_vnext_title_and_methods_center_repeatability_transmission() -> None:
    text = _text()
    first = text.splitlines()[0]
    assert "Where island-syndrome repeatability is retained and lost" in first
    assert "## Operational definition of repeatability across stages" in text
    for phrase in (
        "Coarse directional repeatability",
        "History-level repeatability",
        "Genetic accessibility",
        "Finite realization",
        "location and scale of repeatability loss",
    ):
        assert phrase in text
    lock = json.loads(VNEXT_LOCK.read_text(encoding="utf-8"))
    assert "transmission of repeatability" in lock["novelty_boundary"]["novel_target"]


def test_vnext_has_one_coherent_figure_plan() -> None:
    text = _text()
    assert text.count("# Figure captions") == 1
    assert text.count("**Figure 1.") == 1
    assert text.count("**Figure 2.") == 1
    assert text.count("**Figure 3.") == 1
    assert text.count("**Figure 4.") == 1
    assert text.count("**Figure 5.") == 1
