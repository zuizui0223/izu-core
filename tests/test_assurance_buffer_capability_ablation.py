import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/run_assurance_buffer_capability_ablation.py"


def load_module():
    spec = importlib.util.spec_from_file_location("assurance_buffer_capability_test_module", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_small_matched_ablation_preserves_upstream_service_and_loads_no_empirical_target():
    module = load_module()
    result = module.build(replicates=1, contexts=2, n_lineages=8, steps=30, seed=20260823)
    assert result["status"] == "synthetic_model_capability_test_not_empirical_mechanism_admission"
    assert result["design"]["empirical_targets_loaded"] == []
    assert result["design"]["hawaii_outcomes_loaded"] is False
    assert result["design"]["campanula_outcomes_loaded"] is False
    assert result["design"]["new_buffer_parameter_added"] is False
    assert result["ablation"]["upstream_effective_service_identical_between_assurance_arms"] is True
    assert result["design"]["paired_lineage_contrasts"] == 3 * 3 * 1 * 8


def test_buffer_state_definitions_are_sign_based_not_target_fitted_thresholds():
    module = load_module()
    result = module.build(replicates=1, contexts=1, n_lineages=4, steps=20, seed=20260824)
    definitions = result["threshold_free_state_definitions"]
    assert "< 0" in definitions["service_loss"]
    assert "remains below 0" in definitions["partial_buffer"]
    assert "reaches or exceeds 0" in definitions["full_sign_buffer"]
    assert definitions["epsilon_only_for_floating_point_sign"] == module.EPS


def test_result_never_claims_empirical_hawaii_admission():
    module = load_module()
    result = module.build(replicates=1, contexts=1, n_lineages=4, steps=20, seed=20260825)
    assert "does not identify assurance as the empirical buffer in Hawaiʻi" in result["claim_boundary"]
    assert result["decision"].startswith("existing_assurance_route_")
