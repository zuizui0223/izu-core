from pathlib import Path

from channel_id.campanula_geography_adversary import (
    build_geography_axes,
    fit_trait_models,
    load_observations,
    run_audit,
)


ROOT = Path(__file__).resolve().parents[1]
TRAITS = ROOT / "data" / "inoue_literature_island_traits.csv"
SCAFFOLD = ROOT / "data" / "design" / "izu_regime_scaffold.csv"
GEOGRAPHY = ROOT / "data" / "design" / "izu_geography_covariates.csv"


def test_full_nine_island_geography_is_source_locked():
    axes, anchor = build_geography_axes(SCAFFOLD, GEOGRAPHY)
    assert anchor == (34.75, 138.95)
    assert len(axes) == 9
    indexed = {row.unit_id: row for row in axes}
    assert 91.9 < indexed["izu_oshima"].area_km2 < 92.1
    assert 4.3 < indexed["toshima"].area_km2 < 4.6
    assert indexed["niijima"].nearest_island_distance_km < 10.0
    assert indexed["hachijojima"].nearest_island_distance_km > 60.0


def test_geography_pressure_is_built_before_trait_join():
    rows, axes = load_observations(TRAITS, SCAFFOLD, GEOGRAPHY)
    assert len(axes) == 9
    assert len(rows) == 6
    assert rows[0].island_id == "Oshima"
    assert rows[1].island_id == "Toshima"
    # The composite geography index is not a disguised island-order score.
    assert rows[1].geography_pressure_index > rows[0].geography_pressure_index
    assert rows[2].geography_pressure_index < rows[1].geography_pressure_index


def test_autonomous_step_beats_static_geography_axes():
    rows, _ = load_observations(TRAITS, SCAFFOLD, GEOGRAPHY)
    fits = fit_trait_models(rows)
    indexed = {(fit.trait_id, fit.model_id): fit for fit in fits}
    step = indexed[("bagged_capsule_set_proportion", "oshima_to_toshima_step")]
    assert step.aicc is not None
    for model in (
        "mainland_distance_cline",
        "log_area_cline",
        "nearest_island_distance_cline",
        "geography_pressure_cline",
    ):
        competitor = indexed[("bagged_capsule_set_proportion", model)]
        assert competitor.aicc is not None
        assert step.aicc < competitor.aicc


def test_two_stage_order_hybrid_beats_declared_static_geography_hybrid():
    result = run_audit(TRAITS, SCAFFOLD, GEOGRAPHY)
    composites = {row["model_id"]: row["composite_aicc"] for row in result["composite_fits"]}
    assert result["best_composite"] == "two_stage_order_hybrid"
    assert composites["two_stage_order_hybrid"] < composites["two_stage_geography_hybrid"]
    assert composites["two_stage_order_hybrid"] < composites["two_stage_area_hybrid"]
    assert composites["two_stage_order_hybrid"] < composites["two_stage_nearest_hybrid"]
    assert result["claim_boundary"].startswith("Area, mainland distance")
