import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/diagnose_abm_partner_count_bias.py"
RESULT = ROOT / "data/results/abm_partner_count_ablation.json"


def load_module():
    spec = importlib.util.spec_from_file_location("abm_partner_count_diag", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_ablation_separates_count_from_composition():
    m = load_module()
    v2 = m.load_v2()
    mainland, oceanic, count_only, composition_only = m.diagnostic_scenarios(v2)
    assert count_only.n_pollinator_types == oceanic.n_pollinator_types
    assert count_only.generalist_fraction == mainland.generalist_fraction
    assert composition_only.n_pollinator_types == mainland.n_pollinator_types
    assert composition_only.generalist_fraction == oceanic.generalist_fraction


def test_committed_diagnosis_identifies_count_accumulation_bias():
    x = json.loads(RESULT.read_text())
    assert x["summary"]["count_only"]["mean_delta"] < x["summary"]["oceanic_full"]["mean_delta"]
    assert x["summary"]["composition_only"]["mean_delta"] > 0
    assert x["decision"] == "decline_bias_is_dominated_by_partner_opportunity_accumulation"
