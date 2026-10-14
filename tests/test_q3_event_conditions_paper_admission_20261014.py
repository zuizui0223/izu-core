import json
import shutil

import pytest

from scripts import build_chapter2_unified_el_submission_bundle as builder


def test_event_restrictions_keep_mean_and_event_targets_separate():
    members, provenance = builder.q3_event_conditions_materials()
    summary = json.loads(members['EVIDENCE/Q3_EVENT_SUMMARY.json'])
    assert len(members) == len(provenance) == 5
    main = summary['blocks']['causal_main']
    confirmation = summary['blocks']['causal_confirmation']
    assert main['gain_capable_states'] == 12
    assert confirmation['gain_capable_states'] == 0
    assert main['joint']['01'] == 468 and main['joint']['10'] == 0
    assert confirmation['joint']['01'] == 0 and confirmation['joint']['10'] == 72
    assert summary['original_primary'] == summary['confirmation_margin_0_01'] == 'unresolved'


@pytest.mark.parametrize('name,field,value', [
    ('SUMMARY.json', 'original_primary', 'confirmed'),
    ('FRESH_RAW_REVIEW.json', 'pairs', 3903),
])
def test_wrong_result_or_incomplete_raw_scope_is_rejected(monkeypatch, tmp_path, name, field, value):
    relative = 'data/results/q3_event_conditions_paper_20261014'
    shutil.copytree(builder.ROOT / relative, tmp_path / relative)
    path = tmp_path / relative / name
    data = json.loads(path.read_bytes())
    data[field] = value
    path.write_text(json.dumps(data), encoding='utf-8')
    monkeypatch.setattr(builder, 'ROOT', tmp_path)
    with pytest.raises(ValueError):
        builder.q3_event_conditions_materials()
