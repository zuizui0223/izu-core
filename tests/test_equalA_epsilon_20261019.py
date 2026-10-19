import pytest

from scripts.audit_chapter2_equalA_epsilon_20261019 import first_loss


def test_strict_loss_can_disappear_with_partial_recovery_target():
    assert first_loss([.625, .5, .5], .512, 0, 'upper') == 1
    assert first_loss([.625, .5, .5], .512, .05, 'upper') is None
    assert first_loss([.625, .5, .375], .512, .05, 'upper') == 2


def test_assurance_bound_and_extinction_are_distinct():
    assert first_loss([.25, .5], .492, 0, 'lower') == 1
    assert first_loss([.25, .5], .492, .05, 'lower') is None
    assert first_loss([.625, None], .512, 0, 'upper') is None
    assert first_loss([.625, .375, None], .512, 0, 'upper') == 1


def test_numerical_tolerance_is_not_biological_epsilon():
    assert first_loss([.5-1e-13], .5, 0, 'upper') is None
    with pytest.raises(ValueError):
        first_loss([.5], .5, -.01, 'upper')
