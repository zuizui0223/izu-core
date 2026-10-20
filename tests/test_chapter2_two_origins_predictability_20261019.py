"""Strict mathematical checks of TECHNICAL source-probability information, not biology."""
from __future__ import annotations

import math
import numpy as np
import pytest

from scripts.audit_two_origins_predictability_20261019 import (
    STATUS, analyze, exact_propensity, exposed_islands, exposed_sources,
    optimal_source_forecast_scores,
)


def test_brier_law_of_total_variance_is_exact():
    p = np.array([.12, .5, .8, .93])
    x = optimal_source_forecast_scores(p)
    mu = float(np.mean(p))
    assert x["sources"] == 4
    assert x["mean_fate_probability"] == mu
    assert abs(x["expected_brier_gain"] - float(np.var(p))) < 1e-14
    assert abs(x["baseline_expected_brier"] - mu * (1 - mu)) < 1e-14
    assert abs(x["baseline_expected_brier"] - x["perfect_source_oracle_expected_brier"]
               - x["expected_brier_gain"]) < 1e-14
    assert x["expected_log_loss_gain"] >= -1e-14


def test_constant_propensities_have_zero_explainable_source_fate_variance():
    z = optimal_source_forecast_scores([.72] * 6)
    assert abs(z["expected_brier_gain"]) < 1e-26
    assert abs(z["oracle_expected_binary_accuracy"] -
               z["constant_expected_binary_accuracy"]) < 1e-14
    assert abs(z["expected_log_loss_gain"]) < 1e-14


@pytest.mark.parametrize("invalid", [[], [-.1, .5], [.5, 1.1], [float("nan")],
                                   [[.4, .6]], [float("inf")]])
def test_invalid_propensity_vectors_fail_closed(invalid):
    with pytest.raises(ValueError):
        optimal_source_forecast_scores(invalid)


def test_source_registry_disjoint_from_any_replicated_new_genotypes():
    samples = exposed_sources()
    assert len(samples) == 6
    assert sorted(z.lineage_id for z in samples) == list(range(6))
    assert [z.source_seed for z in samples] == list(range(73000,73006))
    assert len(exposed_islands()) == 2


def test_exact_source_probability_matches_original_v3_technical_job_rounded():
    # These are exposed engineering fixture receipts from Actions run 39269659188.
    # They are not unexposed validation data; original job printed 4 decimals.
    expected = {
        "no_visitors_harsh": [.6061,.6035,.8501,.7943,.9155,.8753],
        "visitors_milder": [.8789,.9233,.9754,.9719,.9898,.9852],
    }
    for island in exposed_islands():
        obtained = [
            exact_propensity(lineage, island, "native")
            for lineage in exposed_sources()
        ]
        assert len(obtained) == 6
        for got, v in zip(obtained, expected[island.island_id]):
            assert abs(got["p_establish_given_arrival"] - v) < .000051
            assert abs(got["p_establish_from_candidate"] -
                       .8 * got["p_establish_given_arrival"]) < 1e-14
            assert got["expected_viable_recruits"] > 0


def test_all_neutral_control_removes_genotype_predictive_information():
    audit = analyze()
    assert audit["status"] == STATUS
    assert audit["no_new_genotypes_or_biological_updates"] is True
    assert audit["independent_heldout_validation"] is False
    assert audit["actual_establishment_observations_used"] is False
    assert len(audit["result"]) == 2
    for island in audit["result"]:
        control = island["mode_results"]["trait_neutral"]
        p = np.asarray([r["p_establish_from_candidate"]
                        for r in control["source_propensities"]])
        assert p.max() - p.min() < 1e-13
        assert control["candidate_to_establishment"]["expected_brier_gain"] < 1e-25
        assert control["arrival_conditional"]["expected_brier_gain"] < 1e-25


def test_oracle_fate_information_is_small_even_with_pollen_loss():
    q = {d["island"]: d for d in analyze()["result"]}
    harsh = q["no_visitors_harsh"]["mode_results"]["native"]["candidate_to_establishment"]
    mild = q["visitors_milder"]["mode_results"]["native"]["candidate_to_establishment"]
    assert .03 < harsh["relative_brier_gain"] < .06
    assert .003 < mild["relative_brier_gain"] < .009
    # Precision of the original 4-decimal receipt explains tolerances.
    assert abs(harsh["baseline_expected_brier"] - .2357659) < 1e-4
    assert abs(harsh["perfect_source_oracle_expected_brier"] - .2257662) < 1e-4
    assert abs(mild["baseline_expected_brier"] - .1806907) < 1e-4
    assert abs(mild["perfect_source_oracle_expected_brier"] - .1796650) < 1e-4
    assert harsh["constant_expected_binary_accuracy"] > .6
    assert harsh["oracle_expected_binary_accuracy"] < .67


def test_no_statistical_confirmation_leaks_into_oracle_readout():
    a = analyze()
    assert "NOT_REGISTERED" in STATUS
    assert "ORACLE" in a["result"][0]["mode_results"]["native"][
        "candidate_to_establishment"]["inference"]
    assert "confidence_interval" not in a
    assert not any("confirmed" in s for s in a["claim_boundary"])
