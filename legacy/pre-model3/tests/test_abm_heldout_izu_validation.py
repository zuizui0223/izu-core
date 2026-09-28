import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate_abm_against_heldout_izu.py"
RESULT = ROOT / "data/results/abm_heldout_izu_validation.json"


def load_module():
    spec = importlib.util.spec_from_file_location("abm_heldout_izu_validation", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_generated_validation_matches_committed_result():
    m = load_module()
    abm = json.loads((ROOT / "data/results/constraint_mechanism_abm_v1.json").read_text())
    izu = json.loads((ROOT / "data/predictive_meta/hiraiwa_ushimaru_cross_channel_concordance.json").read_text())
    assert m.build_validation(abm, izu) == json.loads(RESULT.read_text())


def test_v1_survives_mechanism_class_but_not_quantitative_prediction():
    x = json.loads(RESULT.read_text())
    assert x["tests"]["opportunity_constraint_direction"] == "pass"
    assert x["tests"]["heldout_matching_decline"] == "pass"
    assert x["tests"]["response_branching_class"] == "pass"
    assert x["tests"]["uniform_reproductive_decline"] == "not_supported_as_species_level_prediction"
    assert x["decision"] == "mechanism_class_survives_heldout_but_v1_is_not_a_quantitative_predictor"
