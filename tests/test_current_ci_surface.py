from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / ".github/workflows/ci.yml"
GATE = ROOT / ".github/workflows/chapter2-scientific-gate.yml"


def test_primary_ci_does_not_rerun_legacy_model2_audits_on_every_pr() -> None:
    text = CI.read_text(encoding="utf-8")
    assert "pytest -q" in text
    for legacy in (
        "audit_chapter2_relational_robustness",
        "audit_chapter2_realized_richness_matching",
        "audit_chapter2_finite_community_system_size",
        "audit_finite_n_gaussian_mean_field",
        "audit_trait_adjustment_system_size_rank_crossover",
        "audit_chapter2_postfreeze_grid_update_rule",
        "run_chapter2_phi_timebin_rarefaction_from_locked_sources",
    ):
        assert legacy not in text


def test_chapter2_gate_targets_current_unified_model3_surface() -> None:
    text = GATE.read_text(encoding="utf-8")
    for current in (
        "test_chapter2_mechanistic_funnel.py",
        "test_chapter2_model3_submission.py",
        "test_chapter2_branch_identifiability_boundary.py",
        "test_chapter2_independent_unit_reporting.py",
        "test_chapter2_submission_closure_audit.py",
        "test_chapter2_unified_model3_figures.py",
        "test_repository_artifact_budget.py",
    ):
        assert current in text
    for legacy in (
        "run_response_geometry_realization_stability",
        "run_joint_response_transition_surface",
        "run_context_assurance_threshold_maps",
        "evaluate_chapter2_scientific_gate",
        "audit_chapter2_el_rank_crossover_generalization",
    ):
        assert legacy not in text
