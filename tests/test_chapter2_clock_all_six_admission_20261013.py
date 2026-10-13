"""Synthetic receipt controls for full 1,536-case completeness -- no biology."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
import pytest
from scripts.aggregate_chapter2_clock_pilot_verified_shards_20261013 import (
    aggregate,VALID,CASE,
)

REG=ROOT/'data/design/chapter2_clock_factorial_pilot_input_inventory_20261013.json'


def fake_readouts(directory):
    orig=json.loads(REG.read_text());groups={}
    for case in orig['case_identifiers']:
        m=CASE.fullmatch(case);block,ctx,a,i,r=m.groups()
        groups.setdefault((block,ctx),[]).append({
            'case_key':case,'updates':200,'case_sha256':'a'*64,
            'event_0p05':{'A':None,'I':None,'category':'neither'},
            'genotype_record_source_years':200*48,'parent_pairs':200*48,
        })
    paths=[]
    for k,values in sorted(groups.items()):
        r={'schema':'chapter2_clock_factorial_producer_independent_raw_reader_v1',
           'status':'ALL_256_PILOT_SHARD_RAW_GENOMES_REPLAYED',
           'pilot_registry_git_blob':'f18eae09e3f569ae7edefe970ea17d93c64b1bd5',
           'cases':256,'updates':51200,'new_pilot_biological_histories':256,
           'original_model3_biological_source_replayed':True,
           'producer_loaded_as_python_module':False,
           'original_case_receipts':values}
        p=directory/('synthetic_'+str(k[0])+'_'+str(k[1])+'.json')
        p.write_text(json.dumps(r))
        paths.append(p)
    assert len(paths)==6
    return paths


def test_all_six_original_joint_paired_history_cells_preserved(tmp_path):
    paths=fake_readouts(tmp_path)
    o=aggregate(paths,REG)
    assert o['status']=='ALL1536_NEW_PILOT_CASES_SOURCE_VERIFIED_NOT_CAUSAL_CLOCK_CONFIRMATION'
    assert o['all_starts']==1536 and o['paired_history_clusters']==128
    assert o['total_native_reproductive_updates']==307200
    assert o['six_class_labels']['neither']==1536
    assert sum(o['six_class_labels'].values())==1536
    # Synthetic input labels do NOT imply these historical outcomes exist.


def test_duplicate_missing_extra_and_wrong_six_category_rejected(tmp_path):
    paths=fake_readouts(tmp_path)
    with pytest.raises(ValueError,match='Exactly six unique'):
        aggregate(paths[:5]+[paths[0]],REG)
    bad=paths[0];d=json.loads(bad.read_text())
    d['original_case_receipts'][0]['case_key']=d['original_case_receipts'][1]['case_key']
    bad.write_text(json.dumps(d))
    with pytest.raises(ValueError,match='duplicate|invalid ID'):
        aggregate(paths,REG)
    paths=fake_readouts(tmp_path)
    bad=paths[0];d=json.loads(bad.read_text());d['original_case_receipts'][0]['event_0p05']['category']='non_existent'
    bad.write_text(json.dumps(d))
    with pytest.raises(ValueError,match='six-category'):
        aggregate(paths,REG)


def test_corrupted_registry_or_wrong_history_units_fail_closed(tmp_path):
    files=fake_readouts(tmp_path)
    reg=tmp_path/'registry.json';reg.write_bytes(REG.read_bytes()+b' ')
    with pytest.raises(ValueError,match='registry source drift'):
        aggregate(files,reg)
    corrupt=files[0];d=json.loads(corrupt.read_text());d['original_case_receipts'][0]['updates']=199
    corrupt.write_text(json.dumps(d))
    with pytest.raises(ValueError,match='horizon'):
        aggregate(files,REG)
