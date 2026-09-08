from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.audit_chapter2_equal_turnover_control import OUT, build

ROOT = Path(__file__).resolve().parents[1]


def test_equal_turnover_control_reproduces_recorded_result():
    generated = build()
    recorded = json.loads(OUT.read_text(encoding="utf-8"))
    assert generated == recorded
    assert generated["baseline"]["mixed_sign"] == 41
    assert generated["equal_turnover"]["mixed_sign"] == 70
    assert generated["equal_turnover"]["all_positive"] == 26
    assert generated["equal_turnover"]["all_negative"] == 0
    assert generated["equal_turnover"]["other"] == 0
    assert generated["equal_turnover"]["state_by_community_nonadditivity_fraction"] == pytest.approx(0.6561447178663772)


def test_equal_turnover_claim_is_bounded():
    payload = build()
    assert payload["control"]["island_partner_arrival_after"] == payload["control"]["mainland_partner_arrival"]
    assert payload["control"]["island_partner_loss_after"] == payload["control"]["mainland_partner_loss"]
    assert payload["control"]["other_parameters_retained"] is True
    assert "does not make the two scenarios identical" in payload["claim_boundary"]
    assert "does not establish transportability beyond this plant-pollinator model class" in payload["claim_boundary"]
