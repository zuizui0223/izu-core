import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/design/pr90_blocking_task_ledger.json"


def load_ledger():
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def test_core_blocking_tasks_are_separate_and_present():
    ledger = load_ledger()
    tasks = {task["task_id"]: task for task in ledger["tasks"]}
    assert set(tasks) == {
        "hendriks_provenance",
        "third_floral_system",
        "empirical_reliability",
        "izu_direct_mechanism",
    }
    assert tasks["hendriks_provenance"]["issue"] == 94
    assert tasks["third_floral_system"]["issue"] == 95
    assert tasks["empirical_reliability"]["issue"] == 96
    assert tasks["izu_direct_mechanism"]["issue"] == 91


def test_provenance_repair_does_not_open_eiv_or_formal_fit():
    task = {t["task_id"]: t for t in load_ledger()["tasks"]}["hendriks_provenance"]
    assert "empirical_reliability_gate" in task["does_not_open"]
    assert "formal_cross_system_fit" in task["does_not_open"]


def test_reliability_task_cannot_substitute_an_assumed_value():
    task = {t["task_id"]: t for t in load_ledger()["tasks"]}["empirical_reliability"]
    assert "assumed_reliability_substitution" in task["does_not_open"]
    options = set(task["completion_requires_one_of"])
    assert "source_locked_reliability_with_uncertainty_propagated" in options
    assert "machine_readable_empirical_reliability_unidentifiable_result" in options


def test_field_pilot_cannot_promote_historical_causation():
    task = {t["task_id"]: t for t in load_ledger()["tasks"]}["izu_direct_mechanism"]
    assert "historical_Bombus_causation" in task["does_not_open"]
    assert "Oshima_Toshima_causal_boundary_by_itself" in task["does_not_open"]


def test_formal_cross_system_fit_remains_closed_by_default():
    gate = load_ledger()["formal_cross_system_fit_gate"]
    assert gate["current_state"] == "closed"
    forbidden = set(gate["cannot_be_opened_by"])
    assert "provenance_repair_alone" in forbidden
    assert "sensitivity_assumptions_treated_as_observed_reliability" in forbidden
    assert "abstract_level_effect_reconstruction" in forbidden
