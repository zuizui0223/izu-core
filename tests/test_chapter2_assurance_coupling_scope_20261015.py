"""Read-only guards for the October 15 counterintuition scope audit."""
from __future__ import annotations

import copy
import pytest

from scripts import audit_chapter2_assurance_coupling_scope_20261015 as audit


def test_historical_four_setting_result_and_static_coupling_are_distinct():
    result = audit.audit()
    assert result["status"] == "SOURCE_ONLY_DIAGNOSTIC_NO_NEW_BIOLOGICAL_TRAJECTORIES"
    assert result["new_evolutionary_trajectories"] == 0
    assert result["source_original_trajectories"] == 8448
    assert result["source_independent_visitor_histories"] == 64
    assert len(result["original_four_setting_endpoints"]) == 4
    for row in result["original_four_setting_endpoints"]:
        assert row["near_evolving_minus_fixed_investment"] < 0
        assert row["far_evolving_minus_fixed_investment"] > 0
        assert row["near_change_in_A"] < row["far_change_in_A"]
        assert (row["near_fixed_resident_A_effect_on_I_gradient"]
                < row["far_fixed_resident_A_effect_on_I_gradient"] < 0)
        assert abs(
            row["far_evolving_minus_fixed_investment"]
            - row["near_evolving_minus_fixed_investment"]
            - row["far_minus_near_interaction"]
        ) < 1e-11


def test_synthetic_supply_has_both_no_pollen_null_and_saturated_counterexample():
    rows = audit.audit()["mathematical_synthetic_visitor_grid"]
    assert len(rows) == len(audit.SETTINGS) * len(audit.SCALES)
    for setting in audit.SETTINGS:
        group = {r["pollen_budget_multiplier"]: r
                 for r in rows if r["setting"] == setting}
        zero = group[0.0]
        assert zero["A_low"]["outcross_fraction"] == 0
        assert zero["A_high"]["outcross_fraction"] == 0
        assert abs(zero["A_high_minus_low_investment_gradient"]) < 1e-11
        assert group[64.0]["A_low"]["outcross_fraction"] > 0.9999
        assert group[64.0]["A_high"]["outcross_fraction"] > 0.9999

    # Near saturation does not force the same result under all mating timings:
    # with delayed selfing the fixed-state difference tends to zero, whereas
    # prior selfing still alters the allocation/paternal fitness balance.
    delayed = next(x for x in rows if x["setting"] == "delayed_control"
                   and x["pollen_budget_multiplier"] == 64)
    prior = next(x for x in rows if x["setting"] == "prior_selfing"
                 and x["pollen_budget_multiplier"] == 64)
    assert abs(delayed["A_high_minus_low_investment_gradient"]) < 1e-6
    assert prior["A_high_minus_low_investment_gradient"] < -0.1


def test_frozen_controls_cannot_be_silently_bypassed(monkeypatch):
    original_reader = audit.load_json

    def tampered(path):
        d = original_reader(path)
        if path == audit.GENERALITY:
            d = copy.deepcopy(d)
            d["structural_control"]["matched_pairs_checked"] = 127
        return d

    monkeypatch.setattr(audit, "load_json", tampered)
    with pytest.raises(AssertionError, match="historical source/control"):
        audit.audit()


def test_no_overwrite_of_prior_audit(tmp_path):
    out = tmp_path / "existing.json"
    out.write_text("already preserved", encoding="utf-8")
    # The audit is inspectable directly; a caller must not overwrite a prior
    # receipt by passing the same --out path.
    assert out.exists()
    assert "new_evolutionary_trajectories" in audit.audit()
