"""Regression gates for the source-pinned original F1 matched-context audit."""
import csv
import importlib.util
import io
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "scripts/audit_chapter2_f1_paired_ecology_20261014.py"
spec = importlib.util.spec_from_file_location("f1_paired_ecology_audit", MODULE)
audit = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(audit)


def original_rows():
    return list(csv.DictReader(io.StringIO(audit.SOURCE.read_text(encoding="utf-8"))))


def test_authentic_original_source_and_complete_paired_recount():
    raw = audit.SOURCE.read_bytes()
    assert audit.git_blob_sha(raw) == "ea2c4009fc77cc59813dda0142e8da73c33a26fd"
    out = audit.audit_source(raw)
    stored = json.loads((ROOT / "data/results/chapter2_f1_paired_ecology_divergence_20261014.json").read_text(encoding="utf-8"))
    assert out == stored, "recorded machine result differs from source-pinned independent Python recount"
    assert out["domain"] == {
        "original_starts": 2304,
        "founder_blocks": 2,
        "contexts": 9,
        "paired_founder_seed_clusters": 256,
        "replicates_per_founder": 128,
    }
    assert out["all_six_class_counts"] == {
        "assurance_first": 335, "investment_first": 435,
        "near_simultaneous": 358, "assurance_only": 895,
        "investment_only": 10, "neither": 271,
    }
    assert set(out["clusters_with_identical_f1_metric_by_field"].values()) == {256}
    assert out["paired_context_outcome_divergence"]["different_six_class"] == 255
    assert out["paired_context_outcome_divergence"]["different_A_sustained_status"] == 191
    assert out["paired_context_outcome_divergence"]["different_I_sustained_status"] == 252
    assert out["paired_context_outcome_divergence"]["both_assurance_first_and_investment_first"] == 128
    assert out["paired_context_outcome_divergence"]["c0_to_c7_different_six_class"] == 240
    assert out["paired_context_outcome_divergence"]["c0_to_c7_different_A_sustained_status"] == 152
    assert out["paired_context_outcome_divergence"]["c0_to_c7_different_I_sustained_status"] == 217
    assert out["per_context"]["0"]["A_sustained"] == 256
    assert out["per_context"]["7"]["A_sustained"] == 104
    assert out["F1_mean_change_sign_per_unique_cluster"] == {
        "negative": 131, "positive": 117, "zero": 8,
    }
    assert out["n_distinct_six_class_labels_per_cluster"] == {
        "1": 1, "2": 12, "3": 52, "4": 125, "5": 63, "6": 3,
    }


def test_changed_original_source_bytes_fail_closed():
    with pytest.raises(ValueError, match="frozen original-genotype summary"):
        audit.audit_source(audit.SOURCE.read_bytes() + b"\n")


def test_missing_context_is_rejected_not_imputed():
    rows = original_rows()
    with pytest.raises(ValueError, match="2304"):
        audit.audit_rows(rows[:-1])


def test_duplicate_founder_seed_context_is_rejected():
    rows = original_rows()
    rows[1] = dict(rows[0])
    with pytest.raises(ValueError, match="duplicate"):
        audit.audit_rows(rows)


def test_outcome_relabel_without_event_change_is_rejected():
    rows = original_rows()
    rows[0]["category"] = "neither"
    with pytest.raises(ValueError, match="saved category disagrees"):
        audit.audit_rows(rows)


def test_lost_f1_access_is_rejected():
    rows = original_rows()
    rows[0]["A_F1_has_unmutated_individual_above0p05"] = "False"
    with pytest.raises(ValueError, match="mutation-unflagged"):
        audit.audit_rows(rows)
