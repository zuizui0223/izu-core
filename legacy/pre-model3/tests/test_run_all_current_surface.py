import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "paper" / "run_all.py"
SPEC = importlib.util.spec_from_file_location("izu_run_all", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_consolidated_runner_excludes_superseded_rank_weighted_meta_surface() -> None:
    stage_paths = [path for _, path, _ in MODULE.STAGES]
    assert "scripts/report_current_evidence_state.py" in stage_paths
    assert "paper/validate_regime_transition_registry.py" in stage_paths
    assert "paper/threshold_analysis.py" in stage_paths

    assert "paper/validate_meta_inputs.py" not in stage_paths
    assert "paper/classify_functional_groups.py" not in stage_paths
    assert "paper/meta_synthesis.py" not in stage_paths
    assert "paper/comprehensive_sweep.py" not in stage_paths
