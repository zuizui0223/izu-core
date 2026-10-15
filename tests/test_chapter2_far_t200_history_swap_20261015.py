"""Technical invariants for the post-outcome t200 2x2 conditional continuation.

Tests do not require or fabricate original GitHub Actions archives. No new
biological outcome is promoted by passing these technical source checks.
"""
from dataclasses import replace
import numpy as np
import pytest

from scripts.chapter2_far_t200_history_swap_20261015 import (
    YEAR0, continuation, conditional_price, four_cell_contrast,
    load_protocol, paired_streams,
)
from scripts.model3_island.reproduction import reproduce
from scripts.run_chapter2_assurance_generality import (
    config, founders, load_design, DEFAULT_DESIGN,
)
from scripts.run_model3_persistent_isolation import exposure


def test_authentic_source_contract_and_scope():
    p, d, source = load_protocol()
    assert len(p["setting_order"]) == 4
    assert p["n_full_futures"] == 1024
    assert p["original_demographic_repeat_seed"] == 26111601
    assert p["original_artifact_shards_0_1_2_3"] == [
        z["artifact_id"] for z in source["artifact_shards"]
    ]


def test_paired_future_streams_repeat_deterministically():
    a = paired_streams(26110601, 200)
    b = paired_streams(26110601, 200)
    c = paired_streams(26110601, 201)
    assert a["parents"].random() == b["parents"].random()
    assert a["parents"].random() != c["parents"].random()


def test_conditional_price_exact_same_source_parentage_and_finite_shift():
    design = load_design(DEFAULT_DESIGN)
    state = founders(design)
    conf = config(design, "assurance_cost", 0.01, "evolving")
    history = exposure(26110601, "far")
    ledger = reproduce(state, history.visitors[YEAR0], conf)
    got = conditional_price(state, ledger)
    assert np.isfinite(got)
    I = state.alleles[:, 1, :].mean(axis=1)
    W = (.5 * (ledger.outcross.sum(axis=1) + ledger.outcross.sum(axis=0))
         + ledger.self_viable)
    expect = (np.dot(I, W) / W.sum()) - I.mean()
    assert got == pytest.approx(expect, abs=1e-12)


def test_same_start_and_zero_mutation_has_identical_fixed_and_evolving_futures():
    design = load_design(DEFAULT_DESIGN)
    h = exposure(26110601, "far")
    s = founders(design)
    first = None
    for policy in ("fixed", "evolving"):
        c = replace(config(design, "delayed_control", 0, policy),
                    mutation_rate=0)
        got = continuation(s, h, c, history_seed=26110601,
                           start=200, stop=203)
        assert np.isfinite(got["terminal_mean_I"])
        assert np.all(got["annual"][:, 1] > 0)
        assert np.all(got["annual"][:, 4] == .5)
        if first is None:
            first = got
        else:
            assert np.array_equal(got["genomes"], first["genomes"],
                                  equal_nan=True)
            assert np.array_equal(got["parentage"], first["parentage"])
            assert np.array_equal(got["annual"], first["annual"],
                                  equal_nan=True)


def test_four_cell_contrast_and_extinction_not_dropped():
    rows = []
    for origin in ("fixed", "evolving"):
        for future in ("fixed", "evolving"):
            rows.append({"t200_origin": origin, "future_A_policy": future,
                         "delta_I_from_t200": {
                             ("fixed", "fixed"): -.30,
                             ("fixed", "evolving"): -.28,
                             ("evolving", "fixed"): -.22,
                             ("evolving", "evolving"): -.18,
                         }[origin, future],
                         "terminal_N": 48})
    d = four_cell_contrast(rows)
    assert d["status"] == "defined_conditional_contrasts"
    assert d["origin_x_future_policy_interaction"] == pytest.approx(.02)
    rows[0]["terminal_N"] = 0
    rows[0]["delta_I_from_t200"] = None
    assert four_cell_contrast(rows)["status"] == (
        "undefined_trait_contrast_due_to_extinction"
    )
