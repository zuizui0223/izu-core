import json
import pytest
from scripts import adjudicate_model3_joint_syndrome as a

def test_failed_price_rejected():
    s=json.loads(a.SELECTION.read_text())
    s["exact_multivariate_price"]["passed"]=False
    with pytest.raises(ValueError,match="Price"):
        a.validate_selection(s)

def test_missing_response_rejected():
    s=json.loads(a.SELECTION.read_text())
    del s["full_G_beta_response"]
    with pytest.raises(ValueError,match="response"):
        a.validate_selection(s)

def test_summary_without_records_rejected():
    d=json.loads(a.FINITE_DESIGN.read_text())
    with pytest.raises(ValueError,match="records"):
        a.validate_finite({"setting":"prior_selfing","status":"finite_joint_syndrome_followup_complete"},d)


def test_partial_response_is_explicit_not_silently_accepted():
    s=json.loads(a.SELECTION.read_text())
    assert s["full_G_beta_response"]["frozen_gate_pass_cells"]==46
    assert a.validate_selection(s) is False
