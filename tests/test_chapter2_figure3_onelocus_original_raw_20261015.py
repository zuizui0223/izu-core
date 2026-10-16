"""Read-only original one-locus trace archive Figure3 B/C source checks."""
from pathlib import Path
import hashlib
import json
import pytest

from scripts.verify_chapter2_figure3_onelocus_original_raw_20261015 import (
    ARCHIVE, SUMMARY, VARIABILITY, EXPECTED_ARCHIVE_SHA256,
    SCHEMA, verify,
)


def test_original_native_zip_byte_integrity_and_16_plot_cells():
    """No model run: original archive with all native NPZ traces is reopened."""
    result=verify()
    assert result["status"]==SCHEMA
    assert result["original_zip_sha256"]==EXPECTED_ARCHIVE_SHA256
    assert result["original_native_trace_npz_files"]==64
    assert result["plotted_B_C_rows_recomputed"]==16
    assert result["original_1001_census_trace_values_verified"] is True
    assert result["genetic_pedigree_complete_for_all_censuses"] is False
    assert result["fixed_original_visitor_histories"]==2
    assert result["paired_demographic_repeat_seeds"]==list(range(6101,6109))
    assert result["original_archive_distinct_from_128history_bridge"] is True
    assert result["original_archive_distinct_from_atom_3of32_and_2of32"] is True
    assert result["any_new_biological_updates"] is False
    assert result["external_doi_or_upload"] is False
    assert len(result["rows"])==16
    assert all(len(r["original_recalculated_descriptive_bootstrap95"])==2
               for r in result["rows"])


def test_fail_on_missing_or_changed_original_archive(tmp_path):
    with pytest.raises(FileNotFoundError):
        verify(archive=tmp_path/"original_does_not_exist.zip")
    altered=tmp_path/"original_mutated.zip"
    original=ARCHIVE.read_bytes()
    altered.write_bytes(original[:-1]+bytes([original[-1]^1]))
    with pytest.raises(AssertionError,match="original full one-locus raw ZIP hash mismatch"):
        verify(archive=altered)


def test_source_file_matches_historical_pinned_digest_and_separate_cohorts():
    import json
    assert ARCHIVE.is_file() and ARCHIVE.stat().st_size>0
    j=json.loads(SUMMARY.read_text(encoding="utf-8"))
    s=json.loads(VARIABILITY.read_text(encoding="utf-8"))
    assert j["archive_sha256"]==s["archive_sha256"]==EXPECTED_ARCHIVE_SHA256
    assert s["bootstrap"]["unit"]=="demographic repeat"
    assert s["raw_cases"]==64
    assert len(s["raw_hashes"])==64
    assert s["max_difference_from_existing_means"]==0


@pytest.mark.parametrize("invalid", [float("nan"), float("inf"), -float("inf")])
@pytest.mark.parametrize("source", ["variability", "summary"])
def test_reject_nonfinite_stored_means(tmp_path, invalid, source):
    """Valid original bytes must not authenticate a corrupt displayed mean."""
    summary=json.loads(SUMMARY.read_text(encoding="utf-8"))
    variability=json.loads(VARIABILITY.read_text(encoding="utf-8"))
    if source=="variability":
        variability["rows"][0]["mean"]=invalid
    else:
        row=next(row for row in summary["abm"]
                 if row["common_environment_periods"]==800)
        row["mean_allele_counts"][0]=invalid
    summary_path=tmp_path/"summary.json"
    variability_path=tmp_path/"variability.json"
    summary_path.write_text(json.dumps(summary), encoding="utf-8")
    variability_path.write_text(json.dumps(variability), encoding="utf-8")
    with pytest.raises(AssertionError, match="means/CI differ from source"):
        verify(summary=summary_path, variability=variability_path)
