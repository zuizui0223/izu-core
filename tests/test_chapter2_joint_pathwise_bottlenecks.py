"""Checks for read-only-source re-execution of the previously exposed grid."""
import numpy as np
import pytest

from scripts.audit_chapter2_joint_pathwise_bottlenecks import (
    BUDGETS,HORIZONS,STATUS,_paired_outcomes,_summarize_paths,audit,
)


def test_paired_survivor_table_retains_harmed_as_well_as_helped():
    # Deliberate counterexample to assuming gate reductions are pathwise monotone
    def path(last):
        return {"census":[8, last], "first_extinction":1 if last==0 else None,
                "end_genetic_mean_given_occupied":None}
    a=[path(1),path(0),path(1),path(0)]
    b=[path(0),path(1),path(1),path(0)]
    got=_paired_outcomes(a,b,1)
    assert got["baseline_only"]==1
    assert got["gate_only"]==1
    assert got["both_survived"]==1
    assert got["both_extinct"]==1
    assert got["net_baseline_minus_gate"]==0


def test_extinction_not_imputed_as_zero_genetic_trait():
    extinct={"census":[8,2,0], "first_extinction":2,
             "end_genetic_mean_given_occupied":None}
    alive={"census":[8,3,2], "first_extinction":None,
           "end_genetic_mean_given_occupied":[0.4,0.5,0.6]}
    result=_summarize_paths([extinct,alive],2)
    assert result["n_paths"]==2
    assert result["occupied_count"]==1
    assert result["first_extinction_median_among_extinct"]==2
    assert result["surviving_endpoint_genetic_n_at_80_only"]==1
    assert result["surviving_endpoint_genetic_mean_at_80_only"]==[0.4,0.5,0.6]
    assert result["checkpoints"]["1"]["occupied"]==2
    assert result["mean_terminal_census_unconditional"]==1


def test_replay_source_matching_and_no_visitor_pathwise_invariant_small_fixture():
    out=audit(budgets=(3.,6.),draws=2,verify_original=False)
    assert out["status"]==STATUS
    assert out["independent_visitor_histories"]==0
    assert out["archived_original_cell_counts_reproduced"] is False
    assert len(out["rows"])==2*2*2*2
    import json
    json.dumps(out, sort_keys=True, allow_nan=False)  # Fail if any NumPy scalar leaks
    assert out["design"]["horizons"]==[40,80]
    for row in out["rows"]:
        assert row["n_demographic_paths"]==2
        assert set(row["gate_summaries"])=={"baseline","half_self","half_outcross"}
        for gate, data in row["gate_summaries"].items():
            assert data["occupied_count"]+data["extinct_count"]==2
            assert data["offspring_genetics_not_imputed_after_extinction"]
            assert data["checkpoints"]["1"]["occupied"]<=2
            if data["surviving_endpoint_genetic_mean_at_80_only"] is not None:
                assert len(data["surviving_endpoint_genetic_mean_at_80_only"])==3
        for gate, paired in row["paired_gate_contrasts"].items():
            assert sum(paired[k] for k in ("both_survived","baseline_only","gate_only","both_extinct"))==2
        if row["visitor_regime"]=="no_visitors":
            assert row["paired_gate_contrasts"]["half_outcross"]["baseline_only"]==0
            assert row["paired_gate_contrasts"]["half_outcross"]["gate_only"]==0


@pytest.mark.parametrize("kwargs",[
    {"budgets":(4.5,), "draws":2,"verify_original":False},
    {"budgets":(3.,6.),"draws":24,"verify_original":False},
    {"budgets":BUDGETS,"draws":2,"verify_original":True},
])
def test_fail_closed_unsupported_scope(kwargs):
    with pytest.raises(ValueError,match="unsupported scope"):
        audit(**kwargs)
