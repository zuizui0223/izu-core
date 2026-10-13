"""Source-independent boundaries and hypothetical design power. No new biology."""
from __future__ import annotations
import importlib.util
from pathlib import Path
import json
import math
import os
import pytest
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
MODULE=ROOT/'scripts/audit_chapter2_clock_pilot_historical_power_20261014.py'
spec=importlib.util.spec_from_file_location('ch2_power_audit',MODULE)
audit=importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)
RESULT=ROOT/'data/results/chapter2_clock_pilot_prelaunch_historical_power_20261014.json'


def fixture(a=None,i=None,stop=None):
    m=np.full((201,3),0.5)
    pop=np.full(201,48,dtype=int)
    if a is not None:m[a:,2]=.58
    if i is not None:m[i:,1]=.40
    if stop is not None:pop[stop:]=0;m[stop:]=np.nan
    return m,pop


@pytest.mark.parametrize('label,a,i',[
 ('assurance_first',10,40),('investment_first',40,10),
 ('near_simultaneous',40,45),('assurance_only',10,None),
 ('investment_only',None,10),('neither',None,None),
])
def test_six_original_event_classes(label,a,i):
    m,p=fixture(a,i)
    e=audit.events(m,p)
    assert e=={'A':a,'I':i,'category':label}


def test_sustained_20_window_not_to_terminal_and_terminal_cutoff():
    m,p=fixture(a=20)
    m[40:,2]=.5   # 20 occupied censuses 20..39: registered A event persists even if later reversed
    assert audit.events(m,p)['A']==20
    m,p=fixture(a=182)
    assert audit.events(m,p)['A'] is None
    m,p=fixture(a=181)
    assert audit.events(m,p)['A']==181
    m,p=fixture(a=20,stop=39)
    assert audit.events(m,p)['A'] is None


def test_absorbing_extinction_and_nan_fails_closed():
    m,p=fixture(a=20,stop=80)
    assert audit.events(m,p)['A']==20
    m[85:,1]=0.0
    with pytest.raises(ValueError,match='missingness'):
        audit.events(m,p)
    m,p=fixture(a=20,stop=80)
    p[100]=30
    m[100]=[.5,.5,.6]  # A resurrected population would have defined genotypes, but is forbidden.
    with pytest.raises(ValueError,match='absorbing'):
        audit.events(m,p)


def test_power_is_scenario_not_empirical():
    assert abs(audit.scenario_power(128,.1,.5)-.619)<.002
    assert abs(audit.scenario_power(128,.2,.8)-.807)<.002
    assert .12<audit.target_delta(128,.5)<.125
    assert .19<audit.target_delta(128,.8)<.2
    assert audit.target_delta(64,.5)>audit.target_delta(128,.5)
    with pytest.raises(ValueError):audit.scenario_power(128,0,.5)


def test_frozen_original_actual_outcome_counts():
    j=json.loads(RESULT.read_text())
    assert j['original_cases_verified_from_actual_npz']==2304
    assert j['raw_original_case_checksums_verified']==2304
    assert j['original_fixed_access_comparator']['n_existing_histories']==768
    assert j['original_fixed_access_comparator']['A_event_count']==767
    assert j['original_fixed_access_comparator']['I_event_count']==579
    assert j['original_fixed_access_comparator']['six_class_counts']=={
        'assurance_first':179,'investment_first':217,'near_simultaneous':182,
        'assurance_only':189,'investment_only':1,'neither':0}
    assert len(j['original_fixed_access_comparator']['six_founder_ecology_rows'])==6
    assert j['new_pilot']['n_new_pilot_biological_histories_executed_by_this_audit']==0
    assert j['new_pilot']['observed_new_genetic_treatment_effects'] is None


def test_original_zip_byte_corruption_is_rejected(tmp_path):
    # Reproduce admission rejection without pretending a mock is biological evidence.
    archive=tmp_path/'ecological-original-shard-0.zip'
    archive.write_bytes(b'bad ZIP fixture')
    with pytest.raises((ValueError,FileNotFoundError),match='sha|SHA|shard'):
        audit.audit(tmp_path)


@pytest.mark.skipif(not os.environ.get('CH2_FROZEN_ORIGINAL_ARCHIVE_DIR'),reason='source-only original 9 ZIPs not available in checkout')
def test_full_original_archives_rederive_all_2304():
    path=Path(os.environ['CH2_FROZEN_ORIGINAL_ARCHIVE_DIR'])
    new=audit.audit(path)
    frozen=json.loads(RESULT.read_text())
    assert new==frozen
