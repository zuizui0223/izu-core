"""Audit inherited crossing order without confusing assigned expression with genetics.

This module consumes the actual finite diploid PlantState at every census year.
Only heritable locus means determine crossing events. No transient offsets,
payoff surrogates, or survivor-only selection enter this diagnostic.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math

import numpy as np

from scripts.model3_island.types import PlantState

TRAIT_INDICES = {"I": 1, "A": 2}
CROSSING_THRESHOLD = 0.05


@dataclass
class GeneticOrderRecorder:
    """One initial t0 population, then one observation per census year through 400.

    The returned history is descriptive/post-treatment, never a conditioning
    variable for the primary randomized expression-order ITT estimate.
    """

    founder: PlantState
    threshold: float = CROSSING_THRESHOLD
    final_year: int = 400
    first_hits: dict[str, int | None] = field(
        default_factory=lambda: {"A": None, "I": None}
    )
    observations: list[dict] = field(default_factory=list)
    first_extinction_year: int | None = None

    def __post_init__(self):
        if not isinstance(self.founder, PlantState) or not len(self.founder.ids):
            raise ValueError("a nonempty diploid founder population is required")
        if (not math.isfinite(self.threshold) or self.threshold <= 0
                or self.threshold >= 1 or self.final_year != 400):
            raise ValueError("frozen crossing threshold or horizon changed")
        self.initial_means = self.founder.alleles.mean(axis=(0, 2)).copy()
        self.observe(0, self.founder)

    def observe(self, year: int, state: PlantState) -> None:
        if (not isinstance(year, int) or isinstance(year, bool)
                or not 0 <= year <= self.final_year
                or year != len(self.observations)):
            raise ValueError("missing, duplicate or reordered annual census")
        if not isinstance(state, PlantState):
            raise TypeError("only actual diploid PlantState can be measured")
        if self.first_extinction_year is not None and len(state.ids):
            raise AssertionError("population revived after extinction without immigration")
        n = len(state.ids)
        genetic = state.alleles.mean(axis=(0, 2)) if n else None
        if not n and self.first_extinction_year is None:
            self.first_extinction_year = year
        if genetic is not None:
            for trait, index in TRAIT_INDICES.items():
                if (self.first_hits[trait] is None
                        and abs(float(genetic[index] - self.initial_means[index]))
                        >= self.threshold):
                    self.first_hits[trait] = year
        self.observations.append({
            "year": year,
            "n": n,
            "inherited_means": genetic.tolist() if genetic is not None else None,
        })

    def summary(self) -> dict:
        if len(self.observations) != self.final_year + 1:
            raise AssertionError("incomplete 0–400 annual inherited census")
        a, i = self.first_hits["A"], self.first_hits["I"]
        if a is None and i is None:
            result = "neither"
        elif i is None:
            result = "A_only"
        elif a is None:
            result = "I_only"
        elif a == i:
            result = "tie"
        elif a < i:
            result = "A_before_I"
        else:
            result = "I_before_A"
        return {
            "classification": result,
            "inherited_A_first_crossing": a,
            "inherited_I_first_crossing": i,
            "extinct_by_t400": self.observations[-1]["n"] == 0,
            "first_extinction_year": self.first_extinction_year,
            "actual_founder_genetic_means": self.initial_means.tolist(),
            "threshold": self.threshold,
            "censuses_recorded": len(self.observations),
            "post_treatment_descriptive_only": True,
            "expression_offsets_not_used": True,
        }
