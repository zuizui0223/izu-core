import json
import math
from pathlib import Path

from scripts.audit_chapter2_el_dense_phase_map import (
    clone_probability_for_pairwise_rho,
    expected_distinct_trajectory_support,
    k_eff,
)

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/chapter2_el_dense_phase_map_20260913.json"
POSITIONING = ROOT / "docs/CHAPTER2_ECOLOGY_LETTERS_POSITIONING_20260912.md"


def _load() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_clone_probability_encodes_pairwise_rho_exactly():
    for rho in (0.0, 0.1, 0.25, 0.5, 0.9):
        q = clone_probability_for_pairwise_rho(rho)
        assert math.isclose(q * q, rho, rel_tol=0, abs_tol=1e-12)


def test_exact_keff_two_contour_changes_order_and_support():
    result = _load()
    rows = [row for row in result["exact_k_eff_contours"] if row["target_k_eff"] == 2.0]
    assert [round(row["k_eff"], 12) for row in rows] == [2.0, 2.0, 2.0, 2.0]
    assert [row["order"] for row in rows] == ["CIS", "ICS", "ICS", "ICS"]
    support = [row["support"] for row in rows]
    assert all(b > a for a, b in zip(support, support[1:]))
    assert math.isclose(support[0], 2.0, abs_tol=1e-12)
    assert support[-1] > 6.0


def test_keff_four_contour_can_preserve_order_without_restoring_sufficiency():
    result = _load()
    rows = [row for row in result["exact_k_eff_contours"] if row["target_k_eff"] == 4.0]
    assert [round(row["k_eff"], 12) for row in rows] == [4.0, 4.0, 4.0]
    assert [row["order"] for row in rows] == ["ISC", "ISC", "ISC"]
    assert result["decision"]["k_eff_is_sufficient_statistic_for_nonlinear_order"] is False
    assert result["decision"]["same_k_eff_can_change_order"] is True


def test_support_formula_separates_variance_equivalence_from_support():
    target = 2.0
    points = [(2, 0.0), (4, 1 / 3), (8, 3 / 7), (16, 7 / 15)]
    assert all(math.isclose(k_eff(k, rho), target, abs_tol=1e-12) for k, rho in points)
    support = [expected_distinct_trajectory_support(k, rho) for k, rho in points]
    assert support[0] == 2.0
    assert support[-1] > support[0]


def test_lane_b_positioning_promotes_dense_map_without_reopening_lane_c():
    text = POSITIONING.read_text(encoding="utf-8")
    assert "same-`k_eff=2` contour" in text
    assert "distinct trajectory support" in text
    assert "Figure 3" in text
    assert "Lane C remains paused" in text
