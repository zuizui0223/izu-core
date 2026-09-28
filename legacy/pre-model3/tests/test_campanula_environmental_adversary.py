from pathlib import Path

from channel_id.campanula_environmental_adversary import (
    composite_fits,
    fit_channel_models,
    load_island_rows,
)

ROOT = Path(__file__).resolve().parent.parent


def test_joint_channel_shape_audit_prefers_hybrid_over_single_climate_axis():
    rows = load_island_rows(ROOT / "data/inoue_literature_island_traits.csv")
    fits, loadings = fit_channel_models(rows)
    composites = composite_fits(fits)
    assert set(loadings) == {"mean_temp_c", "annual_precip_mm", "precip_cv"}
    assert composites[0].model_id == "two_stage_hybrid"
    by_key = {(fit.trait_id, fit.model_id): fit for fit in fits}
    assert (
        by_key[("bagged_capsule_set_proportion", "oshima_to_toshima_step")].aicc
        < by_key[("bagged_capsule_set_proportion", "climate_pc1_cline")].aicc
    )
    assert (
        by_key[("outcrossing_midpoint", "island_order_cline")].aicc
        < by_key[("outcrossing_midpoint", "climate_pc1_cline")].aicc
    )


def test_step_cv_is_explicitly_conditional_on_baseline_retention():
    rows = load_island_rows(ROOT / "data/inoue_literature_island_traits.csv")
    fits, _ = fit_channel_models(rows)
    bag_step = next(
        fit for fit in fits
        if fit.trait_id == "bagged_capsule_set_proportion" and fit.model_id == "oshima_to_toshima_step"
    )
    assert bag_step.loo_kind == "leave_no_bombus_out"
    assert bag_step.loo_mse is not None
    assert bag_step.loo_mse < 0.01
