"""Rank observation designs for recovering synthetic Izu ABM worlds."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import product
from typing import Iterable

from .abm_recovery import ObservationDesign, run_recovery_benchmark


@dataclass(frozen=True)
class DesignCandidate:
    island_fraction: float
    missing_rate: float
    measurement_sd: float

    def to_observation_design(self) -> ObservationDesign:
        return ObservationDesign(
            island_fraction=self.island_fraction,
            missing_rate=self.missing_rate,
            measurement_sd=self.measurement_sd,
        )

    @property
    def burden(self) -> float:
        """Simple declared burden score: more islands and precision cost more."""
        precision_cost = 1.0 / (1.0 + 10.0 * self.measurement_sd)
        completeness_cost = 1.0 - self.missing_rate
        return self.island_fraction * completeness_cost * precision_cost


def default_designs() -> tuple[DesignCandidate, ...]:
    return tuple(
        DesignCandidate(island_fraction=i, missing_rate=m, measurement_sd=s)
        for i, m, s in product(
            (0.34, 0.50, 0.67, 1.00),
            (0.00, 0.20, 0.40),
            (0.00, 0.05, 0.10),
        )
    )


def run_design_audit(
    *,
    designs: Iterable[DesignCandidate] | None = None,
    target_accuracy: float = 0.70,
    reference_replicates: int = 8,
    test_replicates: int = 10,
    generations: int = 45,
    founders: int = 120,
    seed: int = 1,
) -> dict[str, object]:
    if not 0 < target_accuracy <= 1:
        raise ValueError("target_accuracy must be in (0, 1]")
    candidates = tuple(designs or default_designs())
    if not candidates:
        raise ValueError("at least one design is required")

    rows = []
    for index, candidate in enumerate(candidates):
        result = run_recovery_benchmark(
            reference_replicates=reference_replicates,
            test_replicates=test_replicates,
            generations=generations,
            founders=founders,
            design=candidate.to_observation_design(),
            seed=seed + index * 10_000,
        )
        worst_truth = min(x["accuracy"] for x in result["per_truth"].values())
        rows.append({
            "design": asdict(candidate),
            "burden": candidate.burden,
            "overall_accuracy": result["overall_accuracy"],
            "worst_truth_accuracy": worst_truth,
            "dominant_confusions": result["dominant_confusions"][:3],
            "meets_target": result["overall_accuracy"] >= target_accuracy and worst_truth >= target_accuracy,
        })

    ranked = sorted(
        rows,
        key=lambda row: (
            not row["meets_target"],
            row["burden"] if row["meets_target"] else -row["overall_accuracy"],
            -row["worst_truth_accuracy"],
        ),
    )
    feasible = [row for row in ranked if row["meets_target"]]
    return {
        "target_accuracy": target_accuracy,
        "n_designs": len(rows),
        "minimum_design": feasible[0] if feasible else None,
        "best_accuracy_design": max(rows, key=lambda row: row["overall_accuracy"]),
        "ranked_designs": ranked,
        "claim_boundary": (
            "The selected minimum design is optimal only under the declared synthetic model, "
            "feature set, burden score, and tested design grid."
        ),
    }
