"""Frozen original 2304-genome t0/F1 segregation and threshold-event checks."""
from __future__ import annotations
import csv
import hashlib
import json
from pathlib import Path
import numpy as np
import pytest
from scripts.audit_original_first_meiosis_access_20261014 import (
    events,analyze,sha256,source_case_name,ORIGINAL_PROVIDER_ZIP_SHA,
    ORIGINAL_SOURCE_MANIFEST_SHA,ORIGINAL_PRODUCER_SHA,
)

ROOT=Path(__file__).resolve().parents[1]
SUMMARY=ROOT/'data/results/chapter2_original_first_meiosis_access_2304_20261014.json'
CASES=ROOT/'data/results/chapter2_original_first_meiosis_access_2304_case_20261014.csv'
EXPECTED_JSON_SHA256='d164d81a4584666ecda890c77d78106833b34748941402bf6174ca4d7f24d6c8'
EXPECTED_CSV_SHA256='80d724ea03757d49b616f82cb3a806b5e31dd1ff31aaa7d2bb8edf449cd3e425'


def trace(a=None,i=None):
    pop=np.full(201,48,dtype=int)
    means=np.full((201,3),.5)
    if a is not None:means[a:,2]=.5625
    if i is not None:means[i:,1]=.4375
    return means,pop


@pytest.mark.parametrize('a,i,label',[
    (None,None,'neither'),(21,None,'assurance_only'),
    (None,21,'investment_only'),(20,50,'assurance_first'),
    (50,20,'investment_first'),(20,25,'near_simultaneous'),
    (25,20,'near_simultaneous'),(181,None,'assurance_only'),
])
def test_all_six_original_20_consecutive_census_onset_contract(a,i,label):
    m,p=trace(a,i)
    result,transient=events(m,p)
    assert result['category']==label
    assert result['A']==a and result['I']==i
    assert transient==[a,i]


def test_transient_early_genotype_does_not_count_as_20_year_event():
    m,p=trace()
    m[20:39,2]=.58  # 19 consecutive occupied censuses are insufficient
    result,transient=events(m,p)
    assert result=={'A':None,'I':None,'category':'neither'}
    assert transient[0]==20
    m[20:40,2]=.58
    result,transient=events(m,p)
    assert result['A']==20 and result['category']=='assurance_only'
    m,p=trace();m[182:,2]=.61
    result,transient=events(m,p)
    assert result['A'] is None and transient[0]==182


def test_original_extinction_is_missing_and_absorbing():
    m,p=trace()
    p[40:]=0;m[40:]=np.nan
    result,transient=events(m,p)
    assert result['category']=='neither' and transient==[None,None]
    m[50,2]=0
    with pytest.raises(ValueError,match='extinct traits'):events(m,p)
    m[50,2]=np.nan;p[80]=4
    with pytest.raises(ValueError,match='reappeared'):events(m,p)


def test_source_identity_cannot_be_reclassified_as_a_new_cohort():
    assert len(ORIGINAL_PROVIDER_ZIP_SHA)==9
    assert len(set(ORIGINAL_PROVIDER_ZIP_SHA.values()))==9
    assert len(ORIGINAL_SOURCE_MANIFEST_SHA)==64
    assert len(ORIGINAL_PRODUCER_SHA)==64
    assert source_case_name({'block':'main','context':4,'replicate':127})=='main_c4_r127.npz'
    with pytest.raises(ValueError,match='Exactly nine'):analyze([])


def test_original_sha_pinned_results_match_all_original_six_classes():
    if not SUMMARY.exists() or not CASES.exists():
        pytest.skip('Standalone script without checked-out archived output JSON/CSV')
    assert sha256(SUMMARY.read_bytes())==EXPECTED_JSON_SHA256
    assert sha256(CASES.read_bytes())==EXPECTED_CSV_SHA256
    m=json.loads(SUMMARY.read_text())
    assert m['status']=='COMPLETE_ORIGINAL_2304_GENOTYPE_AND_EVENT_SHA_ADMITTED_EXPLORATORY'
    assert m['source']['verified_original_case_npzs']==2304
    assert m['source']['paired_history_clusters']==256
    assert m['source']['genetic_t0_profiles']==18
    assert len(m['source']['original_provider_zips'])==9
    assert {int(x['original_provider'].split('-')[-1][:-4]):x['sha256'] for x in m['source']['original_provider_zips']}==ORIGINAL_PROVIDER_ZIP_SHA
    assert m['all_six_original_outcomes']=={
        'assurance_first':335,'investment_first':435,'near_simultaneous':358,
        'assurance_only':895,'investment_only':10,'neither':271,
    }
    assert sum(m['all_six_original_outcomes'].values())==2304
    a=m['all_start_genetic_access']
    assert a['A_t0_phenotype_variance_zero']==2304
    assert a['A_F1_expressed_variance_positive']==2304
    assert a['A_F1_population_has_unmutated_genotype_at_least_founder_plus0p05']==2304
    assert a['A_F1_zero_A_mutated_offspring_cases']==864
    assert a['A_after_F1_sustained_threshold_observed']==2023
    assert a['A_transient_without_20_consecutive_censuses']==83
    assert a['I_transient_without_20_consecutive_censuses']==201
    assert m['new_biological_histories_generated']==0
    assert m['new_Q1Q2_clock_confirmed'] is False


def test_exact_all_case_csv_has_all_paired_contexts_and_censoring():
    if not CASES.exists():pytest.skip('Standalone script lacks source-derived output CSV')
    with CASES.open(newline='') as h:rr=list(csv.DictReader(h))
    assert len(rr)==2304
    assert len({x['case'] for x in rr})==2304
    assert len({(x['founder'],x['replicate']) for x in rr})==256
    assert all(len({x['original_context'] for x in rr if x['founder']==b and x['replicate']==r})==9 for b in ('main','confirmation') for r in map(str,range(128)))
    assert all(x['A_t1_any_individual_above_0p05']=='True' and x['A_F1_has_unmutated_individual_above0p05']=='True' for x in rr)
    assert all(int(x['N_first_offspring'])==48 for x in rr)


def test_original_zips_if_available_to_local_runner():
    candidates=[Path('/mnt/data')/f'ecological-original-shard-{i}.zip' for i in range(9)]
    if not all(x.exists() for x in candidates):
        pytest.skip('Complete original GitHub Actions nine source ZIPs must be supplied separately')
    actual,rows=analyze(candidates)
    assert len(rows)==2304
    assert actual['all_start_genetic_access']['A_F1_expressed_variance_positive']==2304
    if SUMMARY.exists():
        # Pure function determinism, not an independently generated original cohort.
        assert actual==json.loads(SUMMARY.read_text())
