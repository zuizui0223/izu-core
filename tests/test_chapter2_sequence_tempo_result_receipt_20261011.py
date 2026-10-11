"""Protect admitted tempo evidence, its units, and its limited audit scope.

These checks detect substituted/partial artifacts and changed provenance. They
read saved results only; CI must not launch another biological cohort.
"""
from datetime import datetime
import gzip
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "data/results/chapter2_sequence_abrupt_gradual_functional_loss_receipt_20261011.json"
DESIGN = ROOT / "data/design/chapter2_sequence_abrupt_gradual_functional_loss_20261011.json"
READOUT_SHA = "a1b5e84c61e9cc242af8a71bafe57bf852e233445e3e4e7476333aca252009af"
AUDIT_SHA = "ece61c3ce978c58c359ed618ffa31bf4dfe20e7f7c530f55b613d42625e0b600"
DESIGN_SHA = "207a3a0ad3decf096c65f296bebeee69e7f80d5b644abb2318105e50474774d0"
SOURCE_SHA = "dba65f11a4ee7295ae32b623ea1103cc8a25c1b5"
CATEGORIES = {"A_first", "I_first", "near_simultaneous", "A_only", "I_only", "neither"}
OUTCOMES = CATEGORIES | {key + "_by100" for key in CATEGORIES} | {
    "A_crossed_by100", "I_crossed_by100", "persistence100", "persistence400"
}


def _receipt():
    assert RECEIPT.is_file(), "Complete result admission receipt is missing"
    return json.loads(RECEIPT.read_text())


def _read_compressed(entry):
    path = ROOT / entry["path"]
    assert path.is_file(), path
    payload = path.read_bytes()
    assert len(payload) == entry["gzip_size_bytes"]
    assert sha256(payload).hexdigest() == entry["gzip_sha256"]
    unpacked = gzip.decompress(payload)
    assert len(unpacked) == entry["decompressed_size_bytes"]
    assert sha256(unpacked).hexdigest() == entry["decompressed_sha256"]
    return json.loads(unpacked)


def test_admitted_readout_and_audit_are_exact_original_bytes():
    receipt = _receipt()
    assert receipt["status"] == "COMPLETE_MODEL_SPECIFIC_DESCRIPTIVE_RESULT_ADMITTED"
    assert receipt["complete_readout"]["decompressed_sha256"] == READOUT_SHA
    assert receipt["independent_endpoint_audit"]["decompressed_sha256"] == AUDIT_SHA
    readout = _read_compressed(receipt["complete_readout"])
    audit = _read_compressed(receipt["independent_endpoint_audit"])
    design_bytes = DESIGN.read_bytes()
    assert sha256(design_bytes).hexdigest() == DESIGN_SHA
    assert receipt["frozen_design_sha256"] == DESIGN_SHA
    assert json.loads(design_bytes)["execution_policy"]["current_result"] == "NONE"
    assert receipt["historical_registration_current_result_field"] == "NONE"
    assert receipt["historical_registration_preserved_byte_identical"] is True
    assert readout["design_sha256"] == audit["frozen_design_sha256"] == DESIGN_SHA
    assert audit["official_readout_sha256"] == READOUT_SHA
    for key in ("verified_source_identity_sha256", "verified_source_file_sha256",
                "execution_runtime_identity", "founder_identity"):
        assert readout[key] == audit[key]


def test_complete_cohort_counts_are_case_times_not_independent_profiles():
    receipt = _receipt()
    readout = _read_compressed(receipt["complete_readout"])
    audit = _read_compressed(receipt["independent_endpoint_audit"])
    assert readout["total_verified_trajectory_cases"] == len(audit["case_results"]) == 1024
    assert readout["n_independent_synthetic_visitor_profiles"] == 16
    assert readout["n_nested_demographic_replicates_per_profile"] == 4
    assert readout["n_natural_plant_islands"] == 0
    assert len({row["case_key"] for row in audit["case_results"]}) == 1024
    assert all(row["genotype_censuses_checked"] == 401 for row in audit["case_results"])
    assert sum(row["genotype_censuses_checked"] for row in audit["case_results"]) == 410624
    expected = set(product(range(48271001, 48271017), range(49271001, 49271005),
                           ("delayed", "prior"), (0, .5), (0, .01), ("abrupt", "gradual")))
    assert {tuple(row["case"]) for row in audit["case_results"]} == expected
    assert receipt["sampling"]["censuses_including_founders"] == 410624
    assert receipt["sampling"]["synthetic_profiles"] == 16
    manifests = receipt["execution"]["completed_shard_manifest_sha256"]
    assert len(manifests) == 16
    assert manifests == audit["completed_shard_manifest_sha256"]


