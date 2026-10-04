from scripts.audit_model3_joint_response import run_audit


def test_frozen_joint_response_audit_runs_all_declared_cells():
    result=run_audit()
    assert result["status"]=="complete_frozen_multivariate_G_beta_audit"
    assert result["cells"]==48
    assert 0 <= result["local_fidelity_fraction"] <= 1
    assert result["nonzero_offdiagonal_cells"] > 0
