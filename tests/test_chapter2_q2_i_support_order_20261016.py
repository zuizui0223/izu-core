"""Prospective Q2 support/order *technical* tests; no confirmatory histories."""
from __future__ import annotations

import numpy as np
import pytest

from scripts.chapter2_q2_i_support_order_20261016 import (
    CLASSES, declared_tasks, founder_state, load_protocol, native_config,
    response_class, simulate, technical_smoke, preflight_all_t0_ledgers,
    DEFAULT_DESIGN,
)
from scripts.model3_island.reproduction import reproduce
from scripts.run_model3_persistent_isolation import exposure


def _design():
    return load_protocol()


def test_task_inventory_and_prespecified_exposure():
    d = _design()
    tasks = declared_tasks(d)
    assert len(tasks) == len(set(tasks)) == 384
    assert set(t[2] for t in tasks) == {"far", "near"}
    assert set(t[3] for t in tasks) == set(d["policies"])
    assert d["visitors"]["primary_arm"] == "far"
    assert d["mutations"]["traits_enabled"]["investment"] is False
    assert d["inference"]["bootstrap_draws"] == 9999
    assert d["inference"]["primary_familywise_alpha"] == .05


@pytest.mark.parametrize("seed", (860101, 860103, 860108))
def test_t0_phenotypes_identical_but_I_allele_access_differs(seed):
    d = _design()
    states = {p: founder_state(d, seed, p) for p in d["policies"]}
    ref = states["dense_reachable"].alleles.mean(axis=2)
    for p, s in states.items():
        np.testing.assert_array_equal(s.alleles.mean(axis=2), ref)
        np.testing.assert_array_equal(s.alleles[:, 0, :],
                                      states["dense_reachable"].alleles[:, 0, :])
        assert set(np.unique(s.alleles[:, 2, :])) == {.421875, .578125}
        assert np.unique(s.alleles[:, 1, :]).size == 3
        assert (s.mutation_flags[:, 1, :] == 0).all()
        assert (s.ids == states["dense_reachable"].ids).all()
        n_carriers = int(np.count_nonzero(s.alleles[:, 1, 0] < .5))
        assert n_carriers == d["policies"][p]["carrier_count"]
    assert states["dense_reachable"].alleles[:, 1, :].min() == .421875
    assert states["sparse_reachable"].alleles[:, 1, :].min() == .421875
    assert states["dense_unreachable"].alleles[:, 1, :].min() == .453125
    # Proof of no-new-I-mutation/no-immigration accessibility exclusion:
    assert states["dense_unreachable"].alleles[:, 1, :].min() > .5 - .05


@pytest.mark.parametrize("arm", ("far", "near"))
def test_same_initial_native_maternal_paternal_selfing_returns(arm):
    d = _design()
    c = native_config(d)
    vis = exposure(d["visitors"]["first"], arm).visitors[0]
    states = [founder_state(d, d["founders"]["first"], p) for p in d["policies"]]
    ledgers = [reproduce(s, vis, c) for s in states]
    for a in ledgers[1:]:
        for field in ("maternal", "paternal", "outcross", "self_raw",
                      "self_viable", "ovules", "exported", "delivered"):
            np.testing.assert_array_equal(getattr(ledgers[0], field),
                                          getattr(a, field))


@pytest.mark.parametrize("a,i,label", [
    (2, 12, "assurance_first"),
    (12, 2, "investment_first"),
    (2, 5, "near_simultaneous"),
    (2, None, "assurance_only"),
    (None, 2, "investment_only"),
    (None, None, "neither"),
])
def test_six_class_clock_includes_unobserved_events(a, i, label):
    d = _design()
    trace = np.full((44, 5), np.nan)
    trace[:, 0] = 48.
    trace[:, 1] = trace[:, 2] = .5
    trace[:, 3] = .421875
    trace[:, 4] = 24
    if a is not None:
        trace[a:, 1] = .56
    if i is not None:
        trace[i:, 2] = .44
    result = response_class(trace, d["response"])
    assert result["label"] == label
    assert result["A_start"] == a
    assert result["I_start"] == i
    assert label in CLASSES


def test_extinction_does_not_create_false_completed_window():
    d = _design()
    trace = np.full((44, 5), np.nan)
    trace[:, 0] = 48
    trace[:, 1] = trace[:, 2] = .5
    trace[10:18, 1] = .6
    trace[18:, 0] = 0
    verdict = response_class(trace, d["response"])
    assert verdict["label"] == "neither"
    assert verdict["first_extinction"] == 18
    assert verdict["occupied_terminal"] is False


def test_native_four_update_replay_and_full_typed_state_receipt():
    d = _design()
    task = declared_tasks(d)[0]
    a = simulate(d, task, steps=4)
    b = simulate(d, task, steps=4)
    np.testing.assert_array_equal(a["trace"], b["trace"])
    for key in ("alleles", "allele_origin", "mutation_flags",
                "ids", "birth_years", "parentage", "offsets", "parentage_offsets"):
        np.testing.assert_array_equal(a[key], b[key])
    assert len(a["offsets"]) == 6
    assert len(a["parentage_offsets"]) == 5
    assert int(a["offsets"][-1]) == len(a["alleles"])
    assert int(a["parentage_offsets"][-1]) == len(a["parentage"])
    assert a["status"] == "technical_smoke_no_biological_adjudication"
    assert "events" not in a



def test_all_original_t0_ledger_cells_are_matched_before_long_runs():
    evidence = preflight_all_t0_ledgers(_design())
    assert evidence["status"] == "T0_ORIGINAL_MODEL_LEDGER_MATCHES_ALL_POLICIES"
    assert evidence["matched_founder_visitor_arm_cells"] == 128
    assert evidence["policy_evaluations"] == 384
    assert evidence["full_model_updates"] == 0
    assert evidence["independent_biological_histories"] == 0


def test_technical_smoke_never_masquerades_as_confirmatory():
    d = _design()
    report = technical_smoke(d, DEFAULT_DESIGN)
    assert report["status"] == "PASS_TECHNICAL_SMOKE_ONLY_NOT_SCIENTIFIC_RESULTS"
    assert report["cases"] == 6
    assert report["t0_complete_ledger_preflight"]["matched_founder_visitor_arm_cells"] == 128
    assert report["t0_complete_ledger_preflight"]["full_model_updates"] == 0
    assert report["no_full_200_update_scientific_cases_executed"] is True
    assert all(record["censuses"] == 13 for record in report["technical_cases"])
