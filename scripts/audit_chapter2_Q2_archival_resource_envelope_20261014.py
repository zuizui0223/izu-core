"""No-execution Chapter 2 Q2 raw-genome archive envelope.

Pure integer accounting for the original frozen Model3 PlantState/Ledger
array shapes, assuming *maximum occupied census* K=48 at all 201 snapshots.
No births, histories, source generation, or external storage actions occur.
This is not a storage reservation, approval or run time prediction.
"""
from __future__ import annotations

import json
from pathlib import Path

from scripts.audit_chapter2_Q2_cluster_precision_review_20261014 import (
    POSSIBLE_ALLOCATIONS, OLD_CONTEXTS, ARMS, read_review_design,
)

K=48
YEARS=200
SNAPSHOTS=YEARS+1
FLOAT64=8
INT64=8
BOOL=1
GIB=1024**3

STATE_FIELD_PAYLOAD_BYTES_PER_INDIVIDUAL={
    "alleles_N_3_2_float64":3*2*FLOAT64,
    "allele_origin_N_3_2_int64":3*2*INT64,
    "mutation_flags_N_3_2_bool":3*2*BOOL,
    "ids_N_int64":INT64,
    "birth_years_N_int64":INT64,
}
PARENTAL_FULL_MATRIX_FIELDS=("outcross_N_N_float64","delivered_N_N_float64")


def archive_envelope()->dict:
    design=read_review_design()
    if (design["biological_simulations_executed"]!=0 or
            len(design["candidate_equal_compute_allocations"])!=len(POSSIBLE_ALLOCATIONS)):
        raise ValueError("Unapproved future archive budget not admitted")
    options=[]
    for sources,histories in POSSIBLE_ALLOCATIONS:
        paths=sources*histories*len(ARMS)*len(OLD_CONTEXTS)
        source_history_pairs=sources*histories
        snapshots=paths*SNAPSHOTS
        updates=paths*YEARS
        possible_individual_snapshot_records=snapshots*K
        max_state_bytes=sum(STATE_FIELD_PAYLOAD_BYTES_PER_INDIVIDUAL.values())*possible_individual_snapshot_records
        two_full_ledger_matrices_bytes=(
            updates*len(PARENTAL_FULL_MATRIX_FIELDS)*K*K*FLOAT64
        )
        compact_8_return_sums_bytes=updates*8*FLOAT64
        options.append({
            "independent_hypothetical_source_pools":sources,
            "future_histories_per_pool":histories,
            "biological_cases_if_authorized":paths,
            "total_update_calls_if_authorized":updates,
            "source_history_pairs":source_history_pairs,
            "complete_201_annual_snapshots":snapshots,
            "possible_individual_snapshot_records_at_capacity":possible_individual_snapshot_records,
            "raw_state_five_field_payload_bytes_at_max_census":max_state_bytes,
            "raw_state_five_field_payload_GiB_at_max_census":max_state_bytes/GIB,
            "raw_two_full_N_by_N_reproductive_matrices_bytes_at_max_census":
                two_full_ledger_matrices_bytes,
            "raw_two_full_N_by_N_reproductive_matrices_GiB_at_max_census":
                two_full_ledger_matrices_bytes/GIB,
            "raw_eight_aggregated_return_totals_bytes":compact_8_return_sums_bytes,
            "raw_eight_aggregated_return_totals_GiB":compact_8_return_sums_bytes/GIB,
            "illustrative_raw_state_plus_two_full_matrix_payload_GiB":
                (max_state_bytes+two_full_ledger_matrices_bytes)/GIB,
        })
    if (len({x["biological_cases_if_authorized"] for x in options})!=1 or
            len({x["raw_state_five_field_payload_bytes_at_max_census"] for x in options})!=1 or
            len({x["raw_two_full_N_by_N_reproductive_matrices_bytes_at_max_census"] for x in options})!=1):
        raise AssertionError("Illustrative same-path-count envelope changed across allocations")
    return {
        "schema":"chapter2_Q2_original_model3_raw_genotype_archive_estimate_review_only_v1",
        "status":"PRE_BIOLOGY_RESOURCE_ACCOUNTING_NO_EXECUTION",
        "original_model3_capacity":K,
        "original_model3_future_updates":YEARS,
        "original_model3_saved_annual_snapshots":SNAPSHOTS,
        "source_cluster_budget_is_not_stochastic_history_count":True,
        "new_biological_histories":0,
        "archive_files_uploaded":0,
        "real_disk_allocations_made":False,
        "capacity_upper_envelope_only":True,
        "state_field_payload_bytes_per_individual":STATE_FIELD_PAYLOAD_BYTES_PER_INDIVIDUAL,
        "illustrative_full_reproductive_matrix_field_names":
            list(PARENTAL_FULL_MATRIX_FIELDS),
        "items_excluded_from_byte_tallies":[
            "Model3 raw genome ZIP/NPZ overhead, compression variance and file headers",
            "Raw parentage, visitor dynamics, history streams, full input genomic source manifests, per-year other ledger vectors",
            "Independent replay copies, validation manifests, hashes, numerical runtime and external archival DOI",
            "Under-capacity histories use fewer individual records; no capacity occupancy prediction was made",
            "Wall-clock runtime and storage billing not measured",
        ],
        "storage_governance":[
            "Never discard the raw per-census diploid genomes or origin and mutation flags merely to save space",
            "Whether to archive full per-step reproduction matrices or independently recreate them from every saved state and original Model3 source is a separate upfront evidence/replay decision",
            "If only eight return totals are archived, the full matrices need cryptographic/replay verification and this choice must be explicitly reviewed before launch",
            "All source/future history production and external storage remain unapproved",
        ],
        "equal_case_budget_rows":options,
    }


if __name__=="__main__":
    print(json.dumps(archive_envelope(),indent=2,sort_keys=True))
