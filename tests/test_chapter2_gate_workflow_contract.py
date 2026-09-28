from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/chapter2-scientific-gate.yml"


def test_scientific_gate_workflow_runs_current_model3_submission_checks():
    text = WORKFLOW.read_text(encoding="utf-8")
    for token in [
        "tests/test_chapter2_mechanistic_funnel.py",
        "tests/test_chapter2_realized_richness_reframe.py",
        "tests/test_chapter2_branch_identifiability_boundary.py",
        "tests/test_chapter2_independent_unit_reporting.py",
        "tests/test_chapter2_submission_closure_audit.py",
        "tests/test_chapter2_unified_model3_figures.py",
        "tests/test_repository_artifact_budget.py",
        "tests/test_current_ci_surface.py",
        "tests/test_workflow_trigger_policy.py",
    ]:
        assert token in text


def test_scientific_gate_does_not_rerun_legacy_model2_analysis_stages():
    text = WORKFLOW.read_text(encoding="utf-8")
    for token in [
        "run_response_geometry_realization_stability",
        "run_joint_response_transition_surface",
        "run_context_assurance_threshold_maps",
        "evaluate_chapter2_scientific_gate",
        "audit_chapter2_interaction_kernel",
        "audit_chapter2_el_rank_crossover_generalization",
    ]:
        assert token not in text


def test_scientific_gate_does_not_use_direct_script_entrypoints():
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "python scripts/" not in text
