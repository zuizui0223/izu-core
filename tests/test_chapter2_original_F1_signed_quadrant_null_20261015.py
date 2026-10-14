"""Original confirmed-I, artificial A six-carrier four-sign negative control."""
import json

import numpy as np
import pytest

from scripts.audit_chapter2_original_F1_signed_quadrant_null_20261015 import (
    SIGNED_CELLS, SOURCE_BLOB, OUTPUT, ABS_TOL, load_admitted_source,
    signed_joint_events, audit,
)


def test_original_admitted_first_child_source_pinned():
    record=load_admitted_source()
    assert SOURCE_BLOB == "27077b320532f2585ec598140593485f254d563c"
    assert record["original_A_heterozygosity_reset_in_each_arm"] == 42
    assert record["original_I_allele_copies_preserved"]
    assert [x["context"] for x in record["contexts"]] == [0,3,4]


def test_four_quadrant_on_exact_fixed_grid():
    j=np.zeros((33,33),dtype=float)
    j[14,14]=.25 # A below 0.5, I below 0.5
    j[14,20]=.25 # A below 0.5, I above 0.5
    j[18,14]=.25 # A above 0.5, I below 0.5
    j[18,20]=.25 # A above 0.5, I above 0.5
    values=signed_joint_events(j,.5,.5)
    assert set(values)==set(SIGNED_CELLS)
    assert all(abs(v-.25)<1e-15 for v in values.values())


def test_invalid_joint_mass_rejected():
    bad=np.zeros((33,33),dtype=float)
    with pytest.raises(ValueError,match="bivariate"):
        signed_joint_events(bad,.5,.5)
    bad[18,18]=1
    bad[18,17]=-1
    with pytest.raises(ValueError,match="bivariate"):
        signed_joint_events(bad,.5,.5)


def test_actual_original_model3_native_four_tail_null():
    output=audit()
    frozen=json.loads(OUTPUT.read_text(encoding="utf-8"))
    assert frozen["schema"]==output["schema"]
    assert frozen["status"]==output["status"]
    assert (output["new_biological_trajectories"],output["new_offspring_births"])==(0,0)
    assert output["signed_event_classes"]==list(SIGNED_CELLS)
    assert [x["context"] for x in output["contexts"]]==[0,3,4]
    assert len(frozen["contexts"])==3
    for x,y in zip(output["contexts"],frozen["contexts"]):
        assert x["context"]==y["context"]
        for arm in ("m0","m6"):
            assert set(x[arm+"_signed_events"])==set(SIGNED_CELLS)
            for sign in SIGNED_CELLS:
                assert abs(x[arm+"_signed_events"][sign]-y[arm+"_signed_events"][sign])<=ABS_TOL
                if arm=="m0":
                    assert abs(x[arm+"_signed_events"][sign])<=ABS_TOL
                else:
                    assert abs(x[arm+"_signed_events"][sign]-
                               x[arm+"_signed_events"]["A_up_I_down"])<=ABS_TOL
        assert x["m6_signed_events"]["A_up_I_down"]>0
        assert x["reset_A_heterozygotes_per_arm"]==42
        assert x["original_I_homologs_unchanged"] is True
        assert 0.05<x["one_child_joint_A_I_TV"]<0.1
