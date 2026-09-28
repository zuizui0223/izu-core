from pathlib import Path

from channel_id.campanula_volcanic_history_adversary import (
    HISTORY_CASES,
    load_history,
    load_observations,
    run_audit,
)

ROOT = Path(__file__).resolve().parents[1]
TRAITS = ROOT / "data" / "inoue_literature_island_traits.csv"
HISTORY = ROOT / "data" / "design" / "izu_volcanic_history_pre1986.csv"


def test_history_is_frozen_before_first_program_publication():
    records = load_history(HISTORY)
    assert set(records) == {"Oshima", "Toshima", "Niijima", "Kozushima", "Miyake", "Hachijo"}
    assert all(record.cutoff_year == 1986 for record in records.values())
    assert records["Oshima"].latest_pre_cutoff_event.startswith("1974")
    assert "1986 eruption" in records["Oshima"].notes
    assert records["Miyake"].eruption_age_min_years_at_cutoff == 3


def test_toshima_interval_is_not_collapsed_to_a_midpoint():
    young = load_observations(TRAITS, HISTORY, history_case="toshima_young_endpoint")
    old = load_observations(TRAITS, HISTORY, history_case="toshima_old_endpoint")
    young_toshima = next(row for row in young if row.island_id == "Toshima")
    old_toshima = next(row for row in old if row.island_id == "Toshima")
    assert young_toshima.eruption_age_years == 4036
    assert old_toshima.eruption_age_years == 9136
    assert young_toshima.log_eruption_age < old_toshima.log_eruption_age


def test_recent_100y_indicator_has_a_distinct_history_pattern():
    rows = load_observations(TRAITS, HISTORY, history_case="toshima_young_endpoint")
    recent = {row.island_id for row in rows if row.recent_100y_state == 1}
    assert recent == {"Oshima", "Miyake"}
    assert next(row for row in rows if row.island_id == "Toshima").recent_100y_state == 0


def test_audit_runs_both_interval_endpoints_without_postcutoff_leakage():
    result = run_audit(TRAITS, HISTORY)
    assert result["cutoff"] == "1986-01-01"
    assert tuple(result["cases"]) == HISTORY_CASES
    for payload in result["cases"].values():
        assert payload["best_composite"] is not None
        assert len(payload["trait_fits"]) >= 12
