import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/CHAPTER2_MANUSCRIPT_EL_REPEATABILITY_20261003.md"
POSITIONING = ROOT / "docs/CHAPTER2_EL_REPEATABILITY_POSITIONING_20261003.md"
LOCK = ROOT / "data/design/chapter2_el_repeatability_lock_20261003.json"
POP_AUDIT = ROOT / "data/results/chapter2_bridge_population_scale_diagnostic_20261003.json"


def _word_count(text: str) -> int:
    return len(re.findall(r"\\b[\\w–-]+\\b", text))


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
    assert "aggregate evolutionary recurrence" in lower
    assert "uniform realized evolutionary trajectories" in lower


def test_focal_repeatability_evidence_is_occupied_finite_bridge_not_dep075_closure():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8").lower()
    assert "all 3,072 natural near cases and all 3,072 natural far cases remained occupied" in manuscript
    assert "mean far-minus-near inherited-investment effect was -0.1446" in manuscript
    assert "retain the depression-0.75 labels only as a mathematical closure sensitivity" in manuscript
    assert "do not use them as evidence about repeatability among persisting populations" in manuscript


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
    assert "does not, by itself, imply uniform realized evolutionary trajectories" in lock["general_logical_implication"]
    prohibited = set(lock["prohibited_claims"])
    assert "depression 0.75 deterministic history labels as evidence about repeatability among persisting populations" in prohibited
    assert "deterministic genotype density as the stochastic mean of the finite ABM" in prohibited
    assert "41.5 percent gap closure as a finite-population attenuation or convergence coefficient" in prohibited


def test_journal_target_is_explicitly_unresolved():
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    positioning = POSITIONING.read_text(encoding="utf-8")
    assert lock["format_target"]["journal"] == "unresolved: Ecology Letters vs Evolution Letters"
    assert "journal target unresolved" in positioning.lower()


def test_candidate_stays_within_internal_compact_format():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    assert _word_count(_abstract(manuscript)) <= lock["format_target"]["internal_abstract_words_max"]
    assert _word_count(_main_without_core_references(manuscript)) <= lock["format_target"]["internal_main_text_words_max"]


def test_positioning_preserves_constructive_not_calibrated_interpretation():
    positioning = POSITIONING.read_text(encoding="utf-8").lower()
    assert "established by simulation" in positioning
    assert "general implication" in positioning
    assert "natural prediction" in positioning
    assert "conditional deterministic closure" in positioning
    assert "not the stochastic mean" in positioning
