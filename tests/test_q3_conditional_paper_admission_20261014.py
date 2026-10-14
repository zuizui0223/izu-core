import json
import shutil
import pytest
from scripts import build_chapter2_unified_el_submission_bundle as builder


def test_conditional_fixed_state_result_keeps_old_primary_and_event_difference():
    members, provenance = builder.q3_conditional_materials()
    value = json.loads(members['EVIDENCE/Q3_CONDITIONAL_READOUT.json'])
    assert value['original_primary'] == 'unresolved_unchanged'
    assert value['directional_replication'] == 'positive'
    assert value['means']['causal_confirmation']['practical'] == 'unresolved'
    assert value['survival']['both_alive'] == 3904
    assert len(members) == len(provenance) == 13
    counts = {block: [sum(r['event_counts'][arm] for r in value['case_summaries']
                         if r['block'] == block and r['trigger'] is not None)
                     for arm in ('native', 'restored')]
              for block in ('causal_main', 'causal_confirmation')}
    assert counts == {'causal_main': [640, 1108], 'causal_confirmation': [1280, 1208]}


@pytest.mark.parametrize('name,field,value', [
    ('INDEPENDENT_SAVED_ARRAYS.json', 'paths', 7807),
    ('READOUT.json', 'target', 'unconditional_natural_order_benefit'),
])
def test_missing_full_domain_or_changed_target_cannot_be_delivered(monkeypatch, tmp_path, name, field, value):
    relative = 'data/results/q3_conditional_paper_20261014'
    shutil.copytree(builder.ROOT / relative, tmp_path / relative)
    path = tmp_path / relative / name
    data = json.loads(path.read_bytes()); data[field] = value
    path.write_text(json.dumps(data), encoding='utf-8')
    monkeypatch.setattr(builder, 'ROOT', tmp_path)
    with pytest.raises(ValueError):
        builder.q3_conditional_materials()
