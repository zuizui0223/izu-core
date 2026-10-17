"""Original-source readout / *hypothetical* future power-cost claim guard.

No simulations, no new histories, and no reclassification of inconclusive Q2.
"""
import json
from pathlib import Path

import pytest

from scripts.audit_chapter2_q2_crossed_precision_20261017 import assumption_mde

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/"docs/audits/CHAPTER2_Q2_I_SUPPORT_384_ORIGINAL_READOUT_20261016.json"
PREC=ROOT/"docs/audits/CHAPTER2_Q2_CROSSED_RETROSPECTIVE_PRECISION_20261017.json"
NOTE=ROOT/"docs/CHAPTER2_Q2_FUTURE_POWER_COST_NO_GO_20261017.md"


def test_original_two_registered_primary_ends_remain_inconclusive():
    actual=json.loads(OLD.read_text(encoding="utf-8"))
    audit=json.loads(PREC.read_text(encoding="utf-8"))
    assert actual["registered_inference"]["result"]=="both_inconclusive"
    assert audit["status"]=="RETROSPECTIVE_ONLY_NOT_NEW_PROSPECTIVE_POWER_OR_BIOLOGY"
    assert actual["original_run"]["original_cases"]==audit["original_cases"]==384
    for key in ("carrier_order_score_delta","carrier_I_event_delta"):
        original=actual["coprimary"][key]
        readback=audit["co_primary"][key]
        assert readback["estimate"]==original["estimate"]
        assert readback["simultaneous_CI"]==original["simultaneous_familywise_CI"]
        assert readback["simultaneous_CI"][0]<0<readback["simultaneous_CI"][1]


@pytest.mark.parametrize("nf,nv,cases,updates",[
    (8,8,384,76800),
    (16,16,1536,307200),
    (24,24,3456,691200),
    (25,25,3750,750000),
    (32,32,6144,1228800),
    (48,48,13824,2764800),
    (74,74,32856,6571200),
    (87,87,45414,9082800),
])
def test_future_scenario_original_variance_proxy_and_six_arm_budget(nf,nv,cases,updates):
    a=json.loads(PREC.read_text(encoding="utf-8"))
    assert cases==nf*nv*2*3
    assert updates==cases*200
    for key in ("carrier_order_score_delta","carrier_I_event_delta"):
        q=a["co_primary"][key]
        v=dict(founder=q["raw_founder_mean_variance"],
               visitor=q["raw_visitor_mean_variance"],
               interaction=q["interaction_plus_path_noise_MS"])
        mde=assumption_mde(v,nf,nv)
        assert mde>0
        if nf==8: assert mde==pytest.approx(.4,abs=.003)
        if nf==25: assert mde<.2
        if nf==87: assert mde<.1


def test_future_plan_is_hold_not_power_repair_for_old_results():
    s=NOTE.read_text(encoding="utf-8")
    assert "HOLD new confirmatory Q2 intervention" in s
    assert "one stochastic path" in s
    assert "not registered scientific sample-size recommendations" in s
    assert "Do not delay the supported Chapter 2 primary ecological claim" in s
    assert "32 nested original Actions ZIPs" in s
    assert "3,750" in s and "45,414" in s
