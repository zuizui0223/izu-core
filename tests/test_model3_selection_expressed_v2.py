"""Scientific diagnostic regression only; no new evolution experiment."""
import json
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from scripts.model3_island.selection import investment_invasion_terms, syndrome_thresholds
from scripts.selection_expressed_v2 import (
    investment_invasion_terms_expressed, evolvable_joint_syndrome_thresholds,
)
from scripts.model3_island.types import Config, VisitorState


ROOT = Path(__file__).resolve().parents[1]


def _config(mode, timing, discount, cost):
    base = Config.from_dict(json.loads(
        (ROOT / "data/design/model3_ch2_bridge_20260927.json").read_text(encoding="utf-8")
    )["base_config"])
    return replace(base, assurance_mode=mode, fixed_assurance=.5,
                   assurance_timing=timing, pollen_discount=discount,
                   assurance_cost=cost, activity_mode="fixed",
                   investment_cost=.5, depression=.5)


def _visitors():
    optima = np.array([.35, .45, .55, .65])
    return VisitorState(np.arange(len(optima)), optima, np.full(4, .18), np.ones(4))


@pytest.mark.parametrize("timing,discount,cost", [
    ("delayed", 0., 0.), ("prior", 0., 0.),
    ("delayed", 1., 0.), ("delayed", 0., .5),
])
def test_fixed_expression_is_invariant_to_hidden_a(timing, discount, cost):
    c = _config("fixed", timing, discount, cost)
    visitors = _visitors()
    zs = np.array([[.2, .5, a] for a in (.1, .5, .9)])
    got = investment_invasion_terms_expressed(zs, visitors, c)
    baseline = investment_invasion_terms([.2, .5, .5], visitors, c)
    for field in ("gradient", "benefit", "cost", "fitness", "selfed",
                  "female", "ovules", "paternal_export_component"):
        np.testing.assert_allclose(got[field], baseline[field], rtol=0, atol=1e-12)
    assert np.all(np.isfinite(got["gradient"]))


def test_frozen_original_focal_bug_is_exposed_not_rewritten():
    c = _config("fixed", "delayed", 0., .5)
    visitors = _visitors()
    different_hidden_genotypes = np.array([[.2, .5, a] for a in (.1, .5, .9)])
    historical = investment_invasion_terms(different_hidden_genotypes, visitors, c)["gradient"]
    corrected = investment_invasion_terms_expressed(different_hidden_genotypes, visitors, c)["gradient"]
    assert np.ptp(historical) > .05
    np.testing.assert_allclose(corrected, corrected[1], atol=1e-12)


def test_evolving_a_unchanged_and_joint_thresholds_only_in_evolving_mode():
    visitors = _visitors()
    c = _config("evolving", "prior", .5, .25)
    z = np.array([.2, .5, .65])
    got = investment_invasion_terms_expressed(z, visitors, c)
    old = investment_invasion_terms(z, visitors, c)
    assert got["gradient"] == pytest.approx(old["gradient"], abs=1e-14)
    joint = evolvable_joint_syndrome_thresholds(z, visitors, c)
    original_joint = syndrome_thresholds(z, visitors, c)
    assert joint["assurance_gradient"] == pytest.approx(original_joint["assurance_gradient"])
    with pytest.raises(ValueError, match="evolving A"):
        evolvable_joint_syndrome_thresholds(z, visitors, replace(c, assurance_mode="fixed"))


@pytest.mark.parametrize("bad", [[.2, .5, float("nan")], [.2, .5, 1.1], [.5, .5], [float("inf"), .5, .5]])
def test_malformed_hidden_genotypes_rejected_even_when_not_expressed(bad):
    with pytest.raises(ValueError):
        investment_invasion_terms_expressed(bad, _visitors(), _config("fixed", "delayed", 0., 0.))


def test_zero_visitors_retains_model_cost_gradient():
    c = _config("fixed", "delayed", 0., .5)
    z = np.array([.2, .5, .9])
    empty = VisitorState(np.array([], dtype=np.int64), np.array([]), np.array([]), np.array([]))
    got = investment_invasion_terms_expressed(z, empty, c)["gradient"]
    assert got == pytest.approx(-2*c.investment_cost*z[1], abs=1e-12)
