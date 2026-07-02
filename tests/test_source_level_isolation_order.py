from dataclasses import replace
from pathlib import Path
import random

import pytest

from channel_id.island_multichannel import EvidenceChannel, _standardize_environment
from channel_id.island_source_level import load_source_level_evidence
from channel_id.source_level_isolation_order import (
    ISOLATION_ORDER_SCENARIO,
    compare_isolation_order,
    draw_isolation_order_parameters,
    load_region_order,
    predict_isolation_order,
)
from channel_id.source_level_isolation_order_diagnostics import (
    isolation_order_sensitivity,
    profile_isolation_order,
)
from channel_id.source_level_sensitivity import default_sensitivity_settings

ROOT = Path(__file__).parents[1]
SUMMARY = ROOT / "data" / "inoue_literature_island_traits.csv"


def evidence():
    return load_source_level_evidence(
        island_summary_path=SUMMARY,
        outcrossing_path=ROOT / "data" / "two_breakpoint_evidence" / "inoue1990_outcrossing.csv",
        bagging_path=ROOT / "data" / "two_breakpoint_evidence" / "inoue1988_bagging.csv",
        flower_path=ROOT / "data" / "two_breakpoint_evidence" / "inoue1995_flower_length.csv",
    )


def test_region_order_is_source_locked_and_normalized() -> None:
    values = load_region_order(SUMMARY, evidence().islands)

    assert values["Honshu"] == pytest.approx(0.0)
    assert values["Hachijo"] == pytest.approx(1.0)
    assert values["Oshima"] < values["Toshima"] < values["Niijima"]


def test_order_prediction_is_monotone_and_does_not_read_pollinator_fields() -> None:
    rows = evidence().islands
    honshu = next(row for row in rows if row.island_id == "Honshu")
    hachijo = next(row for row in rows if row.island_id == "Hachijo")
    draw = draw_isolation_order_parameters(3, random.Random(19))
    zero_environment = (0.0, 0.0, 0.0)

    first = predict_isolation_order(honshu, draw, zero_environment, 0.0)
    last = predict_isolation_order(hachijo, draw, zero_environment, 1.0)
    no_pollinators = replace(honshu, bombus_diversus=0.0, bombus_ardens=0.0, halictid_pollinator=0.0, megachilid_pollinator=0.0)
    same_order = predict_isolation_order(no_pollinators, draw, zero_environment, 0.0)

    assert last.assurance > first.assurance
    assert last.expected_outcrossing < first.expected_outcrossing
    assert last.expected_bagging > first.expected_bagging
    assert last.expected_flower_length_mm < first.expected_flower_length_mm
    assert same_order == first


def test_source_level_order_comparison_is_deterministic_and_keeps_channels() -> None:
    rows = evidence()
    channels = (EvidenceChannel.OUTCROSSING, EvidenceChannel.BAGGING, EvidenceChannel.FLOWER)
    first = compare_isolation_order(rows, island_summary_path=SUMMARY, draws=180, seed=23, included_channels=channels)
    second = compare_isolation_order(rows, island_summary_path=SUMMARY, draws=180, seed=23, included_channels=channels)

    assert first == second
    assert first.scenario == ISOLATION_ORDER_SCENARIO
    assert first.included_channels == channels
    assert first.n_outcrossing_rows == 17
    assert first.n_bagging_rows == 7
    assert first.n_flower_rows == 6
    assert first.expected_predictions[0].effective_outcross_service is None


def test_order_sensitivity_and_profile_are_reproducible() -> None:
    rows = evidence()
    settings = default_sensitivity_settings()[:1]
    sensitivity = isolation_order_sensitivity(
        rows,
        island_summary_path=SUMMARY,
        guide_constraints=(),
        settings=settings,
        seeds=(20260702,),
        draws=100,
    )
    first = profile_isolation_order(
        rows,
        island_summary_path=SUMMARY,
        population_size=24,
        iterations=2,
        seed=29,
    )
    second = profile_isolation_order(
        rows,
        island_summary_path=SUMMARY,
        population_size=24,
        iterations=2,
        seed=29,
    )

    assert len(sensitivity) == 1
    assert sensitivity[0].scenario == ISOLATION_ORDER_SCENARIO
    assert sensitivity[0].importance_effective_sample_size > 0.0
    assert first == second
    assert first.scenario == ISOLATION_ORDER_SCENARIO


def test_missing_order_is_rejected(tmp_path: Path) -> None:
    broken = tmp_path / "broken.csv"
    broken.write_text("island_id,region_order\nHonshu,0\n", encoding="utf-8")

    with pytest.raises(ValueError, match="region_order missing"):
        load_region_order(broken, evidence().islands)
