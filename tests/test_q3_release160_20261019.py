"""Dry-only final-candidate consistency tests; no biological updates."""
import copy
import hashlib
import importlib
from pathlib import Path
import sys
import pytest

from scripts.q3_release160_20261019 import (
    candidate, validate, assignments, audit, snapshot_sources, emit,
    load_oc, SOURCE_BLOBS, ROOT,
)


def test_plan_matches_tested_method_and_counts():
    p=candidate()
    validate(p)
    assert p['axes']=={'founders':160,'visitors':160,'demographic_repeats':1}
    assert p['design']['fork']==35 and p['design']['end']==80
    assert p['budget']['unique_updates']==6400000
    assert p['budget']['prefix_tasks']==51200
    assert p['budget']['future_tasks']==102400
    assert p['budget']['saved_state_slots']==6553600
    assert p['storage']['raw_arrays_per_copy']==37172019200
    assert p['storage']['raw_arrays_two_copies']==74344038400
    assert p['registered'] is False and p['execution_authorized'] is False
    assert p['sources']['old136_plan_git_blob']=='1491a6523eb2b13d0e8a42508990c7e80c869819'


def test_full_assignment_is_unique_paired_and_not_random_sampling():
    p=candidate();rows=list(assignments(p))
    assert len(rows)==25600
    keys={k for r in rows for k in r['masters'].values()}
    assert len(keys)==51200
    counts=[0]*32
    for r in rows:
        counts[r['shard']]+=1
        assert r['masters']['prefix']!=r['masters']['fork']
        assert r['expected_task_files']==6
        assert r['policies']==['fixed','evolving']
        assert r['budgets']==[8.0,4.5]
    assert counts==[800]*32
    assert len({(r['founder_seed'],r['visitor_seed']) for r in rows})==25600
    assert set(p['seed_registry']['founders']).isdisjoint(range(401001,401137))
    assert set(p['seed_registry']['visitors']).isdisjoint(range(302001,302007))
    assert rows==list(assignments(p))


def test_changes_cannot_be_labeled_as_validated_160_or_approved():
    p=candidate()
    for keys,value in [
        (('axes','founders'),136),(('axes','demographic_repeats'),2),
        (('design','policies'),['evolving','fixed']),
        (('design','budgets'),[4.5,8.]),(('design','fork'),39),
        (('decision','margin'),.05),
        (('seed_registry','founders'),list(range(301001,301161))),
        (('execution_authorized',),True), (('registered',),True),
    ]:
        q=copy.deepcopy(p);obj=q
        for k in keys[:-1]:obj=obj[k]
        obj[keys[-1]]=value
        with pytest.raises(ValueError):validate(q)


def test_source_bytes_checked_before_plan_admission(tmp_path):
    for name in SOURCE_BLOBS:
        dest=tmp_path/name;dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes((ROOT/name).read_bytes())
    assert snapshot_sources(tmp_path)==snapshot_sources(ROOT)
    path=next(iter(SOURCE_BLOBS))
    with (tmp_path/path).open('ab') as f:f.write(b'\n# changed\n')
    with pytest.raises(ValueError,match='source'):snapshot_sources(tmp_path)


def test_review_and_resource_deficits_cannot_become_execution_permission(tmp_path):
    report=audit(candidate(),storage_parent=tmp_path,available_bytes=30_000_000_000)
    assert report['execution_authorized'] is False
    assert report['resource']['admitted'] is False
    assert report['source_validation']=='PASS'
    assert report['status']=='HOLD_NOT_EXECUTABLE'
    assert 'production_runner_binding_missing' in report['unresolved']
    assert 'independent_method_and_margin_review_missing' in report['unresolved']
    good=audit(candidate(),storage_parent=tmp_path,available_bytes=200_000_000_000)
    assert good['resource']['admitted'] is True
    assert good['execution_authorized'] is False
    assert 'archive_location_and_retention_not_approved' in good['unresolved']


def test_oc_is_conditional_evidence_not_biological_power():
    oc=load_oc()
    assert oc['retained_statistical_experiments']==60000
    assert oc['independent_axes']==[160,160]
    assert oc['execution_authorized'] is False
    assert oc['minimum_joint_power_MC_lower']>.8
    assert oc['maximum_null_FWER_MC_upper']<.05
    assert oc['Model3_specific_power_validated'] is False


def test_files_are_deterministic_refuse_overwrite_and_complete(tmp_path):
    first=tmp_path/'first'; second=tmp_path/'second'
    a=emit(first);b=emit(second)
    assert a['assignment_digest']==b['assignment_digest']
    assert a['planned_crossings']==25600
    assert a['proposed_task_files']==153600
    assert a['biological_rng_calls']==a['biological_updates']==0
    with pytest.raises(FileExistsError):emit(first)
    import gzip,json
    rows=[json.loads(s) for s in gzip.open(first/'ASSIGNMENTS.jsonl.gz','rt')]
    assert len(rows)==25600
    for f in ('CANDIDATE_160.json','ASSIGNMENTS.jsonl.gz'):
        assert (first/f).read_bytes()==(second/f).read_bytes()


def test_no_change_to_technical_only_execution_gate(tmp_path):
    # Calling initialize refuses a production plan BEFORE sampling genotypes.
    from scripts import q3_native_runner_20261019 as old
    with pytest.raises(ValueError,match='technical-only'):
        old.initialize(tmp_path/'not-created',candidate())
    assert not (tmp_path/'not-created').exists()
