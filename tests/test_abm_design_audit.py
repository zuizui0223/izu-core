from channel_id.abm_design_audit import DesignCandidate, run_design_audit


def test_design_audit_ranks_candidates() -> None:
    designs = (
        DesignCandidate(1.0, 0.0, 0.0),
        DesignCandidate(0.5, 0.4, 0.1),
    )
    result = run_design_audit(
        designs=designs,
        target_accuracy=0.0 + 0.01,
        reference_replicates=2,
        test_replicates=1,
        generations=3,
        founders=20,
        seed=3,
    )
    assert result["n_designs"] == 2
    assert len(result["ranked_designs"]) == 2
    assert "overall_accuracy" in result["best_accuracy_design"]


def test_design_candidate_burden_decreases_with_missingness() -> None:
    full = DesignCandidate(1.0, 0.0, 0.0)
    sparse = DesignCandidate(1.0, 0.4, 0.0)
    assert sparse.burden < full.burden
