from pathlib import Path

from channel_id.campanula_isolation_adversary import (
    fit_trait_models,
    load_observations,
    run_audit,
)


ROOT = Path(__file__).resolve().parents[1]
TRAITS = ROOT / "data" / "inoue_literature_island_traits.csv"
SCAFFOLD = ROOT / "data" / "design" / "izu_regime_scaffold.csv"


def test_isolation_axis_is_not_just_island_order():
    rows, anchor = load_observations(TRAITS, SCAFFOLD)
    assert anchor == (34.75, 138.95)
    assert rows[0].island_id == "Oshima"
    assert rows[1].island_id == "Toshima"
    # The frozen mainland-distance axis is genuinely distinct from the ordinal
    # north-to-south scaffold: Toshima is slightly closer to the anchor than Oshima.
    assert rows[1].mainland_distance_km < rows[0].mainland_distance_km
    assert 35.0 < rows[0].mainland_distance_km < 45.0
    assert 190.0 < rows[-1].mainland_distance_km < 205.0


def test_locked_channels_do_not_reduce_to_mainland_distance():
    rows, _ = load_observations(TRAITS, SCAFFOLD)
    fits = fit_trait_models(rows)
    indexed = {(fit.trait_id, fit.model_id): fit for fit in fits}

    outcross_order = indexed[("outcrossing_midpoint", "island_order_cline")]
    outcross_distance = indexed[("outcrossing_midpoint", "mainland_distance_cline")]
    assert outcross_order.aicc is not None and outcross_distance.aicc is not None
    assert outcross_order.aicc < outcross_distance.aicc

    autonomous_step = indexed[("bagged_capsule_set_proportion", "oshima_to_toshima_step")]
    autonomous_distance = indexed[("bagged_capsule_set_proportion", "mainland_distance_cline")]
    assert autonomous_step.aicc is not None and autonomous_distance.aicc is not None
    assert autonomous_step.aicc < autonomous_distance.aicc
    assert autonomous_distance.aicc - autonomous_step.aicc > 20.0


def test_two_stage_order_hybrid_is_best_current_isolation_audit():
    result = run_audit(TRAITS, SCAFFOLD)
    assert result["best_composite"] == "two_stage_order_hybrid"
    assert result["claim_boundary"].startswith("Mainland great-circle distance")
