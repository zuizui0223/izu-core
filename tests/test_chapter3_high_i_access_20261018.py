"""Source-only Q3 HIGH-I genetic support tests; no biological simulator imports."""
from __future__ import annotations

import json
import shutil

import numpy as np
import pytest

from scripts.audit_chapter3_high_i_access_20261018 import (
    ROOT, audit, first_loss, sha,
)


def test_first_high_loss_can_precede_single_allele_fixation():
    # High 5/8 disappears; 3/8 and 4/8 persist. Allelic variance remains.
    maxima=np.array([5/8,5/8,4/8,4/8],dtype=float)
    assert first_loss(maxima,0.53125)==2
    assert first_loss(maxima,0.45) is None


def test_transient_temporary_no_change_is_not_a_loss():
    assert first_loss(np.array([5/8,5/8,np.nan,np.nan]),0.53125) is None


def test_first_loss_rejects_resurrection_and_allele_gains():
    with pytest.raises(ValueError,match="occupancy"):
        first_loss(np.array([5/8,np.nan,4/8]),0.53125)
    with pytest.raises(ValueError,match="maximum illegally"):
        first_loss(np.array([4/8,5/8,5/8]),0.53125)


def test_first_loss_strict_target_exclusion():
    # Equal-to-target allele remains structurally available.
    assert first_loss(np.array([.625,.5,.5]),.5) is None


def test_archived_2304_q3_high_vs_low_source_reconciliation(tmp_path):
    result=audit(ROOT, tmp_path/"ch3-audit")
    all_=result["all"]
    assert result["status"]=="SOURCE_ONLY_RETROSPECTIVE_HIGH_I_STRUCTURAL_ACCESS"
    assert all_["cases"]==2304
    assert all_["overlap_with_old_low_I_loss"]+all_[
        "old_low_I_loss_without_high_loss"]==1238
    assert all_["first_high_loss"]+all_["still_high_reachable_at_end"]==2304
    assert (all_["overlap_with_old_low_I_loss"]+
            all_["high_loss_without_old_low_I_loss"]+
            all_["old_low_I_loss_without_high_loss"]+
            all_["no_high_or_low_loss"])==2304
    assert sum(r["cases"] for r in result["by_cell"])==2304
    assert all(r["cases"]==128 for r in result["by_cell"])
    assert sum(r["cases"] for r in result["by_founder"].values())==2304
    assert result["new_biological_histories"]==0
    assert result["new_restoration_futures"]==0
    assert result["preregistered_confirmation"] is False
    saved=json.loads((tmp_path/"ch3-audit/HIGH_I_READOUT.json").read_text())
    assert saved["all"]==all_
    assert len((tmp_path/"ch3-audit/HIGH_I_CASES.csv").read_text().splitlines())==2305


def test_source_digest_guard_refuses_modified_raw_alleles(tmp_path):
    raw=ROOT/"data/results/directional_access_20261013"
    dest=tmp_path/"data/results/directional_access_20261013"
    dest.mkdir(parents=True)
    for name in ("READOUT.json","ALL_CASES.csv","ALL_CENSUS_SUPPORT.npz"):
        shutil.copyfile(raw/name,dest/name)
    with (dest/"ALL_CASES.csv").open("a") as f:
        f.write("unauthorized historical row\n")
    with pytest.raises(ValueError,match="hash mismatch"):
        audit(tmp_path)
