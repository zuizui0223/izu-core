from scripts.audit_model3_analytic_bridge_threshold import run_audit


def test_analytic_threshold_recovers_isolation_regime_switch():
    result = run_audit()
    assert result["status"] == "analytic_isolation_threshold_shift_recovered"
    assert result["diagnostics"]["natural_negative_in_all_histories_all_starts"] is True
    assert result["diagnostics"]["pooled_negative_in_all_histories_all_starts"] is True
    assert result["diagnostics"]["richness_matching_breaks_universal_negative_shift"] is True
    assert result["diagnostics"]["richness_matched_mean_shift_near_zero"] is True
    assert result["diagnostics"]["pooling_strengthens_negative_shift_vs_natural"] is True


def test_analytic_threshold_uses_all_frozen_histories():
    result = run_audit()
    assert len(result["rows"]) == 45
    assert all(row["history_count"] == 128 for row in result["rows"])


def test_central_access_threshold_shift_numeric_lock():
    result = run_audit()
    rows = {
        (row["intervention"], row["start_investment"]):
        row["mean_far_minus_near_selection_margin"]
        for row in result["rows"]
        if row["access"] == 0.5
    }
    expected = {
        ("natural", 0.3): -0.803337,
        ("natural", 0.5): -0.651279,
        ("natural", 0.7): -0.497247,
        ("richness_matched", 0.3): 0.016611,
        ("richness_matched", 0.5): 0.016624,
        ("richness_matched", 0.7): 0.015152,
        ("visitor_pooled", 0.3): -0.921111,
        ("visitor_pooled", 0.5): -0.755125,
        ("visitor_pooled", 0.7): -0.561365,
    }
    for key, target in expected.items():
        assert abs(rows[key] - target) < 1e-6
