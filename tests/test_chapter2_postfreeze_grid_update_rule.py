from __future__ import annotations

import pytest

from scripts.audit_chapter2_postfreeze_grid_update_rule import (
    endpoint_with_rule,
    services_for_grid,
    trait_grid,
)
from scripts.run_response_geometry_parameter_robustness import (
    BASE,
    Pollinator,
    endpoint_on_trajectory,
    pollinator_trajectory,
)


@pytest.mark.parametrize("points", [21, 41, 81])
def test_postfreeze_trait_grids_cover_unit_interval(points: int) -> None:
    grid = trait_grid(points)
    assert len(grid) == points
    assert grid[0] == 0.0
    assert grid[-1] == 1.0
    assert all(b > a for a, b in zip(grid, grid[1:]))


@pytest.mark.parametrize("initial_trait", [0.0, 0.2, 0.5, 0.85, 1.0])
def test_threshold_best_rule_reproduces_frozen_endpoint(initial_trait: float) -> None:
    trajectory = pollinator_trajectory(BASE.mainland, 123456789, BASE)
    expected = endpoint_on_trajectory(initial_trait, trajectory, BASE)
    observed = endpoint_with_rule(initial_trait, trajectory, BASE, "threshold_best")
    assert observed == pytest.approx(expected, rel=0.0, abs=1e-15)


def test_fixed_rule_never_moves_plant_state() -> None:
    trajectory = (
        (Pollinator(trait=0.9, breadth=0.42, introduced=False),),
        (Pollinator(trait=0.8, breadth=0.42, introduced=False),),
    )
    final_trait, _ = endpoint_with_rule(0.1, trajectory, BASE, "fixed")
    assert final_trait == 0.1


def test_smooth_weighted_rule_moves_toward_weighted_partner_centroid() -> None:
    trajectory = (
        (
            Pollinator(trait=0.75, breadth=0.42, introduced=False),
            Pollinator(trait=0.9, breadth=0.42, introduced=False),
        ),
    )
    initial = 0.2
    final_trait, _ = endpoint_with_rule(initial, trajectory, BASE, "smooth_weighted")
    assert final_trait > initial
    assert final_trait < 0.9


@pytest.mark.parametrize("rule", ["threshold_best", "smooth_weighted", "fixed"])
def test_vectorized_grid_services_match_scalar_rule(rule: str) -> None:
    trajectory = pollinator_trajectory(BASE.island, 987654321, BASE)
    grid = (0.0, 0.2, 0.5, 0.85, 1.0)
    vectorized = services_for_grid(grid, trajectory, BASE, rule)
    scalar = [
        endpoint_with_rule(initial_trait, trajectory, BASE, rule)[1]
        for initial_trait in grid
    ]
    assert vectorized.tolist() == pytest.approx(scalar, rel=1e-12, abs=1e-14)
