from scripts.audit_model3_reduced_pde_trajectory import run_audit


def test_reduced_equations_recover_all_60_year_density_directions():
    result = run_audit()
    assert result["n_cells"] == 25
    assert result["replicator_map"]["sign_matches"] == 25
    assert result["replicator_pde"]["sign_matches"] == 25


def test_reduced_equations_meet_exploratory_mean_fidelity_targets():
    result = run_audit()
    assert result["status"] == "reduced_multi_generation_mean_fidelity_passed"
    assert result["replicator_map"]["mean_abs_error"] < 0.01
    assert result["replicator_pde"]["mean_abs_error"] < 0.01
    assert result["replicator_map"]["max_abs_error"] < 0.025
    assert result["replicator_pde"]["max_abs_error"] < 0.025
