from scripts.audit_model3_reduced_pde_selection import (
    mean_investment_velocity,
    run_audit,
)


def test_reduced_pde_recovers_known_model3_fixed_gradient_signs():
    result = run_audit()
    assert result["all_known_fixed_gradient_signs_recovered"] is True
    assert all(row["sign_match"] for row in result["rows"])


def test_reduced_pde_preserves_left_right_symmetry():
    left_low = mean_investment_velocity(0.2, "left4")
    right_high = mean_investment_velocity(0.8, "right4")
    right_low = mean_investment_velocity(0.2, "right4")
    left_high = mean_investment_velocity(0.8, "left4")
    assert abs(left_low - right_high) < 1e-12
    assert abs(right_low - left_high) < 1e-12
    assert left_low > 0 > right_low
