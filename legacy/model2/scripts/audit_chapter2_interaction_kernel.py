from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from scripts.run_response_geometry_parameter_robustness import (
    BASE,
    Pollinator,
    encounter,
    endpoint_on_trajectory,
    service,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/results/chapter2_interaction_kernel_audit_frozen_20260828.json"
EPS = 1e-12


def community_kernel(
    trait: float,
    pollinators: tuple[Pollinator, ...],
) -> float:
    """Return the exact pre-saturation mean-match kernel used by v4 geometry."""
    if not pollinators:
        return 0.0
    return sum(encounter(trait, pollinator, BASE) for pollinator in pollinators) / len(
        pollinators
    )


def saturation_map(kernel: float) -> float:
    return 1.0 - math.exp(-BASE.saturation * kernel)


def sign(value: float) -> int:
    if value > EPS:
        return 1
    if value < -EPS:
        return -1
    return 0


def canonical_text_sha256(path: Path) -> str:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build() -> dict:
    # Deterministic hand fixtures only: no RNG, parameter search, or new scientific run.
    mainland_a = (
        Pollinator(0.18, 0.16, False),
        Pollinator(0.49, 0.42, False),
        Pollinator(0.82, 0.16, False),
    )
    mainland_b = (
        Pollinator(0.24, 0.16, False),
        Pollinator(0.55, 0.42, False),
        Pollinator(0.76, 0.16, False),
    )
    island_a = (
        Pollinator(0.11, 0.42, True),
        Pollinator(0.68, 0.16, False),
    )
    island_b = (
        Pollinator(0.16, 0.42, True),
        Pollinator(0.72, 0.16, False),
    )
    mainland_trajectory = (mainland_a, mainland_b, mainland_b, mainland_a)
    island_trajectory = (island_a, island_b, island_b, island_a)

    direct_errors: list[float] = []
    trajectory_errors: list[float] = []
    sign_checks: list[bool] = []
    fixed_assurance_checks: list[bool] = []
    rows = []
    dependency = 0.70
    fixed_autonomous_route = 0.08

    for initial_trait in (0.0, 0.25, 0.50, 0.75, 1.0):
        for assemblage in ((), mainland_a, mainland_b, island_a, island_b):
            kernel = community_kernel(initial_trait, assemblage)
            direct_errors.append(
                abs(service(initial_trait, assemblage, BASE) - saturation_map(kernel))
            )

        mainland_trait, mainland_service = endpoint_on_trajectory(
            initial_trait, mainland_trajectory, BASE
        )
        island_trait, island_service = endpoint_on_trajectory(
            initial_trait, island_trajectory, BASE
        )
        mainland_kernel = community_kernel(mainland_trait, mainland_trajectory[-1])
        island_kernel = community_kernel(island_trait, island_trajectory[-1])
        trajectory_errors.extend(
            (
                abs(mainland_service - saturation_map(mainland_kernel)),
                abs(island_service - saturation_map(island_kernel)),
            )
        )
        delta_service = island_service - mainland_service
        composite_kernel_difference = island_kernel - mainland_kernel
        sign_checks.append(sign(delta_service) == sign(composite_kernel_difference))

        mainland_reproduction = 1.0 - (1.0 - dependency * mainland_service) * (
            1.0 - fixed_autonomous_route
        )
        island_reproduction = 1.0 - (1.0 - dependency * island_service) * (
            1.0 - fixed_autonomous_route
        )
        fixed_assurance_checks.append(
            sign(island_reproduction - mainland_reproduction) == sign(delta_service)
        )
        rows.append(
            {
                "initial_trait": initial_trait,
                "mainland_final_trait": mainland_trait,
                "island_final_trait": island_trait,
                "mainland_composite_kernel": mainland_kernel,
                "island_composite_kernel": island_kernel,
                "delta_service": delta_service,
                "composite_kernel_difference": composite_kernel_difference,
            }
        )

    sources = [
        ROOT / "scripts/run_response_geometry_parameter_robustness.py",
        ROOT / "scripts/run_constraint_mechanism_abm_v9_local_plant_opportunity.py",
        ROOT / "scripts/run_constraint_mechanism_abm_v10_effective_service_dependency.py",
    ]
    maximum_direct_error = max(direct_errors)
    maximum_trajectory_error = max(trajectory_errors)
    checks = {
        "service_equals_monotone_saturation_of_mean_match_kernel": maximum_direct_error
        <= EPS,
        "trajectory_endpoint_service_equals_saturation_of_composite_kernel": maximum_trajectory_error
        <= EPS,
        "per_realization_service_sign_equals_composite_kernel_difference_sign": all(
            sign_checks
        ),
        "fixed_downstream_assurance_route_preserves_service_sign": all(
            fixed_assurance_checks
        ),
        "no_random_draws_or_parameter_search": True,
    }
    if not all(checks.values()):
        raise RuntimeError(f"interaction-kernel identity audit failed: {checks}")

    return {
        "schema_version": "1.0",
        "updated_on": "2026-08-28",
        "analysis": "chapter2_interaction_kernel_identity_audit",
        "status": "exact_code_identity_verified",
        "audit_kind": "deterministic_algebraic_identity_no_new_simulation",
        "source_canonical_text_sha256": {
            path.relative_to(ROOT).as_posix(): canonical_text_sha256(path)
            for path in sources
        },
        "checks": checks,
        "maximum_direct_identity_error": maximum_direct_error,
        "maximum_trajectory_composite_identity_error": maximum_trajectory_error,
        "fixture_rows": rows,
        "valid_response_coordinate": (
            "G_omega(x0) = K_I,T(Phi_I,T(x0; omega_I)) - "
            "K_M,T(Phi_M,T(x0; omega_M))"
        ),
        "rejected_shortcut": (
            "K_I(x0) - K_M(x0) is not the exact endpoint response coordinate when "
            "environment-specific trait adjustment changes the two final plant states."
        ),
        "aggregation_boundary": (
            "Per-realization sign equivalence does not imply that the sign of mean service "
            "contrast equals the sign of a mean-kernel contrast, because the saturation map "
            "is nonlinear."
        ),
        "local_filtering_boundary": (
            "The local operator stochastically restricts plant, pollinator and pair support, "
            "then conserves the original row budget for retained positive rows and redistributes "
            "weight; it is not a scalar shrinkage of the global kernel."
        ),
        "assurance_boundary": (
            "Sign preservation is an algebraic identity only when dependency and the autonomous "
            "route are held fixed across the comparison. Environment-specific dynamic assurance "
            "is not covered by that theorem; the frozen sensitivity envelope supplies the empirical "
            "model result of zero sign rescues among 580 eligible declines."
        ),
        "claim_boundary": (
            "This audit exposes exact identities already implemented in the frozen model. It adds "
            "no simulation evidence, field calibration, natural-frequency estimate or external "
            "prediction, and it does not convert model-conditional geometry into an ultimate "
            "historical explanation."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "out": str(args.out)}, indent=2))


if __name__ == "__main__":
    main()
