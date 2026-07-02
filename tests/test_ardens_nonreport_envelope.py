from pathlib import Path

from channel_id.ardens_nonreport_envelope import (
    derive_uncertain_ardens_islands,
    enumerate_ardens_context_envelope,
    summarize_envelope,
)
from channel_id.pollinator_hierarchy_counterfactual import load_records
from channel_id.pollinator_regime_evidence_audit import (
    build_audit,
    load_effort_rows,
    load_model_indicators,
    load_rate_rows,
)


ROOT = Path(__file__).parents[1]
INPUT = ROOT / "data" / "inoue_literature_island_traits.csv"
RATES = ROOT / "data" / "two_breakpoint_evidence" / "inoue1986_pollinator_rates.csv"
EFFORT = ROOT / "data" / "two_breakpoint_evidence" / "inoue1986_observation_effort.csv"


def _inputs():
    records = load_records(INPUT)
    audit = build_audit(
        load_model_indicators(INPUT),
        load_rate_rows(RATES),
        load_effort_rows(EFFORT),
    )
    return records, audit


def test_uncertain_islands_follow_nonreport_or_no_effort_semantics_not_oshima_positive() -> None:
    records, audit = _inputs()

    uncertain = derive_uncertain_ardens_islands(records, audit)

    assert uncertain == ("Hachijo", "Kozushima", "Miyake", "Niijima", "Toshima")
    assert "Oshima" not in uncertain
    assert "Honshu" not in uncertain


def test_envelope_enumerates_all_binary_context_codings_without_probability_weights() -> None:
    records, audit = _inputs()
    uncertain = derive_uncertain_ardens_islands(records, audit)

    configurations = enumerate_ardens_context_envelope(records, uncertain)

    assert len(configurations) == 2 ** len(uncertain)
    assert configurations[0].coded_zero_islands == uncertain
    assert configurations[-1].coded_one_islands == uncertain
    assert all(row.pollinator_hierarchy_mae >= 0.0 for row in configurations)
    assert all(1 <= row.pollinator_hierarchy_rank <= 3 for row in configurations)


def test_summary_reports_range_not_posterior_probability() -> None:
    records, audit = _inputs()
    uncertain = derive_uncertain_ardens_islands(records, audit)
    summary = summarize_envelope(enumerate_ardens_context_envelope(records, uncertain), uncertain)

    assert summary["configuration_count"] == 32
    assert summary["pollinator_hierarchy_best_rank"] >= 1
    assert summary["pollinator_hierarchy_worst_rank"] <= 3
    assert "no probability weights" in summary["boundary"]
