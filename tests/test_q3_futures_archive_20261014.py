"""Raw-only tamper checks for the external archive/receipt bindings."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from verify_q3_futures_archive_20261014 import verify_execution_binding, verify_endpoint_binding


def test_execution_binding_rejects_substitution(tmp_path):
    preflight = b'{"cases": []}'
    helper = b'raw-only helper bytes'
    (tmp_path/'preflight.json').write_bytes(preflight)
    (tmp_path/'helper.py').write_bytes(helper)
    execution = dict(preflight_sha256=hashlib.sha256(preflight).hexdigest(),
                     code_sha256={'helper.py': hashlib.sha256(helper).hexdigest()})
    raw=json.dumps(execution).encode()
    expected=hashlib.sha256(raw).hexdigest()
    archive=dict(execution=execution, execution_sha256=expected, github_sha='commit',github_run_id='run')
    receipt=dict(execution_sha256=expected,github_sha='commit',github_run_id='run')
    verify_execution_binding(tmp_path,raw,expected,archive,receipt,'preflight.json')
    changed=deepcopy(archive);changed['execution']['preflight_sha256']='foreign'
    with pytest.raises(ValueError,match='archived execution object'):
        verify_execution_binding(tmp_path,raw,expected,changed,receipt,'preflight.json')
    with pytest.raises(ValueError,match='approved execution bytes'):
        verify_execution_binding(tmp_path,raw+b' ',expected,archive,receipt,'preflight.json')
    (tmp_path/'preflight.json').write_bytes(b'{}')
    with pytest.raises(ValueError,match='preflight identity'):
        verify_execution_binding(tmp_path,raw,expected,archive,receipt,'preflight.json')
    (tmp_path/'preflight.json').write_bytes(preflight)
    (tmp_path/'helper.py').write_bytes(b'changed')
    with pytest.raises(ValueError,match='code identity'):
        verify_execution_binding(tmp_path,raw,expected,archive,receipt,'preflight.json')


def test_raw_endpoint_binding_rejects_mean_survival_and_cross_pair_substitution():
    raw=dict(metadata=dict(key='state',replicate=2,arm='restored'),terminal_I=.375,survived=True)
    record=dict(key='state',replicate=2,restored_I=.375,restored_survived=True)
    verify_endpoint_binding(record,'restored',raw)
    for name,value in [('restored_I',.5),('restored_survived',False),('key','other'),('replicate',3)]:
        changed={**record,name:value}
        with pytest.raises(ValueError):
            verify_endpoint_binding(changed,'restored',raw)
    with pytest.raises(ValueError):
        verify_endpoint_binding(record,'restored',{**raw,'metadata':{**raw['metadata'],'arm':'native'}})
    extinct={**raw,'terminal_I':None,'survived':False}
    verify_endpoint_binding({**record,'restored_I':None,'restored_survived':False},'restored',extinct)
    with pytest.raises(ValueError):
        verify_endpoint_binding(record,'restored',extinct)
