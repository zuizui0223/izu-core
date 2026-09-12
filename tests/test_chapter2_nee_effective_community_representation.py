from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "data" / "design" / "chapter2_nee_effective_community_representation_lock_20260912.json"
READINESS = ROOT / "docs" / "CHAPTER2_NEE_STAGE1_READINESS_20260912.md"


def _load() -> dict:
    return json.loads(LOCK.read_text(encoding="utf-8"))


def test_r4_primary_representation_is_effective_service_composition() -> None:
    data = _load()
    assert data["status"] == "frozen_before_confirmatory_reproductive_outcomes"
    primary = data["primary_representation"]
    assert primary["object"] == "background-controlled effective-service composition vector"
    assert primary["share_definition"] == "p_bg = w_bg / sum_g(w_bg)"
    assert "joint term" in primary["encoding_rule"]


def test_r4_keeps_amount_separate_and_breadth_secondary() -> None:
    data = _load()
    assert data["separate_amount_term"]["object"] == "total_effective_pollen_delivery_per_flower_hour"
    secondary = data["secondary_context_summaries"]
    assert "secondary" in secondary["effective_service_hill_q2"]
    assert "secondary" in secondary["effective_service_evenness_q2"]
    assert "repeated-block" in secondary["service_realization_stability"]


def test_r4_does_not_manufacture_composition_from_failed_measurement() -> None:
    data = _load()
    weights = data["weight_definition"]
    assert weights["background_control_required"] is True
    assert "do not impute zero" in weights["missing_or_uncontrolled_effectiveness"]
    assert "do not clip" in weights["negative_background_adjusted_weight"]
    assert "do not manufacture" in weights["zero_total_effective_service"]


def test_r4_forbids_outcome_informed_reencoding_and_literal_k_mapping() -> None:
    forbidden = "\n".join(_load()["forbidden"])
    assert "synthetic k" in forbidden
    assert "clip negative" in forbidden
    assert "dependency or mature-seed coefficients" in forbidden
    assert "PCA" in forbidden
    assert "breakpoint" in forbidden


def test_readiness_marks_r4_closed_without_closing_pilot_or_precision() -> None:
    text = READINESS.read_text(encoding="utf-8")
    assert "effective-community primary encoding | **CLOSED**" in text
    assert "pilot dispersion/attrition/dependence support | **OPEN**" in text
    assert "confirmatory precision/power | **OPEN**" in text
    assert "R4 representation preserved" in text
