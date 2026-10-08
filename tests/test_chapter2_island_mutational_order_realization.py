"""Audit mutation-access compliance without relabelling failed survival tests."""
import json
from pathlib import Path
import pytest

from scripts.audit_chapter2_island_mutational_order_realization import audit, order
from scripts.run_chapter2_island_mutational_priority_balanced import (
    load_balanced, declared_groups,
)

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/chapter2_island_mutational_order_realization_audit_20261008.json"


@pytest.mark.parametrize("a,i,expected", [
    (2, 4, "A_before_I"),
    (4, 2, "I_before_A"),
    (3, 3, "tie"),
    (None, 4, "I_only"),
    (3, None, "A_only"),
    (None, None, "neither"),
])
def test_all_order_states_retained(a, i, expected):
    assert order({"assurance": a, "investment": i}) == expected


def test_order_audit_verifies_full_grid_and_counts_single_trait_crossings():
    _p, d, _source = load_balanced()
    rows = [{
        "group": group,
        "first_hit": {"assurance": 9, "investment": None},
        "end_pre": {"means": [0.5, 0.5, 0.65]},
    } for group in declared_groups(d)]
    result = audit("balanced", rows)
    assert result["status"].startswith("post_outcome_exploratory")
    assert result["independent_visitor_histories"] == 4
    assert len(result["setting_by_schedule"]) == 16
    for k, v in result["pooled_by_schedule"].items():
        assert v["historical_groups"] == 64
        assert v["A_only"] == 64
        assert v["I_only"] == 0
    assert result["pooled_by_schedule"]["assurance_first"]["intended_trait_preceded_or_only"] == 64
    assert result["pooled_by_schedule"]["investment_first"]["intended_trait_preceded_or_only"] == 0
    rows[0]["group"] = rows[1]["group"]
    with pytest.raises(ValueError):
        audit("balanced", rows)


def test_archived_raw_audit_distinguishes_compliance_from_failed_gate():
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    a = result["pooled_order_counts"]
    assert a["independent16"]["assurance_first"]["intended_first_or_only"] == 118
    assert a["independent16"]["investment_first"]["intended_first_or_only"] == 97
    assert a["balanced"]["assurance_first"]["intended_first_or_only"] == 52
    assert a["balanced"]["investment_first"]["intended_first_or_only"] == 51
    for experiment in a.values():
        for counts in experiment.values():
            assert sum(counts[k] for k in (
                "A_before_I", "I_before_A", "tie", "A_only", "I_only", "neither"
            )) == counts["n"]
    independent = {
        x["setting"]: x
        for x in result["setting_level_descriptive_differences"]["independent16"]
    }
    assert independent["prior_selfing"]["immediate_viable"] > 0
    assert independent["prior_selfing"]["terminal_occupancy"] < 0
    assert any("not" in s.lower() for s in result["claim_boundary"])
