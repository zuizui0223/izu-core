"""Admitted 1,536-source archive threshold sensitivity intake: arithmetic only."""
from pathlib import Path
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "data/results/genetic_access_pilot_20261014/ARCHIVE_THRESHOLD_SENSITIVITY_INTAKE_20261014.json"
PAIRED = ROOT / "data/results/genetic_access_pilot_20261014/PAIRED_CLOCK_RETROSPECTIVE_20261014.json"
CATS = (
    "assurance_first", "investment_first", "near_simultaneous",
    "assurance_only", "investment_only", "neither",
)
SIX = ("main_c0","main_c3","main_c4","confirmation_c0","confirmation_c3","confirmation_c4")


def test_frozen_threshold_data_has_qualified_provenance():
    d = json.loads(FILE.read_text(encoding="utf-8"))
    assert d["schema"] == "chapter2_q2_archive_threshold_scientific_intake_v1"
    assert d["status"].endswith("NOT_NEW_BIOLOGY")
    origin = d["origin"]
    assert (origin["raw_zip_count"],origin["archived_pilot_histories"],
            origin["matched_width_pairs"], origin["independent_original_founder_backgrounds"]) == (6,1536,768,2)
    assert origin["run_id"] == 38573129057
    assert origin["source_job_id"] == 115883381001
    assert origin["artifact_id"] == 11897604659
    assert len(origin["source_artifact_zip_sha256"]) == 64
    assert origin["source_artifact_zip_sha256"] == "a7528e93145990ab711e6e13166d42c8824ecf65ce1d7a5420dbb46fa6c2bfaa"
    assert origin["full_readout_json_sha256"] == "3cfb4bbb32016bb170a2797c81ea97b748c23d129c95abe3da2e98b8d45f4685"
    assert d["classes"] == list(CATS)
    assert d["contexts"] == list(SIX)
    assert d["posthoc_original_0p05_is_only_primary"] is True


def test_threshold_6class_algebra_and_original_0p05_agreement():
    d = json.loads(FILE.read_text(encoding="utf-8"))
    s = d["thresholds"]
    assert set(s) == {"0.025","0.05","0.075","0.1"}
    for t, record in s.items():
        low, high = record["source_768_case_classes_L"], record["source_768_case_classes_H"]
        assert set(low) == set(CATS) == set(high)
        assert sum(low.values()) == sum(high.values()) == 768
        assert all(type(count) is int and count >= 0 for count in list(low.values())+list(high.values()))
        dlo = (low["assurance_first"]-low["investment_first"])/768
        dhi = (high["assurance_first"]-high["investment_first"])/768
        assert math.isclose(dlo,record["D_L"],abs_tol=1e-12)
        assert math.isclose(dhi,record["D_H"],abs_tol=1e-12)
        assert math.isclose(dhi-dlo,record["D_H_minus_L"],abs_tol=1e-12)
        assert math.isclose(sum(record["within_two_founders_six_ecologies_D_change"].values())/6,
                            record["D_H_minus_L"],abs_tol=1e-12)
        assert set(record["within_two_founders_six_ecologies_D_change"]) == set(SIX)
        assert all(0 <= z <= 768 for z in record["detected_A"].values())
        assert all(0 <= z <= 768 for z in record["detected_I"].values())
        assert math.isclose(
            (low["assurance_first"]+low["investment_first"]+low["near_simultaneous"]+low["assurance_only"])/768,
            record["detected_A"]["L"]/768,abs_tol=1e-12)
        assert math.isclose(
            (high["assurance_first"]+high["investment_first"]+high["near_simultaneous"]+high["assurance_only"])/768,
            record["detected_A"]["H"]/768,abs_tol=1e-12)
        for side, counts in (("L",low),("H",high)):
            i_detected = (counts["assurance_first"]+counts["investment_first"]
                          +counts["near_simultaneous"]+counts["investment_only"])
            assert i_detected == record["detected_I"][side]
    p = json.loads(PAIRED.read_text(encoding="utf-8"))
    main = s["0.05"]
    assert main["source_768_case_classes_L"] == p["counts_all_starts"]["L"]
    assert main["source_768_case_classes_H"] == p["counts_all_starts"]["H"]
    assert math.isclose(main["D_H_minus_L"],p["D_A_first_minus_I_first"]["high_minus_low"],abs_tol=1e-12)
    assert math.isclose(main["all_start_A_capped_time_H_minus_L"],
                        p["all_start_capped_first_onset"]["A"]["mean_high_minus_low_capped_updates"],abs_tol=1e-12)
    assert math.isclose(main["all_start_I_capped_time_H_minus_L"],
                        p["all_start_capped_first_onset"]["I"]["mean_high_minus_low_capped_updates"],abs_tol=1e-12)
    assert all(main["within_two_founders_six_ecologies_D_change"][f"{q['founder']}_c{q['context']}"] == q["D_change"]
               for q in p["six_founder_context_strata"])


def test_strict_order_at_point_one_does_not_reverse():
    result=json.loads(FILE.read_text(encoding="utf8"))["thresholds"]
    assert result["0.1"]["D_L"] < 0
    assert result["0.1"]["D_H"] < 0
    assert result["0.1"]["within_two_founders_six_ecologies_D_change"]["main_c4"] < 0
    assert 0 < result["0.1"]["D_H_minus_L"] < 0.03
