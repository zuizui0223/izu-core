import hashlib
import importlib.util
import json
from pathlib import Path
import zipfile
import pytest

spec = importlib.util.spec_from_file_location('remote_atom', Path(__file__).parents[1] / 'scripts/resume_frozen_atom_20261011.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


@pytest.mark.parametrize('failure', ['bundle', 'source', 'traversal'])
def test_rejects_untrusted_transfer(tmp_path, monkeypatch, failure):
    monkeypatch.setattr(m, 'BASE', tmp_path / 'restored')
    bundle = tmp_path / 'input.zip'
    with zipfile.ZipFile(bundle, 'w') as z:
        z.writestr('source.py', 'original')
        z.writestr('remote_transfer_manifest.json', json.dumps({'files': {'source.py': 'wrong'}}))
        if failure == 'traversal':
            z.writestr('../escape.txt', 'escape')
    sha = m.digest(bundle) if failure != 'bundle' else 'wrong'
    with pytest.raises(ValueError):
        m.extract(bundle, sha)
    assert not (tmp_path / 'escape.txt').exists()


def test_restores_exact_bytes(tmp_path, monkeypatch):
    monkeypatch.setattr(m, 'BASE', tmp_path / 'restored')
    raw = b'unchanged\r\nsource\r\n'
    bundle = tmp_path / 'input.zip'
    manifest = {'files': {'source.py': hashlib.sha256(raw).hexdigest()}}
    with zipfile.ZipFile(bundle, 'w') as z:
        z.writestr('source.py', raw)
        z.writestr('remote_transfer_manifest.json', json.dumps(manifest))
    assert m.extract(bundle, m.digest(bundle)) == manifest
    assert (m.BASE / 'source.py').read_bytes() == raw
