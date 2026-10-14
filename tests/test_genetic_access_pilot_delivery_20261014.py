import json

import pytest

import scripts.build_chapter2_unified_el_submission_bundle as builder


def test_pilot_delivery_preserves_exploratory_and_demographic_scope():
    members, provenance = builder.genetic_access_pilot_materials()
    result = json.loads(members['EVIDENCE/GENETIC_ACCESS_FROZEN_EXPLORATORY_READOUT.json'])
    assert result['all_starts'] == 1536
    assert result['n_paired_stochastic_history_clusters'] == 128
    assert result['overall_six_class_counts'] == {
        'assurance_first': 316, 'investment_first': 416,
        'near_simultaneous': 223, 'assurance_only': 555,
        'investment_only': 15, 'neither': 11,
    }
    assert 'NOT_Q1_Q2_CONFIRMATION' in result['status']
    assert len(members) == len(provenance) == 12


def test_pilot_delivery_rejects_changed_admitted_result(monkeypatch, tmp_path):
    original = builder.ROOT
    relative = 'data/results/genetic_access_pilot_20261014'
    target = tmp_path / relative
    target.mkdir(parents=True)
    for source in (original / relative).iterdir():
        (target / source.name).write_bytes(source.read_bytes())
    result = target / 'FROZEN_EXPLORATORY_READOUT.json'
    result.write_bytes(result.read_bytes() + b' ')
    monkeypatch.setattr(builder, 'ROOT', tmp_path)
    with pytest.raises(ValueError, match='genetic-access frozen evidence differs'):
        builder.genetic_access_pilot_materials()
