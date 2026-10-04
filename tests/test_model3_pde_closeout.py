import numpy as np
from scripts.audit_model3_pde_closeout import closure_counterexample, controlled_audit


def test_identical_phenotypes_do_not_determine_sexual_offspring_variance():
    rows = closure_counterexample()
    assert abs(rows[0]['initial_mean'] - rows[1]['initial_mean']) < 1e-12
    assert all(abs(r['initial_variance']) < 1e-12 for r in rows)
    assert all(abs(r['next_mean'] - .5) < 1e-12 for r in rows)
    assert rows[0]['next_variance'] < 1e-12
    assert rows[1]['next_variance'] > 1e-4


def test_controlled_audit_records_numerics_and_all_horizons():
    result = controlled_audit(accesses=[.5], communities=['center4'], horizons=[1, 3])
    assert len(result['rows']) == 2
    for row in result['rows']:
        assert row['ode_tolerance_mean_gap'] < 1e-6
        assert abs(row['ode_mass_error']) < 1e-8
        assert row['ode_min_mass'] >= -1e-10
        assert np.isfinite(row['exact_variance'])
    assert len(result['weak_time_rows']) == 4
