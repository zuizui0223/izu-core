"""Pure, side-effect-free pairing primitives for the Chapter 2 next experiment.

No new histories are generated and no future population is advanced here.
Only authenticated t400 PlantState objects may be supplied by a future runner.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import NamedTuple

import numpy as np

from scripts.model3_island.population import subset
from scripts.model3_island.types import PlantState
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.plan_chapter2_orthogonal_founder_capacity import validate_protocol, PROTOCOL


class PreparedArm(NamedTuple):
    state: PlantState
    capacity: int


FIELDS = ("alleles", "allele_origin", "mutation_flags", "ids", "birth_years")


def state_fingerprint(state: PlantState) -> str:
    if not isinstance(state, PlantState):
        raise TypeError("Require complete diploid PlantState")
    h = hashlib.sha256()
    for key in FIELDS:
        a = np.ascontiguousarray(getattr(state, key))
        h.update(key.encode("ascii"))
        h.update(str(a.shape).encode("ascii"))
        h.update(str(a.dtype).encode("ascii"))
        h.update(a.tobytes())
    return h.hexdigest()


def select_fixed_eight(full: PlantState, *, visitor_history: int,
                       demographic_repeat: int, setting_index: int) -> PlantState:
    """Select IDs once per authenticated t400 source; never select by survival."""
    if not isinstance(full, PlantState) or len(full.ids) > 48:
        raise ValueError("Require a verified t400 population of at most 48")
    if not (39110901 <= visitor_history <= 39110964
            and demographic_repeat >= 0 and 0 <= setting_index < 4):
        raise ValueError("Unexpected prospective cohort or setting identity")
    seed = int(np.random.SeedSequence([
        visitor_history, demographic_repeat, setting_index, 3911092026,
    ]).generate_state(1)[0])
    positions = np.random.default_rng(seed).choice(
        len(full.ids), size=min(8, len(full.ids)), replace=False,
    )
    return subset(full, positions)


def prepare_arms(full: PlantState, selected: PlantState) -> dict[str, PreparedArm]:
    """Check the exact diploid F8 state, then assign only the declared capacities."""
    if not isinstance(full, PlantState) or not isinstance(selected, PlantState):
        raise TypeError("Require complete PlantState archives")
    if len(full.ids) > 48 or len(selected.ids) > 8:
        raise ValueError("Invalid starting abundance")
    positions = {int(i): j for j, i in enumerate(full.ids)}
    if any(int(i) not in positions for i in selected.ids):
        raise AssertionError("F8 genotype IDs absent from full t400 source")
    mapped = subset(full, np.array([positions[int(i)] for i in selected.ids], dtype=int))
    if state_fingerprint(mapped) != state_fingerprint(selected):
        raise AssertionError("F8 immutable complete-genotype mismatch")
    return {
        "eight_founders_capacity8": PreparedArm(selected, 8),
        "eight_founders_capacity48": PreparedArm(selected, 48),
        "all_available_founders_capacity48": PreparedArm(full, 48),
    }


def common_future_seed(*, visitor_history: int, demographic_repeat: int,
                       setting: str, future_visitor: str, budget: float) -> int:
    """Shared across regime, gate and assigned order; independent across strata."""
    if not (39110901 <= visitor_history <= 39110964 and demographic_repeat >= 0):
        raise ValueError("Not a prospective independent visitor history")
    settings = ("delayed_control", "prior_selfing", "pollen_discount", "assurance_cost")
    futures = ("near", "far")
    budgets = (0.5, 1, 2, 3, 4, 5, 8)
    if setting not in settings or future_visitor not in futures or budget not in budgets:
        raise ValueError("Unknown frozen future stratum")
    return int(np.random.SeedSequence([
        visitor_history, demographic_repeat, settings.index(setting),
        futures.index(future_visitor), budgets.index(budget), 3911092048,
    ]).generate_state(1)[0])


def common_future_streams(**kwargs) -> dict[str, np.random.Generator]:
    """New identical-initialization streams; never use legacy regime-index seeding."""
    seed = common_future_seed(**kwargs)
    return {name: stream(seed, name, 0) for name in STREAM_IDS}
