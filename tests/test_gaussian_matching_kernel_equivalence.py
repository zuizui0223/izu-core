import math
from pathlib import Path

import numpy as np
import pytest

import scripts.audit_chapter2_el_nonlinear_reduction as nonlinear
import scripts.run_constraint_mechanism_abm as v1
import scripts.run_constraint_mechanism_abm_v2_branching as v2
import scripts.run_constraint_mechanism_abm_v3_service_quality as v3
import scripts.run_constraint_mechanism_abm_v4_fixed_visit_budget as v4
import scripts.run_response_geometry_parameter_robustness as geometry

ROOT = Path(__file__).resolve().parents[1]
SCALAR_KERNEL_TOKEN = "math.exp(-((mismatch / max(pollinator.breadth, 1e-6)) ** 2))"
EXPECTED_SCALAR_IMPLEMENTATIONS = {
    "run_constraint_mechanism_abm.py",
    "run_constraint_mechanism_abm_v2_branching.py",
    "run_constraint_mechanism_abm_v3_service_quality.py",
    "run_constraint_mechanism_abm_v4_fixed_visit_budget.py",
    "run_response_geometry_parameter_robustness.py",
}


def _v1_score(x: float, p: float, breadth: float) -> float:
    return v1.encounter_score(
        v1.Plant(trait=x, assurance=0.0),
        v1.Pollinator(trait=p, breadth=breadth, introduced=False),
    )


def _v2_state(x: float):
    template = v2.LineageTemplate(
        trait=x,
        pollinator_dependency=0.5,
        assurance_ceiling=0.5,
        assurance_responsiveness=0.01,
        trait_adjustment=0.03,
    )
    return v2.LineageState(template=template, trait=x)


def _v2_score(x: float, p: float, breadth: float) -> float:
    return v2.encounter_score(
        _v2_state(x),
        v2.Pollinator(trait=p, breadth=breadth, introduced=False),
    )


def _v3_state(x: float):
    template = v3.LineageTemplate(
        trait=x,
        pollinator_dependency=0.5,
        assurance_ceiling=0.5,
        assurance_responsiveness=0.01,
        trait_adjustment=0.03,
    )
    return v3.LineageState(template=template, trait=x)


def _v3_score(x: float, p: float, breadth: float) -> float:
    return v3.encounter_score(
        _v3_state(x),
        v3.Pollinator(
            trait=p,
            breadth=breadth,
            introduced=False,
            service_quality=1.0,
        ),
    )


def _v4_state(x: float):
    template = v4.LineageTemplate(
        trait=x,
        pollinator_dependency=0.5,
        assurance_ceiling=0.5,
        assurance_responsiveness=0.01,
        trait_adjustment=0.03,
    )
    return v4.LineageState(template=template, trait=x)


def _v4_score(x: float, p: float, breadth: float) -> float:
    return v4.encounter_score(
        _v4_state(x),
        v4.Pollinator(trait=p, breadth=breadth, introduced=False),
    )


def _geometry_score(x: float, p: float, breadth: float) -> float:
    return geometry.encounter(
        x,
        geometry.Pollinator(trait=p, breadth=breadth, introduced=False),
        geometry.BASE,
    )


SCALAR_ADAPTERS = (_v1_score, _v2_score, _v3_score, _v4_score, _geometry_score)


@pytest.mark.parametrize(
    ("x", "p", "breadth"),
    [
        (0.0, 0.0, 0.16),
        (0.10, 0.35, 0.16),
        (0.25, 0.75, 0.42),
        (0.50, 0.90, 0.42),
        (1.00, 0.00, 0.16),
    ],
)
def test_independent_scalar_gaussian_match_implementations_are_equivalent(
    x: float, p: float, breadth: float
):
    expected = math.exp(-((abs(x - p) / breadth) ** 2))
    observed = [adapter(x, p, breadth) for adapter in SCALAR_ADAPTERS]
    assert observed == pytest.approx([expected] * len(observed), rel=1e-13, abs=1e-15)


def test_all_direct_scalar_kernel_copies_are_covered_by_equivalence_adapters():
    discovered = {
        path.name
        for path in (ROOT / "scripts").glob("*.py")
        if SCALAR_KERNEL_TOKEN in path.read_text(encoding="utf-8")
    }
    assert discovered == EXPECTED_SCALAR_IMPLEMENTATIONS
    assert len(SCALAR_ADAPTERS) == len(discovered)


def test_vectorized_current_kernel_matches_scalar_current_endpoint():
    pollinators = (
        geometry.Pollinator(trait=0.18, breadth=0.16, introduced=False),
        geometry.Pollinator(trait=0.49, breadth=0.42, introduced=False),
        geometry.Pollinator(trait=0.82, breadth=0.16, introduced=True),
    )
    trajectory = (pollinators, pollinators)
    penalty = geometry.BASE.replacement_penalty
    vectorized_trajectory = [
        np.asarray(
            [
                [p.trait, p.breadth, penalty if p.introduced else 1.0]
                for p in pollinators
            ],
            dtype=float,
        )
        for _ in trajectory
    ]

    scalar = [
        geometry.endpoint_on_trajectory(trait, trajectory, geometry.BASE)[1]
        for trait in geometry.TRAIT_GRID
    ]
    vectorized = nonlinear.endpoint_vectorized(vectorized_trajectory)
    assert vectorized.tolist() == pytest.approx(scalar, rel=1e-12, abs=1e-12)
