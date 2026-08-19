import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate_abm_v4_against_heldout_izu.py"
RESULT = ROOT / "data/results/abm_v4_heldout_izu_validation.json"


def load_module():
    spec = importlib.util.spec_from_file_location("abm_v4_heldout_izu_validation", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_committed_validation_matches_generator():
    m = load_module()
    assert m.build_validation() == json.loads(RESULT.read_text())


def test_v4_heldout_result_is_robust_across_full_envelope():
    x = json.loads(RESULT.read_text())
    assert x["tests"]["matching_decline_direction_robust_across_envelope"] == "pass"
    assert x["tests"]["reproductive_response_branching_robust_across_envelope"] == "pass"
    for s in x["model_envelope"].values():
        assert s["predicts_matching_decline_majority"] is True
        assert s["predicts_reproductive_sign_branching"] is True
    assert x["decision"] == "v4_survives_heldout_izu_at_qualitative_mechanism_level"
