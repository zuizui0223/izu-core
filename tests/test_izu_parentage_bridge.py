"""Parentage extension rejects inferred paternity from absent data and fake permits."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

from scripts.audit_izu_parentage_bridge import TEMPLATE, audit

H = "a" * 64


def fixture():
    return {
        "schema":"izu_parentage_extension_v1",
        "status":"SYNTHETIC_QC_ONLY",
        "evidence_mode":"synthetic_test",
        "source_receipts":{
            "chain_audit_sha256":H,"site_registry_audit_sha256":H,
            "parentage_genotype_archive_sha256":H,"parentage_model_report_sha256":H,
        },
        "site_admissions":[{"block_id":"b1","pool_id":"p1",
            "admission_status":"admitted","r1_audit_ref":"synthetic-r1",
            "permit_evidence_ref":"synthetic-permit","access_evidence_ref":"synthetic-access"}],
        "chain_plants":[{"block_id":"b1","plant_id":"mother1",
            "full_chain_plant":True,"predeclared_block":True,
            "source_chain_row_ref":"synthetic-chain1"}],
        "fruits":[{"block_id":"b1","plant_id":"mother1",
            "fruit_id":"fruit1","mature_seed_count":3,
            "treatment_type":"open_pollinated","source_fruit_row_ref":"synthetic-fruit1"}],
        "offspring":[
            {"block_id":"b1","plant_id":"mother1","fruit_id":"fruit1",
             "seed_id":"seed1","assay_status":"usable",
             "genotype_sha256":H,"genotyping_batch_id":"synthetic-batch"},
            {"block_id":"b1","plant_id":"mother1","fruit_id":"fruit1",
             "seed_id":"seed2","assay_status":"usable",
             "genotype_sha256":H,"genotyping_batch_id":"synthetic-batch"}],
        "candidate_fathers":[{"pool_id":"p1","father_id":"father1",
            "sample_id":"synthetic-sample-father1","genotype_sha256":H}],
        "assignments":[
            {"seed_id":"seed1","category":"self","posterior_probability":.2},
            {"seed_id":"seed1","category":"named_father","father_id":"father1","posterior_probability":.7},
            {"seed_id":"seed1","category":"unsampled_or_unknown","posterior_probability":.1},
            {"seed_id":"seed2","category":"self","posterior_probability":.3},
            {"seed_id":"seed2","category":"named_father","father_id":"father1","posterior_probability":.5},
            {"seed_id":"seed2","category":"unsampled_or_unknown","posterior_probability":.2},
        ],
        "parentage_method":{
            "model_id":"synthetic-likelihood-not-an-observation",
            "genotyping_error_model_documented":True,
            "unsampled_fathers_modelled":True,
            "maternal_genotypes_verified":True,
            "paternity_likelihood_report_sha256":H,
        },
    }


def test_empty_template_is_not_field_evidence():
    src = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    r = audit(src)
    assert r["status"] == "NO_FIELD_OFFSPRING_DATA"
    assert r["n_structurally_linked_mothers"] == 0
    assert r["n_usable_seeds"] == 0
    assert r["paternity_algorithm_not_executed"]


def test_complete_synthetic_fixture_only_tests_schema():
    r = audit(fixture())
    assert not r["errors"]
    assert r["status"] == "SYNTHETIC_SCHEMA_CHECK_ONLY"
    assert r["n_structurally_linked_mothers"] == 1
    m=r["mother_rows"][0]
    assert m["n_seed_usable"] == 2
    assert abs(m["expected_self_fraction_among_genotyped"]-.25) < 1e-12
    assert abs(m["expected_unsampled_fraction_among_genotyped"]-.15) < 1e-12
    assert abs(m["expected_named_father_fractions_among_genotyped"]["father1"]-.6) < 1e-12


def test_nonadmitted_site_remains_blocked_even_with_complete_fake_paternity():
    data=fixture()
    data["evidence_mode"]="field_claimed"
    data["site_admissions"][0]["admission_status"]="candidate"
    data["site_admissions"][0].update(
        r1_audit_ref="",permit_evidence_ref="",access_evidence_ref="")
    r=audit(data)
    assert not r["errors"]
    assert r["status"] == "FIELD_PARENTAGE_GATE_BLOCKED"
    assert r["n_structurally_linked_mothers"] == 0


def test_missing_unknown_category_and_bad_total_fail_closed():
    d=fixture()
    d["assignments"]=[
        x for x in d["assignments"]
        if not(x["seed_id"]=="seed1" and x["category"]=="unsampled_or_unknown")]
    r=audit(d)
    assert r["status"]=="INVALID_DATA_OR_LINKAGE"
    assert any("must preserve explicit self AND unsampled" in s for s in r["errors"])
    assert any("posterior mass" in s for s in r["errors"])


def test_failed_genotyping_does_not_turn_into_zero_or_selfing():
    d=fixture()
    d["offspring"]=[{
        **d["offspring"][0],"assay_status":"failed",
        "genotype_sha256":None}]
    d["assignments"]=[]
    r=audit(d)
    assert not r["errors"]
    assert r["status"]=="SYNTHETIC_SCHEMA_CHECK_ONLY"
    assert r["mother_rows"][0]["n_seed_failed"]==1
    assert r["mother_rows"][0]["n_seed_usable"]==0
    assert r["mother_rows"][0]["expected_self_fraction_among_genotyped"] is None


def test_unregistered_father_and_oversampled_fruit_are_invalid():
    d=fixture()
    d["assignments"][1]["father_id"]="invented-father"
    d["fruits"][0]["mature_seed_count"]=1
    r=audit(d)
    assert r["status"]=="INVALID_DATA_OR_LINKAGE"
    assert any("candidate pool" in s for s in r["errors"])
    assert any("sampled > mature" in s for s in r["errors"])


def test_artificial_self_from_mother_id_is_rejected():
    d=fixture()
    d["assignments"][1]["father_id"]="mother1"
    d["candidate_fathers"].append({
        "pool_id":"p1","father_id":"mother1","sample_id":"fake-maternal",
        "genotype_sha256":H})
    r=audit(d)
    assert r["status"]=="INVALID_DATA_OR_LINKAGE"
    assert any("represented as 'self'" in s for s in r["errors"])


def test_bagged_seed_cannot_be_treated_as_natural_father_success():
    d=fixture()
    d["fruits"][0]["treatment_type"]="bagged_autonomous"
    r=audit(d)
    assert r["status"]=="INVALID_DATA_OR_LINKAGE"
    assert any("only from open_pollinated fruits" in s for s in r["errors"])
