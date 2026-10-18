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
        if r["policy"]=="fixed":
            assert abs(r["maternal_no_service_fraction"]-.25)<1e-12
        for kind in ("I","A"):
            d=r["full_genetic_focal_gradients"][kind]
            assert d["sign"] in ("positive","negative","mixed_or_near_zero",
                                 "undefined")
            assert len(d["slopes"])==2
    warnings.warn("Q2_RESTORED_T39_SOURCE_ASSAY="+json.dumps(
        {"status":result["status"],
         "source_sha256":result["original_source_sha256"],
         "auditor_sha256":result["auditor_sha256"],
         "t39":row,
         "N_assayed_state_time_cells":len(result["path_rows"]),
         "assurance_tolerance_fixed_0p5":.25},sort_keys=True,
        allow_nan=False,separators=(",",":")),stacklevel=1)
