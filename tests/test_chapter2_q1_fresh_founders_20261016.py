"""Frozen design, independent founder draws, technical nulls and crossed CI.

Tests are short smoke fixtures; they are NOT the predeclared 1000-update
biological result. The entire 1088-case campaign and its 32 source-verified
artifacts are the exclusive future scientific readout.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from scripts.run_chapter2_q1_fresh_founders_20261016 import (
    DESIGN, MAIN_NAMES, declared_tasks, founder, load_frozen, simulate,
    source_manifest, task_key,
)
from scripts.summarize_chapter2_q1_fresh_founders_20261016 import (
    two_way_bootstrap,
)


def test_frozen_independent_founder_visitor_design_and_nonreuse():
    d, source = load_frozen()
    assert d["status"] == "frozen_before_any_new_founder_outcome"
    assert d["main_cases"] == 1024
    assert d["total_cases"] == 1088
    assert source["main_campaign"]["founder_seed"] == 74001
    assert d["founder_genomes"]["first_seed"] != 74001
    assert d["bootstrap"]["draws"] == 9999
    assert d["bootstrap"]["seed"] == 5606162026
    tasks = declared_tasks(d)
    assert len(tasks) == len(set(tasks)) == 1088
    assert sum(t[0] == "main" for t in tasks) == 1024
    assert sum(t[0] == "null" for t in tasks) == 64
    assert {t[1] for t in tasks} == set(MAIN_NAMES)
    assert {t[6] for t in tasks} == {"near", "far"}
    assert {t[7] for t in tasks} == {"fixed", "evolving"}
    assert len({task_key(t) for t in tasks}) == 1088
    assert set(t[3] for t in tasks if t[0] == "main") == set(range(560201, 560209))
    assert set(t[4] for t in tasks if t[0] == "main") == set(range(560301, 560309))
    shards = [[t for i, t in enumerate(tasks) if i % 32 == j]
              for j in range(32)]
    assert sum(map(len, shards)) == len(tasks)
    assert min(map(len, shards)) == max(map(len, shards)) == 34


def test_8_new_founder_genomes_are_distinct_and_A_initial_is_fixed():
    d, source = load_frozen()
    founder_genotypes = [
        founder(d, seed).alleles for seed in range(560201, 560209)
    ]
    for x in founder_genotypes:
        assert x.shape == (48, 3, 2)
        assert np.all(x[:, 2, :] == .5)
        assert np.any(x[:, 1, :] < .5)
        assert np.any(x[:, 1, :] > .5)
    hashes = {
        hashlib.sha256(x.tobytes()).hexdigest() for x in founder_genotypes
    }
    assert len(hashes) == 8
    assert source["main_campaign"]["fixed_assurance"] == .5


@pytest.mark.parametrize("setting", MAIN_NAMES)
@pytest.mark.parametrize("arm", ("near", "far"))
def test_zero_mutation_fixed_evolvable_modes_exactly_same_in_short_smoke(
    setting, arm,
):
    d, source = load_frozen()
    template = ("null", setting, 0., 560201, 560301, 560401, arm)
    tr0, states0 = simulate(d, source, template + ("fixed",), steps=8)
    tr1, states1 = simulate(d, source, template + ("evolving",), steps=8)
    np.testing.assert_array_equal(tr0, tr1)
    assert set(states0) == set(states1) == {"state_0", "state_8"}
    for key in states0:
        np.testing.assert_array_equal(states0[key], states1[key])


def test_same_founder_same_initial_genetics_across_near_far_and_A_modes():
    d, source = load_frozen()
    initial = []
    for arm in ("near", "far"):
        for mode in ("fixed", "evolving"):
            task = ("main", "assurance_cost", .01, 560201, 560301,
                    560401, arm, mode)
            tr, states = simulate(d, source, task, steps=2)
            initial.append((states["state_0"], tr[0, 2]))
    assert all(np.array_equal(initial[0][0], r[0]) for r in initial[1:])
    assert all(initial[0][1] == r[1] for r in initial[1:])


def test_two_way_crossed_bootstrap_is_not_64_independent_island_bootstrap():
    founder = np.arange(8, dtype=float)[:, None]
    visitor = np.arange(8, dtype=float)[None, :]
    arr = 0.1 + 0.02 * founder + 0.007 * visitor
    rng = np.random.default_rng(123)
    fi = rng.integers(0, 8, size=(1200, 8))
    vi = rng.integers(0, 8, size=(1200, 8))
    ci = two_way_bootstrap(arr, fi, vi)
    assert ci[0] < float(arr.mean()) < ci[1]
    const = two_way_bootstrap(np.full((8, 8), .25), fi, vi)
    assert const == pytest.approx([.25, .25])
    with pytest.raises(ValueError, match="Crossed founder"):
        two_way_bootstrap(np.ones((7, 8)), fi, vi)


def test_original_biology_source_manifest_is_complete_and_no_frozen_edits():
    manifest = source_manifest()
    assert "scripts/model3_island/reproduction.py" in manifest
    assert "scripts/model3_island/population.py" in manifest
    assert "scripts/run_model3_persistent_isolation.py" in manifest
    assert "scripts/run_chapter2_assurance_generality.py" in manifest
    assert "data/design/model3_ch2_bridge_20260927.json" in manifest
    assert "data/design/chapter2_q1_fresh_founder_generality_20261016.json" in manifest
    assert len(manifest) >= 26
    assert all(len(h) == 64 for h in manifest.values())
    d = json.loads(DESIGN.read_text(encoding="utf-8"))
    assert d["registered_failure_rule"].startswith("If the exact cohort")
