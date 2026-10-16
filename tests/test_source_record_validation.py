"""Public receipt comparison boundaries shared by the two source audits."""
import pytest
from scripts.source_record_validation import equal_source_record


@pytest.mark.parametrize("left,right,expected", [
    ({"x": [True, None, 1.0]}, {"x": [True, None, 1.0]}, True),
    ({"x": True}, {"x": 1}, False),
    ({"x": 1}, {"x": True}, False),
    ({"x": 0}, {"x": 0, "extra": 0}, False),
    ([1, 2], [2, 1], False),
    ([1], [1, 2], False),
    (float("nan"), float("nan"), False),
    (float("inf"), float("inf"), False),
    (0.0, 0.0005, True),
    (0.0, 0.002, False),
])
def test_complete_finite_receipt(left, right, expected):
    assert bool(equal_source_record(left, right, atol=0.001)) is expected


def test_caller_selects_tolerance():
    assert equal_source_record(0.0, 5e-11, atol=1e-10)
    assert not equal_source_record(0.0, 5e-11, atol=1e-12)