def test_all_128_outcomes_match_independent_counts_and_intervals():
    receipt = _receipt()
    readout = _read_compressed(receipt["complete_readout"])
    audit = _read_compressed(receipt["independent_endpoint_audit"])
    def key(row):
        return row["timing"], row["direct_assurance_cost"], row["mutation_rate"]
    independent = {key(row): row for row in audit["setting_results"]}
    assert len(independent) == len(readout["results"]) == 8
    for row in readout["results"]:
        assert set(row["outcomes"]) == OUTCOMES
        audited = independent[key(row)]["independently_verified_outcomes"]
        assert set(audited) == OUTCOMES
        for name, outcome in row["outcomes"].items():
            other = audited[name]
            for field in ("P_abrupt", "P_gradual", "abrupt_minus_gradual", "horizon_updates"):
                assert outcome[field] == pytest.approx(other[field], abs=1e-12, rel=0)
            assert outcome["descriptive_history_profile_bootstrap95"] == pytest.approx(
                other["descriptive_profile_bootstrap95"], abs=1e-12, rel=0)
            for schedule in ("abrupt", "gradual"):
                assert outcome["P_" + schedule] == sum(other[schedule + "_events_per_four_repeats"]) / 64
        for suffix in ("", "_by100"):
            for schedule in ("abrupt", "gradual"):
                assert sum(row["outcomes"][c + suffix]["P_" + schedule] for c in CATEGORIES) == 1
    assert audit["bootstrap"]["draws"] == readout["bootstrap"]["draws"] == 9999
    assert audit["bootstrap"]["seed"] == readout["bootstrap"]["seed"] == 48272026


def test_secondary_support_is_retained_without_claiming_independent_recomputation():
    receipt = _receipt()
    readout = _read_compressed(receipt["complete_readout"])
    assert receipt["verification_scope"]["independently_recomputed_setting_outcomes"] == 128
    assert receipt["verification_scope"]["independently_recomputed_secondary_fields"] == 0
    assert receipt["verification_scope"]["official_secondary_fields_per_setting"] == 156
    assert receipt["verification_scope"]["independent_evolutionary_replay"] is False
    for row in readout["results"]:
        assert len(row["secondary_endpoints"]) == 156
        for endpoint in row["secondary_endpoints"].values():
            assert len(endpoint["profile_support"]) == 16
            assert 0 <= endpoint["eligible_paired_trajectories"] <= 64
            assert 0 <= endpoint["eligible_paired_profiles"] <= 16
            if endpoint["eligible_paired_trajectories"] == 0:
                assert endpoint["abrupt_minus_gradual"] is None
                assert endpoint["descriptive_history_profile_bootstrap95"] is None
    conclusions = receipt["scientific_conclusions"]
    assert conclusions["persistence_interpretation"] == (
        "saturated_no_identified_benefit_or_harm_no_equivalence_claim"
    )
    assert conclusions["natural_island_generalization"] is False
    assert receipt["sampling"]["natural_islands"] == 0


def test_local_execution_follows_main_gates_and_archive_is_private_verified():
    receipt = _receipt()
    execution = receipt["execution"]
    assert execution["executor_kind"] == "local_committed_main"
    assert receipt["execution_source_commit"] == SOURCE_SHA
    assert receipt["cohort_github_actions_run_id"] is None
    started = datetime.fromisoformat(execution["started_at_utc"])
    checks = receipt["source_gate_evidence"]["required_checks"]
    for check in checks:
        assert check["head_sha"] == SOURCE_SHA
        assert check["status"] == "completed" and check["conclusion"] == "success"
        assert datetime.fromisoformat(check["completed_at"].replace("Z", "+00:00")) < started
    assert {check["name"] for check in checks} == {
        "tests (3.10)", "tests (3.11)", "tests (3.12)",
        "scientific-gate", "confirmed-process-review-package"
    }
    archive = receipt["raw_archive"]
    assert archive["sha256"] == "034e735d244228c1f4974897a76d16acef10767a81d5dd82f5f5204f48cf0738"
    assert archive["size_bytes"] == 268940123
    assert archive["member_count_including_inventory"] == 2099
    assert archive["original_case_json_count"] == archive["original_case_receipt_count"] == 1024
    assert archive["original_shard_manifest_count"] == 16
    retrieval = archive["storage_retrieval_verification"]
    assert retrieval["retrieved_sha256"] == archive["sha256"]
    assert retrieval["retrieved_size_bytes"] == archive["size_bytes"]
    assert retrieval["retrieved_to_separate_path"] is True
    assert archive["public_scientific_deposit"] is False and archive["doi"] is None


def test_result_figure_table_and_reproduction_scripts_are_hash_linked():
    receipt = _receipt()
    assert len(receipt["figures"]) == 2
    assert len(receipt["reproduction_artifacts"]) == 4
    review = receipt["scientific_interpretation_review"]
    artifacts = [
        *receipt["figures"],
        *receipt["reproduction_artifacts"],
        receipt["original_execution_receipt"],
        receipt["fresh_verification"],
        {"path": review["path"], "size_bytes": review["size_bytes"],
         "sha256": review["report_sha256"]},
    ]
    assert len({artifact["path"] for artifact in artifacts}) == 9
    assert receipt["original_execution_receipt"]["sha256"] == receipt["execution_receipt_sha256"]
    for artifact in artifacts:
        raw = (ROOT / artifact["path"]).read_bytes()
        assert len(raw) == artifact["size_bytes"]
        assert sha256(raw).hexdigest() == artifact["sha256"]
