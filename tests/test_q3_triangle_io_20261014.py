import hashlib
import importlib
import json
from pathlib import Path
import sys
import zipfile

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))


def module():
    return importlib.import_module('q3_triangle_io_20261014')


def test_extracts_only_verified_allowlist_and_never_bytecode(tmp_path):
    path = tmp_path/'input.zip'
    with zipfile.ZipFile(path, 'w') as z:
        z.writestr('frozen_source/model.py', b'approved')
        z.writestr('frozen_source/__pycache__/model.cpython-311.pyc', b'never load')
    inventory = {'frozen_source/model.py': hashlib.sha256(b'approved').hexdigest()}
    with zipfile.ZipFile(path) as z:
        module().extract_registered(z, tmp_path/'out', inventory, lambda:None)
    assert (tmp_path/'out/frozen_source/model.py').read_bytes() == b'approved'
    assert not list((tmp_path/'out').rglob('*.pyc'))


@pytest.mark.parametrize('name', ['../escape', '/absolute', 'C:/absolute', 'a/../../escape',
                                  'frozen_source/__pycache__/model.pyc', 'a\\escape'])
def test_rejects_unsafe_or_bytecode_paths(tmp_path, name):
    path = tmp_path/'input.zip'
    with zipfile.ZipFile(path, 'w') as z:
        z.writestr(name, b'payload')
    with zipfile.ZipFile(path) as z, pytest.raises(ValueError):
        module().extract_registered(z, tmp_path/'out', {name:hashlib.sha256(b'payload').hexdigest()}, lambda:None)


def test_extraction_stops_on_hash_drift_before_writing_member(tmp_path):
    path = tmp_path/'input.zip'
    with zipfile.ZipFile(path, 'w') as z:
        z.writestr('model.py', b'changed')
    with zipfile.ZipFile(path) as z, pytest.raises(ValueError):
        module().extract_registered(z, tmp_path/'out', {'model.py':'0'*64}, lambda:None)
    assert not (tmp_path/'out/model.py').exists()


def test_archive_is_exclusive_and_hash_readback_detects_corruption(tmp_path):
    m = module()
    out = tmp_path/'out';out.mkdir()
    (out/'raw').mkdir();(out/'raw/one').write_bytes(b'raw fields')
    (out/'receipt.json').write_text('{"status":"PASS"}')
    path = tmp_path/'shard.zip'
    receipt = m.package(out, path, lambda:None)
    assert receipt['members'] == 3
    assert m.verify_container(path, lambda:None) == receipt['member_sha256']
    with pytest.raises(FileExistsError):
        m.package(out, tmp_path/'second.zip', lambda:None)
    bad = tmp_path/'bad.zip'
    with zipfile.ZipFile(path) as src, zipfile.ZipFile(bad, 'w') as dst:
        for name in src.namelist():
            dst.writestr(name, b'altered' if name == 'raw/one' else src.read(name))
    with pytest.raises(ValueError, match='hash'):
        m.verify_container(bad, lambda:None)


def test_container_rejects_duplicate_or_unmanifested_members(tmp_path):
    path = tmp_path/'bad.zip'
    with zipfile.ZipFile(path, 'w') as z:
        z.writestr('MANIFEST.json', '{}')
        z.writestr('foreign', 'bad')
    with pytest.raises(ValueError):
        module().verify_container(path, lambda:None)
