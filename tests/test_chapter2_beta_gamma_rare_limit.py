"""No ecological outcomes: source analytic rare-mutant cross-check."""
import json
import math
import numpy as np
from scripts.audit_chapter2_beta_gamma_rare_limit import (
    RESULT_STATUS,run_comparison,
)


def test_complete_K48_source_analytic_rare_vs_finite():
    result=run_comparison()
    assert result["status"]==RESULT_STATUS
    assert result["n_K48_comparison_cells"]==192
    assert sum(result["rare_beta_gamma_seed_class_counts"].values())==192
    assert result["n_finite_discordances_retaining_same_analytic_rare_class"] <= (
        result["n_finite_K48_discordances"]
    )
    assert len(result["all_rows"])==192
    json.dumps(result,allow_nan=False)
    for r in result["all_rows"]:
        assert r["K"]==r["B"]==48
        assert r["not_an_independent_evolutionary_history"] is True
        assert math.isfinite(r["source_analytic_rare_beta"])
        assert math.isfinite(r["finite_one_individual_beta"])
        assert math.isfinite(r["gamma_group_seed"])
        assert r["rare_beta_group_seed_classification"] in (
            "aligned","individual_advantage_group_harm",
            "individual_disadvantage_group_benefit","inconclusive"
        )


def test_no_visitor_rare_selection_has_no_collective_outcross_effect():
    r=run_comparison()
    no=[x for x in r["all_rows"] if x["visitor_regime"]=="none"]
    assert len(no)==64
    assert all(x["rare_beta_group_seed_classification"]=="aligned" for x in no)
