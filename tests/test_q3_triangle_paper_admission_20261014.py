import json
import shutil
import zipfile

import pytest

from scripts import build_chapter2_unified_el_submission_bundle as bundle
from test_chapter2_unified_el_review_bundle_20261010 import fake_pdfs, supplementary_figures


def test_triangle_delivery_contains_frozen_full_readout(tmp_path):
    out = tmp_path / 'review.zip'
    bundle.build(out, figures=fake_pdfs(tmp_path), supplementary_figures=supplementary_figures(tmp_path))
    with zipfile.ZipFile(out) as z:
        raw = z.read('EVIDENCE/Q3_TRIANGLE_READOUT.json')
        assert raw == (bundle.ROOT / 'data/results/q3_triangle_20261014/READOUT.json').read_bytes()
        assert json.loads(z.read('EVIDENCE/Q3_TRIANGLE_INDEPENDENT_VERIFICATION.json'))['triplets'] == 8784
        assert '## S26.' in z.read('SUPPORTING_INFORMATION.md').decode()


def test_triangle_admission_rejects_altered_readout(tmp_path, monkeypatch):
    folder = tmp_path / 'data/results/q3_triangle_20261014'
    shutil.copytree(bundle.ROOT / 'data/results/q3_triangle_20261014', folder)
    (folder / 'READOUT.json').write_bytes(b'{}')
    monkeypatch.setattr(bundle, 'ROOT', tmp_path)
    with pytest.raises(ValueError, match='triangle source hash'):
        bundle.q3_triangle_materials()
