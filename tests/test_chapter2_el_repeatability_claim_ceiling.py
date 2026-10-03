import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/CHAPTER2_MANUSCRIPT_EL_REPEATABILITY_20261003.md"
POSITIONING = ROOT / "docs/CHAPTER2_EL_REPEATABILITY_POSITIONING_20261003.md"
LOCK = ROOT / "data/design/chapter2_el_repeatability_lock_20261003.json"
POP_AUDIT = ROOT / "data/results/chapter2_bridge_population_scale_diagnostic_20261003.json"
BOUNDARY_STAGE1 = ROOT / "data/results/chapter2_deterministic_persistence_boundary_stage1_20261003.json"
BOUNDARY_REFINEMENT = ROOT / "data/results/chapter2_deterministic_persistence_boundary_refinement_20261003.json"
HISTORY_SIGNAL = ROOT / "data/results/chapter2_finite_history_signal_diagnostic_20261003.json"


def _word_count(text: str) -> int:
    return len(re.findall(r"\b[\w–-]+\b", text))


def _abstract(manuscript: str) -> str:
    return manuscript.split("## Abstract", 1)[1].split("## Keywords", 1)[0].strip()


def _main_without_core_references(manuscript: str) -> str:
    return manuscript.split("# Core references for framing", 1)[0]


def test_repeatability_candidate_keeps_three_inference_levels_separate():
    lower = MANUSCRIPT.read_text(encoding="utf-8").lower()
    assert "## claim hierarchy and simulation inference ceiling" in lower
    assert "model-established result" in lower
    assert "general logical implication" in lower
    assert "empirical prediction" in lower
    assert "directional sign uniformity" in lower
    assert "historical repeatability" in lower


def test_focal_repeatability_evidence_is_occupied_finite_bridge_not_dep075_closure():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8").lower()
    assert "all 3,072 near and 3,072 far cases were occupied" in manuscript
    assert "finite abm mean far-minus-near investment effect was -0.1446" in manuscript
    assert "high-depression deterministic sensitivity entered quasi-extinction" in manuscript
    assert "excluded from persisting-population inference" in manuscript


def test_population_scale_audit_separates_dep050_from_dep075():
    audit = json.loads(POP_AUDIT.read_text(encoding="utf-8"))
    d50 = audit["depression_0_50_at_200"]
    d75 = audit["depression_0_75_at_200"]
    assert d50["deterministic_far_density_mass"]["median"] == 48.0
    assert d50["finite_far_population_demo_101"]["occupied_fraction"] == 1.0
    assert d50["decision"] == "no_population_scale_disagreement_at_original_headline_condition"
    assert d75["deterministic_far_density_mass"]["below_1_fraction"] > 0.98
    assert d75["finite_far_population_demo_101"]["occupied_fraction"] == 0.0
    assert d75["decision"] == "depression_0_75_deterministic_history_labels_not_population_persistence_evidence"


def test_lock_prohibits_density_as_stochastic_expectation_and_dep075_headline():
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    assert lock["active_oikos_submission_replaced"] is False
    assert "occupied depression-0.50" in lock["safe_claim"]
    assert "does not, by itself, identify weaker historical contingency" in lock["general_logical_implication"]
    prohibited = set(lock["prohibited_claims"])
    assert "depression 0.75 deterministic history labels as evidence about repeatability among persisting populations" in prohibited
    assert "deterministic genotype density as the stochastic mean of the finite ABM" in prohibited
    assert "41.5 percent gap closure as a finite-population attenuation or convergence coefficient" in prohibited


def test_journal_fit_prefers_evolution_letters_without_submitting():
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    positioning = POSITIONING.read_text(encoding="utf-8").lower()
    assert lock["format_target"]["journal_preferred"] == "Evolution Letters"
    assert lock["format_target"]["journal_fallback"].startswith("Ecology Letters")
    assert lock["format_target"]["submission_action_taken"] is False
    assert "preferred candidate: evolution letters" in positioning
    assert "journal-fit recommendation" in positioning


def test_candidate_stays_within_internal_compact_format():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    assert _word_count(_abstract(manuscript)) <= lock["format_target"]["evolution_letters"]["abstract_words_max"]
    assert _word_count(_main_without_core_references(manuscript)) <= lock["format_target"]["evolution_letters"]["main_text_guide_words"]


def test_positioning_preserves_constructive_not_calibrated_interpretation():
    positioning = POSITIONING.read_text(encoding="utf-8").lower()
    assert "established by simulation" in positioning
    assert "general implication" in positioning
    assert "natural prediction" in positioning
    assert "conditional deterministic closure" in positioning
    assert "not the stochastic mean" in positioning


def test_deterministic_nonparallelism_is_excluded_before_persistence_boundary():
    stage1 = json.loads(BOUNDARY_STAGE1.read_text(encoding="utf-8"))
    refine = json.loads(BOUNDARY_REFINEMENT.read_text(encoding="utf-8"))
    assert "No deterministic mixed/positive history was observed through depression 0.70" in stage1["first_stage_decision"]
    assert refine["decision"]["pre_quasi_extinction_nonparallelism_detected"] is False
    assert "negative-only" in refine["decision"]["conclusion"]

    manuscript = MANUSCRIPT.read_text(encoding="utf-8").lower()
    positioning = POSITIONING.read_text(encoding="utf-8").lower()
    lock = json.loads(LOCK.read_text(encoding="utf-8"))

    assert "found no mixed or positive deterministic history among histories whose three starts and both near/far endpoints all retained mass >=1" in manuscript
    assert "no deterministic history-level nonparallelism was observed among pre-quasi-extinction histories" in positioning
    assert lock["persistence_boundary_scan"]["headline_action"] == (
        "exclude deterministic history-level nonparallelism from the persisting-population repeatability claim"
    )
    assert "deterministic history-level nonparallelism among persisting isolation-assembly populations" in set(lock["prohibited_claims"])


def test_sign_uniformity_and_history_signal_move_differently():
    result = json.loads(HISTORY_SIGNAL.read_text(encoding="utf-8"))
    est = result["estimates"]
    assert result["status"] == "complete_posthoc_exact_source_finite_history_signal_diagnostic"
    assert est["natural"]["sign_mixed_histories_eps0"] == 12
    assert est["large_plant_capacity"]["sign_mixed_histories_eps0"] == 1
    assert est["visitor_pooled"]["sign_mixed_histories_eps0"] == 0
    assert est["large_plant_capacity"]["eight_repeat_reliability"]["estimate"] > est["natural"]["eight_repeat_reliability"]["estimate"]
    assert est["visitor_pooled"]["eight_repeat_reliability"]["estimate"] < est["natural"]["eight_repeat_reliability"]["estimate"]
    assert est["large_plant_capacity"]["split_half_history_correlation"]["estimate"] > 0.8
    assert est["visitor_pooled"]["split_half_history_correlation"]["estimate"] < 0.3

    lower = MANUSCRIPT.read_text(encoding="utf-8").lower()
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    assert "same increase in directional sign uniformity can accompany either a stronger reproducible historical imprint" in lower
    assert lock["finite_history_signal_diagnostic"]["status"].startswith("posthoc exploratory")
    assert "mixed-sign history counts as a complete measure of evolutionary repeatability" in set(lock["prohibited_claims"])
