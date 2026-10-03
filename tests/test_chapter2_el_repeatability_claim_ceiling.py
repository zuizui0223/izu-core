import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/CHAPTER2_MANUSCRIPT_EL_REPEATABILITY_20261003.md"
POSITIONING = ROOT / "docs/CHAPTER2_EL_REPEATABILITY_POSITIONING_20261003.md"
LOCK = ROOT / "data/design/chapter2_el_repeatability_lock_20261003.json"
POP_AUDIT = ROOT / "data/results/chapter2_bridge_population_scale_diagnostic_20261003.json"
BOUNDARY_STAGE1 = ROOT / "data/results/chapter2_deterministic_persistence_boundary_stage1_20261003.json"
BOUNDARY_REFINEMENT = ROOT / "data/results/chapter2_deterministic_persistence_boundary_refinement_20261003.json"
HISTORY_SIGNAL = ROOT / "data/results/chapter2_finite_history_signal_diagnostic_20261003.json"
HISTORY_SIGNAL_RECEIPT = ROOT / "data/results/chapter2_finite_history_signal_reproduction_receipt_20261003.json"
VALIDATION_DESIGN = ROOT / "data/design/chapter2_finite_history_signal_validation_20261003.json"
VALIDATION_RESULT = ROOT / "data/results/chapter2_finite_history_signal_validation_20261003.json"
VALIDATION_RECEIPT = ROOT / "data/results/chapter2_finite_history_signal_validation_receipt_20261003.json"
VALIDATION_RUNNER = ROOT / "scripts/run_chapter2_finite_history_signal_validation.py"
VALIDATION_SUMMARIZER = ROOT / "scripts/summarize_chapter2_finite_history_signal_validation.py"
VALIDATION_SOURCE_SNAPSHOT = ROOT / "data/results/model3_ch2_bridge_resource_pilot_v2_20260927.sources.zip"
BRIDGE_SOURCE_CONTRACT = ROOT / "data/design/model3_ch2_bridge_execution_20260927.json"


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
    assert "same increase in directional sign uniformity can accompany either strong preservation of history-specific magnitude" in lower
    assert lock["finite_history_signal_diagnostic"]["status"].startswith("posthoc exploratory")
    assert "mixed-sign history counts as a complete measure of evolutionary repeatability" in set(lock["prohibited_claims"])


def test_history_signal_reproduction_receipt_is_complete_and_matches_result():
    result = json.loads(HISTORY_SIGNAL.read_text(encoding="utf-8"))
    receipt = json.loads(HISTORY_SIGNAL_RECEIPT.read_text(encoding="utf-8"))

    assert receipt["status"].endswith("shard_hashes_verified")
    hashes = receipt["source"]["shard_sha256"]
    assert len(hashes) == 16
    assert sorted(hashes) == [f"shard-{i:02d}.json" for i in range(16)]
    assert len(set(hashes.values())) == 16
    assert all(re.fullmatch(r"[0-9a-f]{64}", h) for h in hashes.values())
    assert receipt["source"]["shard_sha256_root"] == "840655ed8352d1da1889b9b383a09406414514807eabdc0158019fe75858b447"

    for arm in ("natural", "richness_matched", "visitor_pooled", "large_plant_capacity"):
        rr = receipt["matched_point_estimates"][arm]
        er = result["estimates"][arm]
        assert rr["mean_effect"] == er["mean_effect"]
        assert rr["sigma_history"] == er["sigma_history"]["estimate"]
        assert rr["sigma_start_by_history"] == er["sigma_start_by_history"]["estimate"]
        assert rr["sigma_demographic_residual"] == er["sigma_demographic_residual"]["estimate"]
        assert rr["eight_repeat_reliability"] == er["eight_repeat_reliability"]["estimate"]
        assert rr["split_half_history_correlation"] == er["split_half_history_correlation"]["estimate"]

    assert "does not upgrade the post-hoc diagnostic" in receipt["claim_boundary"]

    assert receipt["matched_balanced_split_half_robustness"] == result["balanced_split_half_robustness"]


def test_measurement_novelty_boundary_is_fail_closed():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8").lower()
    positioning = POSITIONING.read_text(encoding="utf-8").lower()
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    prohibited = set(lock["prohibited_claims"])
    citations = {x["citation"]: x for x in lock["key_literature"]}

    assert manuscript.splitlines()[0].lower().startswith("# directional similarity can mask")
    assert "general direction metric should not simply be equated with geometric parallelism" in manuscript
    assert "bisschop et al. (2026)" in manuscript
    assert "environmental and demographic heterogeneity can reduce evolutionary repeatability" in manuscript

    assert "directional sign similarity as identical to geometric parallelism" in prohibited
    assert "first demonstration that environmental or demographic heterogeneity changes evolutionary repeatability" in prohibited
    assert citations["Bisschop et al. 2026"]["doi"] == "10.1093/evlett/qrag017"

    assert "do not claim that direction and magnitude are newly separated" in positioning
    assert "environmental/demographic variation affecting repeatability is new" in positioning


