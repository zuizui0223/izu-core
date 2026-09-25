import json
from pathlib import Path

import pytest

from scripts import verify_model3_reproduction_exposure as verifier


def test_receipt_scope_and_identities():
    r = verifier.build_receipt()
    assert r['status'] == 'mathematical_verification_only'
    assert r['evolutionary_simulation_run'] is False
    assert {'scripts/model3_reproduction.py', 'scripts/model3_exposure.py',
            'docs/superpowers/specs/2026-09-25-model3-reproduction-exposure.md'} <= set(r['source_sha256'])
    assert all(len(h) == 64 for h in r['source_sha256'].values())
    assert all(c['passed'] and c['absolute_error'] <= 1e-10 for c in r['checks'])


def test_write_receipt_never_overwrites(tmp_path):
    path = tmp_path/'receipt.json'
    verifier.write_receipt(path)
    original = path.read_bytes()
    assert json.loads(original)['status'] == 'mathematical_verification_only'
    with pytest.raises(FileExistsError):
        verifier.write_receipt(path)
    assert path.read_bytes() == original


def test_bad_identity_does_not_create_receipt(monkeypatch, tmp_path):
    actual = verifier.reproductive_ledger
    def broken(*args, **kwargs):
        r = actual(*args, **kwargs)
        r['male_outcross'] += 1
        return r
    monkeypatch.setattr(verifier, 'reproductive_ledger', broken)
    path = tmp_path/'bad.json'
    with pytest.raises(ArithmeticError):
        verifier.write_receipt(path)
    assert not path.exists()
