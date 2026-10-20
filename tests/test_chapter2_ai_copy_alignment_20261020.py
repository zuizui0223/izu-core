"""TECHNICAL-ONLY per-census A-mutant-token × same-individual I readout.

The biological source is the unchanged PR569 Model3 Q1 reproductive process.
Every technical update independently matches original genome/trace. These
are descriptive observations among tagged genetic copies, NOT phased linkage
disequilibrium, a causal hitchhiking effect or independent natural islands.
"""
from __future__ import annotations

from functools import lru_cache
import math

import numpy as np
import pytest

from scripts.audit_chapter2_ai_mutation_origin_20261020 import (
    STATUS, audit_bounded, census_mutation_tag_I_alignment,
)
from scripts.run_chapter2_q1_fresh_founders_20261016 import (
    founder,load_frozen,
)


@lru_cache(maxsize=1)
def cohort():
    return audit_bounded()


def test_initial_Q1_founders_have_no_A_mutant_tags():
    design,_=load_frozen()
    plant=founder(design,560201)
    tags=np.empty((len(plant.ids),2),dtype=object)
    tags.fill(None)
    z=census_mutation_tag_I_alignment(plant,tags)
    assert z["n_A_copies_with_mutation_token"]==0
    assert z["n_A_copies_without_mutation_token"]==96
    assert z["mean_I_in_mutation_tagged_A_copies"] is None
    assert abs(z["mean_I_in_untagged_A_copies"]-z["mean_I_in_population"])<1e-14
    assert z["tagged_minus_untagged_I"] is None
    assert z["per_token_current_copy_I_mean"]=={}


def test_exact_tag_copy_weighting_and_no_source_I_allele_modification():
    design,_=load_frozen()
    plant=founder(design,560202)
    original=plant.alleles.copy()
    tags=np.empty((48,2),dtype=object)
    tags.fill(None)
    tags[0,0]="A_variant_test"
    tags[1,0]=tags[1,1]="A_variant_test"
    tags[2,1]="another_A_variant_test"
    z=census_mutation_tag_I_alignment(plant,tags)
    I=plant.alleles[:,1,:].mean(axis=1)
    expected=(float(I[0])+2*float(I[1]))/3
    assert z["n_A_copies_with_mutation_token"]==4
    assert z["n_A_copies_without_mutation_token"]==92
    assert abs(z["per_token_current_copy_I_mean"]["A_variant_test"]-expected)<1e-14
    assert abs(z["per_token_current_copy_I_mean"]["another_A_variant_test"]-float(I[2]))<1e-14
    assert abs(z["mean_I_in_mutation_tagged_A_copies"]-
               (float(I[0])+2*float(I[1])+float(I[2]))/4)<1e-14
    reconstructed=(4*z["mean_I_in_mutation_tagged_A_copies"]+
                   92*z["mean_I_in_untagged_A_copies"])/96
    assert abs(reconstructed-I.mean())<1e-14
    assert np.array_equal(plant.alleles,original)


def test_bad_tokens_and_shapes_fail_closed():
    d,_=load_frozen()
    x=founder(d,560201)
    with pytest.raises(ValueError,match="align"):
        census_mutation_tag_I_alignment(x,np.empty((47,2),dtype=object))
    bad=np.empty((48,2),dtype=object)
    bad.fill(None)
    bad[0,0]=3
    with pytest.raises(ValueError,match="nonempty"):
        census_mutation_tag_I_alignment(x,bad)


def test_all_native_censuses_have_exact_mutant_and_untagged_I_census_ledger():
    q=cohort()
    assert q["status"]==STATUS
    assert q["trace_cohort_cases"]==16
    assert q["source_mutation_births_total"]==216
    nonempty=0
    for case in q["cases"]:
        seen={e["event_id"]:e for e in case["raw_A_mutation_event_births"]}
        assert case["per_census"][0]["A_token_I_alignment"][
            "n_A_copies_with_mutation_token"]==0
        for row in case["per_census"]:
            z=row["A_token_I_alignment"]
            tagged=z["n_A_copies_with_mutation_token"]
            untagged=z["n_A_copies_without_mutation_token"]
            assert tagged==row["n_A_copies_with_token"]
            assert tagged+untagged==row["n_A_allele_copies"]==2*row["N"]
            assert set(z["per_token_current_copy_I_mean"])==set(
                row["A_mutation_token_copies_present"])
            for token,I in z["per_token_current_copy_I_mean"].items():
                assert token in seen
                assert seen[token]["mutation_census"]<=row["census"]
                assert 0<=I<=1
            if tagged:
                nonempty+=1
                assert z["mean_I_in_mutation_tagged_A_copies"] is not None
            else:
                assert z["mean_I_in_mutation_tagged_A_copies"] is None
            if untagged:
                assert z["mean_I_in_untagged_A_copies"] is not None
            else:
                assert z["mean_I_in_untagged_A_copies"] is None
            if 0<tagged<2*row["N"]:
                m=(tagged*z["mean_I_in_mutation_tagged_A_copies"]+
                   untagged*z["mean_I_in_untagged_A_copies"])/(2*row["N"])
                assert abs(m-row["mean_I"])<1e-12
                assert abs(z["tagged_minus_untagged_I"]-
                           (z["mean_I_in_mutation_tagged_A_copies"]-
                            z["mean_I_in_untagged_A_copies"]))<1e-13
            elif not tagged or not untagged:
                assert z["tagged_minus_untagged_I"] is None
    assert nonempty>0


def test_emit_tech_only_dynamic_genetic_background_alignment():
    q=cohort()
    for setting in ("delayed_control","assurance_cost"):
        for arm in ("near","far"):
            cases=[c for c in q["cases"] if c["setting"]==setting and c["arm"]==arm]
            assert len(cases)==4
            for year in (3,6,9,12):
                vec=[c["per_census"][year]["A_token_I_alignment"] for c in cases]
                available=[x["tagged_minus_untagged_I"] for x in vec
                           if x["tagged_minus_untagged_I"] is not None]
                mean=sum(available)/len(available) if available else None
                tagged=sum(x["n_A_copies_with_mutation_token"] for x in vec)
                print(
                    "Q1 A-TOKEN/I TECHNICAL ALIGNMENT", setting, arm,
                    f"year={year}",
                    f"cases_with_both_tagged_and_untagged={len(available)}/4",
                    f"tagged_A_homolog_copies={tagged}",
                    f"unweighted_case_mean_tagged_minus_untagged_I={mean}",
                )
    print("TECHNICAL: NO HITCHHIKING CAUSALITY, NO 1000-UPDATE SOURCE CLAIM")
