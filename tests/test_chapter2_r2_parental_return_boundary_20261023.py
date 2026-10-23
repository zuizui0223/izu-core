"""Source-exact Model 3 R2 fixed-state parental versus maternal A selection."""
from __future__ import annotations

import pytest

from scripts.audit_chapter2_r2_parental_return_boundary_20261023 import (
    STATUS, CANDIDATE_A, mathematical_boundary, readback, reporter,
)


def test_exact_native_fixed_state_return_agrees_with_both_analytic_gradients():
    r = readback()
    assert r["status"] == STATUS
    assert r["new_biological_population_updates"] == 0
    assert r["new_preregistered_tests"] == 0
    assert r["original_frozen_source_protocol_sha256"] == (
        "87af92484af9988181b4f3bed6760d39325de70cca8c0b4e1cec19c47b8c9849"
    )
    assert len(r["rows"]) == 8
    assert {x["A_reporter"] for x in r["rows"]} == set(CANDIDATE_A)
    assert all(x["native_focal_paternal_outcross_invariant"] for x in r["rows"])
    for row in r["rows"]:
        assert row["native_fd_parental_gradient"] == pytest.approx(
            row["parental_genome_gradient"], abs=2e-7
        )
        assert row["native_fd_maternal_gradient"] == pytest.approx(
            row["maternal_gradient"], abs=2e-7
        )
        assert row["parental_minus_maternal"] == pytest.approx(
            row["parental_genome_gradient"] - row["maternal_gradient"], abs=1e-12
        )
        assert row["parental_minus_maternal"] > 0
        assert row["maternal_sign_q_cutoff"] < row["parental_sign_q_cutoff"]
        assert row["full_parental_return_includes_both_maternal_and_paternal_outcross_halves"]


def test_frozen_reproductive_settings_identify_sign_disagreement_at_A_half():
    x = readback()
    d = {(r["A_reporter"], r["baseline"], r["future"]): r
         for r in x["rows"]}
    weak = "weak_baseline_limitation"
    strong = "strong_baseline_limitation"
    # A=.5 and activity decline: q lies between the two theoretical cutoffs.
    focal = d[0.5, weak, "decline"]
    assert focal["maternal_sign_q_cutoff"] == pytest.approx(3 / 7, abs=1e-12)
    assert focal["parental_sign_q_cutoff"] == pytest.approx(0.6, abs=1e-12)
    assert focal["source_q"] > focal["maternal_sign_q_cutoff"]
    assert focal["source_q"] < focal["parental_sign_q_cutoff"]
    assert focal["maternal_gradient"] < 0 < focal["parental_genome_gradient"]
    assert x["key_counterexample"]["description"].startswith("maternal negative")
    for a in (0.3, 0.5):
        assert d[a, strong, "control"]["maternal_gradient_positive"]
        assert d[a, strong, "decline"]["parental_gradient_positive"]
        assert not d[a, weak, "control"]["parental_gradient_positive"]
        assert d[a, weak, "decline"]["parental_gradient_positive"]
    assert d[0.3, weak, "decline"]["maternal_gradient_positive"]


def test_pollen_thresholds_and_exact_gap():
    r3 = mathematical_boundary(0.3, 0.44)
    r5 = mathematical_boundary(0.5, 0.44)
    assert r3["maternal_sign_q_cutoff"] == pytest.approx(0.6026490066225165)
    assert r3["parental_sign_q_cutoff"] == pytest.approx(0.7520661157024794)
    assert r5["maternal_sign_q_cutoff"] == pytest.approx(3 / 7)
    assert r5["parental_sign_q_cutoff"] == pytest.approx(0.6)
    assert r3["parental_genome_gradient"] > 0
    assert r5["maternal_gradient"] < 0 < r5["parental_genome_gradient"]
    assert r5["parental_minus_maternal"] == pytest.approx(
        0.5 * 0.5 * 0.44 / (0.44 + 0.5 * 0.5 * (1 - 0.44)), abs=1e-14
    )


def test_reject_invalid_assumptions_and_noninterior_states():
    for invalid in ((0.0, 0.1), (1.0, 0.9), (0.5, -0.1), (0.5, 1.1)):
        with pytest.raises(ValueError):
            mathematical_boundary(*invalid)
    with pytest.raises(ValueError):
        mathematical_boundary(0.5, 0.5, v=0)
    with pytest.raises(ValueError):
        mathematical_boundary(0.5, 0.5, assurance_cost=0)
    with pytest.raises(ValueError):
        reporter(10, 0.5)
    with pytest.raises(ValueError):
        reporter(48, 0)


def test_no_independent_selection_or_natural_island_claim():
    r = readback()
    assert any("not a true evolutionary invasion" in s for s in r["scope"])
    assert any("No A locus evolution" in s for s in r["scope"])
    assert any("No causal mediation" in s for s in r["scope"])
    assert r["new_biological_population_updates"] == 0
    assert r["new_preregistered_tests"] == 0
