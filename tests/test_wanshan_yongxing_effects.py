import math

import pytest

from channel_id.paired_effect_uncertainty import exact_bootstrap_median_interval
from scripts.summarize_wanshan_yongxing_effects import build_effect_document


def test_exact_bootstrap_median_interval_is_deterministic_and_normalized():
    result = exact_bootstrap_median_interval([-3.0, -2.0, -1.0])
    assert result["estimate"] == pytest.approx(-2.0)
    assert result["lower"] == pytest.approx(-3.0)
    assert result["upper"] == pytest.approx(-1.0)
    assert result["weak_composition_support_size"] == math.comb(5, 2)
    assert result["probability_mass"] == pytest.approx(1.0)
    assert "does not add" in result["boundary"].lower()


def test_wanshan_effect_document_keeps_geographic_replication_closed():
    analysis = {
        "source_id": "source",
        "article_doi": "article",
        "dataset_doi": "dataset",
        "source_sha256": "abc",
    }
    rows = [
        {
            "plant_name": f"plant_{index}",
            "visitation_log_response_ratio": value,
            "pollinator_richness_log_response_ratio": value / 10,
            "pollinator_morisita_horn_turnover": 0.8 + index / 100,
        }
        for index, value in enumerate((-3.0, -2.5, -2.0, -1.5, -1.0, -0.5, -0.25))
    ]
    result = build_effect_document(analysis, rows)
    assert len(result["effects"]) == 3
    assert result["formal_cross_system_fit_ready"] is False
    assert all(effect["cross_system_model_eligible"] for effect in result["effects"])
    assert all(effect["n_effect_units"] == 7 for effect in result["effects"])
    assert all(effect["causal_claim_allowed"] is False for effect in result["effects"])
    assert "do not provide geographic replication" in result["claim_boundary"]
