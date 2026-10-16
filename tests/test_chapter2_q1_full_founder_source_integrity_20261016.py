"""Adversarial regressions for the retrospective Q1 admission readout.

All archived biological producer files and the 1088 original trajectories stay
untouched. These negative fixtures test cases that previously passed overly
weak provenance / initial-founder checks.
"""
from __future__ import annotations

import json

import numpy as np
import pytest

from scripts.summarize_chapter2_q1_fresh_founders_20261016 import (
    admit_source_manifest, load_trace, register_initial_genome,
)
from scripts.run_chapter2_q1_fresh_founders_20261016 import source_manifest


def _state():
    x = np.full((48, 3, 2), .5)
    x[0, 1, :] = (.3, .7)
    x[1, 0, :] = (.2, .8)
    return x


def _sample_npz(tmp_path, *, census=None, initial=None, mean_override=None):
    state = _state() if initial is None else initial
    trace = np.full((1001, 10), np.nan)
    trace[:, 0] = 48 if census is None else census
    trace[0, 2] = state.mean(axis=(0, 2))[1] if mean_override is None else mean_override
    trace[-1, 2] = .4
    file = tmp_path / "source.npz"
    np.savez_compressed(file, trace=trace, state_0=state)
    return file


def test_all_original_source_paths_are_pinned_to_actual_checkout():
    current = source_manifest()
    admit_source_manifest(current)
    replaced = dict(current)
    replaced["scripts/model3_island/reproduction.py"] = "0" * 64
    with pytest.raises(ValueError, match="source manifest differs"):
        admit_source_manifest(replaced)
    with pytest.raises(ValueError, match="source manifest differs"):
        admit_source_manifest({})


def test_genome_admission_detects_different_diploid_state_at_equal_mean():
    original = _state()
    altered = original.copy()
    altered[[0, 2], 0, :] = altered[[2, 0], 0, :]
    assert original.shape == altered.shape
    np.testing.assert_array_equal(original.mean(axis=(0, 2)),
                                  altered.mean(axis=(0, 2)))
    expected: dict[int, str] = {}
    left = register_initial_genome(expected, 560201, original)
    assert register_initial_genome(expected, 560201, original.copy()) == left
    with pytest.raises(ValueError, match="different t0 diploid genomes"):
        register_initial_genome(expected, 560201, altered)
    assert register_initial_genome(expected, 560202, altered) != left


@pytest.mark.parametrize("invalid", [
    lambda x: np.full(1001, -1.),
    lambda x: np.full(1001, 49.),
    lambda x: np.full(1001, .5),
    lambda x: np.full(1001, np.nan),
])
def test_invalid_census_never_qualifies_for_genome_result(tmp_path, invalid):
    d = {"updates": 1000, "founder_genomes": {"n": 48}}
    path = _sample_npz(tmp_path, census=invalid(None))
    with pytest.raises(ValueError, match="Invalid original founder or census"):
        load_trace(path, d)


def test_t0_full_genome_and_saved_trace_must_match(tmp_path):
    d = {"updates": 1000, "founder_genomes": {"n": 48}}
    path = _sample_npz(tmp_path, mean_override=.11)
    with pytest.raises(ValueError, match="Trace t0 investment disagrees"):
        load_trace(path, d)


def test_valid_small_signed_file_returns_full_genome(tmp_path):
    d = {"updates": 1000, "founder_genomes": {"n": 48}}
    path = _sample_npz(tmp_path)
    alive, t0, final, genome = load_trace(path, d)
    assert alive
    assert final == .4
    np.testing.assert_array_equal(genome, _state())
    assert t0 == pytest.approx(.5)
