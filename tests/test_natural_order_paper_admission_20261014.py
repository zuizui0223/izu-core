import json
from pathlib import Path
import shutil
import zipfile

import pytest

from scripts.natural_order_paper_admission_20261014 import materials

ROOT = Path(__file__).resolve().parents[1]
REL = Path('data/results/natural_order_existing_paper_20261014')


def copied(tmp_path):
    shutil.copytree(ROOT / REL, tmp_path / REL)
    return tmp_path


def test_complete_observational_groups_are_delivered_without_promotion():
    files, provenance = materials(ROOT)
    assert len(files) == len(provenance) == 3
    summary = json.loads(files['EVIDENCE/NATURAL_ORDER_SUMMARY.json'])
    assert len(summary['groups']) == 36
    assert summary['exploratory'] is True
    assert summary['randomized_order_effect'] is False
    assert summary['mean_control_executed'] is False
    strict = {(g['block'], g['category']): (g['n'], g['survived'])
              for g in summary['groups'] if g['target'] == 1.05}
    assert strict['main', 'assurance_first'] == (52, 10)
    assert strict['main', 'investment_first'] == (26, 6)
    assert strict['confirmation', 'assurance_first'] == (58, 22)
    assert strict['confirmation', 'investment_first'] == (37, 4)
    assert all(b'zuizui0223' not in raw for raw in files.values())


def test_changed_survival_count_cannot_enter_packet(tmp_path):
    root = copied(tmp_path)
    p = root / REL / 'SUMMARY.json'
    value = json.loads(p.read_text(encoding='utf-8'))
    value['groups'][0]['survived'] += 1
    p.write_text(json.dumps(value), encoding='utf-8')
    with pytest.raises(ValueError, match='frozen'):
        materials(root)


def test_missing_independent_review_cannot_enter_packet(tmp_path):
    root = copied(tmp_path)
    (root / REL / 'INDEPENDENT_REVIEW.json').unlink()
    with pytest.raises(FileNotFoundError):
        materials(root)


def test_line_ending_portability_changes_no_delivered_value(tmp_path):
    root = copied(tmp_path)
    before, _ = materials(root)
    for p in (root / REL).iterdir():
        canonical = p.read_bytes().replace(b'\r\n', b'\n')
        p.write_bytes(canonical.replace(b'\n', b'\r\n'))
    after, provenance = materials(root)
    assert after == before
    assert all('LF' in item['transformation'] for item in provenance.values())


def test_actual_review_archive_includes_the_independent_observational_evidence(tmp_path):
    from scripts.build_chapter2_unified_el_submission_bundle import build
    path = tmp_path / 'review.zip'
    build(path)
    with zipfile.ZipFile(path) as archive:
        summary = json.loads(archive.read('EVIDENCE/NATURAL_ORDER_SUMMARY.json'))
        review = json.loads(archive.read('EVIDENCE/NATURAL_ORDER_INDEPENDENT_REVIEW.json'))
        assert len(summary['groups']) == review['groups'] == 36
        assert review['preparations'] == 1024 and review['futures'] == 2048
        assert summary['randomized_order_effect'] is False
        assert b'## S25.' in archive.read('SUPPORTING_INFORMATION.md')
