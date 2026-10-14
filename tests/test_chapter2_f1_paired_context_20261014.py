"""Adversarial checks for the source-pinned original F1 paired-context audit."""
from __future__ import annotations

import csv
import io

import pytest

from scripts.audit_chapter2_f1_paired_context_20261014 import (
    SOURCE,
    SOURCE_GIT_BLOB,
    audit_bytes,
    git_blob_sha1,
)


def modified_source(mutator) -> bytes:
    original = SOURCE.read_bytes().decode("utf-8")
    reader = csv.DictReader(io.StringIO(original))
    fields = reader.fieldnames
    assert fields is not None
    rows = list(reader)
    mutator(rows)
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue().encode("utf-8")


def test_authentic_original_csv_and_paired_context_results():
    raw = SOURCE.read_bytes()
    assert git_blob_sha1(raw) == SOURCE_GIT_BLOB
    result = audit_bytes(raw)
    assert result["original_case_rows"] == 2304
    assert result["original_founder_by_context_cells"] == 18
    assert result["paired_founder_by_replicate_clusters"] == 256
    assert result["identical_7_field_F1_A_signatures_across_all_9_contexts"] == 256
    assert result["different_six_class_outcome_across_contexts"] == 255
    assert result["different_A_sustained_incidence_across_contexts"] == 191
    assert result["different_I_sustained_incidence_across_contexts"] == 252
    assert result["number_of_distinct_categories_within_pair"] == {
        "1": 1, "2": 12, "3": 52, "4": 125, "5": 63, "6": 3,
    }
    assert result["pairs_with_identical_six_class_category"] == ["confirmation_r115"]
    assert result["A_F1_zero_flagged_mutant_offspring_cases"] == 864
    assert result["original_six_class_counts"] == {
        "assurance_first": 335,
        "assurance_only": 895,
        "investment_first": 435,
        "investment_only": 10,
        "near_simultaneous": 358,
        "neither": 271,
    }
    assert result["by_founder"]["main"]["different_category"] == 128
    assert result["by_founder"]["confirmation"]["different_category"] == 127


def test_fail_closed_on_same_numbers_but_changed_source_bytes():
    wrong_bytes = SOURCE.read_bytes() + b"\n"
    with pytest.raises(ValueError, match="Source bytes differ"):
        audit_bytes(wrong_bytes)


def test_fail_closed_on_first_offspring_context_difference():
    def tamper(rows):
        rows[1]["A_t1_expressed_variance"] = "0.001"
    with pytest.raises(ValueError, match="First-offspring A summary varies"):
        audit_bytes(modified_source(tamper), require_pinned_blob=False)


def test_fail_closed_on_missing_original_case():
    with pytest.raises(ValueError, match="Expected 2304"):
        audit_bytes(modified_source(lambda rows: rows.pop()), require_pinned_blob=False)


def test_fail_closed_on_duplicate_registered_case():
    def duplicate(rows):
        rows[1] = dict(rows[0])
    with pytest.raises(ValueError, match="Duplicate case"):
        audit_bytes(modified_source(duplicate), require_pinned_blob=False)


def test_fail_closed_on_event_category_inconsistency():
    def tamper(rows):
        rows[0]["category"] = "neither"
    with pytest.raises(ValueError, match="Sustained-event presence disagrees"):
        audit_bytes(modified_source(tamper), require_pinned_blob=False)


def test_fail_closed_on_false_unmutated_f1_access():
    def tamper(rows):
        rows[0]["A_F1_has_unmutated_individual_above0p05"] = "False"
    with pytest.raises(ValueError, match="Unexpected first-offspring A access"):
        audit_bytes(modified_source(tamper), require_pinned_blob=False)


def test_fail_closed_on_tie_mislabeled_as_strict_order():
    def tamper(rows):
        assert rows[0]["category"] == "near_simultaneous"
        rows[0]["category"] = "investment_first"
    with pytest.raises(ValueError, match="Sustained-event ordering disagrees"):
        audit_bytes(modified_source(tamper), require_pinned_blob=False)


def test_fail_closed_on_unattainable_sustained_start_year():
    def tamper(rows):
        row = next(row for row in rows if row["category"] == "assurance_only")
        row["A_sustained_first"] = "182"
    with pytest.raises(ValueError, match="Invalid original event year"):
        audit_bytes(modified_source(tamper), require_pinned_blob=False)
