"""Audit the only rigorous diffusion limit currently present in Model 3.

The adult genotype-density update is not a PDE: sexual reproduction is a
non-local integral operator. This audit isolates the mutation kernel used in
scripts.model3_island.density and checks its continuum interpretation.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import json
from math import exp, pi

import numpy as np

from scripts.model3_island.density import mutation_matrix


def cosine_mode_semigroup_error(
    n_nodes: int,
    *,
    mutation_rate: float,
    mutation_sd: float,
    mode: int,
) -> dict:
    """Compare the discrete mutation matrix with the reflected heat semigroup."""
    if n_nodes < 3:
        raise ValueError("n_nodes must be >= 3")
    nodes = np.linspace(0.0, 1.0, n_nodes)
    matrix = mutation_matrix(nodes, mutation_rate, mutation_sd)
    values = np.cos(mode * pi * nodes)
    observed = matrix @ values
    exact_multiplier = (1.0 - mutation_rate) + mutation_rate * exp(
        -0.5 * (mode * pi * mutation_sd) ** 2
    )
    expected = exact_multiplier * values
    diffusion_multiplier = 1.0 - (
        mutation_rate * mutation_sd**2 / 2.0
    ) * (mode * pi) ** 2
    return {
        "n_nodes": n_nodes,
        "mutation_rate": mutation_rate,
        "mutation_sd": mutation_sd,
        "mode": mode,
        "diffusion_coefficient": mutation_rate * mutation_sd**2 / 2.0,
        "exact_semigroup_multiplier": exact_multiplier,
        "diffusion_multiplier": diffusion_multiplier,
        "max_abs_discretization_error": float(np.max(np.abs(observed - expected))),
        "abs_weak_mutation_multiplier_error": abs(
            exact_multiplier - diffusion_multiplier
        ),
    }


def mutation_rescaled_time_audit() -> list[dict]:
    """Analytic reflected-kernel iterates at fixed diffusion time, not fitted data.

    Probability u alone tending to zero at fixed jump width gives a nonlocal
    jump generator. A local heat limit additionally requires small jumps and
    rescaled time. These eigenvalues test that distinction without grid error.
    """
    rows = []
    u, tau = .2, .01
    for mode in (1, 2, 4):
        target = exp(-(mode*pi)**2*tau)
        for sd in (.1, .05, .025):
            steps = round(2*tau/(u*sd**2))
            per_step = (1-u) + u*exp(-.5*(mode*pi*sd)**2)
            observed = per_step**steps
            rows.append(dict(mode=mode, mutation_sd=sd, steps=steps,
                diffusion_time=tau, exact_kernel_multiplier=observed,
                heat_multiplier=target, absolute_error=abs(observed-target)))
    return rows


def run_audit() -> dict:
    spatial = [
        cosine_mode_semigroup_error(
            n,
            mutation_rate=0.05,
            mutation_sd=0.05,
            mode=2,
        )
        for n in (51, 101, 201)
    ]
    weak = [
        cosine_mode_semigroup_error(
            201,
            mutation_rate=0.05,
            mutation_sd=sd,
            mode=2,
        )
        for sd in (0.1, 0.05, 0.025)
    ]
    return {
        "status": "mutation_component_has_reflected_diffusion_limit",
        "source_sha256": {name: hashlib.sha256((Path(__file__).resolve().parents[1]/name).read_bytes().replace(b'\r\n', b'\n')).hexdigest() for name in ("scripts/audit_model3_continuum_limit.py", "scripts/model3_island/density.py")},
        "full_model_status": "nonlinear_nonlocal_integro_difference_not_pure_pde",
        "boundary_condition": "Neumann_reflecting_at_0_and_1",
        "spatial_refinement": spatial,
        "weak_mutation": weak,
        "rescaled_time_small_jump": mutation_rescaled_time_audit(),
        "claim_boundary": [
            "This validates only the mutation kernel continuum interpretation.",
            "Mendelian segregation, outcrossing, recombination, and capacity regulation remain nonlocal/global.",
            "The focal 2026-09-27 Chapter 2 bridge has mutation_rate=0, so mutation diffusion does not generate its headline response.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out")
    args = parser.parse_args()
    result = run_audit()
    rendered = json.dumps(result, indent=2, sort_keys=True)
    print(rendered)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(rendered + "\n")


if __name__ == "__main__":
    main()
