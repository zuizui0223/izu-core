import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/run_network_context_buffering_capability_ablation.py"


def load_module():
    spec = importlib.util.spec_from_file_location("network_context_buffering_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_assurance_is_fully_disabled_for_network_context_test():
    module = load_module()
    v4 = module.load_module(module.V4_SCRIPT, "network_context_test_v4")
    templates = v4.make_lineages(__import__("random").Random(17), 6)
    disabled = module.disable_assurance(templates)
    assert all(row.assurance_ceiling == 0.0 for row in disabled)
    assert all(row.assurance_responsiveness == 0.0 for row in disabled)
    assert [row.pollinator_dependency for row in disabled] == [row.pollinator_dependency for row in templates]
    assert [row.trait for row in disabled] == [row.trait for row in templates]


def test_small_network_context_ablation_uses_no_empirical_targets_and_has_valid_counts():
    module = load_module()
    result = module.build(replicates=1, contexts=2, n_lineages=8, steps=20, seed=20260823)
    summary = result["summary"]

    assert result["status"] == "synthetic_matched_capability_test_not_empirical_mechanism_admission"
    assert result["matched_ablation"]["empirical_targets_loaded"] == []
    assert result["matched_ablation"]["assurance_ceiling"] == 0.0
    assert result["matched_ablation"]["assurance_responsiveness"] == 0.0
    assert result["matched_ablation"]["same_global_opportunity_networks_between_support_modes"] is True
    assert summary["lineage_contrasts"] == 3 * 1 * 8
    assert 0 <= summary["global_decline_and_support_off_service_decline"] <= summary["global_opportunity_decline_contrasts"]
    assert 0 <= summary["global_decline_and_support_off_reproduction_decline"] <= summary["global_opportunity_decline_contrasts"]
    assert summary["service_sign_rescue_count"] <= summary["global_decline_and_support_off_service_decline"]
    assert summary["reproduction_sign_rescue_count"] <= summary["global_decline_and_support_off_reproduction_decline"]
    assert result["decision"] in {
        "existing_local_support_route_has_synthetic_network_context_sign_buffering_capability",
        "existing_local_support_route_can_rescue_effective_service_sign_without_reproductive_sign_rescue",
        "existing_local_support_route_changes_buffering_magnitude_without_sign_rescue",
        "existing_local_support_route_does_not_buffer_declining_global_opportunity_in_declared_envelope",
    }


def test_with_assurance_off_reproductive_sign_tracks_effective_service_sign():
    module = load_module()
    result = module.build(replicates=1, contexts=2, n_lineages=8, steps=20, seed=1234)
    summary = result["summary"]
    assert summary["reproduction_sign_rescue_count"] == summary["service_sign_rescue_count"]
    assert summary["reproduction_magnitude_rescue_count"] == summary["service_magnitude_rescue_count"]


def test_claim_boundary_keeps_guaiacum_empirical_admission_separate():
    module = load_module()
    result = module.build(replicates=1, contexts=1, n_lineages=4, steps=10, seed=9)
    assert "synthetic capability" in result["claim_boundary"]
    assert "Guaiacum" in result["claim_boundary"]
    assert "Empirical admission remains governed" in result["claim_boundary"]
    assert "zero directional boundary" in result["design"]["sign_rescue_definition"]
