"""Completed intervention admission must reject edited or incomplete evidence."""
import gzip
import hashlib
import json
import shutil
from pathlib import Path
import pytest
from scripts import natural_order_mean_paper_admission_20261015 as admission
ROOT = Path(__file__).resolve().parents[1]

def test_completed_intake_preserves_full_scope():
    members, derivations = admission.materials(ROOT)
    assert len(members) == len(derivations) == 3
    value = json.loads(gzip.decompress(members['EVIDENCE/NATURAL_ORDER_MEAN_READOUT.json.gz']))
    assert value['scientific_paths'] == value['independent_replays'] == 2048
    assert value['references'] == 8 and len(value['groups']) == 36
    assert value['completed_updates'] == 820804

@pytest.mark.parametrize('name', ['READOUT.json.gz', 'INDEPENDENT_ADMISSION.json', 'PUBLIC_READBACK.json'])
def test_changed_evidence_is_rejected(tmp_path, name):
    target = tmp_path / admission.FOLDER
    shutil.copytree(ROOT / admission.FOLDER, target)
    p = target / name
    p.write_bytes(p.read_bytes() + b' ')
    with pytest.raises(ValueError, match='frozen mean-control evidence'):
        admission.materials(tmp_path)

def test_pending_independent_result_rejected_even_if_pin_changed(tmp_path, monkeypatch):
    target = tmp_path / admission.FOLDER
    shutil.copytree(ROOT / admission.FOLDER, target)
    p = target / 'INDEPENDENT_ADMISSION.json'
    value = json.loads(p.read_bytes())
    next(iter(value.values()))['summary']['status'] = 'PENDING'
    raw = (json.dumps(value) + '\n').encode()
    p.write_bytes(raw)
    pins = dict(admission.PINS)
    pins[p.name] = hashlib.sha256(raw).hexdigest()
    monkeypatch.setattr(admission, 'PINS', pins)
    with pytest.raises(ValueError, match='independent mean-control admission'):
        admission.materials(tmp_path)
