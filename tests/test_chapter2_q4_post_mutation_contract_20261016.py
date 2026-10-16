"""Cross-operator regression and fail-closed frozen Q4 mutation policy.

No biological campaign, raw receipts, or archived 2026-10-08 producer is edited.
"""
from __future__ import annotations

from dataclasses import replace
import json

import numpy as np
import pytest

from scripts.audit_chapter2_q4_post_mutation_contract_20261016 import (
    DESIGN, PRODUCER, admit, audit,
)
from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.model3_island.population import subset
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.types import VisitorState
from scripts.run_chapter2_assurance_generality import config, founders, load_design, DEFAULT_DESIGN


def test_original_frozen_q4_future_rate_is_exactly_what_source_implements():
    receipt = audit()
    assert receipt["status"] == "PASS_FROZEN_Q4_PRE_POST_MUTATION_RATE_IDENTITY"
    assert receipt["effective_original_pre_rate"] == .01
    assert receipt["effective_original_future_rate"] == .01
    assert "continues" in receipt["future_A_evolvability"]
    d = json.loads(DESIGN.read_text(encoding="utf-8"))
    assert d["post_mutation_rate"] == d["pre_mutation_rate"] == .01


def test_future_post_mutation_rate_change_fails_closed_without_versioned_producer():
    d = json.loads(DESIGN.read_text(encoding="utf-8"))
    d["post_mutation_rate"] = 0.0
    source = PRODUCER.read_text(encoding="utf-8")
    with pytest.raises(ValueError, match="ignores post_mutation_rate"):
        admit(d, source)


def test_q4_source_policy_change_is_not_silently_admitted():
    d = json.loads(DESIGN.read_text(encoding="utf-8"))
    source = PRODUCER.read_text(encoding="utf-8")
    altered = source.replace(
        'cfg, capacity=d["post_capacity"], ovule_budget=float(budget),',
        'cfg, mutation_rate=0., capacity=d["post_capacity"], ovule_budget=float(budget),',
    )
    assert altered != source
    with pytest.raises(ValueError, match="post-rate or demographic source changed"):
        admit(d, altered)


@pytest.mark.parametrize("setting", (
    "delayed_control", "prior_selfing", "pollen_discount", "assurance_cost",
))
@pytest.mark.parametrize("a_mode", ("fixed", "evolving"))
@pytest.mark.parametrize("capacity", (8, 48))
def test_kb_reproductive_kernel_equals_original_exactly_when_b_equals_k(
    setting, a_mode, capacity,
):
    design = load_design(DEFAULT_DESIGN)
    state = subset(founders(design), np.arange(8, dtype=np.int64))
    genotypes = state.alleles.copy()
    # Exercise varying A at all eight individuals for the evolving mode;
    # fixed mode should ignore these standing A alleles for expression.
    genotypes[:, 2, :] = np.linspace(.15, .85, 8)[:, None]
    state = replace(state, alleles=genotypes)
    visitors = VisitorState(
        np.array([101, 102], dtype=np.int64),
        np.array([.35, .65], dtype=float),
        np.array([.3, .3], dtype=float),
        np.array([.9, 1.], dtype=float),
    )
    original_config = replace(config(design, setting, .01, a_mode),
                              capacity=capacity)
    canonical = reproduce(state, visitors, original_config)
    disentangled = reproduce_kb(
        state, visitors, original_config,
        background_denominator_capacity=capacity,
    )
    for field in (
        "outcross", "self_raw", "self_viable", "ovules",
        "exported", "delivered", "lost", "maternal", "paternal",
    ):
        np.testing.assert_array_equal(
            getattr(canonical, field), getattr(disentangled, field),
            err_msg=f"source/B-fixed operator mismatch in {setting}:{a_mode}:{capacity}:{field}",
        )
    np.testing.assert_allclose(
        disentangled.maternal.sum(), disentangled.paternal.sum(),
        atol=1e-12, rtol=0,
    )


def test_fixed_plant_count_b48_vs_b8_changes_pollen_transfer_not_export():
    design = load_design(DEFAULT_DESIGN)
    state = subset(founders(design), np.arange(8))
    visitors = VisitorState(
        np.array([55], dtype=np.int64),
        np.array([.5], dtype=float),
        np.array([.3], dtype=float),
        np.array([1.], dtype=float),
    )
    cfg = replace(config(design, "delayed_control", .01, "fixed"), capacity=8)
    b8 = reproduce_kb(state, visitors, cfg, background_denominator_capacity=8)
    b48 = reproduce_kb(state, visitors, cfg, background_denominator_capacity=48)
    np.testing.assert_array_equal(b8.exported, b48.exported)
    assert b8.delivered.sum() > b48.delivered.sum()
    assert b8.outcross.sum() > b48.outcross.sum()
    assert b8.self_viable.sum() < b48.self_viable.sum()