def test_history_signal_is_robust_to_all_balanced_repeat_splits():
    result = json.loads(HISTORY_SIGNAL.read_text(encoding="utf-8"))
    robust = result["balanced_split_half_robustness"]
    large = robust["paired_difference_vs_natural"]["large_plant_capacity"]
    pooled = robust["paired_difference_vs_natural"]["visitor_pooled"]

    assert large["positive_splits"] == large["total_splits"] == 35
    assert pooled["positive_splits"] == 0 and pooled["total_splits"] == 35
    assert robust["large_plant_capacity"]["min"] > robust["natural"]["max"]
    assert robust["visitor_pooled"]["max"] < robust["natural"]["min"]

    manuscript = MANUSCRIPT.read_text(encoding="utf-8").lower()
    assert "all 35 balanced 4-versus-4 splits" in manuscript
    assert "ordering was invariant across all 35 balanced 4-versus-4 splits" in manuscript


def test_new_demographic_seed_validation_meets_frozen_strong_success_rule():
    design = json.loads(VALIDATION_DESIGN.read_text(encoding="utf-8"))
    result = json.loads(VALIDATION_RESULT.read_text(encoding="utf-8"))
    receipt = json.loads(VALIDATION_RECEIPT.read_text(encoding="utf-8"))
    lock = json.loads(LOCK.read_text(encoding="utf-8"))

    assert design["status"] == "prospective_frozen_before_new_demographic_execution"
    assert design["validation_source"]["new_demographic_seeds"] == [201, 202, 203, 204]
    assert result["status"] == "complete_prospectively_frozen_new_demographic_seed_validation"
    assert result["provenance"]["finite_arm_trajectories"] == 9216
    assert result["primary_decision"]["strong_success"] is True

    corr = {
        k: result["reports"][k]["discovery_validation_history_correlation"]["estimate"]
        for k in ("natural", "visitor_pooled", "large_plant_capacity")
    }
    assert corr["large_plant_capacity"] > corr["natural"] > corr["visitor_pooled"]

    large = result["paired_bootstrap_differences"]["large_capacity_minus_natural_history_correlation"]["bootstrap95"]
    pooled = result["paired_bootstrap_differences"]["visitor_pooled_minus_natural_history_correlation"]["bootstrap95"]
    assert large[0] > 0
    assert pooled[1] < 0
    assert all(v["occupied_fraction"] == 1.0 for v in result["terminal_occupancy"].values())

    assert receipt["status"] == "complete_local_exact_source_validation_execution_with_separate_committed_reproduction_surface"
    assert receipt["execution"]["shard_count"] == 16
    freeze = receipt["prospective_freeze_provenance"]
    assert freeze["validation_design_commit"] == "4ca0193625fce2f9abac8a937a234b6c7825ee10"
    assert freeze["validation_design_commit_utc"] == "2026-10-03T14:04:10Z"
    assert freeze["decision"].startswith("validation design, new seeds")
    assert receipt["execution"]["total_arm_trajectories"] == 9216
    assert len(receipt["execution"]["shard_sha256"]) == 16
    assert receipt["exact_implementation_check"]["full_simulate_vs_compact_runner_terminal_population_all_equal"] is True
    assert receipt["exact_implementation_check"]["maximum_absolute_investment_change_difference"] < 2e-15

    validation = lock["finite_history_signal_validation"]
    assert validation["strong_success"] is True
    assert validation["validation_scope"] == "same 128 frozen visitor histories; new demographic seeds 201-204"

    manuscript = MANUSCRIPT.read_text(encoding="utf-8").lower()
    assert "9,216 trajectories using new demographic seeds 201–204" in manuscript
    assert "prospectively frozen new-seed validation met its strong-success rule" in manuscript
    assert "not transfer to new environmental histories or natural islands" in manuscript

    prohibited = set(lock["prohibited_claims"])
    assert "the original posthoc finite-history discovery as preregistered or confirmatory" in prohibited
    assert "new demographic seed validation as independent environmental-history replication" in prohibited
    assert "new demographic seed validation as natural-island validation" in prohibited


def test_validation_receipt_distinguishes_execution_provenance_from_committed_reproduction():
    receipt = json.loads(VALIDATION_RECEIPT.read_text(encoding="utf-8"))

    def sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def git_blob_sha(path: Path) -> str:
        rel = path.relative_to(ROOT).as_posix()
        proc = subprocess.run(
            ["git", "rev-parse", f"HEAD:{rel}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return proc.stdout.strip()

    assert re.fullmatch(r"[0-9a-f]{64}", receipt["execution"]["local_execution_runner_sha256"])
    assert re.fullmatch(r"[0-9a-f]{64}", receipt["execution"]["local_aggregation_script_sha256"])

    surface = receipt["committed_reproduction_surface"]
    assert surface["byte_identical_to_local_execution_scripts"] is False
    assert git_blob_sha(VALIDATION_RUNNER) == surface["runner_git_blob_sha"]
    assert git_blob_sha(VALIDATION_SUMMARIZER) == surface["summarizer_git_blob_sha"]

    exact = receipt["exact_source"]
    assert sha256(VALIDATION_SOURCE_SNAPSHOT) == exact["committed_reproduction_zip_sha256"]
    bridge = json.loads(BRIDGE_SOURCE_CONTRACT.read_text(encoding="utf-8"))
    with zipfile.ZipFile(VALIDATION_SOURCE_SNAPSHOT) as zf:
        names = set(zf.namelist())
        for rel, expected in bridge["source_hashes"].items():
            assert rel in names, rel
            assert hashlib.sha256(zf.read(rel)).hexdigest() == expected, rel

    assert "zip byte identity is not claimed" in exact["relationship"].lower()
    assert "need not be byte-identical" in receipt["claim_boundary"]
