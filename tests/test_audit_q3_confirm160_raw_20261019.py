"""Only the pre-existing 3x3 engineering namespace may execute in fixtures."""
import ast
import io
import json
from pathlib import Path
import shutil
import subprocess
import zipfile

import numpy as np
import pytest

from scripts import audit_q3_confirm160_raw_20261019 as audit


def audit_technical(root):
    # CI may have a depth-one checkout; fixture provenance belongs to that
    # checkout, whereas production CLI remains pinned to its execution SHA.
    head = subprocess.run(['git','rev-parse','HEAD'],cwd=audit.ROOT,
                          check=True,capture_output=True,text=True).stdout.strip()
    return audit.audit(root,technical=True,source_commit=head)


def write_hashes(root):
    (root/'hashes-0.txt').write_text(''.join(
        f'{audit.file_digest(root/name)}  {name}\n'
        for name in ('raw-shard-0.zip','seal-0.json')),encoding='utf8')


@pytest.fixture(scope='module')
def technical_release(tmp_path_factory):
    from scripts import q3_production160_20261019 as producer
    from scripts import q3_archive160_20261019 as archive
    tmp = tmp_path_factory.mktemp('independent-raw-audit')
    run = tmp/'run'
    producer.initialize(run,technical=True)
    producer.run(run)
    seal = producer.seal(run)
    assets = tmp/'assets'
    assets.mkdir()
    archive.pack(run,assets/'raw-shard-0.zip')
    (assets/'seal-0.json').write_bytes(audit.canonical(seal))
    (assets/'SUMMARY160.json').write_bytes(audit.canonical(producer.aggregate([seal],technical=True)))
    write_hashes(assets)
    return assets


def test_full_raw_audit_and_independent_mathematics(technical_release):
    result = audit_technical(technical_release)
    assert result['status']=='PASS_INDEPENDENT_RAW_ARITHMETIC_AUDIT'
    assert (result['crossings'],result['raw_files'],result['saved_states'])==(9,54,2304)
    assert len(result['epsilon_descriptive'])==5
    summary=json.loads((technical_release/'SUMMARY160.json').read_bytes())
    assert result['primary']['joint_positive']==summary['primary']['joint_positive']


@pytest.mark.parametrize('change',['missing','extra','hash','summary','contract'])
def test_reject_incomplete_or_inconsistent_release(technical_release,tmp_path,change):
    root=tmp_path/'assets';shutil.copytree(technical_release,root)
    if change=='missing': (root/'SUMMARY160.json').unlink()
    elif change=='extra': (root/'unregistered.txt').write_text('extra')
    elif change=='hash': (root/'hashes-0.txt').write_text('0'*64+'  raw-shard-0.zip\n')
    elif change=='summary':
        s=json.loads((root/'SUMMARY160.json').read_bytes());s['genetic_loss_inputs'][0][0][0]^=1
        (root/'SUMMARY160.json').write_bytes(audit.canonical(s))
    else:
        s=json.loads((root/'seal-0.json').read_bytes());s['contract']['plan']['founders'][0]+=1
        s['seal_sha256']=audit.digest(audit.canonical({k:v for k,v in s.items() if k!='seal_sha256'}))
        (root/'seal-0.json').write_bytes(audit.canonical(s));write_hashes(root)
    with pytest.raises(ValueError):audit_technical(root)


def test_reject_rehashed_archive_duplicate_member(technical_release,tmp_path):
    root=tmp_path/'assets';shutil.copytree(technical_release,root)
    with zipfile.ZipFile(root/'raw-shard-0.zip','a') as z:
        with pytest.warns(UserWarning,match='Duplicate name'):
            z.writestr('RUN.json',z.read('RUN.json'))
    write_hashes(root)
    with pytest.raises(ValueError,match='archive member inventory'):
        audit_technical(root)


@pytest.mark.parametrize('change',['founder','birth','padding','payload','fork'])
def test_snapshot_semantic_failures_after_valid_payload_hash(technical_release,change):
    with zipfile.ZipFile(technical_release/'raw-shard-0.zip') as z:
        contract=json.loads(z.read('RUN.json'))
        name='states/9100001_9200001_fixed_prefix.npz'
        raw=z.read(name)
    with np.load(io.BytesIO(raw),allow_pickle=False) as saved:
        meta=json.loads(saved['_meta'].tobytes())
        arrays={k:saved[k].copy() for k in saved.files if k!='_meta'}
    initial=audit.founder_arrays(9100001)
    if change=='founder':
        arrays['alleles'][0,0,0,0]=.123
    elif change=='birth':arrays['birth_years'][1,0]=999
    elif change=='padding':
        arrays['counts'][1]=47
        arrays['ids'][1,47]=999
    elif change=='fork':meta['parent_payload_sha256']='invented'
    h=__import__('hashlib').sha256(audit.canonical({k:v for k,v in meta.items() if k!='payload_sha256'}))
    for key in sorted(arrays):
        a=arrays[key];h.update(audit.canonical([key,a.dtype.str,list(a.shape)]));h.update(a.tobytes())
    meta['payload_sha256']=h.hexdigest() if change!='payload' else '0'*64
    out=io.BytesIO();np.savez_compressed(out,_meta=np.frombuffer(audit.canonical(meta),dtype=np.uint8),**arrays)
    with pytest.raises(ValueError):audit.snapshot(out.getvalue(),meta['task'],contract,initial)


def test_extinction_order_and_degenerate_inference():
    assert audit.events([.625,.375,None],.5)==(True,False,1)
    assert audit.events([.625,None,None],.5)==(False,True,None)
    assert audit.events([.625,.5,.5],.5)==(False,False,None)
    result=audit.infer(np.zeros((3,3,2),int),np.ones((3,3,2,2),int))
    assert all(x['classification']=='degenerate_unresolved' and x['interval'] is None
               for x in result['endpoints'])


def test_auditor_has_no_producer_imports():
    tree=ast.parse(Path(audit.__file__).read_text())
    modules=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Import):modules.extend(x.name for x in node.names)
        elif isinstance(node,ast.ImportFrom):modules.append(node.module or '')
    assert not any(m.startswith('scripts') or 'model3' in m for m in modules)
