"""Exact rational transfer and analytic Model3-seed identification tests."""
from fractions import Fraction as Q
import math

import numpy as np

from scripts.prove_pollen_flow_identifiability import (
    TA, TB, certificate, matrix_metrics, seed_ledger, source_dimension,
    source_seed_bounds, sharp_paternal_bounds,
)


def test_exact_rational_columns_match_but_donor_mass_changes():
    ma, mb = matrix_metrics(TA), matrix_metrics(TB)
    assert ma["recipient_receipt"] == mb["recipient_receipt"] == (
        Q(1), Q(1), Q(1))
    assert ma["father_pollen_delivered"] == (Q(1), Q(1), Q(1))
    assert mb["father_pollen_delivered"] == (
        Q(9, 5), Q(1, 5), Q(1))
    assert source_dimension(2) == 0
    assert source_dimension(3) == 3
    assert source_dimension(8) == 48


def test_identical_all_recipient_receipts_and_seeds_can_mask_paternity():
    a,b=seed_ledger(TA),seed_ledger(TB)
    np.testing.assert_allclose(
        a["maternal_outcross"],b["maternal_outcross"],atol=0,rtol=0)
    np.testing.assert_allclose(
        a["viable_self"],b["viable_self"],atol=0,rtol=0)
    assert a["group_viable_seed"] == b["group_viable_seed"]
    np.testing.assert_allclose(a["paternity_shares"],
                               [1/3]*3,atol=1e-12,rtol=0)
    np.testing.assert_allclose(b["paternity_shares"],
                               [.6,1/15,1/3],atol=1e-12,rtol=0)
    assert not np.allclose(a["focal_genetic_W"],b["focal_genetic_W"])


def test_fixed_total_delivery_without_recipient_vector_does_not_fix_seed():
    # All three recipients have one incoming pollen under TA.
    even=seed_ledger(TA)
    # Same D=3 but all arrives at recipient 0, entirely from father 1.
    extreme=((Q(0),Q(0),Q(0)),(Q(3),Q(0),Q(0)),(Q(0),Q(0),Q(0)))
    concentrated=seed_ledger(extreme)
    assert sum(matrix_metrics(extreme)["recipient_receipt"]) == 3
    assert sum(matrix_metrics(TA)["recipient_receipt"]) == 3
    assert even["group_viable_seed"] > concentrated["group_viable_seed"]
    bounds=source_seed_bounds()
    np.testing.assert_allclose(even["group_viable_seed"],
                               bounds["maximum_seed_at_equal_maternal_receipt"],
                               rtol=0,atol=1e-12)
    np.testing.assert_allclose(concentrated["group_viable_seed"],
                               bounds["minimum_seed_at_concentrated_receipt"],
                               rtol=0,atol=1e-12)


def test_opposite_local_parentage_response_is_unidentifiable_from_same_state():
    # T(x)=TA+x(TB-TA), and T(-x) are valid nonnegative zero-diagonal
    # matrices for -1<=x<=1. Both preserve every column for all x.
    eps=Q(1,1000)
    h=tuple(tuple(TB[i][j]-TA[i][j] for j in range(3))
            for i in range(3))
    tplus=tuple(tuple(TA[i][j]+eps*h[i][j] for j in range(3))
                for i in range(3))
    tminus=tuple(tuple(TA[i][j]-eps*h[i][j] for j in range(3))
                 for i in range(3))
    assert matrix_metrics(tplus)["recipient_receipt"] == (
        Q(1),Q(1),Q(1))
    assert matrix_metrics(tminus)["recipient_receipt"] == (
        Q(1),Q(1),Q(1))
    p,m=seed_ledger(tplus),seed_ledger(tminus)
    z=seed_ledger(TA)
    assert p["group_viable_seed"]==m["group_viable_seed"]==z["group_viable_seed"]
    derivative=(math.log(p["focal_genetic_W"][0])-
                math.log(m["focal_genetic_W"][0]))/(2*float(eps))
    expected=certificate()["focal_log_W_derivative_with_plus_family"]
    np.testing.assert_allclose(derivative,expected,rtol=1e-7,atol=1e-7)
    assert expected>0
    assert certificate()["focal_log_W_derivative_with_minus_family"]<0


def test_certificate_is_math_only_not_model_reachability():
    r=certificate()
    assert r["status"]=="MATHEMATICAL_LEDGER_CERTIFICATE_NOT_FIELD_OR_MODEL3_REACHABILITY"
    assert r["individual_trait_mapping_unknown"] is True
    np.testing.assert_allclose(r["paternity_L1_difference"],
                               8/15,rtol=0,atol=1e-12)
    assert r["fixed_total_receipt_seed_bounds_n3"]["width"]>0


def test_sharp_father_bounds_and_two_adult_identification_threshold():
    # With n=2 no other candidate exists; with n=3 there are alternative
    # possible fathers for each mother and independent columns can vary.
    assert sharp_paternal_bounds((2., 3.)) == ((3.,3.),(2.,2.))
    assert sharp_paternal_bounds((2.,3.,5.)) == (
        (0.,8.),(0.,7.),(0.,5.))
    f=seed_ledger(TA)["maternal_outcross"]
    b=sharp_paternal_bounds(f)
    for i, paternal in enumerate(seed_ledger(TB)["paternal_outcross"]):
        assert b[i][0]-1e-12 <= paternal <= b[i][1]+1e-12
