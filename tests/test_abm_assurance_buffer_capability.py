import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/run_abm_assurance_buffer_capability.py"


def load_script():
    spec = importlib.util.spec_from_file_location("abm_assurance_buffer_capability_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_small_matched_ablation_preserves_upstream_service_and_loads_no_empirical_targets():
    module = load_script()
    payload = module.build(replicates=1, contexts=2, n_lineages=8, steps=20, seed=20260823)
    summary = payload["summary"]

    assert payload["design"]["empirical_inputs_loaded"] == []
    assert payload["design"]["empirical_target_values_loaded"] is False
    assert summary["upstream_service_identical_between_assurance_ablations"] is True
    assert summary["configuration_count"] == 9
    assert summary["lineage_contrast_count"] == 72
    assert summary["decision"] in {
        "existing_assurance_route_can_generate_full_sign_buffering_without_new_parameter",
        "existing_assurance_route_can_attenuate_reproductive_propagation_without_full_sign_buffering",
        "existing_assurance_route_does_not_generate_buffering_under_frozen_envelope",
    }


def test_buffer_definitions_are_sign_based_not_effect_size_thresholded():
    module = load_script()
    interpretation = module.build(replicates=1, contexts=1, n_lineages=4, steps=5)[
        "threshold_free_interpretation"
    ]
    assert "service < 0" in interpretation["eligible"]
    assert "reproduction < 0" in interpretation["eligible"]
    assert "> matched assurance-OFF contrast" in interpretation["partial_attenuation"]
    assert ">= 0" in interpretation["full_sign_buffer"]
    assert "numerical sign tolerance only" in interpretation["note"]
