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
    assert len(result["rows"]) == 9
    assert all(row["history_count"] == 128 for row in result["rows"])
