"""Exact algebra regression and fail-closed tests, no Model3 import or simulation."""
from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from math import comb
import json

import pytest

from scripts.audit_chapter2_joint_founder_access_20261014 import (
    SPEC, audit_design, carrier_count_distribution, joint_access_exact
)


def test_four_class_closure_and_original_marginals():
    for overlap in (0,3,6,12):
        for n in (1,2,8,24,48):
            r=joint_access_exact(48,12,12,overlap,n)
            keys=("p_A_retained_I_lost","p_I_retained_A_lost",
                  "p_both_retained","p_both_lost")
            assert sum(r[x] for x in keys)==1
            p0=Fraction(comb(36,n),comb(48,n)) if n<=36 else Fraction(0)
            assert r["p_A_retained_I_lost"]+r["p_both_retained"]==1-p0
            assert r["p_I_retained_A_lost"]+r["p_both_retained"]==1-p0
            assert r["p_only_one_axis_retained"]==(
                r["p_A_retained_I_lost"]+r["p_I_retained_A_lost"])


def test_source_overlap_negative_zero_positive_carrier_covariance():
    assert joint_access_exact(48,12,12,0,8)["covariance_founder_carrier_fractions"] < 0
    assert joint_access_exact(48,12,12,3,8)["covariance_founder_carrier_fractions"] == 0
    assert joint_access_exact(48,12,12,6,8)["covariance_founder_carrier_fractions"] > 0
    assert joint_access_exact(48,12,12,12,8)["p_only_one_axis_retained"] == 0


def test_eight_founders_anti_correlated_retention_and_all_founders():
    r=joint_access_exact(48,12,12,0,8)
    assert abs(float(r["p_only_one_axis_retained"])-0.15648574380458002)<1e-15
    assert abs(float(r["p_both_retained"])-0.841565208995893)<1e-15
    for overlap in (0,3,6,12):
        full=joint_access_exact(48,12,12,overlap,48)
        assert full["p_both_retained"]==1
        assert full["p_only_one_axis_retained"]==0


def test_marginal_carrier_count_distribution():
    for n in (1,2,8,24,48):
        probs=carrier_count_distribution(48,12,n)
        assert len(probs)==n+1 and sum(probs)==1
        p0=Fraction(comb(36,n),comb(48,n)) if n<=36 else Fraction(0)
        assert probs[0]==p0
        assert sum(Fraction(k,n)*p for k,p in enumerate(probs))==Fraction(1,4)


def test_explicit_design_hold_and_full_scenario_grid():
    d=json.loads(SPEC.read_text(encoding="utf-8"))
    r=audit_design(d)
    assert r["new_biological_histories"]==0
    assert len(r["joint_access_rows"])==16
    assert len(r["marginal_A_founder_distribution_moments"])==4
    changed=deepcopy(d)
    changed["approval"]["new_biological_histories"]=1
    with pytest.raises(ValueError,match="No new biology"):
        audit_design(changed)


@pytest.mark.parametrize("args",[
    (0,0,0,0,1),(48,12,12,13,8),(48,36,36,0,8),
    (48,12,12,-1,8),(48,12,12,3,49),(48,12,12,3,0),
])
def test_impossible_joint_margins_fail_closed(args):
    with pytest.raises(ValueError,match="Impossible"):
        joint_access_exact(*args)
