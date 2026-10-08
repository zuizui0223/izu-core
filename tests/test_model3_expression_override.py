"""Engineering-only tests for phenotype shifts; no new visitor histories."""
import numpy as np
import pytest

from scripts.model3_island.types import PlantState
from scripts.model3_island.expression_override import expressed_traits


def sample_state():
    a = np.asarray([
        [[0.4, 0.6], [0.5, 0.5], [0.5, 0.5]],
        [[1.0, 1.0], [0.0, 0.0], [1.0, 1.0]],
    ], dtype=float)
    return PlantState(
        alleles=a,
        allele_origin=np.zeros((2, 3, 2), dtype=int),
        mutation_flags=np.zeros((2, 3, 2), dtype=bool),
        ids=np.array([0, 1], dtype=int),
        birth_years=np.array([0, 0], dtype=int),
    )


def test_zero_offset_is_bitwise_equal_to_frozen_genetic_phenotype():
    state = sample_state()
    original = state.alleles.mean(axis=2)
    actual = expressed_traits(state)
    assert np.array_equal(actual, original)
    assert actual[1].tolist() == [1.0, 0.0, 1.0]


def test_assigned_expression_changes_return_not_inherited_alleles():
    state = sample_state()
    allele_bytes = state.alleles.tobytes()
    origin_bytes = state.allele_origin.tobytes()
    before = state.alleles.mean(axis=2)
    shifted = expressed_traits(
        state, assurance_shift=0.45, investment_shift=-0.45
    )
    assert shifted.shape == (2, 3)
    assert np.array_equal(shifted[:, 0], before[:, 0])
    assert shifted[0, 1] < before[0, 1]
    assert shifted[0, 2] > before[0, 2]
    assert (shifted >= 0).all() and (shifted <= 1).all()
    assert state.alleles.tobytes() == allele_bytes
    assert state.allele_origin.tobytes() == origin_bytes
    assert not state.alleles.flags.writeable


def test_target_axis_untouched_under_other_axis_schedule():
    state = sample_state()
    genetic = state.alleles.mean(axis=2)
    a_first = expressed_traits(state, assurance_shift=0.45)
    i_first = expressed_traits(state, investment_shift=-0.45)
    assert np.array_equal(a_first[:, 1], genetic[:, 1])
    assert np.array_equal(i_first[:, 2], genetic[:, 2])
    assert np.array_equal(a_first[:, 0], genetic[:, 0])
    assert np.array_equal(i_first[:, 0], genetic[:, 0])


@pytest.mark.parametrize("bad", [True, np.nan, np.inf, -np.inf, "0.45"])
def test_invalid_offsets_rejected_without_mutating_genotypes(bad):
    state = sample_state()
    before = state.alleles.tobytes()
    with pytest.raises(ValueError):
        expressed_traits(state, assurance_shift=bad)
    assert state.alleles.tobytes() == before
