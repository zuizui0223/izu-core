from scripts.audit_model3_continuum_limit import run_audit


def test_mutation_kernel_converges_to_reflected_heat_semigroup():
    result = run_audit()
    rows = result["spatial_refinement"]
    errors = [row["max_abs_discretization_error"] for row in rows]
    assert errors[2] < errors[1] < errors[0]
    assert errors[-1] < 3e-6


def test_weak_mutation_diffusion_approximation_improves_as_sd_shrinks():
    result = run_audit()
    errors = [row["abs_weak_mutation_multiplier_error"] for row in result["weak_mutation"]]
    assert errors[2] < errors[1] < errors[0]
    assert errors[0] / errors[1] > 10
    assert errors[1] / errors[2] > 10


def test_claim_boundary_keeps_full_model_outside_pure_pde():
    result = run_audit()
    assert result["full_model_status"] == "nonlinear_nonlocal_integro_difference_not_pure_pde"
    assert "mutation_rate=0" in " ".join(result["claim_boundary"])


def test_repeated_mutation_converges_at_fixed_diffusion_time():
    rows = run_audit()['rescaled_time_small_jump']
    for mode in (1, 2, 4):
        errors = [r['absolute_error'] for r in rows if r['mode'] == mode]
        assert errors[2] < errors[1] < errors[0]
        assert errors[0] / errors[1] > 3
        assert errors[1] / errors[2] > 3
