from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/chapter2-scientific-gate.yml"


def test_scientific_gate_workflow_runs_all_fixed_analysis_stages():
    text = WORKFLOW.read_text(encoding="utf-8")
    for token in [
        "--replicates 96",
        "--points 48",
        "--replicates 24",
        "--replicates 12",
        "run_response_geometry_realization_stability.py",
        "run_joint_response_transition_surface.py",
        "run_context_assurance_threshold_maps.py",
        "evaluate_chapter2_scientific_gate.py",
        "chapter2-scientific-gate-results",
    ]:
        assert token in text
