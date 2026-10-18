"""Read-only denominator regression on original 18-cell exploratory log."""
import copy
import json
from scripts.audit_chapter2_recovery_policy_denominators_20261018 import (
    INPUT, compare_readout,
)


def test_source_18_cells_two_distinct_estimands_with_opposite_t45_direction():
    d=compare_readout(json.loads(INPUT.read_text(encoding="utf-8")))
    assert d["source_run_id"] == 39045405754
    assert len(d["results"]) == 3
    by_time = {r["t"]: r for r in d["results"]}
    assert by_time[10]["descriptive_conditional_evolving_minus_fixed"] is None
    assert by_time[30]["descriptive_unconditional_historical_A_evolving_minus_fixed"] == 0
    assert by_time[30]["descriptive_conditional_evolving_minus_fixed"] == .25
    at45 = by_time[45]
    assert at45["historical_policies"]["fixed"]["unconditional_high_I_attainment_restored"] == 3/8
    assert at45["historical_policies"]["evolving"]["unconditional_high_I_attainment_restored"] == 4/8
    assert at45["historical_policies"]["fixed"]["eligible_declined_source_states"] == 3
    assert at45["historical_policies"]["evolving"]["eligible_declined_source_states"] == 1
    assert at45["descriptive_unconditional_historical_A_evolving_minus_fixed"] == 1/8
    assert at45["descriptive_conditional_evolving_minus_fixed"] == -1/6
    assert at45["historical_policies"]["evolving"]["occupied_source_genetic_support_closures"] == 1
    assert at45["historical_policies"]["fixed"]["occupied_source_genetic_support_closures"] == 0


def test_duplicate_cell_or_broken_conditional_inference_fails_closed():
    original=json.loads(INPUT.read_text(encoding="utf-8"))
    a=copy.deepcopy(original)
    a["results"]["complete_18_cell_readout"][1]=a["results"]["complete_18_cell_readout"][0]
    try:
        compare_readout(a)
    except ValueError as exc:
        assert "duplicate" in str(exc)
    else:
        raise AssertionError("duplicate accepted")
    b=copy.deepcopy(original)
    cell=next(x for x in b["results"]["complete_18_cell_readout"]
              if x["t"]==10 and x["historical_A"]=="fixed" and
              x["service"]=="functional_pollinators_restored")
    assert cell["N_eligible"]==0
    cell["P_regain_conditional"]=0.0
    try:
        compare_readout(b)
    except ValueError as exc:
        assert "eligibility" in str(exc)
    else:
        raise AssertionError("zero eligible falsely assigned a recovery rate")


def test_committed_exploratory_denominator_readout_matches_fresh_source_only_arithmetic():
    from pathlib import Path
    expected_path = INPUT.parents[0] / "CHAPTER2_RECOVERY_POLICY_DENOMINATORS_READOUT_20261018.json"
    committed=json.loads(expected_path.read_text(encoding="utf-8"))
    derived=compare_readout(json.loads(INPUT.read_text(encoding="utf-8")))
    assert derived == committed
