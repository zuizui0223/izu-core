from pathlib import Path

from channel_id.pollinator_regime_evidence_audit import (
    build_audit,
    load_effort_rows,
    load_model_indicators,
    load_rate_rows,
)


ROOT = Path(__file__).parents[1]


def _audit():
    return build_audit(
        load_model_indicators(ROOT / "data" / "inoue_literature_island_traits.csv"),
        load_rate_rows(ROOT / "data" / "two_breakpoint_evidence" / "inoue1986_pollinator_rates.csv"),
        load_effort_rows(ROOT / "data" / "two_breakpoint_evidence" / "inoue1986_observation_effort.csv"),
    )


def _row(rows, island_id, indicator):
    return next(row for row in rows if row.island_id == island_id and row.model_indicator == indicator)


def test_positive_rate_and_effort_are_retained_for_oshima_ardens() -> None:
    row = _row(_audit(), "Oshima", "bombus_ardens")

    assert row.model_value == 1
    assert row.effort_hours == 9.0
    assert [rate.rate_per_hour for rate in row.positive_rates] == [1.1]
    assert row.source_status == "positive_rate_reported"


def test_nonreport_after_effort_is_not_relabelled_as_absence() -> None:
    row = _row(_audit(), "Hachijo", "bombus_ardens")

    assert row.model_value == 0
    assert row.effort_hours == 6.0
    assert row.positive_rates == ()
    assert row.source_status == "not_reported_in_rate_table_after_recorded_effort"
    assert "not a confirmed zero" in row.interpretation


def test_toshima_is_explicitly_outside_inoue_1986_effort_coverage() -> None:
    row = _row(_audit(), "Toshima", "halictid_pollinator")

    assert row.model_value == 1
    assert row.effort_hours == 0.0
    assert row.source_status == "no_inoue1986_effort_row_for_unit"


def test_mainland_positive_rates_map_to_honshu() -> None:
    row = _row(_audit(), "Honshu", "bombus_diversus")

    assert row.model_value == 1
    assert row.effort_hours == 12.5
    assert len(row.positive_rates) >= 1
    assert row.source_status == "positive_rate_reported"


def test_current_binary_inputs_do_not_discard_any_direct_positive_rate() -> None:
    conflicts = [
        row
        for row in _audit()
        if row.source_status == "positive_rate_reported" and row.model_value == 0
    ]

    assert conflicts == []
