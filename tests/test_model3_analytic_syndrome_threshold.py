import numpy as np

from scripts.audit_model3_analytic_syndrome_threshold import (
    COMMUNITIES,
    monomorphic_log_fitness,
    monomorphic_terms,
    run_audit,
)


def test_analytic_gradient_matches_numerical_derivative():
    for access in (0.2, 0.5, 0.8):
        for name in ("left4", "right4", "center4"):
            h = 1e-6
            plus = monomorphic_log_fitness(
                access=access,
                visitor_optima=COMMUNITIES[name],
                investment=0.5 + h,
            )
            minus = monomorphic_log_fitness(
                access=access,
                visitor_optima=COMMUNITIES[name],
                investment=0.5 - h,
            )
            numeric = (plus - minus) / (2 * h)
            analytic = monomorphic_terms(
                access=access,
                visitor_optima=COMMUNITIES[name],
            )["log_fitness_gradient"]
            assert abs(numeric - analytic) < 1e-8


def test_threshold_recovers_source_locked_extreme_directions():
    result = run_audit()
    assert result["all_four_extreme_signs_match"] is True


def test_left_right_threshold_is_mirror_symmetric():
    low_left = monomorphic_terms(access=0.2, visitor_optima=COMMUNITIES["left4"])
    high_right = monomorphic_terms(access=0.8, visitor_optima=COMMUNITIES["right4"])
    low_right = monomorphic_terms(access=0.2, visitor_optima=COMMUNITIES["right4"])
    high_left = monomorphic_terms(access=0.8, visitor_optima=COMMUNITIES["left4"])
    assert np.isclose(low_left["threshold_ratio"], high_right["threshold_ratio"], atol=1e-12)
    assert np.isclose(low_right["threshold_ratio"], high_left["threshold_ratio"], atol=1e-12)
    assert low_left["threshold_ratio"] > 1
    assert low_right["threshold_ratio"] < 1
