from scripts.audit_model3_joint_selection_price import run_audit


def test_two_trait_price_identity_is_exact():
    result = run_audit()
    assert result["status"] == "rare_mutant_and_multivariate_price_validated"
    assert result["max_price_abs_error"] < 1e-12


def test_rare_mutant_gradient_is_numerically_stable():
    result = run_audit()
    assert result["max_gradient_stability_error"] < 1e-5


def test_local_g_beta_preserves_response_direction_in_small_variance_cases():
    result = run_audit()
    assert result["min_lande_cosine"] >= 0.90
    assert result["all_lande_component_signs_match"] is True


def test_price_validation_includes_nonzero_covariance_both_signs():
    result = run_audit()
    signs = set()
    for row in result["rows"]:
        offdiag = row["G"][0][1]
        if offdiag > 0:
            signs.add(1)
        elif offdiag < 0:
            signs.add(-1)
    assert signs == {-1, 1}
