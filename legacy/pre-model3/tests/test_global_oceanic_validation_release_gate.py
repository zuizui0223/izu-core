import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/audit_global_oceanic_validation_release.py"
RESULT = ROOT / "data/results/global_oceanic_validation_release_gate_v1.json"


def load_module():
    spec = importlib.util.spec_from_file_location("global_oceanic_validation_release_gate", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_committed_release_gate_matches_generator():
    m = load_module()
    assert m.build_gate() == json.loads(RESULT.read_text())


def test_four_strata_freeze_does_not_release_fit():
    x = json.loads(RESULT.read_text())
    assert x["candidate_strata_with_two_independent_systems"] == 4
    assert x["candidate_geographic_minimum_met"] is True
    assert x["candidate_sample_frozen"] is True
    assert x["balanced_global_quantitative_fit_released"] is False
    assert x["fully_admitted_strata_with_two_independent_systems"] == 0


def test_frozen_systems_are_outcome_blind_and_include_western_pacific_pair():
    x = json.loads(RESULT.read_text())
    strata = {s["stratum"]: s for s in x["frozen_candidate_strata"]}
    assert set(strata) == {
        "North Atlantic / Macaronesia",
        "western Indian Ocean",
        "eastern / central Pacific",
        "NW / western Pacific",
    }
    nw = {z["system"] for z in strata["NW / western Pacific"]["systems"]}
    assert nw == {"Izu archipelago", "Yongxing / Xisha"}
    assert "replace a frozen system because its ABM fit is poor" in x["forbidden_post_freeze_actions"]
    assert "no named-system ABM fit has been inspected" in x["claim_boundary"]
