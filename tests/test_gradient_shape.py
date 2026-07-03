import math

import pytest

from channel_id.gradient_shape import classify_gradient_shape


POS = [0, 1, 2, 3, 4, 5, 6]


def test_flat_series_is_none():
    r = classify_gradient_shape(POS, [5.0, 5.1, 4.9, 5.0, 5.05, 4.95, 5.0])
    assert r.shape == "none"
    assert r.direction == "flat"


def test_linear_series_is_cline():
    r = classify_gradient_shape(POS, [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    assert r.shape == "cline"
    assert r.direction == "increase"
    assert r.effect == pytest.approx(1.0, abs=1e-6)


def test_step_series_detects_breakpoint():
    # flat low, then jump to flat high between index 1 and 2 (Oshima->Toshima analogue)
    r = classify_gradient_shape(POS, [10.0, 11.0, 100.0, 98.0, 97.0, 99.0, 100.0])
    assert r.shape == "step"
    assert r.breakpoint_index == 1
    assert r.direction == "increase"
    assert r.effect > 50


def test_missing_values_are_dropped():
    r = classify_gradient_shape(POS, [0.0, None, 2.0, None, 4.0, 5.0, 6.0])
    assert r.n == 5
    assert r.shape in {"cline", "step", "none"}


def test_too_few_points_raises():
    with pytest.raises(ValueError):
        classify_gradient_shape([0, 1, 2], [1.0, 2.0, 3.0])


def test_campanula_selfing_is_step_at_bumblebee_boundary():
    # bagged capsule set % from data/inoue_literature_island_traits.csv
    bagged = [5.5, 11.3, 100.0, 100.0, 97.8, 90.6, 97.0]
    r = classify_gradient_shape(POS, bagged)
    assert r.shape == "step"
    assert r.breakpoint_index == 1  # split between Oshima(1) and Toshima(2)
    assert r.direction == "increase"


def test_campanula_flower_length_is_cline():
    # corolla length (mm), missing on Kozushima & Miyake
    fl = [49.91, 39.31, 35.27, 28.62, None, None, 23.14]
    r = classify_gradient_shape(POS, fl)
    assert r.shape in {"cline", "step"}
    assert r.direction == "reduction"
