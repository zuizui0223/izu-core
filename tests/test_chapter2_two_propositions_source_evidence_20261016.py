"""Theorem/registered-evidence separation for the two Chapter 2 propositions.

All evidence is historical source-locked; tests generate no new evolutionary
cohort and do not treat separate Q1/Q2/Q3 records as one mediation chain.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from scripts.model3_island.population import inherit
from scripts.model3_island.types import PlantState
from scripts.run_chapter2_assurance_generality import config, load_design, DEFAULT_DESIGN
from scripts.audit_chapter2_q1_fixedA_new_founders_20261016 import (
    SETTINGS, crossed_ci, evaluate,
)

ROOT = Path(__file__).resolve().parents[1]


def _read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _artificial_parents():
    # Three diploid loci and four distinct adults; deliberately preserved
    # homo/heterozygosity so no-memory trait-mean closure cannot substitute.
    a = np.array([
        [[.4, .6], [.1, .9], [.5, .5]],
        [[.2, .8], [.3, .7], [.5, .5]],
        [[.4, .4], [.1, .3], [.5, .5]],
        [[.8, .8], [.7, .9], [.5, .5]],
    ])
    return PlantState(
        alleles=a,
        allele_origin=np.arange(a.size).reshape(a.shape),
        mutation_flags=np.zeros_like(a, dtype=bool),
        ids=np.arange(4, dtype=np.int64),
        birth_years=np.zeros(4, dtype=np.int64),
    )


def test_no_mutation_no_immigration_has_nested_allele_support_every_locus():
    d = load_design(DEFAULT_DESIGN)
    cfg = config(d, "assurance_cost", 0.0, "fixed")
    state = _artificial_parents()
    before = [{float(x) for x in state.alleles[:, i, :].ravel()}
              for i in range(3)]
    next_state = inherit(
        state, np.arange(32) % 4, (np.arange(32) * 3 + 1) % 4,
        cfg, segregation_rng=np.random.default_rng(4401),
        mutation_rng=np.random.default_rng(4402),
        year=1, mutation_traits=(False, False, False),
    )
    for locus in range(3):
        values = {float(x) for x in next_state.alleles[:, locus, :].ravel()}
        assert values <= before[locus]
        founder_min, founder_max = min(before[locus]), max(before[locus])
        assert np.all(next_state.alleles[:, locus, :].mean(axis=1) >= founder_min)
        assert np.all(next_state.alleles[:, locus, :].mean(axis=1) <= founder_max)
        assert np.all(np.isin(next_state.alleles[:, locus, :],
                              np.asarray(list(before[locus]))))
    assert not next_state.mutation_flags.any()


def test_exact_half_width_bounds_require_symmetric_initial_center():
    center = .5
    for halfwidth in (.046875, .078125):
        allowed = np.array([center-halfwidth, center+halfwidth])
        possible_means = (allowed[:, None] + allowed[None, :]) / 2
        assert np.all(np.abs(possible_means-center) <= halfwidth + 1e-15)
    # For unsymmetrical founder means, +/-h centered on 0.5 does not imply
    # the historical mean can change by at most h in either direction.
    support = np.array([.2, .8])
    observed_initial = .2
    assert max(support) - observed_initial > (max(support)-min(support))/2


def test_q1_original_fixed_A_intervention_supports_negative_far_near_four():
    j = _read("data/results/chapter2_assurance_generality_20261006.json")
    assert len(j["settings"]) == 4
    for row in j["settings"]:
        comp = row["fixed_far_minus_near"]
        assert comp["mean"] < 0
        assert max(comp["bootstrap95"]) < 0
        assert row["passes_frozen_rule"]
    assert j["structural_control"]["status"] == "passed"


def test_original_I_allele_support_exclusion_and_favourable_expected_loss_are_distinct():
    report = _read("data/results/low_allele_loss_20261014/PRIOR_SUPPORT_READOUT.json")
    loss = _read("data/results/low_allele_loss_20261014/extracted/READOUT.json")
    independent = _read("data/results/low_allele_loss_20261014/INDEPENDENT_REVIEW.json")
    assert report["cases"] == loss["cases"] == independent["cases"] == 2304
    assert report["ever_excluded"] == loss["eligible_loss"] == 1238
    assert report["excluded_before_fixation"] == 703
    assert report["excluded_at_fixation"] == 535
    assert report["missing_I_excluded_before_fixation"] == 702
    assert report["excluded_with_expressed_variance"] == 703
    assert loss["direction_counts"]["favouring_needed"] == 315
    assert loss["direction_counts"]["opposing_needed"] == 923
    assert sum(loss["direction_counts"].values()) == 1238
    assert independent["eligible_loss"] == 1238
    assert independent["new_biological_histories"] == 0
    assert independent["max_scalar_error"] < 1e-11


def test_registered_boundary_sensitivity_is_one_cohort_not_three_new_experiments():
    j = _read("data/results/four_question_resolution_20261011/boundary_access_diagnosis.json")
    assert len(j["rows"]) == 36
    scores = {}
    for h in (.046875, .078125):
        subset = [r for r in j["rows"]
                  if r["threshold"] == .025 and r["allele_half_width"] == h]
        assert len(subset) == 6
        assert sum(r["starts"] for r in subset) == 3072
        assert all(r["threshold_accessible_without_mutation"] for r in subset)
        a = sum(r["categories"].get("assurance_first", 0) for r in subset)
        i = sum(r["categories"].get("investment_first", 0) for r in subset)
        scores[h] = (a, i, (a-i)/3072)
        assert all((r["categories"].get("assurance_first", 0)
                    -r["categories"].get("investment_first", 0)) *
                   (a-i) > 0 for r in subset)
    assert scores[.046875][:2] == (566, 1003)
    assert scores[.078125][:2] == (944, 268)
    assert scores[.046875][2] < 0 < scores[.078125][2]
    # At the preregistered 0.05 event, small A halfwidth needs mutation.
    narrow = [r for r in j["rows"]
              if r["threshold"] == .05 and r["allele_half_width"] == .046875]
    assert len(narrow) == 6
    assert all(not r["threshold_accessible_without_mutation"] for r in narrow)


def test_320_original_accounting_is_an_identity_not_a_drift_causal_fraction():
    j = _read("data/results/genome_response_accounting_readout_20261013.json")
    assert j["cases"] == 320
    main = [x for x in j["contexts"]
            if x["block"] == "causal_main"
            and x["supply"] == .125 and x["composition"] == "matched"]
    assert len(main) == 1 and main[0]["cases"] == 32
    c = main[0]["mean_cumulative_components"]
    index_i = 1
    terms = [c[k][index_i] for k in (
        "selection", "parent_sampling", "transmission", "birth_mutation")]
    np.testing.assert_allclose(
        sum(terms), c["observed_change"][index_i], atol=1e-12, rtol=0,
    )
    np.testing.assert_allclose(
        terms,
        [-.050198272939771596, .021816925283521558,
         .00836181640625004, 0],
        atol=1e-14, rtol=0,
    )
    assert abs(c["observed_change"][index_i] + .02001953125) < 1e-12


def test_q1_fixed_A_source_only_readout_preserves_D_arithmetic_and_crossed_units():
    terminal = np.full((4, 8, 8, 2, 2), .5)
    t0 = terminal.copy()
    terminal[:, :, :, 0, 0] = .5
    terminal[:, :, :, 1, 0] = .25
    terminal[:, :, :, 0, 1] = .48
    terminal[:, :, :, 1, 1] = .30
    report = evaluate(terminal, t0, {"original_cases": 1088})
    assert len(report["settings"]) == 4
    for row in report["settings"]:
        assert row["fixed_far_minus_near_mean"] == -.25
        assert row["fixed_negative_cells_of_64"] == 64
        assert row["fixed_negative_founder_means_of_8"] == 8
        assert row["fixed_far_absolute_change_from_founders_mean"] == -.25
        assert row["evolutionary_interaction_D_mean"] == pytest.approx(.07)
        assert row["fixed_far_minus_near_two_way_bootstrap95"] == pytest.approx(
            [-.25, -.25]
        )
