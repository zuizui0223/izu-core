"""Immutable independent scientific readout: no numerical re-fitting in CI."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "results/chapter2/orthogonal_capacity_full_readout_20261009.json"
ORIGINAL_SHA256 = "e52d92a4586b92ca0aa3e93b560b2d603d63a9e9ee0b7fa61432a5b7f734d69c"


def test_full_original_machine_readout_is_byte_identical_to_production_archive():
    raw = RESULT.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == ORIGINAL_SHA256
    d = json.loads(raw)
    assert d["status"] == "ALL_64_NEW_HISTORIES_2048_SOURCES_172032_FUTURES_AUTHENTICATED"
    assert d["n_independent_visitor_histories"] == 64
    assert d["n_t400_sources"] == 2048
    assert d["n_future_trajectories"] == 172032
    assert d["primary_decision"] == "inconclusive"


def test_frozen_primary_inconclusive_not_promoted_to_positive_or_equivalent():
    d = json.loads(RESULT.read_text(encoding="utf-8"))
    i = d["inference"]
    assert i["independent_inference_unit"] == "visitor_history"
    assert i["bootstrap"] == {
        "draws": 9999, "seed": 2026100943, "unit": "paired_visitor_history",
    }
    p = i["contrasts"]["primary_capacity_conditional_fixed_eight"]
    assert p["positive_histories"] == 31 and p["negative_histories"] == 33
    assert p["mean"] < 0.005
    assert p["history_bootstrap95"][0] < 0 < p["history_bootstrap95"][1]
    assert i["primary_decision_if_and_only_if_complete_raw_archive_admitted"] == "inconclusive"


def test_secondary_contrast_does_not_claim_genetic_diversity_mediation():
    d = json.loads(RESULT.read_text(encoding="utf-8"))
    s = d["inference"]["contrasts"]["secondary_founder_abundance_and_sampling"]
    assert s["history_bootstrap95"][0] < 0 < s["history_bootstrap95"][1]
    assert "genotype sampling" in d["interpretation_limit"]
    assert "Not a field-calibrated Izu effect" in d["interpretation_limit"]
