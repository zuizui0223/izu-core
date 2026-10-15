"""Q2 S29 paper bridge must match original source and preserve claim limits."""
from __future__ import annotations

from copy import deepcopy
import json

import pytest

from scripts.verify_chapter2_q2_s29_source_bridge_20261015 import (
    ROOT, PAPER, SI, SOURCES, verify, verify_f1_bridge,
)


def data():
    return {key:json.loads((ROOT/path).read_text(encoding="utf-8"))
            for key,(path,_) in SOURCES.items()}


def bridge(d,si=None,paper=None):
    return verify_f1_bridge(d["original"],d["f1"],d["sign"],d["returns"],
                            (ROOT/SI).read_text(encoding="utf-8") if si is None else si,
                            (ROOT/PAPER).read_text(encoding="utf-8") if paper is None else paper)


def test_source_pinned_original_F1_and_focal_W_complete():
    r=verify()
    assert r["status"]=="PASS_SOURCE_PINNED_S29_NO_NEW_BIOLOGY"
    assert r["historical_original_genome_sources"]==2
    assert r["hypothetical_mechanism_source_backgrounds"]==1
    assert r["original_F1_visitor_contexts"]==[0,3,4]
    assert len(r["four_signed_F1_classes"])==4
    assert r["possible_M_values"]==3
    assert r["native_focal_W_analytical_cells"]==36
    assert r["native_Model3_population_updates"]==0
    assert r["new_DOI_deposit"] is False
    assert r["not_a_persistence_or_evolutionary_order_effect"] is True


def test_reject_directional_inheritance_claim_for_symmetric_source():
    sources=data()
    sources["sign"]["contexts"][1]["m6_signed_events"]["A_up_I_up"]+=.01
    with pytest.raises(ValueError,match="equal-sign"):
        bridge(sources)


def test_reject_impossible_unchanged_A_background_or_added_biology():
    sources=data()
    sources["f1"]["original_A_heterozygosity_reset_in_each_arm"]=0
    with pytest.raises(ValueError,match="F1 original-I"):
        bridge(sources)
    sources=data()
    sources["returns"]["new_population_advance_calls"]=1
    with pytest.raises(ValueError,match="W source"):
        bridge(sources)


def test_reject_false_W_values_even_if_cached_source_claim_says_best():
    sources=data()
    sources["returns"]["native_four_corner_rows"][0][
        "static_focal_expected_returns_by_sign"]["A_up_I_down"]["parental_genome_W"]+=.12
    with pytest.raises(ValueError,match="W=F/2"):
        bridge(sources)


def test_reject_incomplete_S29_table_and_missing_limit_language():
    sources=data()
    si=(ROOT/SI).read_text(encoding="utf-8")
    with pytest.raises(ValueError,match="W table"):
        bridge(sources,si.replace("1.790356","1.790999",1))
    with pytest.raises(ValueError,match="interpretation"):
        bridge(sources,si.replace(
            "The F1 access probabilities and static W scores must not be combined",
            "F1 access directly predicts evolutionary survival"))
    with pytest.raises(ValueError,match="interpretation"):
        bridge(sources,paper=(ROOT/PAPER).read_text(encoding="utf-8").replace("(S29)","(S20)"))


def test_source_github_blob_rejection(tmp_path):
    import shutil
    # Read-only operation is exact; corrupting any source object must be rejected
    # before accepting its cached derived paper numbers.
    for key,(path,_) in SOURCES.items():
        dst=tmp_path/path
        dst.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/path,dst)
    for path in (SI,PAPER):
        dst=tmp_path/path
        dst.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/path,dst)
    raw=tmp_path/SOURCES["returns"][0]
    raw.write_bytes(raw.read_bytes()+b" ")
    with pytest.raises(ValueError,match="Git blob drift"):
        verify(tmp_path)
