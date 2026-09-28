import json
from copy import deepcopy
from pathlib import Path

from scripts.audit_model3_unified_reduction import run_audit


ROOT = Path(__file__).resolve().parents[1]


def _design():
    d = json.loads((ROOT / "data/design/model3_unified_reduction_audit_20260927.json").read_text())
    d = deepcopy(d)
    d["config"]["years"] = 6
    d["starting_access_states"] = [0.2, 0.8]
    d["demographic_replicates"] = [101, 102]
    return d


def test_nested_model3_reduction_audit_is_reproducible_and_count_control_is_exact():
    a = run_audit(_design())
    b = run_audit(_design())
    assert a == b
    assert a["status"] == "complete_prospective_model3_reduction_audit"
    assert a["diagnostics"]["duplicate_count_control_pass"]
    assert a["diagnostics"]["duplicate_count_control_max_abs_error"] < 1e-12
    assert len(a["fixed_state_rows"]) == 10
    assert len(a["trajectory_rows"]) == 10
    assert len(a["reference_contrasts"]) == 6


def test_scientific_decision_is_reported_not_hardcoded_as_test_success():
    result = run_audit(_design())
    assert result["decision"] in {
        "model2_not_required_as_independent_mechanistic_model",
        "model2_retains_unique_role_pending_unresolved_model3_reduction",
    }
    assert isinstance(result["diagnostics"]["fixed_state_branching_present"], bool)
    assert isinstance(result["diagnostics"]["deterministic_density_branching_present"], bool)
