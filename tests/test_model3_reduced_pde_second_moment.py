from scripts.audit_model3_reduced_pde_second_moment import run_audit


def test_first_moment_remains_exact_while_second_moment_does_not_close():
    result = run_audit()
    assert result["n_cells"] == 25
    assert result["max_abs_mean_error"] < 1e-12
    assert result["positive_variance_corrections"] > 0
    assert result["negative_variance_corrections"] > 0
    assert result["variance_correction_min"] < 0 < result["variance_correction_max"]
