import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/run_assurance_buffering_capability_ablation.py"


def load_module():
    spec = importlib.util.spec_from_file_location("assurance_buffering_capability_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_assurance_modes_change_only_reproductive_route():
    module = load_module()
    v4 = module.load_module(module.V4_SCRIPT, "assurance_test_v4")
    templates = v4.make_lineages(__import__("random").Random(11), 5)
    off = module.transform_templates(templates, "off")
    baseline = module.transform_templates(templates, "baseline_only")
    full = module.transform_templates(templates, "full_adaptive")

    assert all(row.assurance_ceiling == 0.0 and row.assurance_responsiveness == 0.0 for row in off)
    assert all(row.assurance_ceiling == source.assurance_ceiling for row, source in zip(baseline, templates))
    assert all(row.assurance_responsiveness == 0.0 for row in baseline)
    assert full == templates


def test_small_matched_ablation_preserves_upstream_and_never_loads_empirical_targets():
    module = load_module()
    result = module.build(replicates=1, contexts=2, n_lineages=8, steps=20, seed=20260823)
    summary = result["summary"]

    assert result["status"] == "synthetic_matched_capability_test_not_empirical_mechanism_admission"
    assert result["fixed_components"]["empirical_targets_loaded"] == []
    assert result["fixed_components"]["hawaii_outcomes_loaded"] is False
    assert result["fixed_components"]["campanula_outcomes_loaded"] is False
    assert summary["service_and_opportunity_invariant_all_contrasts"] is True
    assert summary["lineage_contrasts"] == 3 * 3 * 1 * 8
    assert 0 <= summary["service_decline_and_assurance_off_reproduction_decline"] <= summary["service_decline_contrasts"]
    assert summary["full_sign_rescue_count"] <= summary["full_attenuation_count"]
    assert result["decision"] in {
        "existing_assurance_route_has_synthetic_sign_rescue_buffering_capability",
        "existing_assurance_route_attenuates_service_driven_reproductive_declines_without_sign_rescue",
        "existing_assurance_route_does_not_buffer_service_driven_reproductive_declines_in_declared_envelope",
    }


def test_buffer_definition_is_threshold_free_and_empirical_admission_remains_separate():
    module = load_module()
    result = module.build(replicates=1, contexts=1, n_lineages=4, steps=10, seed=7)
    definition = result["design"]["buffer_definition"]
    assert "OFF < 0 and ON >= 0" in definition
    assert "No empirical tolerance" in definition
    assert "model capability only" in result["claim_boundary"]
    assert "buffer_mechanism_abm_admission_interface.json" in result["claim_boundary"]
