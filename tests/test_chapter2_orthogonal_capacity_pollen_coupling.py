"""Synthetic fixed-state audit: demographic capacity also enters pollen delivery."""
from dataclasses import replace
from pathlib import Path
import json

import numpy as np

from scripts.model3_island.types import VisitorState
from scripts.model3_island.population import subset
from scripts.model3_island.reproduction import reproduce
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, load_design, config, founders,
)


def test_capacity_directly_changes_initial_female_payoff_at_fixed_eight_genotypes():
    biology = load_design(DEFAULT_DESIGN)
    state = subset(founders(biology), np.arange(8))
    visitors = VisitorState(
        ids=np.array([17, 18], dtype=np.int64),
        optima=np.array([0.4, 0.6], dtype=float),
        breadths=np.array([0.5, 0.5], dtype=float),
        effectiveness=np.array([0.9, 0.9], dtype=float),
    )
    common = config(biology, "delayed_control", 0.01, "evolving")
    assert common.background_ratio > 0
    small = reproduce(state, visitors, replace(common, capacity=8))
    large = reproduce(state, visitors, replace(common, capacity=48))

    # Export depends on floral genotype/visitor activity, not this denominator.
    np.testing.assert_array_equal(small.exported, large.exported)
    # The denominator includes capacity*background_ratio: pollen dilution
    # directly affects outcross recruitment supply, before density diverges.
    assert small.outcross.sum() > large.outcross.sum()
    assert not np.allclose(small.outcross, large.outcross)
    # In delayed-selfing mode, reduced female outcross leaves more for selfing.
    assert common.assurance_timing == "delayed"
    assert small.self_viable.sum() < large.self_viable.sum()


def test_original_frozen_inconclusive_primary_remains_unchanged():
    p = Path("results/chapter2/orthogonal_capacity_full_readout_20261009.json")
    d = json.loads(p.read_text())
    assert d["primary_decision"] == "inconclusive"
    assert d["n_independent_visitor_histories"] == 64
    assert d["n_future_trajectories"] == 172032
    assert abs(d["inference"]["contrasts"][
        "primary_capacity_conditional_fixed_eight"]["mean"]
        - 0.0018484189036193578) < 1e-14


def test_manuscript_scope_preserves_direct_pollen_path_warning():
    source = Path("scripts/model3_island/reproduction.py").read_text()
    assert "config.capacity*config.background_ratio" in source
    report = Path("docs/CHAPTER2_ORTHOGONAL_MECHANISM_CHANNEL_AUDIT_20261009.md").read_text()
    assert "EXPLORATORY AFTER SEEING THE OUTCOME" in report
    assert "pure demographic ceiling" in report


def test_raw_mechanism_result_is_immutable_exploratory_and_full_cohort():
    import hashlib
    path = Path("results/chapter2/orthogonal_capacity_mechanism_posthoc_20261009.json")
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == (
        "255d62055760e49fa3e032ac16040c790ebc2fc02564e1584fcf597aecbc14c3"
    )
    d = json.loads(raw)
    assert d["status"] == "POST_OUTCOME_EXPLORATORY_RAW_AUTHENTICATED_CHANNEL_AUDIT"
    assert d["full_future_count"] == 172032
    assert d["history_bootstrap"]["n"] == 64
    assert d["frozen_primary_unchanged"]["decision"] == "inconclusive"
    assert abs(d["frozen_primary_unchanged"]["estimate"] -
               0.0018484189036193578) < 1e-14
    checks = d["initial_mechanical_checks"]
    assert checks["identical_F8_starting_counts"] is True
    assert checks["viability_gate_preserves_outcross_and_pollen"] is True
    assert checks["viability_gate_halves_selfed_viable_seed"] is True
    assert checks["F8_max_initial_payoff_abs_difference_capacity8_vs_capacity48"][
        "t0_outcross_viable"
    ] > 0
