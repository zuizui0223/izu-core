"""Experimental, strictly phenotype-only offsets for assigned trait-order tests.

This adapter is intentionally NOT wired into reproduce() yet. Until a future
runner explicitly passes its output to the payoff operator, it cannot change
any published or frozen Model 3 result. It never modifies PlantState alleles.
"""
from __future__ import annotations

import math
import numpy as np

from scripts.model3_island.types import PlantState

_EPS = 1e-8


def expressed_traits(state: PlantState, *, assurance_shift: float = 0.0,
                     investment_shift: float = 0.0) -> np.ndarray:
    """Return N × 3 expressed phenotypes in [0,1], not inherited alleles.

    The genetic loci are matching X, investment I, assurance A, in that order.
    A zero offset must return the original numeric genetic means EXACTLY:
    clipping even at zero shift would silently modify frozen source biology.
    """
    if not isinstance(state, PlantState):
        raise TypeError("PlantState required; phenotype cannot become genotype")
    for value in (assurance_shift, investment_shift):
        if isinstance(value, (bool, np.bool_)) or not isinstance(
            value, (int, float, np.number)
        ) or not math.isfinite(float(value)):
            raise ValueError("finite numeric logit offsets required")
    traits = state.alleles.mean(axis=2)
    if assurance_shift == 0 and investment_shift == 0:
        return traits
    expressed = traits.copy()
    for trait_index, offset in ((1, investment_shift), (2, assurance_shift)):
        if offset:
            x = np.clip(traits[:, trait_index], _EPS, 1 - _EPS)
            z = np.log(x) - np.log1p(-x) + float(offset)
            expressed[:, trait_index] = 1 / (1 + np.exp(-z))
    if not np.isfinite(expressed).all() or (
        (expressed < 0).any() or (expressed > 1).any()
    ):
        raise AssertionError("invalid experimental phenotype")
    return expressed
