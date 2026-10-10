"""Source-matched 64-new-visitor-history transfer of beta/Gamma_seed to Gamma_persist.

All 64 visitor RNG IDs, arms, statistics and sign thresholds are committed
before this cohort's outcomes. This is a model-internal holdout of an already
exploratory source: NOT independently observed islands and NOT evolutionary
suicide. Parents begin monomorphic so NO allele-frequency evolution can occur.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.audit_chapter2_beta_gamma_seed_map import (
    changed_state, state_of_clones, log_mean, visitors_for,
)
from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.chapter2_postzygotic_viability_gate import gate_postzygotic_seed_viability
from scripts.model3_island.history import make_history
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config, load_design,
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_gamma_persist_new_visitor_holdout_20261010.json"
STATUS = "SOURCE_LOCKED_MODEL_INTERNAL_NEW_VISITOR_GAMMA_PERSIST_NOT_EVOLUTION"
GATES = ("baseline", "half_self")
DIRECTIONS = (-0.05, 0.05)
CAPACITIES = (8, 48)
ASSURANCES = (0.35, 0.65)
STEPS = 80
FIRST_YEAR_SEED = 61021001
LAST_YEAR_SEED = 61021064


def load_contract():
    raw = DESIGN.read_bytes()
    d = json.loads(raw)
    conditions = d["conditions"]
    out = d["outcome_contract"]
    assert d["status"] == "PROSPECTIVELY_SOURCE_LOCKED_MODEL_INTERNAL_HOLDOUT_BEFORE_NEW_VISITOR_OUTCOMES"
    assert (
        conditions["independent_visitor_seed_first"],
        conditions["independent_visitor_seed_last"],
        conditions["n_independent_visitor_histories"]
    ) == (FIRST_YEAR_SEED, LAST_YEAR_SEED, 64)
    assert conditions["n_demographic_repeats_per_history"] == 1
    assert conditions["K"] == [8,48]
    assert conditions["pollen_background_B"] == 48
    assert conditions["resident_assurance_values"] == [0.35,0.65]
    assert conditions["collective_shifts"] == [-0.05,0.05]
    assert conditions["viability_gates"] == {
        "baseline":[1.0,1.0],"half_self":[0.5,1.0]}
    assert conditions["total_years"] == 80
    assert conditions["ovule_budget"] == 6.0
    assert conditions["n_futures_total"] == 1024
    assert out["effect_deadband_absolute_probability"] == 0.05
    assert out["uncertainty"].startswith("paired 1999")
    assert "evolution" in out["zero_monomorphic_variation_note"]
    return d, hashlib.sha256(raw).hexdigest()


def base_config(d, capacity):
    if capacity not in CAPACITIES:
        raise ValueError("unregistered population capacity")
    biology = load_design(DEFAULT_DESIGN)
    setting = source_config(
        biology, d["conditions"]["reproductive_setting"], 0.0, "evolving"
    )
    cfg = replace(
        setting,
        capacity=int(capacity), years=STEPS,
        island_history="separation", initial_visitors=4,\n        ovule_budget=6.0, survival=0.0, mutation_rate=0.0, mutation_sd=0.0,\n        visitor_arrival=replace(setting.visitor_arrival,distance=0.0),\n        seed_arrival=replace(setting.seed_arrival,supply=0.0),
    )
    return cfg
