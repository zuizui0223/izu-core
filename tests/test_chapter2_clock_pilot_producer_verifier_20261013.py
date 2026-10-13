"""Source-anchored pilot producer / independent admission tests.

The real 200-update pilot is blocked. Tests execute only disjoint 3-update
technical fixture paths, if immutable source modules and originals are present.
"""
from __future__ import annotations
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
import numpy as np
import pytest
from scripts.prepare_chapter2_clock_pilot_archive_20261013 import (
    CASE_RE,APPROVAL_GIT_BLOB,REGISTRY_SHA,ORIGINAL_T0_SHA,DESIGN_SHA,
    TECH_SALT, WIDTHS,HIDDEN, CONTEXTS, FIELDS,
    case_parts,original_events,technical_case_keys,shard_case_keys,
    sources,native,archive,
)
from scripts.verify_chapter2_clock_pilot_raw_20261013 import (
    six_class,OP_RE,require_array_shape,verify,
)

ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/'data/design/chapter2_clock_factorial_pilot_input_inventory_20261013.json'
FIX=ROOT/'data/design/chapter2_clock_original_t0_typed_fixture_20261013.json'
DESIGN=ROOT/'data/design/chapter2_clock_factorial_pilot_protocol_20261013.json'
LEDGER=ROOT/'data/results/chapter2_clock_t0_reproduction_equivalence_20261013.json'


def test_all_six_censored_event_labels_original_formula():
    pop=np.full(201,48,dtype=int)
    means=np.full((201,3),0.5)
    cases=[('assurance_first',10,50),('investment_first',50,10),
           ('near_simultaneous',40,44),('assurance_only',10,None),
           ('investment_only',None,10),('neither',None,None)]
    for label,ass,invest in cases:
        m=means.copy()
        if ass is not None:m[ass:,2]=.58
        if invest is not None:m[invest:,1]=.40
        result=original_events(m,pop)
        assert result['category']==label
        assert six_class(m,pop)==result
    m=means.copy();m[195:,2]=.65
    assert original_events(m,pop)['A'] is None  # fewer than20 occupied censuses
    pop[40:]=0;m[40:]=np.nan
    assert original_events(m,pop)['category']=='neither'
    m[40:,1]=0
    with pytest.raises(ValueError,match='extinct|missing'):
        six_class(m,pop)


def test_original_frozen_case_and_shard_partition():
    registry=json.loads(REG.read_text())
    cases=registry['case_identifiers']
    assert len(cases)==1536 and len(set(cases))==1536
    assert len(technical_case_keys(registry))==48
    assert all(CASE_RE.fullmatch(k) and OP_RE.fullmatch(k) for k in cases)
    shards=[shard_case_keys(registry,i) for i in range(6)]
    assert [len(s) for s in shards]==[256]*6
    assert set().union(*(set(s) for s in shards))==set(cases)
    assert len({tuple(case_parts(x)[:2]) for x in cases})==6
    assert APPROVAL_GIT_BLOB is None  # later reviewed approval must be explicit
    assert TECH_SALT!=registry['pilot_salt']
    assert len(registry['stochastic_history_cluster_master_seeds_decimal'])==128
    assert tuple(WIDTHS.values())==(.046875,.078125)
    assert tuple(HIDDEN.values())==(0.,1.)
    assert set(CONTEXTS)=={0,3,4}
    assert FIELDS==('ids','alleles','allele_origin','mutation_flags','birth_years')
    with pytest.raises(ValueError):case_parts('main_c3_AL_I0_r064')
    with pytest.raises(ValueError):shard_case_keys(registry,6)


def test_raw_admission_rejects_inconsistent_shapes():
    yrs=3
    bad={key:np.empty((0,)) for key in FIELDS}
    bad.update(offsets=np.zeros(yrs+2,dtype=int),population=np.zeros(yrs+1,dtype=int),
               means=np.zeros((yrs+1,3)),parentage=np.empty((0,3),dtype=int),
               parent_offsets=np.zeros(yrs+1,dtype=int),
               source_parent_returns=np.empty((0,3)),source_offsets=np.zeros(yrs+1,dtype=int),
               returns=np.empty((yrs,8)),sexual_selection=np.empty((yrs,3,3)),
               reproductive_ledger_sha256=np.empty(yrs,dtype='S64'),
               recruitment=np.empty((yrs,8),dtype=int),metadata=np.array('{}'))
    with pytest.raises(ValueError):require_array_shape(bad,48,yrs)


def test_no_unapproved_true_pilot_launch_without_source_access(tmp_path):
    # After source admission the actual pilot checks require a separately pinned
    # approval Git blob; this file cannot perform 200-year biology in CI.
    assert APPROVAL_GIT_BLOB is None
    assert not (tmp_path/'real-pilot').exists()
    assert TECH_SALT!='chapter2-clock-factorial-pilot-v1-20261013'


def test_native_48_archival_and_independent_source_heredity_verifier(tmp_path):
    # The repository CI has full actual original Model3 biological source and
    # historical fixture/ledger; a detached numerical-only scratchpad does not.
    if not all(p.exists() for p in (REG,FIX,DESIGN,LEDGER)):
        pytest.skip('full source archive/typed original fixture only available in repository checkout')
    source=ROOT/'scripts/model3_island/types.py'
    if not source.exists():
        pytest.skip('standalone scratchpad lacks frozen biological source')
    historical=sources(REG,FIX,DESIGN,LEDGER)
    assert len(historical[1]['original_founders'])==2
    modules=native()
    assert len(modules)==4
    out=tmp_path/'technical-only'
    receipt=archive(out,REG,FIX,DESIGN,LEDGER,technical=True)
    assert receipt['cases']==48 and receipt['updates_per_case']==3
    assert receipt['new_scientific_pilot_histories']==0
    checked=verify(out,REG,FIX,DESIGN,technical=True)
    assert checked['status']=='ALL_48_NATIVE_TECHNICAL_PATHS_REPRODUCED'
    assert checked['cases']==48 and checked['updates']==144
    assert checked['parent_pairs']>=0 and checked['producer_loaded_as_python_module'] is False
    assert not any(r['event_0p05'] is not None for r in checked['original_case_receipts'])
    with pytest.raises(FileExistsError):
        archive(out,REG,FIX,DESIGN,LEDGER,technical=True)
    # Do not trust the producer's original SHA receipt without independent bytes.
    import shutil
    one=out/(receipt['case_records'][0]['case_key']+'.npz')
    backup=tmp_path/'original.npz';shutil.copy2(one,backup)
    with one.open('ab') as fh:fh.write(b'unregistered')
    with pytest.raises(ValueError,match='SHA changed'):
        verify(out,REG,FIX,DESIGN,technical=True)
    shutil.copy2(backup,one)
    assert verify(out,REG,FIX,DESIGN,technical=True)['updates']==144
