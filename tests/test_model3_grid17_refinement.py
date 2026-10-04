import json
import hashlib
import numpy as np
import pytest
from scripts import run_model3_grid17_refinement as stage
from scripts import run_model3_grid_refinement as prior


def test_same_conditions_and_founders_only_resolution_changes(tmp_path):
    before=prior.refinement_tasks(tmp_path)
    after=stage.refinement_tasks(tmp_path)
    assert len(before)==len(after)==32
    for a,b in zip(before,after):
        assert a[2:8]==b[2:8] and a[9:]==b[9:]
        assert b[8]==17 and b[1]==a[1].replace('_n13_','_n17_')
    assert set([0,.25,.5,.75,1]) <= set(np.linspace(0,1,17))


def test_predecessor_requires_all_verified_cases(tmp_path):
    with pytest.raises(ValueError,match='incomplete'):
        stage.verify_predecessor(tmp_path)
    tasks=prior.refinement_tasks(tmp_path)
    prior.snapshot(tmp_path)
    (tmp_path/'complete.json').write_text(json.dumps(dict(status='completed',n_cases=32,keys=[t[1] for t in tasks])))
    for t in tasks:
        p=tmp_path/(t[1]+'.npz');p.write_bytes(b'fixture')
        (tmp_path/(t[1]+'.json')).write_text(json.dumps(dict(task=list(t[2:]),sha256=hashlib.sha256(p.read_bytes()).hexdigest())))
    manifest=stage.verify_predecessor(tmp_path)
    assert len(manifest['case_hashes'])==32
    (tmp_path/(tasks[-1][1]+'.npz')).write_bytes(b'corrupt')
    with pytest.raises(ValueError,match='receipt'):
        stage.verify_predecessor(tmp_path)


def test_snapshot_rejects_corrupt_archive_and_changed_parent(tmp_path):
    stage.snapshot(tmp_path,{'parent':'a'})
    with pytest.raises(ValueError,match='predecessor'):
        stage.snapshot(tmp_path,{'parent':'b'})
    (tmp_path/'sources.zip').write_bytes(b'corrupt')
    with pytest.raises(ValueError,match='archive'):
        stage.snapshot(tmp_path,{'parent':'a'})


def test_precision_summary_rejects_partial_stage(tmp_path):
    with pytest.raises(ValueError,match='incomplete'):
        stage.summarize(tmp_path,tmp_path)


def test_precision_comparison_cannot_hide_occupancy_or_initial_mismatch():
    a=np.zeros((1001,10));a[:,0]=48;a[:,1:4]=.5
    b=a.copy();b[-1,2]+=.02
    r=stage.compare_traces(a,b)
    assert not r['terminal_pass'] and r['terminal_max_gap']==pytest.approx(.02)
    b=a.copy();b[0,1]+=.01
    with pytest.raises(ValueError,match='initial'):
        stage.compare_traces(a,b)
    b=a.copy();b[-1,0]=0;b[-1,1:4]=np.nan
    r=stage.compare_traces(a,b)
    assert not r['terminal_pass'] and r['occupancy_mismatch_count']==1


def test_verification_never_recreates_missing_provenance(tmp_path):
    tasks=prior.refinement_tasks(tmp_path)
    prior.snapshot(tmp_path)
    original=(tmp_path/'sources.zip').read_bytes()
    (tmp_path/'complete.json').write_text(json.dumps(dict(status='completed',n_cases=32,keys=[t[1] for t in tasks])))
    (tmp_path/'sources.json').unlink()
    with pytest.raises(ValueError,match='provenance'):
        stage.verify_predecessor(tmp_path)
    assert not (tmp_path/'sources.json').exists()
    assert (tmp_path/'sources.zip').read_bytes()==original


def test_cannot_stamp_new_provenance_on_existing_case(tmp_path):
    (tmp_path/'existing.npz').write_bytes(b'existing result')
    with pytest.raises(ValueError,match='provenance'):
        stage.snapshot(tmp_path,{})


def test_summary_checks_own_archive_and_predecessor(tmp_path,monkeypatch):
    stage.snapshot(tmp_path,{'parent':'a'})
    monkeypatch.setattr(stage,'read_receipt',lambda *args:{})
    monkeypatch.setattr(stage,'verify_predecessor',lambda *args:{'parent':'b'})
    with pytest.raises(ValueError,match='predecessor'):
        stage.summarize(tmp_path,tmp_path)
    monkeypatch.setattr(stage,'verify_predecessor',lambda *args:{'parent':'a'})
    (tmp_path/'sources.zip').write_bytes(b'corrupt')
    with pytest.raises(ValueError,match='archive'):
        stage.summarize(tmp_path,tmp_path)
