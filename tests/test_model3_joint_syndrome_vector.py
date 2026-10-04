from scripts.audit_model3_joint_syndrome_vector import run_audit


def test_natural_isolation_rotates_joint_syndrome_vector_in_all_states():
    result = run_audit()
    assert result["status"] == "joint_island_syndrome_selection_vector_recovered"
    assert result["states"] == 45
    assert result["histories_per_state"] == 128
    assert result["diagnostics"]["all_histories_all_states_shift_investment_down"] is True
    assert result["diagnostics"]["all_histories_all_states_shift_assurance_up"] is True
    assert result["diagnostics"]["every_paired_history_has_nonempty_assurance_cost_window"] is True


def test_central_state_assurance_cost_window_is_source_locked():
    row = run_audit()["central_state"]
    assert abs(row["mean_far_minus_near_investment_gradient"] - (-0.6512794913507407)) < 1e-9
    assert abs(row["mean_far_minus_near_assurance_gradient"] - 0.7877915922576683) < 1e-9
    assert abs(row["mean_near_critical_assurance_cost"] - 1.01738737447808) < 1e-9
    assert abs(row["mean_far_critical_assurance_cost"] - 1.805178966735748) < 1e-9
    assert row["paired_nonempty_cost_window_fraction"] == 1.0
