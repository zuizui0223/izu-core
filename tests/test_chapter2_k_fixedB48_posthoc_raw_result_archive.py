"""Lock the original full-cohort read-only *exploratory* demographic-channel JSON.

No future trajectory generation, no re-fitting or new histories during CI.
"""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
FROZEN=ROOT/"results/chapter2/k_fixedB48_independent_primary_20261009.json"
POSTHOC=ROOT/"results/chapter2/k_fixedB48_posthoc_pathways_20261009.json"
SHA256="8fea4bd8c1858c445ba0eb57dfc038bac6819ed767932c596b79e4cd3ed6e542"


def test_exact_original_exploratory_machine_bytes_and_full_audit():
    raw=POSTHOC.read_bytes()
    assert hashlib.sha256(raw).hexdigest()==SHA256
    row=json.loads(raw)
    assert row["status"]=="POST_OUTCOME_EXPLORATORY_SOURCE_ADMITTED_CHANNEL_AUDIT"
    assert row["verified_raw_future_cells"]==114688
    assert row["n_independent_histories"]==64
    assert row["exploratory_bootstrap"]=={"draws":9999,"seed":2026100973}
    assert row["source_production_run_id"]==37896872795
    assert row["original_readout_run_id"]==37900150213


def test_registered_primary_not_refit_or_downgraded():
    post=json.loads(POSTHOC.read_text())
    original=json.loads(FROZEN.read_text())
    primary=original["contrasts"]["primary_K_at_fixed_B48"]
    assert original["primary_verdict"]=="supported_controlled_demographic_K_moderation_at_fixed_B48"
    assert post["immutable_registered_primary"]=={
        "status":original["primary_verdict"],
        "mean":primary["mean"],
        "bootstrap95":primary["bootstrap95"]
    }
    assert original["n_independent_visitor_histories"]==64
    assert original["n_future_cells"]==114688
    # Primary CI used distinct prospectively frozen seed from posthoc diagnostics.
    assert original["paired_bootstrap"]["seed"]==2026100967


def test_early_late_timing_and_recruitment_are_descriptive_not_mediation():
    row=json.loads(POSTHOC.read_text())
    d=row["channels"]
    early=d["extinct_by_update_20"]["K8_minus_K48_sensitivity"]
    late=d["extinct_by_update_60"]["K8_minus_K48_sensitivity"]
    selfed=d["cumulative_self_recruits"]["K8_minus_K48_sensitivity"]
    assert early["bootstrap95"][0]<0<early["bootstrap95"][1]
    assert late["mean"]<0 and late["bootstrap95"][1]<0
    assert selfed["mean"]<0 and selfed["bootstrap95"][1]<0
    initial=d["t0_self_viable"]["K8_minus_K48_sensitivity"]
    assert initial["mean"]==0 and initial["bootstrap95"]==[0,0]
    assert any("not independent mediators" in s.lower() for s in row["limits"])
    doc=(ROOT/"docs/CHAPTER2_FIXEDB48_POSTHOC_EXTINCTION_RECRUITMENT_20261009.md").read_text()
    assert "POST-OUTCOME EXPLORATORY" in doc
    assert "not" in doc.lower()
