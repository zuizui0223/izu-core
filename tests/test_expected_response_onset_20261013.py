import numpy as np
import pytest
from scripts.expected_response_onset_20261013.audit_response_onset import first_direction, compare_onsets


def test_first_direction_keeps_zero_missing_and_correct_direction():
    assert first_direction([0, np.nan, 0, 2e-12], 1) == 3
    assert first_direction([0, -2e-12, 3e-12], -1) == 1
    assert first_direction([0, np.nan, 1e-13], 1) is None


def test_sustained_direction_requires_full_unbroken_window():
    assert first_direction([2e-12] * 19, 1, 20) is None
    assert first_direction([2e-12] * 19 + [np.nan] + [2e-12] * 20, 1, 20) == 20
    assert first_direction([-2e-12] * 20, -1, 20) == 0


@pytest.mark.parametrize('a,i,label', [(1,0,'I_earlier'), (0,1,'A_earlier'), (1,1,'tie'),
                                     (1,None,'A_only'), (None,1,'I_only'), (None,None,'neither')])
def test_comparison_preserves_missing_onsets(a,i,label):
    assert compare_onsets(a,i) == label
