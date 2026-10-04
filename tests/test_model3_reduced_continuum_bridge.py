from scripts.audit_model3_reduced_continuum_bridge import run_audit


def test_reduced_continuum_recovers_bridge_directions_and_regime_order():
    result = run_audit()
    assert result["histories"] == 128
    assert result["start_level_sign_matches"] == result["start_level_cells"] == 9
    assert result["regime_order_matches"] is True
    assert result["condition_level_correlation"] > 0.95


def test_reduced_continuum_does_not_claim_full_density_magnitude():
    result = run_audit()
    ratios = {row["intervention"]: row["magnitude_ratio"] for row in result["rows"]}
    # The reduced model should remain visibly distinct from the exact inherited
    # density result; agreement in sign/regime is not silently promoted to
    # magnitude equivalence.
    assert ratios["natural"] < 0.9
    assert ratios["visitor_pooled"] < 0.9
