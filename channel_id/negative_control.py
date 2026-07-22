"""Negative-control analysis for specialist versus generalist island responses.

This module separates three conclusions that are often conflated:
(1) evidence of change, (2) evidence of practical equivalence, and
(3) insufficient precision. It then asks whether a predeclared pollinator
boundary is selectively expressed in specialist lineages.
"""
from __future__ import annotations

import csv
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

GROUPS = {"specialist", "generalist"}


@dataclass(frozen=True)
class Contrast:
    lineage: str
    group: str
    trait: str
    mainland_mean: float
    island_mean: float
    mainland_se: float
    island_se: float
    boundary: str
    matched_set: str

    @property
    def effect(self) -> float:
        return self.island_mean - self.mainland_mean

    @property
    def se(self) -> float:
        return math.sqrt(self.mainland_se ** 2 + self.island_se ** 2)


def load_contrasts(path: str | Path) -> tuple[Contrast, ...]:
    required = {
        "lineage", "group", "trait", "mainland_mean", "island_mean",
        "mainland_se", "island_se", "boundary", "matched_set",
    }
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("contrast table is empty")
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"missing columns: {sorted(missing)}")
    out = []
    for row in rows:
        group = row["group"].strip().lower()
        if group not in GROUPS:
            raise ValueError(f"unknown group: {group}")
        item = Contrast(
            lineage=row["lineage"].strip(), group=group, trait=row["trait"].strip(),
            mainland_mean=float(row["mainland_mean"]), island_mean=float(row["island_mean"]),
            mainland_se=float(row["mainland_se"]), island_se=float(row["island_se"]),
            boundary=row["boundary"].strip(), matched_set=row["matched_set"].strip(),
        )
        if not item.lineage or not item.trait or not item.matched_set:
            raise ValueError("lineage, trait and matched_set are required")
        if item.mainland_se <= 0 or item.island_se <= 0:
            raise ValueError("standard errors must be positive")
        out.append(item)
    return tuple(out)


def classify_effect(item: Contrast, *, equivalence_margin: float, z: float = 1.96) -> dict[str, object]:
    if equivalence_margin <= 0:
        raise ValueError("equivalence_margin must be positive")
    low = item.effect - z * item.se
    high = item.effect + z * item.se
    if low > equivalence_margin or high < -equivalence_margin:
        status = "changed"
    elif low >= -equivalence_margin and high <= equivalence_margin:
        status = "equivalent"
    else:
        status = "inconclusive"
    return {
        "effect": item.effect, "se": item.se, "ci_low": low, "ci_high": high,
        "equivalence_margin": equivalence_margin, "status": status,
    }


def _weighted_mean(items: Sequence[Contrast]) -> tuple[float, float]:
    weights = [1.0 / (item.se ** 2) for item in items]
    total = sum(weights)
    if total == 0:
        raise ValueError("zero total precision")
    mean = sum(w * item.effect for w, item in zip(weights, items)) / total
    return mean, math.sqrt(1.0 / total)


def analyse_negative_control(
    contrasts: Sequence[Contrast], *, equivalence_margin: float,
    target_boundary: str = "bombus_loss",
) -> dict[str, object]:
    target = [item for item in contrasts if item.boundary == target_boundary]
    if not target:
        raise ValueError("no contrasts for target boundary")
    groups = {name: [item for item in target if item.group == name] for name in GROUPS}
    if any(not values for values in groups.values()):
        raise ValueError("target boundary requires specialist and generalist contrasts")

    lineages = []
    for item in target:
        lineages.append({
            "lineage": item.lineage, "group": item.group, "trait": item.trait,
            "matched_set": item.matched_set,
            **classify_effect(item, equivalence_margin=equivalence_margin),
        })

    summary = {}
    for name, values in groups.items():
        mean, se = _weighted_mean(values)
        summary[name] = {
            "n_contrasts": len(values), "pooled_effect": mean, "pooled_se": se,
            "changed": sum(classify_effect(v, equivalence_margin=equivalence_margin)["status"] == "changed" for v in values),
            "equivalent": sum(classify_effect(v, equivalence_margin=equivalence_margin)["status"] == "equivalent" for v in values),
            "inconclusive": sum(classify_effect(v, equivalence_margin=equivalence_margin)["status"] == "inconclusive" for v in values),
        }
    interaction = summary["specialist"]["pooled_effect"] - summary["generalist"]["pooled_effect"]
    interaction_se = math.sqrt(summary["specialist"]["pooled_se"] ** 2 + summary["generalist"]["pooled_se"] ** 2)
    return {
        "target_boundary": target_boundary,
        "equivalence_margin": equivalence_margin,
        "lineages": lineages,
        "group_summary": summary,
        "specialist_minus_generalist": {
            "effect": interaction,
            "se": interaction_se,
            "z": interaction / interaction_se if interaction_se else None,
        },
        "claim_boundary": (
            "A generalist non-response is supported only when its interval lies inside the predeclared "
            "equivalence margin. Non-significance alone is not evidence of no change."
        ),
    }


def simulate_refutation_power(
    contrasts: Sequence[Contrast], *, equivalence_margin: float,
    specialist_effect: float, generalist_effect: float,
    replicates: int = 2000, seed: int = 20260722,
) -> dict[str, object]:
    if replicates <= 0:
        raise ValueError("replicates must be positive")
    rng = random.Random(seed)
    outcomes = {"supports_selective_response": 0, "shared_change_refutes": 0, "inconclusive": 0}
    target = [item for item in contrasts if item.boundary == "bombus_loss"]
    for _ in range(replicates):
        simulated = []
        for item in target:
            truth = specialist_effect if item.group == "specialist" else generalist_effect
            observed = rng.gauss(truth, item.se)
            simulated.append(Contrast(
                item.lineage, item.group, item.trait, 0.0, observed,
                item.se / math.sqrt(2), item.se / math.sqrt(2), item.boundary, item.matched_set,
            ))
        result = analyse_negative_control(simulated, equivalence_margin=equivalence_margin)
        spec = result["group_summary"]["specialist"]
        gen = result["group_summary"]["generalist"]
        if spec["changed"] > 0 and gen["equivalent"] > 0 and gen["changed"] == 0:
            outcomes["supports_selective_response"] += 1
        elif gen["changed"] > 0:
            outcomes["shared_change_refutes"] += 1
        else:
            outcomes["inconclusive"] += 1
    return {"replicates": replicates, "rates": {k: v / replicates for k, v in outcomes.items()}}
