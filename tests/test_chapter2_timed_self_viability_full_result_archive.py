"""Verify byte-exact, whole-cohort independent timed selfed viability result.

This suite does not run population simulations or compute new significance.
"""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/"results/chapter2/timed_self_viability_independent_readout_20261009.json"
ORIGINAL_SHA256="42d90c17cef4be1643b987428d3a6367ba09dee6594055ae2d2b693ccb190a01"


def original_result():
    content=RESULT.read_bytes()
    assert hashlib.sha256(content).hexdigest()==ORIGINAL_SHA256
    return json.loads(content)


def test_original_full_grid_and_preregistered_primary_is_inconclusive():
    d=original_result()
    assert d["status"]=="INDEPENDENT_64_HISTORIES_2048_T400_229376_TIMED_SELF_FUTURES_ADMITTED"
    assert (d["n_independent_visitor_histories"],d["n_t400_sources"],d["n_future_cells"])==(64,2048,229376)
    assert d["paired_bootstrap"]=={"unit":"visitor_history","draws":9999,"seed":2026100981}
    assert d["original_predeclared_primary"]=="[tau_late(K8)-tau_late(K48)]-[tau_early(K8)-tau_early(K48)]"
    assert d["primary_verdict"]=="inconclusive"
    p=d["contrasts"]["primary_late_minus_early_K_moderation"]
    assert abs(p["mean"]-(-0.002964903233790813))<1e-14
    assert p["bootstrap95"]==[-0.0072632190572351615,0.001317320645942908]
    assert p["bootstrap95"][0]<0<p["bootstrap95"][1]
    assert p["bootstrap95"][0]<-0.005
    assert (p["positive_histories"],p["negative_histories"])==(31,33)


def test_secondary_descriptions_cannot_replace_negative_primary():
    d=original_result()
    q=d["contrasts"]
    assert set(q)=={
        "primary_late_minus_early_K_moderation",
        "descriptive_early_K_moderation",
        "descriptive_late_K_moderation",
        "descriptive_full_K_moderation",
        "descriptive_full_minus_early_minus_late"
    }
    assert q["descriptive_early_K_moderation"]["bootstrap95"][0]>0
    assert q["descriptive_late_K_moderation"]["bootstrap95"][0]<0
    assert d["primary_verdict"]=="inconclusive"


def test_new_conclusion_does_not_alter_older_confirmations_or_inconclusives():
    positive=json.loads((ROOT/"results/chapter2/k_fixedB48_independent_primary_20261009.json").read_text())
    assert positive["primary_verdict"]=="supported_controlled_demographic_K_moderation_at_fixed_B48"
    assert abs(positive["contrasts"]["primary_K_at_fixed_B48"]["mean"]-0.007745713876893593)<1e-14
    older=json.loads((ROOT/"results/chapter2/kb_independent_full_readout_20261009.json").read_text())
    assert older["primary_verdict"]=="inconclusive"
    report=(ROOT/"docs/CHAPTER2_TIMED_SELF_VIABILITY_INDEPENDENT_RESULT_20261010.md").read_text()
    assert "INCONCLUSIVE" in report
    assert "42110901–42110964" in report
    assert "posthoc" in report.lower()
