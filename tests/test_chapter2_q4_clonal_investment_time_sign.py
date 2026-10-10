"""Guard exact Q4 time-horizon sign reversal against reinterpretation as evolution."""
import json

import numpy as np
import pytest

from scripts.audit_chapter2_q4_clonal_investment_time_sign import (
    HORIZONS, STATUS, DERIVATIVE_STEP,
    investment_kernel, mean_seed_at_census, run_all,
    state_gradient_contributions, propagations,
)


def test_source_one_generation_slope_changes_sign_across_census():
    for n in range(1, 9):
        dmu = (
            mean_seed_at_census(n, 8, 6.0, .36)
            - mean_seed_at_census(n, 8, 6.0, .34)
        ) / .02
        if n <= 5:
            assert dmu < 0
        else:
            assert dmu > 0
    assert mean_seed_at_census(8, 8, 6.0, .35) == pytest.approx(
        8.99442415119334, rel=0, abs=1e-10
    )
    assert mean_seed_at_census(8, 48, 6.0, .35) == pytest.approx(
        mean_seed_at_census(8, 8, 6.0, .35), rel=0, abs=1e-11
    )


def test_exact_kernel_preserves_mass_and_absorbing_extinction():
    T, mu = investment_kernel(8, 6., .35)
    assert T.shape == (9,9)
    np.testing.assert_allclose(T.sum(axis=1), 1., atol=1e-12, rtol=0)
    assert T[0,0] == 1 and (T[0,1:]==0).all()
    assert T[8,0] > 0 and T[8,8] > 0
    assert len(propagations(T)) == 81
    assert np.isclose(mu[8], 8.99442415119334, atol=1e-10)


def test_all_six_source_conditions_exact_horizon_and_no_genetic_history():
    out = run_all()
    assert out["status"] == STATUS
    assert out["new_visitor_histories"] == 0
    assert out["new_evolutionary_trajectories"] == 0
    assert out["independent_confirmatory_tests"] == 0
    assert out["no_allele_change"] and out["no_pollinator_turnover"]
    assert len(out["results"]) == 6
    assert out["horizons"] == list(HORIZONS)
    lookup = {(r["K"],r["resource_budget"]): r for r in out["results"]}
    assert set(lookup) == {
        (8,4.5),(8,6.0),(8,8.0),(48,4.5),(48,6.0),(48,8.0)
    }
    for row in out["results"]:
        assert row["baseline_P80"] == pytest.approx(
            row["horizons"]["80"]["P_occupied"]["0.35"], abs=1e-12
        )
        assert 0 <= row["baseline_P80"] <= 1
        for h in HORIZONS:
            assert set(row["horizons"][str(h)]["P_occupied"]) == {"0.34","0.35","0.36"}
        assert row["H80_tangent_sensitivity"]["total"] == pytest.approx(
            row["H80_tangent_forward_check"], abs=5e-9
        )

    k8 = lookup[(8,6.)]
    k48 = lookup[(48,6.)]
    assert k8["baseline_P80"] == pytest.approx(.030242646454152422, abs=1e-10)
    assert k48["baseline_P80"] == pytest.approx(.828719233465605, abs=1e-10)
    assert k8["source_seed_response_N8_delta_per_unit"] == pytest.approx(
        1.4229153138312, abs=1e-7
    )
    assert k48["source_seed_response_N8_delta_per_unit"] == pytest.approx(
        k8["source_seed_response_N8_delta_per_unit"], abs=1e-11
    )
    assert k8["source_seed_response_N1_delta_per_unit"] < 0
    assert k48["source_seed_response_N1_delta_per_unit"] < 0
    assert k8["horizons"]["1"]["group_shift_0p34_to_0p36"] > 0
    assert k8["horizons"]["80"]["group_shift_0p34_to_0p36"] == pytest.approx(
        -.0004659065526794841, abs=1e-10
    )
    assert k48["horizons"]["80"]["group_shift_0p34_to_0p36"] == pytest.approx(
        +.004220453946611302, abs=1e-10
    )
    assert k8["H80_tangent_sensitivity"]["low_N1_5"] == pytest.approx(
        -.072457907305327, abs=2e-6
    )
    assert k8["H80_tangent_sensitivity"]["high_N6_K"] == pytest.approx(
        +.049165613942204, abs=2e-6
    )
    assert k48["H80_tangent_sensitivity"]["low_N1_5"] < 0
    assert k48["H80_tangent_sensitivity"]["high_N6_K"] > 0

    # Full resource grid is reported, including weak/near-ceiling effects.
    assert lookup[(8,4.5)]["horizons"]["80"]["group_shift_0p34_to_0p36"] < 0
    assert lookup[(8,8.0)]["horizons"]["80"]["group_shift_0p34_to_0p36"] > 0
    assert all(lookup[(48,b)]["horizons"]["80"]["group_shift_0p34_to_0p36"] > 0 for b in (4.5,6.,8.))
    assert "not an individual" in out["limitations"][0]
    json.dumps(out, allow_nan=False)


@pytest.mark.parametrize("args", [
    (0,8,6.,.35),
    (9,8,6.,.35),
    (8,8,6.,1.),
    (8,8,6.,-.2),
    (8,8,7.5,.35),
])
def test_fail_closed_invalid_intervention(args):
    with pytest.raises(ValueError):
        mean_seed_at_census(*args)


def test_total_tangent_is_census_partition_and_not_mediation():
    T,_ = investment_kernel(8,6.,.35)
    Tp,_ = investment_kernel(8,6.,.35+DERIVATIVE_STEP)
    Tm,_ = investment_kernel(8,6.,.35-DERIVATIVE_STEP)
    parts = state_gradient_contributions(T, (Tp-Tm)/(2*DERIVATIVE_STEP), 80)
    assert parts["zero_N0"] == 0
    assert parts["total"] == pytest.approx(
        parts["low_N1_5"]+parts["high_N6_K"], abs=1e-9
    )
    assert parts["low_N1_5"] < 0 < parts["high_N6_K"]
