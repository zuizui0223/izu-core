"""Immutable science contract for the complete independent K/B experiment."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FILE=ROOT/"results/chapter2/kb_independent_full_readout_20261009.json"
SHA256="74df9619590023ee7416035ea31068b541e08dd731b603e879a27c26ccd35ed9"


def test_byte_identical_authenticated_full_result():
    raw=FILE.read_bytes()
    assert hashlib.sha256(raw).hexdigest()==SHA256
    v=json.loads(raw)
    assert v["status"]=="INDEPENDENT_64_HISTORIES_2048_T400_229376_KB_FUTURES_ADMITTED"
    assert (v["n_independent_visitor_histories"],v["n_t400_sources"],
            v["n_future_cells"])==(64,2048,229376)
    assert v["original_predeclared_primary"]=="tau(K8,B8)-tau(K8,B48)"
    assert v["primary_verdict"]=="inconclusive"
    assert v["paired_bootstrap"]=={
        "unit":"visitor_history","draws":9999,"seed":2026100957,
    }


def test_original_primary_must_never_be_promoted():
    v=json.loads(FILE.read_text())
    p=v["contrasts"]["primary_B_at_K8"]
    assert abs(p["mean"]-(-0.0017526045561689334))<1e-15
    assert p["bootstrap95"]==[-0.00633362622725208,
                              0.0028719524357433655]
    assert (p["positive_histories"],p["negative_histories"])==(30,34)
    assert p["bootstrap95"][0]<0<p["bootstrap95"][1]
    assert not abs(p["mean"])>=0.005
    assert not (-0.005<p["bootstrap95"][0] and p["bootstrap95"][1]<0.005)


def test_secondary_positive_intervals_are_descriptive_not_confirmatory():
    v=json.loads(FILE.read_text())
    sec=v["contrasts"]
    for key in ("secondary_K_at_B8","secondary_K_at_B48",
                "secondary_B_at_K48","secondary_K_by_B"):
        assert key in sec
        assert sec[key]["bootstrap95"][0]<=sec[key]["mean"]<=sec[key]["bootstrap95"][1]
    assert sec["secondary_K_at_B48"]["mean"]>0.013
    assert sec["secondary_K_by_B"]["mean"]<0
    report=(ROOT/"docs/CHAPTER2_KB_INDEPENDENT_FULL_RESULT_20261009.md").read_text()
    assert "secondary/descriptive" in report
    assert "multiplicity" in report
    assert "inconclusive" in report
