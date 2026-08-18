import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/analyze_mainland_island_falsification.py"
LEDGER = ROOT / "data/results/mainland_island_falsification_ledger.json"
SUMMARY = ROOT / "data/results/mainland_island_falsification_summary.json"


def load_module():
    spec = importlib.util.spec_from_file_location("mainland_island_falsification", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_generated_summary_matches_committed_result():
    module = load_module()
    data = json.loads(LEDGER.read_text())
    expected = json.loads(SUMMARY.read_text())
    assert module.build_summary(data) == expected


def test_overbroad_island_specific_claims_are_rejected():
    summary = json.loads(SUMMARY.read_text())
    assert summary["hypothesis_assessment"]["H0_functional_recurrence_is_island_specific"] == "rejected"
    assert summary["hypothesis_assessment"]["H0_architectural_contingency_is_island_specific"] == "rejected"


def test_surviving_candidate_is_narrower_than_functional_recurrence():
    summary = json.loads(SUMMARY.read_text())
    assert summary["surviving_island_specific_candidate"] == "oceanic_insularity_changes_architectural_opportunity_space"
    assert summary["hypothesis_assessment"]["H2_island_specificity_of_function_architecture_coupling"] == "not_yet_established"
