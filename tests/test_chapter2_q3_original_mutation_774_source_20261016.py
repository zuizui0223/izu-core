"""Source-only QA for the registered 774 original-member Q3 archive.

These tests are FAST and do not download the 390 MB source. A separately
restricted GitHub Actions job runs the full original member/genome readback.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from scripts.verify_chapter2_q3_original_mutation_774_source_20261016 import (
    EXPECTED_ARCHIVE_SHA256, EXPECTED_BYTES, PRESERVATION, MATCHED,
    INDEPENDENT, event, provenance, verify,
)

ROOT=Path(__file__).resolve().parents[1]
PROTOCOL=ROOT/"docs/protocols/chapter2_q3_originalmutation_774_archive_readback_20261016.json"


def means(*, A_change=None, I_change=None):
    """Create deterministic normalized t0..200 synthetic event-class fixtures."""
    x=np.full((201,3),.5,dtype=float)
    if A_change is not None:
        x[A_change:,2]=.65
    if I_change is not None:
        x[I_change:,1]=.35
    return x


def test_frozen_public_source_contract_and_ten_original_contexts():
    p=json.loads(PROTOCOL.read_text(encoding="utf-8"))
    receipt,m,i,entries=provenance()
    assert p["status"] in ("PREPARED_NOT_ACTIVATED","ACTIVATE_SOURCE_ONLY_ONCE")
    assert p["original_full_archive_members"]==receipt["members"]==774
    assert p["original_member_manifest_records"]==len(entries)==773
    assert p["native_finite_diploid_cases"]==receipt["abm_cases"]==320
    assert p["native_density_archive_cases"]==receipt["numerical_cases"]==30
    assert p["original_contexts"]==len(m["rows"])==10
    assert p["original_independent_event_and_checkpoint_checks"]==[990,40]
    assert p["event_thresholds"]==[.025,.05,.1]
    assert p["event_sustained_censuses"]==20
    assert p["near_simultaneous_tolerance_censuses"]==5
    asset=p["source_assets"][0]
    assert asset["sha256"]==EXPECTED_ARCHIVE_SHA256==receipt["sha256"]
    assert asset["bytes"]==EXPECTED_BYTES==receipt["size_bytes"]
    assert len(m["abm_archive_sha256"])==320
    assert len(set(m["abm_archive_sha256"]))==320
    assert i["event_checks"]==990 and i["checkpoint_checks"]==40
    assert p["no_externally_assigned_doi"] is True


def test_original_rare_assurance_first_counts_are_threshold_conditional():
    m=json.loads(MATCHED.read_text(encoding="utf-8"))
    low=[r for r in m["rows"] if "s0.125_matched" in r["context"]]
    assert len(low)==2
    vals=[]
    for r in low:
        at={x["threshold"]:x for x in r["events"]}
        assert set(at)=={.025,.05,.1}
        assert at[.05]["density"]["category"]=="assurance_first"
        assert at[.05]["all_starts"]==32
        vals.append((at[.05]["abm_counts"]["assurance_first"],
                     at[.05]["abm_counts"]["assurance_only"]))
        assert next(x for x in r["checkpoints"] if x["year"]==200)["living_abm_starts"]==32
    assert sorted(vals)==[(2,7),(3,15)]
    assert "near_simultaneous" in [
        next(x for x in r["events"] if x["threshold"]==.025)["density"]["category"]
        for r in low
    ]


def test_event_windows_use_20_censuses_and_original_tie_rule():
    assert event(means(),.05)=={
        "assurance_time":None,"investment_time":None,"category":"neither"}
    assert event(means(A_change=30),.05)=={
        "assurance_time":30,"investment_time":None,"category":"assurance_only"}
    assert event(means(I_change=30),.05)=={
        "assurance_time":None,"investment_time":30,"category":"investment_only"}
    assert event(means(A_change=30,I_change=80),.05)["category"]=="assurance_first"
    assert event(means(A_change=80,I_change=30),.05)["category"]=="investment_first"
    assert event(means(A_change=30,I_change=35),.05)["category"]=="near_simultaneous"
    assert event(means(A_change=30,I_change=36),.05)["category"]=="assurance_first"
    assert event(means(A_change=185),.05)["category"]=="neither"
    with pytest.raises(AssertionError):
        event(np.zeros((200,3)),.05)


def test_raw_source_never_inferred_from_only_saved_manifest(tmp_path):
    with pytest.raises(FileNotFoundError):
        verify(tmp_path/"not_present.zip")
    corrupt=tmp_path/"fake-source.zip"
    corrupt.write_bytes(b"foo")
    with pytest.raises(AssertionError,match="original 389MB ZIP bytes differ"):
        verify(corrupt)
