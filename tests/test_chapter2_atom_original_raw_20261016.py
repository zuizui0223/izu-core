"""Fast policy/equation guards: NO 389MB download in ordinary CI."""
from pathlib import Path
import json

import numpy as np
import pytest

from scripts.verify_chapter2_atom_original_raw_20261016 import (
    CATEGORIES, DATA, ORIGINAL_ZIP_SHA256, ORIGINAL_ZIP_SIZE,
    THRESHOLDS, classify, source_files, verify,
)


def test_original_320_plus_30_source_archive_record_pinned():
    preserve,table,registration,independent=source_files()
    assert ORIGINAL_ZIP_SIZE==389730774
    assert ORIGINAL_ZIP_SHA256==preserve["sha256"]
    assert preserve["members"]==774
    assert len(preserve["manifest"]["files"])==773
    assert preserve["manifest"]["run_id"]==38120835221
    assert preserve["numerical_cases"]==30
    assert preserve["abm_cases"]==len(table["abm_archive_sha256"])==320
    assert len(table["rows"])==10
    assert independent["event_checks"]==990
    assert independent["checkpoint_checks"]==40


def test_independent_event_observer_preserves_real_onset_and_tie_definition():
    data=np.tile([.5,.5,.5],(201,1))
    assert classify(data,.05)=={"assurance_time":None,"investment_time":None,"category":"neither"}
    data[31:,2]=.59
    data[43:,1]=.43
    assert classify(data,.05)=={"assurance_time":31,"investment_time":43,
                                 "category":"assurance_first"}
    data[34:,1]=.43
    assert classify(data,.05)["category"]=="near_simultaneous"
    data[:,2]=.5
    assert classify(data,.05)["category"]=="investment_only"
    data[:,1]=.5
    assert classify(data,.05)["category"]=="neither"
    data[31:,2]=.59
    assert classify(data,.05)["category"]=="assurance_only"
    assert THRESHOLDS==(.025,.05,.10)
    assert set(CATEGORIES)=={"assurance_first","assurance_only","investment_first",
                             "investment_only","near_simultaneous","neither"}


def test_reject_modified_or_missing_source_without_resimulating(tmp_path):
    with pytest.raises(FileNotFoundError):
        verify(tmp_path/"missing-complete-original.zip")
    damaged=tmp_path/"wrong-origin.zip"
    damaged.write_bytes(b"this is not the 389 MB original scientific source")
    with pytest.raises(AssertionError,match="whole-file size/SHA mismatch"):
        verify(damaged)


def test_original_saved_comparison_retains_two_distinct_low_supply_contexts():
    matched=json.loads((DATA/"matched_comparison.json").read_text())
    focal=[]
    for r in matched["rows"]:
        ev=next(e for e in r["events"] if e["threshold"]==.05)
        if "s0.125_matched" in r["context"]:
            focal.append((r["context"],ev["density"]["category"],
                          ev["abm_counts"]["assurance_first"],
                          ev["abm_counts"]["assurance_only"],
                          next(c for c in r["checkpoints"] if c["year"]==200)["living_abm_starts"]))
    assert len(focal)==2
    assert sorted(x[2] for x in focal)==[2,3]
    assert sorted(x[3] for x in focal)==[7,15]
    assert all(x[1]=="assurance_first" and x[4]==32 for x in focal)
