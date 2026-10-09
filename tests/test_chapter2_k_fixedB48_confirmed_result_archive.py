"""Preserve the original complete independent fixed-B48 64-history verdict.

This archive test reads an immutable machine JSON; no biological simulations,
no refitting and no new seeded visitor histories run during PR CI.
"""
import hashlib
import json
from pathlib import Path


ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/"results/chapter2/k_fixedB48_independent_primary_20261009.json"
EXPECTED_SHA256="a6f3aad995b561ef4613301857a4e92e24d2d2138d2c66d59a7a28e1bd902023"


def test_original_machine_bytes_and_full_audit_receipts():
    raw=RESULT.read_bytes()
    assert hashlib.sha256(raw).hexdigest()==EXPECTED_SHA256
    d=json.loads(raw)
    assert d["status"]=="INDEPENDENT_64_HISTORIES_2048_T400_114688_FIXEDB48_FUTURES_ADMITTED"
    assert (d["n_independent_visitor_histories"],d["n_t400_sources"],d["n_future_cells"])==(64,2048,114688)
    assert d["original_predeclared_primary"]=="tau(K8,B48)-tau(K48,B48)"
    assert d["paired_bootstrap"]=={"unit":"visitor_history","draws":9999,"seed":2026100967}


def test_frozen_registered_positive_capacity_verdict_is_nonzero_but_bounded():
    d=json.loads(RESULT.read_text())
    assert d["primary_verdict"]=="supported_controlled_demographic_K_moderation_at_fixed_B48"
    c=d["contrasts"]["primary_K_at_fixed_B48"]
    assert abs(c["mean"]-0.007745713876893593)<1e-14
    assert c["bootstrap95"]==[0.002497158065469939,0.013015478808429596]
    assert c["bootstrap95"][0]>0
    assert c["mean"]>=0.005
    assert (c["positive_histories"],c["negative_histories"])==(43,21)


def test_previously_inconclusive_primary_is_preserved():
    previous=json.loads((ROOT/"results/chapter2/kb_independent_full_readout_20261009.json").read_text())
    assert previous["primary_verdict"]=="inconclusive"
    assert abs(previous["contrasts"]["primary_B_at_K8"]["mean"]-(-0.0017526045561689334))<1e-14
    older=json.loads((ROOT/"results/chapter2/orthogonal_capacity_full_readout_20261009.json").read_text())
    assert older["primary_decision"]=="inconclusive"
    assert abs(older["inference"]["contrasts"]["primary_capacity_conditional_fixed_eight"]["mean"]-0.0018484189036193578)<1e-14


def test_finite_population_scope_and_original_history_ids_not_reused():
    report=(ROOT/"docs/CHAPTER2_FIXEDB48_INDEPENDENT_K_CONFIRMATION_20261009.md").read_text()
    assert "model" in report.lower()
    assert "not a first confirmatory replication" in report
    assert "41110901–41110964" in report
    assert "inconclusive" in report
