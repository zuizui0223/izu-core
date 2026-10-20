"""Check the exploratory three-state figure candidate without promoting it to G/S."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import pytest

from scripts.audit_chapter2_three_state_publication_20261019 import derive, SOURCE


def read():
    return json.loads(SOURCE.read_text(encoding="utf-8"))


def test_original_registered_endpoints_reproduced_without_inference_change():
    d = derive(read())
    assert d["status"] == "POST_OUTCOME_DESCRIPTIVE_READONLY_NOT_REGISTERED"
    assert d["new_uncertainty_estimated"] is False
    assert d["independent_confirmation"] is False
    assert d["n_founders"] == d["n_visitor_histories"] == 160
    assert d["crossed_cells_not_independent_islands"] == 25600
    assert d["registered_G_estimate"] == .08328125
    assert d["registered_S_estimate"] == .9270703125


def test_three_states_conserve_all_start_denominators():
    d = derive(read())
    expected = {
        ("B8", "fixed"): (11732, 13868, 0),
        ("B8", "evolving"): (9600, 16000, 0),
        ("B4p5", "fixed"): (140, 1245, 24215),
        ("B4p5", "evolving"): (9245, 15873, 482)
    }
    for (budget, policy), values in expected.items():
        group = d["budgets"][budget]["arms"][policy]
        actual = (group["alive_and_target_accessible"],
                  group["alive_but_target_closed"], group["extinct"])
        assert actual == values
        assert sum(actual) == group["denominator"] == 25600
    assert d["budgets"]["B8"]["evolving_minus_fixed_accessible_alive_pp"] == -8.328125
    assert d["budgets"]["B4p5"]["evolving_minus_fixed_accessible_alive_pp"] == 35.56640625
    assert d["descriptive_budget_interaction_pp"] == 43.89453125


@pytest.mark.parametrize("policy_budget,key,delta", [
    ("fixed_B8", "alive_accessible", 1),
    ("evolving_B4p5", "alive", 1),
    ("fixed_B4p5", "genetic_first", 1),
    ("evolving_B8", "extinction_first", 1),
])
def test_inconsistent_source_counts_fail_closed(policy_budget, key, delta):
    d = read()
    d["arms"][policy_budget][key] += delta
    with pytest.raises(ValueError):
        derive(d)


def test_registered_primaries_cannot_be_silently_changed():
    d = read()
    d["primary"]["endpoints"][0]["estimate"] += .001
    with pytest.raises(ValueError, match="registered G/S"):
        derive(d)


def test_current_manuscript_does_not_call_posthoc_contrast_confirmed():
    d = derive(read())
    assert not d["new_uncertainty_estimated"]
    assert d["status"].endswith("NOT_REGISTERED")
    text = (Path(__file__).resolve().parents[1] /
            "docs/CHAPTER2_PUBLICATION_NOVELTY_DECISION_20261019.md").read_text(encoding="utf8")
    assert "43.89453125" in text
    assert "探索的" in text
    assert "事前登録" in text



def test_noncausal_product_identity_not_a_mediation_estimate():
    d = derive(read())
    q = d["budgets"]
    for budget in ("B8", "B4p5"):
        row = q[budget]["descriptive_product_identity_not_mediation"]
        assert row["survivor_conditioning_selection_bias_possible"] is True
        assert abs(row["sum_pp"] - q[budget]["evolving_minus_fixed_accessible_alive_pp"]) < 1e-11
        assert abs(row["survival_prevalence_term_pp"] +
                   row["survivor_conditional_composition_term_pp"] -
                   row["sum_pp"]) < 1e-11
    b8=q["B8"]["descriptive_product_identity_not_mediation"]
    assert b8["survival_prevalence_term_pp"] == 0
    assert abs(b8["survivor_conditional_composition_term_pp"] + 8.328125) < 1e-11
    b4=q["B4p5"]["descriptive_product_identity_not_mediation"]
    assert abs(b4["survival_prevalence_term_pp"] - 21.74655607397929) < 1e-11
    assert abs(b4["survivor_conditional_composition_term_pp"] - 13.81985017602072) < 1e-11
    assert "mediator" not in d["status"].lower()
