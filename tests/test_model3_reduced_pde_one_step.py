from scripts.audit_model3_reduced_pde_one_step import run_audit


def test_price_mean_update_matches_exact_density_one_step():
    result = run_audit()
    assert result["status"] == "exact_one_generation_mean_closure_passed"
    assert result["n_cells"] == 25
    assert result["max_abs_mean_error"] < 1e-12
    assert result["all_change_signs_match"] is True
