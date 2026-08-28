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
        "python -m scripts.run_response_geometry_realization_stability",
        "python -m scripts.run_joint_response_transition_surface",
        "python -m scripts.run_context_assurance_threshold_maps",
        "python -m scripts.evaluate_chapter2_scientific_gate",
        "chapter2-scientific-gate-results",
    ]:
        assert token in text


def test_scientific_gate_does_not_use_direct_script_entrypoints():
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "python scripts/" not in text
