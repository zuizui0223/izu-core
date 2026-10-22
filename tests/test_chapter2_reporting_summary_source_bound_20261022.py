"""Source-based reporting-summary tests; zero biology, DOI or inference generation."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil

import pytest

from scripts.verify_chapter2_computational_reporting_20261022 import (
    ROOT, SOURCES, SUMMARY, verify, main,
)


def test_current_archived_crosswalk_and_limits():
    d = verify(ROOT)
    assert d["status"] == "SOURCE_BOUND_REPORTING_SUMMARY_PASS_NO_EXTERNAL_DEPOSIT_CLAIM"
    assert d["n_source_files_checked"] == len(SOURCES) == 13
    assert d["reported_counts"] == {
        "fresh_main": 1024,
        "fresh_technical_null": 64,
        "pollen_baseline": 384,
        "matched_repeat": 12288,
        "crossed_160x160": 25600,
        "original_assets": 97,
        "bounded_transfer_futures": 10240,
        "secondary_colonization_nested": 240,
    }
    assert d["registered_G_pp"] == pytest.approx(8.328125)
    assert d["registered_S_pp"] == pytest.approx(92.70703125)
    assert d["no_new_biological_simulation"]
    assert not d["cohorts_pooled_as_independent_islands"]
    assert not d["doi_external_deposit_verified"]
    assert not d["journal_reporting_summary_author_approved"]
    assert not d["external_rights_confirmed"]
    assert set(d["source_sha256"]) == set(SOURCES.values())


def mirror(tmp_path):
    for p in (*SOURCES.values(), SUMMARY):
        src = ROOT / p
        dest = tmp_path / p
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
    return tmp_path


def test_reject_changed_registered_primary_before_reporting(tmp_path):
    p = mirror(tmp_path) / SOURCES["registered_result"]
    d = json.loads(p.read_text())
    d["primary"]["endpoints"][0]["estimate"] = 0.2
    p.write_text(json.dumps(d))
    with pytest.raises(ValueError, match="registered G/S estimates"):
        verify(tmp_path)


def test_reject_fake_crossed_unit_and_pollen_allocation(tmp_path):
    root = mirror(tmp_path)
    p = root / SOURCES["registered_result"]
    original = p.read_bytes()
    d = json.loads(original)
    d["independent_axes"] = [25600]
    p.write_text(json.dumps(d))
    with pytest.raises(ValueError, match="registered crossed design"):
        verify(root)
    p.write_bytes(original)
    q = root / SOURCES["baseline_results"]
    j = json.loads(q.read_text())
    j["raw_rows"] = 383
    q.write_text(json.dumps(j))
    with pytest.raises(ValueError, match="baseline pollen factorial allocation"):
        verify(root)


def test_reject_false_deposit_and_missing_conditions(tmp_path):
    root = mirror(tmp_path)
    p = root / SUMMARY
    original = p.read_text(encoding="utf-8")
    p.write_text(original.replace("520/521", "521/521"), encoding="utf-8")
    with pytest.raises(ValueError, match="520/521"):
        verify(root)
    p.write_text(original.replace("not a new biological experiment", "novel trial"),
                 encoding="utf-8")
    with pytest.raises(ValueError, match="not a new biological experiment"):
        verify(root)


def test_report_output_never_overwritten(tmp_path, monkeypatch):
    out = tmp_path / "REPORTING.json"
    monkeypatch.setattr("sys.argv", ["report", "--root", str(ROOT), "--out", str(out)])
    main()
    d = json.loads(out.read_text())
    assert d["n_source_files_checked"] == 13
    with pytest.raises(SystemExit, match="2"):
        main()
