"""Unit guards for original-source archive intake, without requiring expired ZIPs in CI."""
import io
import json
from pathlib import Path
import zipfile

import pytest

from scripts.verify_chapter2_figure3_original_bridge_intake_20261015 import (
    ROOT, CONDITIONS, KINDS, PIN, digest, read_config,
    source_bytes, verify,
)


def test_exact_original_17_asset_contract_and_nonraw_ceiling():
    d=read_config()
    assert len(d["shards"])==16
    assert d["summary_artifact"]["artifact_id"]==10929715247
    assert d["source_original_run"]==36311030639
    assert d["case_total"]==24576
    assert d["independent_visitor_histories"]==128
    assert d["source_code_files_identical_across_16_shards"] is True
    assert d["full_raw_annual_trajectories_in_original_shards"] is False
    assert "runner-local" in d["original_shard_scope_string"]
    assert d["summary_artifact"]["github_outer_sha256"]==(
        "63215332a97f3140ea8cc4b7d380384023f5b25284713b3486f21ac47c3fb253"
    )
    for i,shard in enumerate(d["shards"]):
        assert shard["shard"]==i
        assert shard["expected_own_cases"]==1536
        assert len(shard["expected_history_seeds"])==8
        assert all(74001<=s<=74128 for s in shard["expected_history_seeds"])
        assert len(shard["github_outer_sha256"])==64
    assert len({seed for row in d["shards"] for seed in row["expected_history_seeds"]})==128


def test_signed_eight_panel_A_means_remain_separate_from_other_q3_evidence():
    d=read_config()
    summary=json.loads((ROOT/"data/results/model3_ch2_bridge_summary_20260927/summary.json").read_text())
    assert set(d["means"])==set(CONDITIONS)
    assert all(set(v)==set(KINDS) for v in d["means"].values())
    for condition in CONDITIONS:
        for kind in KINDS:
            assert d["means"][condition][kind]==pytest.approx(
                summary["campaigns"]["main"]["pairs"][condition][kind]["mean"],
                abs=1e-13)
            assert summary["campaigns"]["main"]["pairs"][condition][kind]["n_histories"]==128
    assert d["means"]["natural"]["individual"]<0
    assert d["means"]["richness_matched"]["individual"]>0
    assert d["means"]["richness_matched"]["density"]>0
    assert "NOT the one-locus panel B/C" in d["separate_paper_evidence"]


def test_byte_visitor_inference_unit_is_not_original_case_count():
    d=read_config()
    assert 16*8*3*8*8==d["case_total"]
    assert d["independent_visitor_histories"]==16*8
    assert d["within_history_initial_starts"]==3
    assert d["within_history_nested_demographic_repeats"]==8


def test_original_zip_readback_fails_on_missing_or_tampered_input(tmp_path):
    d=read_config()
    with pytest.raises(FileNotFoundError):
        source_bytes(source_dir=tmp_path)
    with zipfile.ZipFile(tmp_path/"broken.zip","w") as z:
        z.writestr("not-original.txt","foo")
    with pytest.raises(AssertionError,match="bundle original source entries incomplete"):
        source_bytes(bundle=tmp_path/"broken.zip")
    original_names={f"model3_ch2_bridge_original_shard{i}.zip":b"not a source ZIP" for i in range(16)}
    original_names["model3_ch2_bridge_original_summary.zip"]=b"not a summary"
    with pytest.raises(AssertionError,match="source summary original outer archive identity mismatch"):
        verify(original_names)
    assert digest(b"")=="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


def test_receipt_not_equivalent_to_complete_raw_data_or_zenodo_deposit():
    source=(ROOT/"scripts/verify_chapter2_figure3_original_bridge_intake_20261015.py").read_text()
    d=read_config()
    assert "full_annual_genetic_trajectories_admitted" in source
    assert "external_deposit_or_doi_created" in source
    assert d["no_new_biological_runs"] is True
    assert "NOT full native trajectories" in d["conclusion_scope"]
