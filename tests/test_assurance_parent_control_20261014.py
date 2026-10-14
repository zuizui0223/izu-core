from dataclasses import dataclass
from types import SimpleNamespace
import numpy as np
import pytest
from scripts import assurance_parent_control_20261014 as control


def ledger(o, s):
    return SimpleNamespace(outcross=np.asarray(o, float), self_viable=np.asarray(s, float),
                           ovules=np.ones(len(s)))


def test_reference_class_rescaling_retains_native_totals_not_uniform_parents():
    native = ledger([[0, 2], [4, 0]], [3, 1])
    shadow = ledger([[0, 1], [2, 0]], [1, 3])
    result = control.rescale_shadow(native, shadow)
    np.testing.assert_allclose(result.outcross, native.outcross)
    np.testing.assert_allclose(result.self_viable, [1, 3])
    assert result.outcross.sum() == native.outcross.sum()
    assert result.self_viable.sum() == native.self_viable.sum()
    np.testing.assert_array_equal(result.ovules, native.ovules)


def test_native_zero_classes_remain_zero_and_missing_shadow_support_stops():
    result = control.rescale_shadow(ledger([[0]], [0]), ledger([[0]], [2]))
    assert result.self_viable[0] == 0
    with pytest.raises(ValueError, match='shadow support'):
        control.rescale_shadow(ledger([[0]], [1]), ledger([[0]], [0]))
    result = control.rescale_shadow(ledger(np.empty((0, 0)), []), ledger(np.empty((0, 0)), []))
    assert result.outcross.shape == (0, 0)


@pytest.mark.parametrize('o,s', [([[1]], [2]), ([[0, 1]], [1]), ([[0]], [-1]), ([[0]], [np.nan])])
def test_invalid_sampling_inputs_fail_closed(o, s):
    with pytest.raises(ValueError):
        control.rescale_shadow(ledger(o, s), ledger([[0]], [1]))


@dataclass
class State:
    alleles: np.ndarray
    ids: np.ndarray


def fake_reproduction(state, visitors, config, policy):
    assert policy == 'native'
    traits = state.alleles.mean(axis=2)
    return ledger(np.zeros((len(traits), len(traits))),
                  traits[:, 2] * np.exp(-traits[:, 1] ** 2))


def test_shadow_changes_only_A_expression_without_changing_inherited_state(monkeypatch):
    monkeypatch.setattr(control.native, 'expression_ledger', fake_reproduction)
    genes = np.array([[[.5, .5], [.2, .2], [.1, .3]], [[.5, .5], [.2, .2], [.7, .9]]])
    state = State(genes.copy(), np.arange(2))
    biological, sampled, shadow = control.ledgers(state, None, None)
    np.testing.assert_array_equal(state.alleles, genes)
    np.testing.assert_allclose(sampled.self_viable, np.full(2, biological.self_viable.sum() / 2))
    assert sampled.self_viable.sum() == pytest.approx(biological.self_viable.sum())
    assert not np.array_equal(shadow.self_viable, biological.self_viable)


def test_indirect_A_response_through_MI_is_retained(monkeypatch):
    monkeypatch.setattr(control.native, 'expression_ledger', fake_reproduction)
    genes = np.array([[[.5, .5], [.1, .1], [.2, .2]], [[.5, .5], [.9, .9], [.8, .8]]])
    state = State(genes, np.arange(2))
    biological, sampled, shadow = control.ledgers(state, None, None)
    expected_A = sampled.self_viable @ genes[:, 2].mean(1) / sampled.self_viable.sum()
    assert expected_A < .5  # direct A weighting removed; correlated I selection persists
    assert biological.self_viable.sum() == pytest.approx(sampled.self_viable.sum())


def test_identical_A_expression_retains_exact_native_ledger(monkeypatch):
    monkeypatch.setattr(control.native, 'expression_ledger', fake_reproduction)
    genes = np.array([[[.5, .5], [.1, .1], [.2, .8]], [[.5, .5], [.9, .9], [.5, .5]]])
    state = State(genes, np.arange(2))
    biological, sampled, shadow = control.ledgers(state, None, None)
    assert sampled is biological and shadow is biological


def test_fixed_task_domain_has_no_new_preparations_or_environment():
    tasks = control.tasks()
    assert len(tasks) == len({tuple(sorted(t.items())) for t in tasks}) == 4096
    assert {t['target'] for t in tasks} == {1.05, 1.5}
    assert {t['policy'] for t in tasks} == {control.POLICY}


def test_four_fixed_contrasts_preserve_all_starts_and_scope():
    values = np.zeros((2,512,2,3,2), dtype=np.int8)
    values[:,:,:,0,0] = 1
    readout = control.analyze(values, bootstrap_count=9)
    assert readout['primary_family'] == 4
    assert [x['estimate'] for x in readout['primary']] == [1.,0.,1.,0.]
    assert readout['bootstrap_seed_base'] == 2026101407
    assert readout['policy_order'][1] == control.POLICY
    assert 'within-class' in readout['inference']
    with pytest.raises(ValueError):
        control.analyze(values[:,:511], bootstrap_count=9)
