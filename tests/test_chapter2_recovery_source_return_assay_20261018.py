"""Technical source replay + deterministic fixed-genotype return diagnostic.

Not an independent stochastic evolutionary restoration trial.
"""
import json
import warnings

from scripts.audit_chapter2_recovery_source_return_assay_20261018 import (
    assayed_source, TEST_TIMES,
)


def test_old_eight_history_source_return_assay_is_complete_and_source_consistent():
    result=assayed_source()
    assert result["new_biological_histories"]==0
    assert result["new_random_future_paths"]==0
    assert result["existing_historical_paths"]==8
    assert len(result["path_rows"])==8*len(TEST_TIMES)
    row=result["t39_source_example"]
    assert row["t"]==39
    assert row["founder"]==0
    assert row["visitor"]==0
    assert row["policy"]=="evolving"
    assert row["census"]>0
    assert row["high_I_support_closed"] is True
    assert row["max_retained_I"]<row["founder_I_target"]
    # Fixed-genotype pollen return service must be actually measurable.
    for r in result["path_rows"]:
        assert r["census"]>0
        assert r["expected_outcross_return_gain"]>0
        assert 0<=r["maternal_no_service_fraction"]<=.5+1e-12
        assert 0.<=r["min_retained_A_allele"]<=r["max_retained_A_allele"]<=1.
        predicted_low_A_bound=(r["min_retained_A_allele"] >
                               r["ancestral_founder_A_mean"]+1e-12)
        if r["policy"]=="evolving":
            assert r["ancestral_low_A_target_structurally_closed"] is bool(predicted_low_A_bound)
        else:
            assert r["ancestral_low_A_target_structurally_closed"] is None
        if r["policy"]=="fixed":
            assert abs(r["maternal_no_service_fraction"]-.25)<1e-12
        for kind in ("I","A"):
            d=r["full_genetic_focal_gradients"][kind]
            assert d["sign"] in ("positive","negative","mixed_or_near_zero",
                                 "undefined")
            assert len(d["slopes"])==2
    # The 40 states are repeated nested historical snapshots, not 40
    # independent plant lineages or new descendant restoration outcomes.
    rows = result["path_rows"]
    table = []
    for t in TEST_TIMES:
        for policy in ("fixed", "evolving"):
            subset=[r for r in rows if r["t"]==t and r["policy"]==policy]
            assert len(subset)==4
            def nsign(trait, sign):
                return sum(x["full_genetic_focal_gradients"][trait]["sign"]==sign
                           for x in subset)
            table.append({
                "t":t,"historical_A":policy,"saved_genotypes":len(subset),
                "high_I_support_closed":sum(x["high_I_support_closed"] is True
                                           for x in subset),
                "ancestral_low_A_support_closed":sum(
                    x["ancestral_low_A_target_structurally_closed"] is True
                    for x in subset),
                "I_focal_positive":nsign("I","positive"),
                "I_focal_negative":nsign("I","negative"),
                "I_focal_undefined":nsign("I","undefined"),
                "A_focal_negative":nsign("A","negative"),
                "A_focal_positive":nsign("A","positive"),
                "A_focal_undefined":nsign("A","undefined"),
                "restored_outcross_positive":sum(
                    x["expected_outcross_return_gain"]>0 for x in subset),
                "source_positive_I_and_closed":sum(
                    x["high_I_support_closed"] is True
                    and x["full_genetic_focal_gradients"]["I"]["sign"]=="positive"
                    for x in subset),
            })
    selected=[r for r in rows if (r["founder"],r["visitor"],r["policy"])
              ==(0,0,"evolving")]
    assert len(selected)==len(TEST_TIMES)
    warning_data={
        "status":"POST_OUTCOME_GENOTYPE_STATE_SIGN_MATRIX_NOT_INDEPENDENT_CONF",
        "selected_source_timeline":selected,
        "time_policy_counts":table,
        "predeclared_source_times":list(TEST_TIMES),
        "historical_sources":8,"saved_state_time_cells":40,
        "new_biological_history_paths":0,
        "source_sha256":result["original_source_sha256"],
        "auditor_sha256":result["auditor_sha256"],
    }
    warnings.warn("Q2_RESTORED_SOURCE_SIGN_MATRIX="+json.dumps(
        warning_data,sort_keys=True,separators=(",",":"),allow_nan=False),
        stacklevel=1)
    warnings.warn("Q2_RESTORED_T39_SOURCE_ASSAY="+json.dumps(
        {"status":result["status"],
         "source_sha256":result["original_source_sha256"],
         "auditor_sha256":result["auditor_sha256"],
         "t39":row,
         "N_assayed_state_time_cells":len(result["path_rows"]),
         "assurance_tolerance_fixed_0p5":.25},sort_keys=True,
        allow_nan=False,separators=(",",":")),stacklevel=1)
