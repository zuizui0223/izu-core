import importlib.util
from pathlib import Path
import sys

import pytest


def api():
    scripts=Path(__file__).parents[1]/'scripts';sys.path.insert(0,str(scripts))
    spec=importlib.util.spec_from_file_location('q3_run_test',scripts/'run_q3_futures_20261014.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def manifest(m):
    return dict(approved=True,experiment='izu-q3-conditional-restoration-v1-20261014',new_trajectories=7808,
        delta=.01,max_native_calls=1981472,max_worker_seconds=28800,max_disk_bytes=17179869184,workers=2,
        python='3.11.14',numpy='2.2.6',reviewed_commit='a'*40,
        protocol_sha256=m.PROTOCOL_SHA,preflight_sha256=m.PREFLIGHT_SHA,
        archive_sha256=m.ARCHIVE_SHA,source_input_sha256=m.SOURCE_SHA,
        authorization_sha256=m.AUTHORIZATION_SHA,
        code_sha256={p:'a'*64 for p in m.REQUIRED_FILES})


@pytest.mark.parametrize('damage',['empty','omitted_runner','extra','hash','count','source','approval','reviewed_commit'])
def test_approval_contract_rejects_incomplete_or_changed_manifest(damage):
    m=api();x=manifest(m);m.validate_execution_document(x)
    if damage=='empty':x['code_sha256']={}
    elif damage=='omitted_runner':del x['code_sha256']['scripts/run_q3_futures_20261014.py']
    elif damage=='extra':x['code_sha256']['alien.py']='a'*64
    elif damage=='hash':x['code_sha256']['scripts/run_q3_futures_20261014.py']='broken'
    elif damage=='count':x['new_trajectories']=7809
    elif damage=='source':x['archive_sha256']='b'*64
    elif damage=='approval':x['approved']=False
    else:x['reviewed_commit']='main'
    with pytest.raises(ValueError):m.validate_execution_document(x)


def test_exact_numpy_version_attribute_and_runtime_gate(monkeypatch):
    m=api();x=manifest(m)
    monkeypatch.setattr(m.platform,'python_version',lambda:'3.11.14')
    monkeypatch.setattr(m.np,'__version__','2.2.6')
    m.check_runtime(x)
    monkeypatch.setattr(m.np,'__version__','2.2.5')
    with pytest.raises(ValueError):m.check_runtime(x)


def test_packaging_checks_deadline_during_streaming(tmp_path):
    m=api();source=tmp_path/'out';source.mkdir();(source/'raw').write_bytes(b'x'*(4*1024*1024))
    calls=[]
    def guard():
        calls.append(1)
        if len(calls)>=4:raise ValueError('deadline')
    with pytest.raises(ValueError,match='deadline'):
        m.package_archive(source,tmp_path/'out.zip',{'raw':m.sha((source/'raw').read_bytes())},guard)
    assert len(calls)==4
