from pathlib import Path
import random

from channel_id.regime_shape_identifiability import (
    design_rows,
    identifiable_models,
    load_effort,
    load_scaffold,
    run_identifiability_audit,
    select_model_once,
)

ROOT = Path(__file__).resolve().parents[1]
SCAFFOLD = ROOT / "data" / "design" / "izu_regime_scaffold.csv"
EFFORT = ROOT / "data" / "public" / "izu_occurrence_audit" / "izu_9island_effort.csv"


def test_nine_island_scaffold_locks_two_boundaries() -> None:
    rows = load_scaffold(SCAFFOLD)
    islands = [row for row in rows if row.unit_type == "island"]

    assert len(rows) == 10
    assert len(islands) == 9
    assert rows[0].pollinator_regime == "large_bombus"
    oshima = next(row for row in rows if row.unit_id == "izu_oshima")
    toshima = next(row for row in rows if row.unit_id == "toshima")
    assert (oshima.first_boundary_state, oshima.second_boundary_state) == (1, 0)
    assert (toshima.first_boundary_state, toshima.second_boundary_state) == (1, 1)
    assert toshima.analysis_role == "second_boundary_anchor"


def test_mainland_reference_is_required_to_identify_first_step() -> None:
    rows = load_scaffold(SCAFFOLD)
    with_mainland = design_rows(rows, "current_six_plus_mainland", "continuous")
    island_only = design_rows(rows, "current_six_island_only", "continuous")

    assert "first_step" in identifiable_models(with_mainland)
    assert "first_step" not in identifiable_models(island_only)
    assert "second_step" in identifiable_models(island_only)


def test_low_noise_virtual_truths_recover_cline_and_second_step() -> None:
    rows = load_scaffold(SCAFFOLD)
    effort = load_effort(EFFORT)
    full = design_rows(rows, "full_nine_plus_mainland", "continuous")

    assert select_model_once(
        random.Random(7),
        full,
        "continuous",
        "cline",
        effort,
        lineages=60,
        effect_size=2.0,
        continuous_noise_sd=0.20,
    ) == "cline"
    assert select_model_once(
        random.Random(11),
        full,
        "continuous",
        "second_step",
        effort,
        lineages=60,
        effect_size=2.0,
        continuous_noise_sd=0.20,
    ) == "second_step"


def test_small_audit_reports_focus_metrics() -> None:
    report = run_identifiability_audit(
        load_scaffold(SCAFFOLD),
        load_effort(EFFORT),
        replicates=12,
        lineages=8,
        seed=20260715,
    )

    assert len(report.cells) == 5 * 3 * 6
    assert report.focus["first_step_identifiable"]["current_six_plus_mainland"] is True
    assert report.focus["first_step_identifiable"]["current_six_island_only"] is False
    for domain in (
        "continuous_second_step_recovery",
        "binary_second_step_recovery",
        "occupancy_second_step_recovery",
    ):
        assert all(0.0 <= value <= 1.0 for value in report.focus[domain].values())
