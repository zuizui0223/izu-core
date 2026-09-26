import json
from hashlib import sha256
import pytest
from scripts.model3_island.design import digest, canonical
from scripts.model3_island_continue import pending_cases

def fixture_case(tmp_path):
    case = {'case_id': 'a', 'value': 1}
    folder = tmp_path / 'a'
    folder.mkdir()
    (folder / 'input.json').write_bytes(canonical(case))
    (folder / 'arrays.npz').write_bytes(b'original')
    receipt = {'case_hash': digest(case), 'manifest_hash': 'm', 'mode': 'production',
               'status': 'complete', 'arrays_sha256': sha256(b'original').hexdigest()}
    (folder / 'receipt.json').write_text(json.dumps(receipt))
    return case, folder

def test_preserves_complete_and_returns_missing(tmp_path):
    case, folder = fixture_case(tmp_path)
    before = (folder / 'receipt.json').read_bytes()
    missing = {'case_id': 'b'}
    assert pending_cases([case, missing], tmp_path, 'm') == [missing]
    assert (folder / 'receipt.json').read_bytes() == before

@pytest.mark.parametrize('target', ['arrays.npz', 'input.json', 'receipt.json'])
def test_rejects_corruption(tmp_path, target):
    case, folder = fixture_case(tmp_path)
    (folder / target).write_bytes(b'corrupt')
    with pytest.raises(ValueError):
        pending_cases([case], tmp_path, 'm')

def test_rejects_unexpected_receipt(tmp_path):
    fixture_case(tmp_path)
    with pytest.raises(ValueError):
        pending_cases([], tmp_path, 'm')

def test_continuation_preserves_stop_and_uses_only_missing(tmp_path, monkeypatch):
    import scripts.model3_island_continue as runner
    import numpy as np
    case, folder = fixture_case(tmp_path)
    case['cohort'] = 'production'
    (folder/'input.json').write_bytes(canonical(case))
    r=json.loads((folder/'receipt.json').read_text());r['case_hash']=digest(case)
    doc={'source_hashes': {}, 'storage': {}, 'resource_limits': {'memory_mb': 10000, 'output_mb':100, 'min_free_mb':0}}
    mh=digest(doc);r['manifest_hash']=mh;(folder/'receipt.json').write_text(json.dumps(r))
    original_receipt=(folder/'receipt.json').read_bytes()
    missing={'case_id':'b','cohort':'production'}
    original=canonical({'complete':False,'completed':1,'stop_reason':'runtime_budget'})
    (tmp_path/'campaign_status.json').write_bytes(original)
    (tmp_path/'manifest.json').write_bytes(canonical({'identity':{'manifest_hash':mh,'mode':'production'},'design':doc}))
    design=tmp_path/'design.json'; design.write_bytes(canonical(doc))
    amendment=tmp_path/'amendment.json'; amendment.write_bytes(canonical({'id':'test','manifest_hash':mh,
        'runner_sha256':sha256(__import__('pathlib').Path(runner.__file__).read_bytes()).hexdigest(),
        'original_status_sha256':sha256(original).hexdigest(),'missing_cases':1,'additional_runtime_seconds':10}))
    monkeypatch.setattr(runner,'source_hashes',lambda:{})
    monkeypatch.setattr(runner,'verify_snapshot',lambda *a,**kw:None)
    monkeypatch.setattr(runner,'compile_design',lambda d:[case,missing])
    seen=[]
    def execute(c,d,check):
        seen.append(c['case_id']);check();return {'x':np.array([1.])}
    monkeypatch.setattr(runner,'execute_case',execute)
    monkeypatch.setattr(runner,'pack_result',lambda r,s:r)
    result=runner.run(design,tmp_path,amendment)
    assert result['complete'] and result['executed']==1 and seen==['b']
    assert (folder/'receipt.json').read_bytes()==original_receipt
    assert (tmp_path/'continuations/test/original_campaign_status.json').read_bytes()==original
    with pytest.raises(ValueError):
        runner.run(design,tmp_path,amendment)
