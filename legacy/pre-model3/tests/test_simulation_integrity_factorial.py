import json
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from scripts import run_chapter2_conditional_why_diagnostics as diagnostics
from scripts.run_response_geometry_parameter_robustness import BASE, Pollinator, endpoint_on_trajectory, pollinator_trajectory


def test_corrected_name_does_not_authorize_changed_content(tmp_path, monkeypatch):
    (tmp_path / 'data/design').mkdir(parents=True)
    (tmp_path / 'scripts').mkdir()
    name = 'scripts/example.py'
    (tmp_path / name).write_text('changed\n')
    (tmp_path / 'data/design/chapter2_rng_stream_correction_20260922.json').write_text(json.dumps({
        'status': 'implementation_correction_protocol',
        'corrected_source_identity': {name: 'blob:' + '0' * 40},
    }))
    monkeypatch.setattr(diagnostics, 'ROOT', tmp_path)
    with pytest.raises(RuntimeError, match='identity mismatch'):
        diagnostics.verify_inputs({'input_identity': {name: 'sha256:' + '0' * 64}})


def test_all_parameters_are_locked():
    from scripts.chapter2_simulation_integrity import verify_model
    with pytest.raises(ValueError, match='configuration'):
        verify_model(replace(BASE, saturation=99))
    receipt = verify_model(BASE)
    assert receipt['resolved_configuration']['saturation'] == 2
    assert receipt['source_sha256']


def test_source_guard_accepts_newlines_but_rejects_content(tmp_path, monkeypatch):
    import hashlib
    from dataclasses import asdict
    from scripts import chapter2_simulation_integrity as integrity
    source = tmp_path / 'model.py'
    source.write_bytes(b'original\r\n')
    lock = tmp_path / 'lock.json'
    lock.write_text(json.dumps({'configuration': asdict(BASE), 'source_sha256': {
        'model.py': hashlib.sha256(b'original\n').hexdigest()}}))
    monkeypatch.setattr(integrity, 'ROOT', tmp_path)
    monkeypatch.setattr(integrity, 'LOCK', lock)
    assert integrity.verify_model(BASE)['source_sha256']
    source.write_text('different\n')
    with pytest.raises(ValueError, match='source identity'):
        integrity.verify_model(BASE)


def test_old_challenge_rejects_drift_before_simulation(monkeypatch):
    from scripts import audit_chapter2_postfreeze_grid_update_rule as audit
    monkeypatch.setattr(audit, 'BASE', replace(BASE, mainland=replace(BASE.mainland, partner_loss=.9)))
    with pytest.raises(ValueError, match='configuration'):
        audit.build()


def test_factorial_frozen_rule_reproduces_scalar():
    from scripts.audit_chapter2_update_factorial import endpoints
    grid = np.linspace(0, 1, 21)
    history = pollinator_trajectory(BASE.island, 98765, BASE)
    traits, services = endpoints(grid, history, BASE, threshold=True, target='best', damping=False)
    expected = np.array([endpoint_on_trajectory(x, history, BASE) for x in grid])
    np.testing.assert_allclose(traits, expected[:, 0], atol=1e-13)
    np.testing.assert_allclose(services, expected[:, 1], atol=1e-13)


def test_factorial_fixed_retains_traits_and_smooth_matches_reference():
    from scripts.audit_chapter2_update_factorial import endpoints
    from scripts.audit_chapter2_postfreeze_grid_update_rule import endpoint_with_rule
    grid = np.linspace(0, 1, 21)
    history = pollinator_trajectory(BASE.mainland, 98765, BASE)
    traits, services = endpoints(grid, history, BASE, threshold=False, target='centroid', damping=True)
    expected = np.array([endpoint_with_rule(x, history, BASE, 'smooth_weighted') for x in grid])
    np.testing.assert_allclose(traits, expected[:, 0], atol=1e-13)
    np.testing.assert_allclose(services, expected[:, 1], atol=1e-13)
    fixed, _ = endpoints(grid, history, BASE, threshold=False, target='fixed', damping=False)
    np.testing.assert_array_equal(fixed, grid)


def test_empty_history_and_empty_communities():
    from scripts.audit_chapter2_update_factorial import endpoints
    for history in [(), ((), ())]:
        x, y = endpoints(np.array([0., .5, 1.]), history, BASE, threshold=False, target='centroid', damping=True)
        np.testing.assert_array_equal(x, [0, .5, 1])
        np.testing.assert_array_equal(y, [0, 0, 0])


def test_factorial_includes_eight_rules_and_fixed():
    from scripts.audit_chapter2_update_factorial import RULES, paired_effects
    assert len(RULES) == 9
    rows = []
    for rule in RULES:
        rows.append({'rule': rule, 'seed': 1, 'k': 1, 'S': float(RULES[rule]['threshold']), 'C': 0., 'I': 0.})
    effects = paired_effects(rows)
    assert len(effects) == 12
    assert all(e['delta_S'] == 1 for e in effects if e['factor'] == 'threshold')
