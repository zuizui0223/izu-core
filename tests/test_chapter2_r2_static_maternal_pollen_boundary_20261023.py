"""Source-only R2 maternal payoff contrasts, not confirmation or evolution."""
from __future__ import annotations

import pytest

from scripts.audit_chapter2_r2_static_maternal_pollen_boundary_20261023 import (
    STATUS, analyze, maternal_grad_and_threshold,
)


def test_native_source_static_maternal_gradient_and_provenance():
    x = analyze()
    assert x["status"] == STATUS
    assert x["original_source_protocol_sha256"] == (
        "87af92484af9988181b4f3bed6760d39325de70cca8c0b4e1cec19c47b8c9849"
    )
    assert len(x["rows"]) == 8
    assert x["new_biological_population_updates"] == 0
    assert x["new_statistical_tests"] == 0
    assert not x["observed_R2_384_results_reused_as_outcomes"]
    assert "NOT_INDEPENDENT_CONFIRMATION" in x["registration_claim"]
    assert all(row["no_evolution_trajectory"] for row in x["rows"])
    for r in x["rows"]:
        assert abs(r["analytic_log_maternal_return_gradient_A"] -
                   r["finite_difference_gradient_A"]) < 2e-7


def test_static_return_sign_switch_is_conditional_on_current_A_and_q():
    x = analyze()
    pairs = {(r["initial_reporter_A"], r["baseline"], r["future_arm"]): r
             for r in x["rows"]}
    assert len(pairs) == 8
    for a, cutoff in ((0.3, 0.6026490066225165), (0.5, 0.42857142857142855)):
        for level in ("strong_baseline_limitation", "weak_baseline_limitation"):
            for arm in ("control", "decline"):
                row = pairs[a, level, arm]
                assert row["conditional_q_sign_switch_for_this_A"] == pytest.approx(cutoff, abs=1e-12)
                assert row["within_source_maternal_gradient_positive"] == (
                    row["outcross_ovule_fraction_q"] < cutoff
                )
    assert all(pairs[0.3, "strong_baseline_limitation", a]["within_source_maternal_gradient_positive"] for a in ("control", "decline"))
    assert all(pairs[0.5, "strong_baseline_limitation", a]["within_source_maternal_gradient_positive"] for a in ("control", "decline"))
    assert not pairs[0.3, "weak_baseline_limitation", "control"]["within_source_maternal_gradient_positive"]
    assert pairs[0.3, "weak_baseline_limitation", "decline"]["within_source_maternal_gradient_positive"]
    assert not pairs[0.5, "weak_baseline_limitation", "control"]["within_source_maternal_gradient_positive"]
    assert not pairs[0.5, "weak_baseline_limitation", "decline"]["within_source_maternal_gradient_positive"]


def test_analytic_pollen_boundary_validates_interior_parameter_region():
    with pytest.raises(ValueError):
        maternal_grad_and_threshold(0, 0.5, 0.5, 0.5)
    with pytest.raises(ValueError):
        maternal_grad_and_threshold(0.5, 1.1, 0.5, 0.5)
    with pytest.raises(ValueError):
        maternal_grad_and_threshold(0.5, 0.4, 0, 0.5)
    with pytest.raises(ValueError):
        maternal_grad_and_threshold(0.5, 0.4, 0.5, -0.1)
    g, qstar = maternal_grad_and_threshold(0.5, 3.0/7.0, 0.5, 0.5)
    assert qstar == pytest.approx(3.0/7.0, abs=1e-12)
    assert g == pytest.approx(0, abs=1e-12)


def test_no_false_causal_mediation_or_paternal_claim():
    x = analyze()
    assert "MATERNAL" in x["comparison"]
    assert "paternal-inclusive" in x["comparison"]
    assert "does not" in x["comparison"]
    assert "evolution" in x["design"].lower() or x["new_biological_population_updates"] == 0
