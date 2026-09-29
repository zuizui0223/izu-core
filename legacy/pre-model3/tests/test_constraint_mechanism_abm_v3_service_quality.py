import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v3_service_quality.py"
RESULT = ROOT / "data/results/constraint_mechanism_abm_v3_service_quality.json"
V2 = ROOT / "data/results/constraint_mechanism_abm_v2_branching.json"


def load_module():
    spec = importlib.util.spec_from_file_location("constraint_mechanism_abm_v3", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_service_quality_is_not_conditioned_on_geography_or_origin():
    m = load_module()
    import random
    mainland, oceanic = m.scenarios()
    p1 = m.make_pollinator(random.Random(1), mainland)
    p2 = m.make_pollinator(random.Random(2), oceanic)
    assert 0.20 <= p1.service_quality <= 1.80
    assert 0.20 <= p2.service_quality <= 1.80


def test_v3_result_preserves_falsification_instead_of_retuning():
    x = json.loads(RESULT.read_text())
    v2 = json.loads(V2.read_text())
    assert x["falsification"]["both_response_signs_present"] is True
    assert x["falsification"]["service_quality_heterogeneity_broadens_branching_relative_to_v2"] is False
    assert x["summary"]["positive_lineage_responses"] < v2["summary"]["positive_lineage_responses"]
    assert x["decision"] == "partner_service_quality_heterogeneity_alone_is_insufficient"
