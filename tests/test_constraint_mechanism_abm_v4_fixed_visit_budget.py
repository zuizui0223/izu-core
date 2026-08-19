import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v4_fixed_visit_budget.py"
RESULT = ROOT / "data/results/constraint_mechanism_abm_v4_fixed_visit_budget.json"


def load_module():
    spec = importlib.util.spec_from_file_location("constraint_mechanism_abm_v4", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_fixed_budget_pollination_is_not_mechanically_increased_by_duplicate_partner_types():
    m = load_module()
    one = m.fixed_budget_pollination([0.5], 2.0)
    many_same = m.fixed_budget_pollination([0.5, 0.5, 0.5, 0.5], 2.0)
    assert one == many_same


def test_v4_sensitivity_envelope_keeps_both_response_signs():
    x = json.loads(RESULT.read_text())
    for s in x["saturation_envelope"].values():
        assert s["positive_lineage_responses"] > 0
        assert s["negative_lineage_responses"] > 0
    assert x["decision"] == "fixed_visit_budget_removes_partner_count_decline_bias_and_recovers_functional_conservation_with_branching"
