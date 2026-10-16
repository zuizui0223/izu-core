"""Q3 original cohort source-only 320-case genotype auditor safeguards.

Fast CI uses synthetic data and immutable historical metadata; raw 389MB source
is checked only by its narrowly activated original-release GitHub Actions job.
"""
import json
import numpy as np
import pytest

from scripts.audit_chapter2_q3_original320_annual_genomes_20261016 import (
    ROOT, PRESERVATION, MATCHED, DENSITY_VERIFICATION, REGISTRATION,
    ORIGINAL_ZIP_SHA, CATEGORIES, THRESHOLDS, SCHEMA,
    event, genomic_means, context_from_task, verify,
)


def test_literature_and_genetic_q3_source_identity_locked():
    p=json.loads(PRESERVATION.read_text(encoding="utf-8"))
    r=json.loads(MATCHED.read_text(encoding="utf-8"))
    d=json.loads(DENSITY_VERIFICATION.read_text(encoding="utf-8"))
    job=json.loads(REGISTRATION.read_text(encoding="utf-8"))
    assert p["status"]=="all_preserved_members_read_back_and_hashed"
    assert p["sha256"]==ORIGINAL_ZIP_SHA
    assert p["size_bytes"]==389730774
    assert p["members"]==774
    assert p["abm_cases"]==320
    assert p["numerical_cases"]==30
    assert len(p["manifest"]["files"])==773
    assert r["status"]=="all_ten_contexts_accounted"
    assert len(r["rows"])==10
    assert len(r["abm_archive_sha256"])==320
    assert d["status"]=="all_30_archives_and_10_decisions_verified"
    assert len(d["archive_sha256"])==30
    assert job["horizon"]==200
    assert len(job["jobs"])==30
    assert set(THRESHOLDS)=={.025,.05,.1}
    assert SCHEMA.endswith("_20261016")


def test_first_crossing_is_sustained_20_not_single_noise():
    arr=np.full((201,3),.5)
    assert event(arr,.05)==dict(assurance_time=None,investment_time=None,category="neither")
    arr[5:19,2]=.6  # only 14 censuses, never certified
    assert event(arr,.05)["category"]=="neither"
    arr[20:,2]=.6
    assert event(arr,.05)==dict(assurance_time=20,investment_time=None,category="assurance_only")
    arr[28:,1]=.4
    assert event(arr,.05)==dict(assurance_time=20,investment_time=28,category="assurance_first")


def test_near_simultaneous_and_threshold_specific_loss():
    arr=np.full((201,3),.5)
    arr[50:,2]=.56
    arr[54:,1]=.44
    assert event(arr,.05)==dict(assurance_time=50,investment_time=54,category="near_simultaneous")
    assert event(arr,.1)["category"]=="neither"
    arr[:]=.5
    arr[30:,1]=.39
    assert event(arr,.1)["category"]=="investment_only"


def test_exact_native_diploid_201_census_means_and_invalid_population():
    raw=dict(
      offsets=np.arange(202,dtype=np.int64),
      alleles=np.full((201,3,2),.5,dtype=float),
      population=np.ones(201,dtype=np.int64),
      means=np.full((201,3),.5,dtype=float),
    )
    means,n,error=genomic_means(raw)
    assert means.shape==(201,3)
    assert np.all(means==.5)
    assert np.array_equal(n,raw["population"])
    assert error==0
    raw["alleles"][44,1,0]=.2
    with pytest.raises(AssertionError,match="contradict"):
        genomic_means(raw)
    raw["alleles"][44,1,0]=.5
    raw["population"][55]=0
    with pytest.raises(AssertionError,match="trajectory invalid"):
        genomic_means(raw)


def test_no_missing_binary_or_fake_source_as_valid_raw(tmp_path):
    with pytest.raises(FileNotFoundError):
        verify(tmp_path/"absent.zip")
    path=tmp_path/"fabricated.zip"
    path.write_bytes(b"not-original-genotypes")
    with pytest.raises(AssertionError,match="original 389MB source/provenance contract mismatch"):
        verify(path)


def test_original_matched_low_supply_counts_bounded_and_not_drift_claim():
    r=json.loads(MATCHED.read_text(encoding="utf-8"))
    low=[row for row in r["rows"] if ("s0.125_matched" in row["context"])]
    assert len(low)==2
    byblock={}
    for row in low:
        focus=next(x for x in row["events"] if x["threshold"]==.05)
        assert focus["density"]["category"]=="assurance_first"
        assert set(focus["abm_counts"])==set(CATEGORIES)
        assert sum(focus["abm_counts"].values())==32
        assert next(x for x in row["checkpoints"] if x["year"]==200)["living_abm_starts"]==32
        byblock[row["context"].split("_s0.125_")[0]]=focus["abm_counts"]["assurance_first"]
    assert byblock=={"causal_main":3,"causal_confirmation":2}
    source=(ROOT/"scripts/audit_chapter2_q3_original320_annual_genomes_20261016.py").read_text()
    assert "new_simulation_updates" in source
    assert "external_doi_deposit_created" in source
    assert "genomic_means" in source
