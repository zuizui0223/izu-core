from scripts.audit_model3_joint_G_beta_response import run_audit


def test_joint_G_beta_response_runs_all_frozen_cells():
    result = run_audit()
    assert result["status"] == "joint_G_beta_response_complete"
    assert result["cells"] == 48
    assert 0 <= result["pass_cells"] <= 48
    assert -1 <= result["minimum_cosine_full_G"] <= 1


def test_full_G_is_never_silently_diagonalized():
    result = run_audit()
    assert any(abs(row["G_ia"]) > 1e-12 for row in result["rows"])
    assert all(len(row["G"]) == 2 and len(row["G"][0]) == 2 for row in result["rows"])
