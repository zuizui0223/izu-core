"""Static upper-envelope resource accounting, no biological trajectories."""
from scripts.audit_chapter2_Q2_archival_resource_envelope_20261014 import (
    K, YEARS, STATE_FIELD_PAYLOAD_BYTES_PER_INDIVIDUAL, archive_envelope
)


def test_source_cluster_comparisons_at_equal_hypothetical_compute():
    d=archive_envelope()
    assert d["status"]=="PRE_BIOLOGY_RESOURCE_ACCOUNTING_NO_EXECUTION"
    assert d["new_biological_histories"]==0
    assert d["archive_files_uploaded"]==0
    assert d["real_disk_allocations_made"] is False
    assert d["capacity_upper_envelope_only"] is True
    assert K==48 and YEARS==200
    assert len(d["equal_case_budget_rows"])==5
    for x in d["equal_case_budget_rows"]:
        assert x["biological_cases_if_authorized"]==1536
        assert x["total_update_calls_if_authorized"]==307200
        assert x["complete_201_annual_snapshots"]==308736
        assert x["possible_individual_snapshot_records_at_capacity"]==14819328
        assert x["source_history_pairs"]==256


def test_original_native_stored_field_bytes_and_parent_matrix_footprint():
    result=archive_envelope()
    fields=result["state_field_payload_bytes_per_individual"]
    assert fields == {
        "alleles_N_3_2_float64":48,
        "allele_origin_N_3_2_int64":48,
        "mutation_flags_N_3_2_bool":6,
        "ids_N_int64":8,
        "birth_years_N_int64":8,
    }
    assert sum(fields.values())==118
    for x in result["equal_case_budget_rows"]:
        assert x["raw_state_five_field_payload_bytes_at_max_census"]==1748680704
        assert x["raw_two_full_N_by_N_reproductive_matrices_bytes_at_max_census"]==11324620800
        assert x["raw_eight_aggregated_return_totals_bytes"]==19660800
        assert abs(x["raw_state_five_field_payload_GiB_at_max_census"]-
                   1.6285858154296875)<1e-12
        assert abs(x["raw_two_full_N_by_N_reproductive_matrices_GiB_at_max_census"]-
                   10.546875)<1e-12


def test_resource_envelope_does_not_approve_dropping_full_genotypes():
    r=archive_envelope()
    s=" ".join(r["storage_governance"])
    assert "Never discard the raw per-census diploid genomes" in s
    assert "before launch" in s
    assert "unapproved" in s
    assert "raw-genome" in " ".join(r["items_excluded_from_byte_tallies"]) or len(
        r["items_excluded_from_byte_tallies"])>=4
