"""Native original t0 m0-vs-m6 F1 check; no births or biological futures."""
from dataclasses import replace
import numpy as np
import pytest

from scripts.audit_chapter2_original_confirmation_m0_m6_F1_20261015 import (
    A_HALFWIDTH, N_A_CARRIERS, assign_A_only, audit, source_carriers,
)
from scripts.audit_chapter2_original_founder_compatibility_20261014 import (
    original_fixture, source_state,
)


def test_original_I_exact_m0_m6_carriers_and_source():
    initial=source_state(original_fixture(),"confirmation")
    arm=source_carriers(initial)
    assert arm["m0"] == (5,13,21,29,37,45)
    assert arm["m6"] == (1,3,6,9,11,14)
    assert set(arm["m0"]).isdisjoint(arm["m6"])
    assert N_A_CARRIERS == 6 and A_HALFWIDTH == .0625
    for k, expected in (("m0",0),("m6",6)):
        modified=assign_A_only(initial,arm[k])
        original_phen=initial.alleles.mean(axis=2)
        assert np.array_equal(modified.alleles.mean(axis=2),original_phen)
        assert np.array_equal(modified.alleles[:,0:2,:],initial.alleles[:,0:2,:])
        assert np.array_equal(modified.allele_origin[:,0:2,:],initial.allele_origin[:,0:2,:])
        assert np.count_nonzero(modified.alleles[:,2,0]!=modified.alleles[:,2,1]) == 6
        overlap=np.count_nonzero(
            (modified.alleles[:,1,0]!=modified.alleles[:,1,1]) &
            (modified.alleles[:,2,0]!=modified.alleles[:,2,1])
        )
        assert overlap==expected


def test_original_native_joint_f1_readback_all_visitor_contexts():
    result=audit()
    assert result["status"]=="ORIGINAL_I_UNMODIFIED_F1_ANALYTICAL_ONLY_NOT_EVOLUTION"
    assert result["source_founder_background"]=="confirmation"
    assert result["independent_source_genome_realizations"]==1
    assert result["arm_m0_vs_m6_I_A_co_carrier_counts"]==[0,6]
    assert (result["new_biological_born_offspring"],result["new_Model3_future_updates"],
            result["new_sustained_6class_response_histories"])==(0,0,0)
    assert [v["context"] for v in result["contexts"]]==[0,3,4]
    for row in result["contexts"]:
        assert row["original_I_homologs_identical_in_both_arms"]
        assert row["original_adult_M_I_A_identical_in_both_arms"]
        assert row["original_native_reproductive_return_matrices_identical"]
        assert row["entire_F1_A_marginal_max_bin_error"]<=1e-12
        assert row["entire_F1_I_marginal_max_bin_error"]<=1e-12
        # A testable change in the two-locus law, NOT a predicted evolutionary effect.
        assert 0.0 < row["F1_joint_A_I_total_variation"]<=1.0
        event=row["P_one_child_Aup_Itdown_relative_to_original_founder_mean"]
        assert set(event)=={"m0","m6"}
        assert all(0.0<=p<=1.0 for p in event.values())


def test_unregistered_carriers_and_I_genome_drift_fail():
    initial=source_state(original_fixture(),"confirmation")
    with pytest.raises(ValueError,match="6-carrier"):
        assign_A_only(initial,(1,3,6,9,11))
    original_alleles=initial.alleles.copy()
    original_alleles[5,1,0]=.4375
    drift=replace(initial,alleles=original_alleles)
    with pytest.raises(ValueError,match="composition drift"):
        source_carriers(drift)
