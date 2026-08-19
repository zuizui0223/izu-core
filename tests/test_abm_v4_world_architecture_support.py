import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/check_abm_v4_world_architecture_support.py"
RESULT = ROOT / "data/results/abm_v4_world_architecture_support.json"


def load_module():
    spec = importlib.util.spec_from_file_location("abm_v4_world_support", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_committed_world_support_matches_generator():
    m = load_module()
    assert m.build_support() == json.loads(RESULT.read_text())


def test_all_observed_macroclasses_are_generated_across_full_envelope():
    x = json.loads(RESULT.read_text())
    assert x["test"] == "pass"
    for s in x["saturation_envelope"].values():
        assert s["all_observed_macroclasses_covered"] is True
    assert x["decision"] == "v4_has_robust_generative_support_for_all_observed_world_architecture_macroclasses"
