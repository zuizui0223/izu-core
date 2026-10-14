"""Stacked diploid genotype parsing tests: invented, NOT real Model3 histories."""
from copy import deepcopy
from hashlib import sha256

import numpy as np
import pytest

from scripts.audit_chapter2_Q2_stacked_genome_class_replay_20261014 import (
    GENOME_FIELDS, annual_from_stacked_diploid_source,
    validate_supplied_stacked_diploid_case_records,
)


def invented_stacked_genomes(category="neither", extinction_at=None):
    """Make syntactically coherent original-type raw arrays; NO reproduction."""
    starts={
        "assurance_first":(20,55),
        "investment_first":(55,20),
        "near_simultaneous":(20,25),
        "assurance_only":(20,None),
        "investment_only":(None,20),
        "neither":(None,None)
    }
    if category not in starts:raise ValueError("Toy category not registered")
    A,I=starts[category]
    a,origins,flags,ids,births=[],[],[],[],[]
    offsets=[0]
    archived_population=[]
    archived_means=[]
    for year in range(201):
        n=48 if year==0 else (0 if extinction_at is not None and year>=extinction_at else 1)
        mean=np.array([.5,
            .4 if year and I is not None and year>=I else .5,
            .6 if year and A is not None and year>=A else .5])
        arr=np.repeat(mean[None,:,None],n,axis=0)
        arr=np.repeat(arr,2,axis=2)
        aa_ids=(np.arange(48,dtype=np.int64) if year==0 else
                np.arange(year*48,year*48+n,dtype=np.int64))
        a.append(arr)
        origins.append(np.broadcast_to(
            aa_ids[:,None,None],(n,3,2)).copy())
        flags.append(np.zeros((n,3,2),dtype=bool))
        ids.append(aa_ids)
        births.append(np.full(n,year,dtype=np.int64))
        archived_population.append(n)
        archived_means.append(mean if n else np.full(3,np.nan))
        offsets.append(offsets[-1]+n)
    return {
        "alleles":np.concatenate(a),
        "allele_origin":np.concatenate(origins),
        "mutation_flags":np.concatenate(flags),
        "ids":np.concatenate(ids),
        "birth_years":np.concatenate(births),
        "offsets":np.array(offsets,dtype=np.int64),
        "population":np.array(archived_population,dtype=np.int64),
        "means":np.array(archived_means,dtype=np.float64),
    }


@pytest.mark.parametrize("category",[
    "assurance_first","investment_first","near_simultaneous",
    "assurance_only","investment_only","neither",
])
def test_six_class_from_complete_original_shape_toy_annual_genomes(category):
    toy=invented_stacked_genomes(category)
    result=annual_from_stacked_diploid_source(toy)
    assert result["classification"]["category"]==category
    assert result["classification"]["extinct_by_horizon"] is False
    assert result["source_archive_or_parentage_identity_verified"] is False
    assert result["new_Model3_population_updates"]==0
    assert result["n_stacked_genotyped_individual_census_rows"]==248
    assert len(result["all_raw_alleles_sha256"])==64
    assert np.array_equal(result["recomputed_annual_census"],
                          toy["population"])


def test_extinct_case_is_kept_and_nan_means_reconstructed():
    toy=invented_stacked_genomes("assurance_only",extinction_at=90)
    replay=annual_from_stacked_diploid_source(toy)
    assert replay["classification"]["category"]=="assurance_only"
    assert replay["classification"]["A_first_sustained_onset"]==20
    assert replay["classification"]["extinct_by_horizon"] is True
    assert replay["classification"]["first_extinct_census"]==90
    assert replay["n_stacked_genotyped_individual_census_rows"]==48+89
    assert np.isnan(replay["recomputed_annual_means"][90:]).all()


@pytest.mark.parametrize("error",[
    "allele_modified_not_in_means", "wrong_census",
    "wrong_year_ID", "unexpected_I_mutation", "bad_birth_year",
    "missing_origins", "bad_offspring_id", "wrong_offset",
])
def test_genome_source_corruption_is_refused(error):
    toy=invented_stacked_genomes("assurance_first")
    if error=="allele_modified_not_in_means":
        toy["alleles"][49,2,:]=.1
    elif error=="wrong_census":
        toy["population"][1]=2
    elif error=="wrong_year_ID":
        toy["ids"][48]=1000
    elif error=="unexpected_I_mutation":
        toy["mutation_flags"][48,1,0]=True
    elif error=="bad_birth_year":
        toy["birth_years"][49]=0
    elif error=="missing_origins":
        del toy["allele_origin"]
    elif error=="bad_offspring_id":
        toy["ids"][60]=toy["ids"][59]
    elif error=="wrong_offset":
        toy["offsets"][3]=toy["offsets"][2]
    with pytest.raises(ValueError):
        annual_from_stacked_diploid_source(toy)


def invented_paired_raw_records():
    entries=[]
    for source in ("S0","S1"):
        for context in (0,3,4):
            for m in (0,12):
                category=("assurance_first" if m==12 else "investment_first") if source=="S0" else "neither"
                extinct=(source=="S1" and context==4 and m==0)
                raw=invented_stacked_genomes(
                    category,extinction_at=(90 if extinct else None))
                entries.append({
                    "source_id":source,
                    "original_source_genome_sha256":
                        sha256(("INVENTED_SOURCE_"+source).encode()).hexdigest(),
                    "history_id":"toy0",
                    "future_master_identity":"TOY-NO-BIOLOGY-"+source,
                    "context":context,
                    "m":m,
                    "archived_category":category,
                    "archived_extinct_by_horizon":extinct,
                    "raw_stacked_model3":raw,
                })
    return entries


def test_full_genotype_to_category_to_source_cluster_procedure_is_readonly():
    r=validate_supplied_stacked_diploid_case_records(
        invented_paired_raw_records())
    assert r["status"]=="SOURCE_STACKED_DIPOID_TO_SIX_CLASS_TECHNICAL_REPLAY_ONLY"
    assert r["genotype_arrays_recomputed"]==12
    assert r["independent_source_clusters"]==2
    assert r["extinct_cases_in_all_start_denominator"]==1
    assert r["source_archive_or_full_parentage_independently_verified"] is False
    assert r["new_Model3_biological_histories_generated"]==0


def test_mislabeled_raw_genomes_cannot_be_silently_admitted():
    cases=invented_paired_raw_records()
    cases[0]["archived_category"]="assurance_first"
    with pytest.raises(ValueError,match="event replay disagrees"):
        validate_supplied_stacked_diploid_case_records(cases)
