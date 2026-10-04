from scripts.audit_model3_multivariate_price import run_audit


def test_multivariate_price_identity_is_exact_for_all_three_traits():
    result = run_audit()
    assert result["cells"] == 48
    assert result["status"] == "exact_multivariate_price_identity_passed"
    assert result["max_abs_error"] <= 1e-12
