from __future__ import annotations

import math

from scripts.derive_izu_effective_service_scale import derive_block_scales


def test_equal_two_group_service_has_hill_q2_two():
    rows = [
        {"block_id": "B1", "visitor_group": "g1", "effective_pollen_delivery_per_flower_hour": "4"},
        {"block_id": "B1", "visitor_group": "g2", "effective_pollen_delivery_per_flower_hour": "4"},
    ]
    out = derive_block_scales(rows)[0]
    assert out["effective_service_scale_ready"] is True
    assert math.isclose(out["effective_service_hill_q2"], 2.0)
    assert math.isclose(out["effective_service_evenness_q2"], 1.0)
    assert math.isclose(out["max_effective_service_share"], 0.5)


def test_uneven_service_reduces_effective_group_number():
    rows = [
        {"block_id": "B1", "visitor_group": "g1", "effective_pollen_delivery_per_flower_hour": "3"},
        {"block_id": "B1", "visitor_group": "g2", "effective_pollen_delivery_per_flower_hour": "1"},
    ]
    out = derive_block_scales(rows)[0]
    assert math.isclose(out["effective_service_hill_q2"], 1.6)
    assert math.isclose(out["effective_service_evenness_q2"], 0.8)


def test_negative_background_adjusted_service_is_not_clipped_into_scale():
    rows = [
        {"block_id": "B1", "visitor_group": "g1", "effective_pollen_delivery_per_flower_hour": "2"},
        {"block_id": "B1", "visitor_group": "g2", "effective_pollen_delivery_per_flower_hour": "-0.2"},
    ]
    out = derive_block_scales(rows)[0]
    assert out["effective_service_scale_ready"] is False
    assert out["effective_service_hill_q2"] is None
    assert out["effective_service_evenness_q2"] is None


def test_missing_group_effectiveness_keeps_scale_unavailable():
    rows = [
        {"block_id": "B1", "visitor_group": "g1", "effective_pollen_delivery_per_flower_hour": "2"},
        {"block_id": "B1", "visitor_group": "g2", "effective_pollen_delivery_per_flower_hour": ""},
    ]
    out = derive_block_scales(rows)[0]
    assert out["effective_service_scale_ready"] is False
    assert out["controlled_effective_group_count"] == 0
