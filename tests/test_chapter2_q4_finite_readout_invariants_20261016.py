"""Fail-closed Q4 input validation without changing frozen Q4 biology."""
from __future__ import annotations

import pytest

from scripts.summarize_chapter2_island_demographic_independent32 import (
    validate_future_case,
)


DESIGN = {"post_capacity": 8, "post_updates": 80}


def _valid():
    return {
        "occupied": 1,
        "terminal_N": 6,
        "min_N": 2,
        "first_extinction": None,
        "initial_viable_maternal_per_capita": 2.1,
        "end_traits": [.45, .5, .55],
    }


def test_valid_surviving_and_extinct_endpoints_are_admitted():
    validate_future_case(_valid(), DESIGN)
    gone = _valid()
    gone.update({
        "occupied": 0, "terminal_N": 0, "min_N": 0,
        "first_extinction": 17, "end_traits": None,
    })
    validate_future_case(gone, DESIGN)


@pytest.mark.parametrize(("column", "value"), [
    ("terminal_N", -1),
    ("terminal_N", 9),
    ("terminal_N", 2.5),
    ("terminal_N", True),
    ("occupied", True),
    ("occupied", 0),
    ("min_N", -1),
    ("min_N", 9),
    ("min_N", 7),
    ("first_extinction", 0),
    ("first_extinction", 81),
    ("first_extinction", 12),
    ("initial_viable_maternal_per_capita", -1.),
    ("initial_viable_maternal_per_capita", float("nan")),
    ("end_traits", None),
    ("end_traits", [.4, .5, 1.2]),
])
def test_impossible_demography_is_never_admitted(column, value):
    row = _valid()
    row[column] = value
    with pytest.raises(ValueError):
        validate_future_case(row, DESIGN)


def test_no_recolonization_after_extinction_in_the_closed_q4_cohort():
    row = _valid()
    row["min_N"] = 0
    with pytest.raises(ValueError):
        validate_future_case(row, DESIGN)
    row = _valid()
    row.update({"terminal_N": 0, "occupied": 0, "min_N": 0, "end_traits": None})
    with pytest.raises(ValueError):
        validate_future_case(row, DESIGN)


def test_bad_terminal_census_originally_had_same_bool_as_occupied():
    assert bool(-1) == bool(1)  # Historical reader only checked truthiness.
    row = _valid()
    row["terminal_N"] = -1
    with pytest.raises(ValueError, match="impossible or invalid"):
        validate_future_case(row, DESIGN)
