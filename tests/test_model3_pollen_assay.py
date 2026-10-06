from importlib import import_module
import pytest


def assay(**changes):
    args = dict(ovules=[10.], outcross=[0.], capacity=[.5], depression=.5, timing='delayed')
    args.update(changes)
    return import_module('scripts.model3_pollen_assay').assay_totals(**args)


def test_absence_selfing_compensates_raw_but_depression_leaves_larger_viable_deficit():
    r = assay()
    assert r['raw_deficit'] == .5
    assert r['viable_deficit'] == .75
    assert r['viable_selfed'] == 2.5


def test_prior_selfed_ovules_cannot_be_reassigned_by_supplement():
    r = assay(timing='prior')
    assert r['saturated_viable'] == 7.5
    assert r['viable_deficit'] == pytest.approx(2/3)
    assert assay(timing='prior', capacity=[1.])['viable_deficit'] == 0


def test_saturated_delayed_has_no_residual_selfing_or_deficit():
    r = assay(outcross=[10.])
    assert r['viable_selfed'] == 0
    assert r['raw_deficit'] == r['viable_deficit'] == 0


def test_no_ovules_is_undefined_not_zero_limitation():
    r = assay(ovules=[0.])
    assert r['raw_deficit'] is None and r['viable_deficit'] is None


def test_impossible_prior_outcross_is_rejected():
    with pytest.raises(ValueError):
        assay(timing='prior', outcross=[8.])
