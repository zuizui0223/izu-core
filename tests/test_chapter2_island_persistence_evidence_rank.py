"""Evidence status: distinct frozen estimands never overwrite one another."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def load(relative):
    return json.loads((ROOT/relative).read_text(encoding="utf-8"))


def test_independent32_simulation_persistence_is_a_passed_targeted_gate():
    protocol=load("data/design/chapter2_island_demographic_independent32_20261008.json")
    outcome=load("data/results/chapter2_island_demographic_independent32_20261008.json")
    assert protocol["status"]=="frozen_before_new_history_demographic_confirmation"
    assert protocol["independent_visitor_histories"]["count"]==32
    assert protocol["stress_ovule_budgets"]==[2,3,4,5]
    assert outcome["status"]=="independent_new_history_targeted_gate_passed_pilot_informed_grid"
    assert outcome["post_switch_trajectories"]==4096
    primary=outcome["predeclared_pooled_primary"]
    assert primary["pass"] is True
    assert primary["mean"]==0.1083984375
    assert primary["bootstrap95"]==[0.0654296875,0.1513671875]
    prior=next(s for s in outcome["per_setting"] if s["setting"]=="prior_selfing")
    assert prior["bootstrap95"][0]<0<prior["bootstrap95"][1]


def test_later_failure_does_not_reverse_different_independent32_inference():
    payoff=load("data/results/chapter2_island_payoff_independent_offline_20261008.json")
    order=load("data/results/chapter2_island_mutational_priority_independent16_20261008.json")
    donor=load("data/results/chapter2_island_genetic_state_transplant_independent16_20261008.json")
    assert payoff["adjudication"]["global_pass"] is False
    assert order["frozen_primary"]["passed"] is False
    assert donor["frozen_primary"]["passed"] is False
    status=(ROOT/"docs/CHAPTER2_ISLAND_PERSISTENCE_PROMOTION_DECISION_20261008.md").read_text(encoding="utf-8")
    assert "Independent conditional confirmation: PASS" in status
    assert "not discarded or downgraded" in (ROOT/"docs/CHAPTER2_ISLAND_DEMOGRAPHIC_PERSISTENCE_20261008.md").read_text(encoding="utf-8")
    assert "Pilot-informed stress range" in status
    assert "one demographic realization per history" in status
    assert "not a general island-biogeographic law" in status
