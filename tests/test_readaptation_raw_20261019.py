"""Independent raw checks against deliberately corrupted synthetic records."""
import copy
import json

import numpy as np
import pytest

from scripts.audit_readaptation_raw_20261019 import (
    audit_future, raw_state_digest, summarize_allocations, indicator_interval,
)


def record():
    # One selfed child per year; hand-constructed, without the producer.
    d=dict(schema='readaptation_future_v1',horizon=80,
           population=np.ones(81,dtype=np.int64),state_offsets=np.arange(82,dtype=np.int64),
           state_alleles=np.full((81,3,2),.5),state_allele_origin=np.zeros((81,3,2),dtype=np.int64),
           state_mutation_flags=np.zeros((81,3,2),bool),state_ids=np.arange(81,dtype=np.int64)*48,
           state_birth_years=np.arange(81,dtype=np.int64),
           trait_mean=np.full((81,3),.5),trait_variance=np.zeros((81,3)),
           allele_min=np.full((81,3),.5),allele_max=np.full((81,3),.5),
           parentage_offsets=np.arange(81,dtype=np.int64),first_extinction=None)
    d['parentage']=np.array([[48*t,48*(t-1),48*(t-1)] for t in range(1,81)],dtype=np.int64)
    d['state_sha256']=[raw_state_digest(d,t) for t in range(81)]
    assay=dict(occupied=True,population=1,reference_competitors=47,maternal_outcross=[2.],
               paternal_outcross=[6.],viable_self=[3.],genetic_return=[7.],mean_genetic_return=7.)
    d['assays']={'0':copy.deepcopy(assay),'80':copy.deepcopy(assay)}
    return d


def test_hand_constructed_path():
    result=audit_future(record())
    assert result['occupied'] is True and result['initial_population']==1
    assert result['change']==[0.,0.,0.]
    assert result['assay_change']==0
    json.dumps(result,allow_nan=False)


@pytest.mark.parametrize('field,index,value',[
    ('trait_mean',(40,1),.6),('trait_variance',(2,0),.1),
    ('allele_max',(3,2),.7),('population',4,0),
    ('parentage',(3,1),999),('state_birth_years',5,0),
])
def test_rejects_tampered_raw_or_summary(field,index,value):
    d=record(); d[field][index]=value
    with pytest.raises(ValueError):
        audit_future(d)


def test_origin_tamper_cannot_be_hidden_by_rehashing():
    d=record(); d['state_allele_origin'][5,1,0]=999
    d['state_sha256'][5]=raw_state_digest(d,5)
    with pytest.raises(ValueError,match='inheritance'):
        audit_future(d)


def test_wrong_assay_arithmetic_and_missing_census_fail():
    d=record(); d['assays']['80']['mean_genetic_return']=8
    with pytest.raises(ValueError,match='assay'):
        audit_future(d)
    d=record(); d['state_sha256'].pop()
    with pytest.raises(ValueError):
        audit_future(d)


def extinct_record(at):
    d=record()
    d['population'][at:]=0
    d['state_offsets']=np.r_[0,np.cumsum(d['population'])]
    for key in ('alleles','allele_origin','mutation_flags','ids','birth_years'):
        d['state_'+key]=d['state_'+key][:at]
    d['parentage']=d['parentage'][:max(0,at-1)]
    d['parentage_offsets']=np.r_[0,np.cumsum(d['population'][1:])]
    for key in ('trait_mean','trait_variance','allele_min','allele_max'):
        d[key][at:]=np.nan
    d['first_extinction']=at
    d['state_sha256']=[raw_state_digest(d,t) for t in range(81)]
    empty=dict(occupied=False,population=0,reference_competitors=47,
               maternal_outcross=[],paternal_outcross=[],viable_self=[],
               genetic_return=[],mean_genetic_return=None)
    d['assays']['80']=copy.deepcopy(empty)
    if at==0:
        d['assays']['0']=copy.deepcopy(empty)
    return d


@pytest.mark.parametrize('at',[0,1,40])
def test_same_empty_endpoint_retains_distinct_timing(at):
    result=audit_future(extinct_record(at))
    assert result['first_extinction']==at
    assert result['change'] is None and result['assay_change'] is None
    assert result['occupied'] is False
    json.dumps(result,allow_nan=False)


def summaries():
    keys=[(0,0,'fixed',c,d,.5,r) for c in range(2) for d in range(2) for r in range(32)]
    rows=[]
    for key in keys:
        occupied=key[-1]!=0
        rows.append(dict(key=list(key),cohort_sha256=str(key[3])*64,
                         occupied=occupied,change=[.1,0.,-.1] if occupied else None,
                         first_extinction=None if occupied else 4,
                         assay_change=2. if occupied else None))
    return keys,rows


def test_preserves_cohort_denominators_and_extinction():
    keys,rows=summaries()
    result=summarize_allocations(rows,keys)
    assert result['allocated']==128 and result['cohorts']==2
    assert len(result['groups'])==4
    for group in result['groups']:
        assert group['repeats']==32
        assert group['occupancy']['count']==31
        assert group['directions']['I']['zero']['count']==31
        assert group['directions']['I']['extinct']['count']==1
        assert group['directions']['I']['zero']['denominator']==32
        assert group['survivor_mean_change']==pytest.approx([.1,0.,-.1])
    assert len(result['paired_destinations'])==2
    assert result['paired_destinations'][0]['occupancy_difference']==0
    json.dumps(result,allow_nan=False)


@pytest.mark.parametrize('damage',['missing','duplicate','hash','unknown'])
def test_allocation_failure_is_closed(damage):
    keys,rows=summaries()
    if damage=='missing': rows.pop()
    elif damage=='duplicate': rows.append(copy.deepcopy(rows[0]))
    elif damage=='hash': rows[0]['cohort_sha256']='f'*64
    else: rows[0]['key'][3]=999
    with pytest.raises(ValueError):
        summarize_allocations(rows,keys)


def test_exact_zero_failure_bound_is_pointwise_and_not_pooled():
    for n in (32,64):
        interval=indicator_interval(0,n)
        assert interval['one_sided_upper_95']==pytest.approx(1-.05**(1/n))
        assert interval['interval_95'][0]==0
        assert interval['interval_95'][1]==pytest.approx(1-.025**(1/n))
        assert interval['scope']=='pointwise conditional; not simultaneous'


def test_all_destination_pairs_include_nonzero_comparators():
    keys,rows=summaries()
    for row in list(rows):
        if row['key'][4]==1:
            extra=copy.deepcopy(row); extra['key'][4]=2
            rows.append(extra); keys.append(tuple(extra['key']))
    result=summarize_allocations(rows,keys)
    assert len(result['paired_destinations'])==6
    assert any(p['destination']==2 and p['reference_destination']==1
               for p in result['paired_destinations'])
