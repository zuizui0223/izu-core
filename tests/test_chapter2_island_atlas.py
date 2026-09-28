from copy import deepcopy
from pathlib import Path
import json

import pytest

from scripts.build_chapter2_island_atlas import build_atlas, validate_coordinate

ROOT = Path(__file__).resolve().parents[1]


def test_observational_and_literature_denominators_remain_distinct():
    atlas = build_atlas(ROOT)
    assert len(atlas['coordinates']) == 42
    assert len({r['source_study_id'] for r in atlas['coordinates']}) == 6
    assert atlas['units']['network_observations'] == 42
    assert atlas['units']['literature_entries'] == 42
    assert atlas['units']['literature_geographic_labels'] == 37
    assert atlas['units']['propagation_layers'] == 14
    assert atlas['empirical_k_mapping'] is None
    assert atlas['inherited_trajectory_validation'] is False


def test_izu_negative_deletion_and_species_directions_are_preserved():
    atlas = build_atlas(ROOT)
    assert atlas['izu']['pollen']['leave_one_out']['hachijo'] < 0
    assert all(v > 0 for v in atlas['izu']['matching']['leave_one_out'].values())
    rows = atlas['izu']['species']
    assert len(rows) == 8
    assert sum(float(r['pollen_delta_post_minus_oshima']) < 0 for r in rows) == 4
    assert all(float(r['matching_delta_post_minus_oshima']) < 0 for r in rows)
    assert len(atlas['source_sha256']) >= 11


def test_percentile_interval_need_not_contain_point():
    row = deepcopy(build_atlas(ROOT)['coordinates'][0])
    row['breadth_D1'] = 2.0
    row['breadth_D1_ci95'] = [2.1, 2.3]
    validate_coordinate(row)


@pytest.mark.parametrize('key,value', [('breadth_D1', 0), ('phi', float('nan')), ('phi', 1.1)])
def test_invalid_coordinates_are_rejected(key, value):
    row = deepcopy(build_atlas(ROOT)['coordinates'][0])
    row[key] = value
    with pytest.raises(ValueError):
        validate_coordinate(row)


def test_reversed_interval_rejected():
    row = deepcopy(build_atlas(ROOT)['coordinates'][0])
    row['phi_ci95'] = [0.8, 0.2]
    with pytest.raises(ValueError):
        validate_coordinate(row)


def test_source_native_hawaii_identity_and_izu_analysis_units():
    atlas = build_atlas(ROOT)
    hawaii = next(r for r in atlas['coordinates'] if 'hawaii' in r['source_study_id'])
    assert hawaii['system_id'] == 'pohakuloa_high_elevation_dryland_pollination_community'
    assert atlas['izu']['matching']['n_analysis_rows'] == 25
    assert atlas['izu']['pollen']['n_analysis_rows'] == 78
    assert atlas['izu']['pollen']['n_plant_taxa'] == 10
    assert 'site' in atlas['izu']['pollen']['analysis_unit']


@pytest.mark.parametrize('defect', ['nonfinite', 'missing_site'])
def test_invalid_izu_stage_fails_closed(tmp_path, defect):
    for rel in build_atlas(ROOT)['source_sha256']:
        target = tmp_path / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / rel).read_bytes())
    target = tmp_path / 'data/predictive_meta/hiraiwa_ushimaru_matching_to_pollen.json'
    payload = json.loads(target.read_text())
    if defect == 'nonfinite':
        payload['fixed_effect_subsets']['izu_five_islands']['tm_coefficient'] = float('nan')
    else:
        del payload['leave_one_site_sensitivity']['izu_five_islands']['tm_coefficients_by_omitted_site']['hachijo']
    target.write_text(json.dumps(payload))
    with pytest.raises(ValueError):
        build_atlas(tmp_path)
