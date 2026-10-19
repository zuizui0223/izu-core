"""Cross-runner transfer tests; NO new scientific or production trajectories."""
import json
from pathlib import Path
import zipfile
import pytest

from scripts import q3_actions_artifacts_20261019 as bridge
from scripts import q3_partitioned_runner_20261019 as partition

SOURCE='8920121da21f1c614cae70671038942146fb8a4c'
BATCH='123456-1'

def prepared(tmp_path):
    root=tmp_path/'producer';partition.prepare(root,3)
    return root

def rewrite(src,dst,change):
    with zipfile.ZipFile(src) as z: files={n:z.read(n) for n in z.namelist()}
    change(files)
    with zipfile.ZipFile(dst,'w') as z:
        for name,data in files.items(): z.writestr(name,data)

def test_initial_plan_moves_across_runners_without_drawing_rng(tmp_path):
    root=prepared(tmp_path);packet=tmp_path/'plan.zip'
    bridge.pack(root,packet,source=SOURCE,batch=BATCH)
    dest=tmp_path/'remote'
    bridge.restore(packet,dest,source=SOURCE,batch=BATCH)
    assert partition.manifest(dest)==partition.manifest(root)
    assert all((dest/'shards'/f'shard-{i:03d}'/'states').is_dir() for i in range(3))
    assert not list(dest.rglob('*.npz'))
    with pytest.raises(ValueError,match='exists'):
        bridge.restore(packet,dest,source=SOURCE,batch=BATCH)

def test_wrong_run_and_source_rejected_before_creating_output(tmp_path):
    root=prepared(tmp_path);packet=tmp_path/'plan.zip'
    bridge.pack(root,packet,source=SOURCE,batch=BATCH)
    for source,batch in [('0'*40,BATCH),(SOURCE,'123456-2')]:
        dest=tmp_path/'bad'
        with pytest.raises(ValueError,match='identity'):
            bridge.restore(packet,dest,source=source,batch=batch)
        assert not dest.exists()

def test_corrupt_payload_or_foreign_archive_member_fails_closed(tmp_path):
    root=prepared(tmp_path);packet=tmp_path/'plan.zip'
    bridge.pack(root,packet,source=SOURCE,batch=BATCH)
    bad=tmp_path/'corrupt.zip'
    rewrite(packet,bad,lambda f:f.__setitem__('PARTITION.json',b'{}'))
    with pytest.raises(ValueError,match='digest'):
        bridge.restore(bad,tmp_path/'corrupt',source=SOURCE,batch=BATCH)
    evil=tmp_path/'evil.zip'
    rewrite(packet,evil,lambda f:f.__setitem__('../outside',b'bad'))
    with pytest.raises(ValueError,match='inventory'):
        bridge.restore(evil,tmp_path/'evil',source=SOURCE,batch=BATCH)
    assert not (tmp_path/'outside').exists()

def test_unsealed_worker_not_uploadable_as_completed(tmp_path):
    root=prepared(tmp_path)
    with pytest.raises(ValueError,match='unsealed'):
        bridge.pack(root,tmp_path/'ready.zip',source=SOURCE,batch=BATCH,shard=0)
    assert not (tmp_path/'ready.zip').exists()

def test_only_three_technical_shards_and_safe_source_identity(tmp_path):
    root=prepared(tmp_path)
    for bad in (3,160,-1):
        with pytest.raises(ValueError):
            bridge.pack(root,tmp_path/'x.zip',source=SOURCE,batch=BATCH,shard=bad)
    with pytest.raises(ValueError,match='identity'):
        bridge.pack(root,tmp_path/'x.zip',source='${{ secrets.X }}',batch=BATCH)
    assert not (tmp_path/'x.zip').exists()

def test_ci_retains_original_trigger_and_uses_readonly_separate_runner_jobs():
    yaml=pytest.importorskip('yaml')
    ci=Path(__file__).parents[1]/'.github/workflows/ci.yml'
    d=yaml.load(ci.read_text(),Loader=yaml.BaseLoader)
    assert set(d['on'])=={'push','pull_request'}
    assert d['on']['push']['branches']==['main']
    assert d['jobs']['q3-worker']['strategy']['matrix']['shard']==['0','1','2']
    for job in ('q3-prepare','q3-worker','q3-collect'):
        j=d['jobs'][job]
        assert j['permissions']=={'contents':'read','actions':'read'}
        assert j['timeout-minutes']=='20'
        assert j['runs-on']=='ubuntu-24.04'
    condition=d['jobs']['q3-prepare']['if']
    assert '597' in condition and 'head.repo.full_name' in condition
    assert d['jobs']['q3-worker']['needs']=='q3-prepare'
    assert set(d['jobs']['q3-collect']['needs'])=={'q3-prepare','q3-worker'}
    assert 'q3_release160_20261019' in ci.read_text()
    assert 'production' not in str(d['jobs']['q3-worker']['strategy'])
