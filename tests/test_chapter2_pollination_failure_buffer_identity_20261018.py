"""Native-source maternal fault-buffer identity; not new ecological simulation."""
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.types import Config, PlantState, VisitorState


ROOT = Path(__file__).resolve().parents[1]


def build_state():
    a = np.full((4, 3, 2), .5, dtype=float)
    return PlantState(
        alleles=a,
        allele_origin=np.zeros(a.shape, dtype=np.int64),
        mutation_flags=np.zeros(a.shape, dtype=bool),
        ids=np.arange(4, dtype=np.int64),
        birth_years=np.zeros(4, dtype=np.int64),
    )


def config(timing):
    base = json.loads((ROOT / "data/design/model3_ch2_bridge_20260927.json").read_text())["base_config"]
    return replace(
        Config.from_dict(base), capacity=4, survival=0.0,
        assurance_mode="fixed", fixed_assurance=.5,
        assurance_timing=timing, assurance_cost=0.0,
        pollen_discount=0.0, depression=.5,
    )


def visitors(present):
    opt = np.array([.45, .55]) if present else np.array([])
    return VisitorState(
        ids=np.arange(len(opt), dtype=np.int64), optima=opt,
        breadths=np.full(len(opt), .2), effectiveness=np.ones(len(opt)),
    )


def test_source_delayed_maternal_buffer_and_zero_visitor_floor():
    state = build_state()
    cfg = config("delayed")
    v = 1-cfg.depression
    a = cfg.fixed_assurance
    for present in (False, True):
        ledger = reproduce(state, visitors(present), cfg)
        o = ledger.ovules
        female = ledger.outcross.sum(axis=0)
        q = female/o
        expected = o*(q+v*a*(1-q))
        np.testing.assert_allclose(ledger.maternal, expected, rtol=1e-13, atol=1e-13)
        if not present:
            np.testing.assert_allclose(ledger.maternal/o, v*a, atol=1e-13)
        # Intrinsic seed-buffering does NOT imply fitness or pollen-service recovery.
        assert np.all(ledger.maternal >= 0)


def test_prior_selfing_is_not_costless_delayed_insurance():
    state = build_state()
    cfg = config("prior")
    l = reproduce(state, visitors(True), cfg)
    a = cfg.fixed_assurance
    o = l.ovules
    q = l.outcross.sum(axis=0)/(o*(1-a))
    np.testing.assert_allclose(
        l.maternal/o, (1-a)*q+(1-cfg.depression)*a,
        atol=1e-13,
    )
    assert np.any(q > 0)


def test_fixed_state_pollination_variance_is_attenuated_by_assurance():
    q = np.array([0.0, .15, .45, .85, 1.0])
    d = .5
    a = .5
    normalized = q+(1-d)*a*(1-q)
    np.testing.assert_allclose(
        np.var(normalized),
        (1-(1-d)*a)**2*np.var(q),
        atol=1e-15,
    )
