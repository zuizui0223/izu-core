import json
import shutil

import pytest

from scripts.validate_chapter2_completed_evidence_20261019 import (
    ROOT, SOURCES, MANUSCRIPT, EXTENDED, validate,
)


@pytest.fixture
def isolated(tmp_path):
    for name in [MANUSCRIPT, EXTENDED, *SOURCES.values()]:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, path)
    return tmp_path


def test_current_selected_completed_claims():
    result = validate()
    assert result['status'] == 'PASS_SELECTED_COMPLETED_EVIDENCE_CLAIMS'
    assert result['raw_archive_reaudited'] is False
    assert set(result['source_sha256']) == set(SOURCES)


@pytest.mark.parametrize('source', ['pollen', 'confirm', 'variation', 'transfer'])
def test_source_estimate_or_denominator_change_is_detected(isolated, source):
    path = isolated / SOURCES[source]
    data = json.loads(path.read_text())
    if source == 'pollen':
        data['interactions'][0]['interaction_A'] += .01
    elif source == 'confirm':
        data['primary']['endpoints'][0]['estimate'] += .01
    elif source == 'variation':
        row = next(x for x in data['contrasts'] if x['trait'] == 'I'
                   and x['budget'] == 'B8' and x['endpoint'] == 'occupied_polymorphic_duration')
        row['estimate'] += 1
    else:
        data['allocated'] -= 1
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError):
        validate(isolated)


@pytest.mark.parametrize('old,new', [
    ('+0.1037 and +0.0836', '+0.2037 and +0.0836'),
    ('+8.33 percentage points', '+9.33 percentage points'),
    ('2.628 updates at B8', '3.628 updates at B8'),
    ('10,240 futures', '10,241 futures'),
    ('shortened occupied I-polymorphic', 'extended occupied I-polymorphic'),
    ('704,1,024,961,1,024 and1,021', '705,1,024,961,1,024 and1,021'),
])
def test_wrong_manuscript_claim_is_detected(isolated, old, new):
    path = isolated / (MANUSCRIPT if old == '+8.33 percentage points' else EXTENDED)
    text = path.read_text(encoding='utf8')
    assert old in text
    path.write_text(text.replace(old, new), encoding='utf8')
    with pytest.raises(ValueError):
        validate(isolated)


def test_transfer_occupancy_drift_even_with_conserved_total(isolated):
    path = isolated / SOURCES['transfer_tables']
    data = json.loads(path.read_text())
    data['tables'][0]['occupied'] += 1
    data['tables'][0]['extinct'] -= 1
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError):
        validate(isolated)


@pytest.mark.parametrize('source', ['pollen', 'confirm', 'variation', 'transfer'])
def test_incomplete_source_is_rejected(isolated, source):
    path = isolated / SOURCES[source]
    data = json.loads(path.read_text())
    data['status'] = 'INCOMPLETE'
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError):
        validate(isolated)


def test_extended_link_is_required(isolated):
    path=isolated/MANUSCRIPT
    path.write_text(path.read_text(encoding='utf8').replace('CHAPTER2_FIVE_RESULTS_EXTENDED_EVIDENCE_20261021.md','missing.md'),encoding='utf8')
    with pytest.raises(ValueError,match='missing extended evidence link'):validate(isolated)


def test_correct_supplement_does_not_mask_bad_main_survival(isolated):
    path=isolated/MANUSCRIPT
    path.write_text(path.read_text(encoding='utf8').replace('+92.71 points','+93.71 points'),encoding='utf8')
    with pytest.raises(ValueError,match='main survival interaction'):validate(isolated)
