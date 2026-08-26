from scripts.run_response_geometry_parameter_robustness import (
    BASE,
    SWEEPS,
    TRAIT_GRID,
    apply_sweep,
    build,
    endpoint,
    geometry,
)


def test_declared_geometry_covers_full_trait_axis_and_key_parameters():
    assert TRAIT_GRID[0] == 0.0
    assert TRAIT_GRID[-1] == 1.0
    assert len(TRAIT_GRID) == 21
    for name in [
        "trait_dispersion_multiplier",
        "generalist_fraction_shift",
        "replacement_fraction_shift",
        "partner_loss_multiplier",
        "partner_arrival_multiplier",
        "saturation",
        "trait_adjustment",
        "generalist_breadth",
        "specialist_breadth",
        "replacement_penalty",
    ]:
        assert name in SWEEPS


def test_endpoint_is_deterministic_for_fixed_seed():
    first = endpoint(0.35, BASE.mainland, 12345, BASE)
    second = endpoint(0.35, BASE.mainland, 12345, BASE)
    assert first == second
    assert 0.0 <= first[0] <= 1.0
    assert 0.0 <= first[1] <= 1.0


def test_sweep_changes_requested_parameter_without_retuning_others():
    changed = apply_sweep(BASE, "replacement_penalty", 0.65)
    assert changed.replacement_penalty == 0.65
    assert changed.mainland == BASE.mainland
    assert changed.island == BASE.island
    assert changed.saturation == BASE.saturation


def test_geometry_returns_matched_sign_map_without_empirical_fit():
    result = geometry(BASE, replicates=2, seed=20260826)
    assert result["matched_pollinator_realizations_across_trait_grid"] is True
    assert len(result["trait_rows"]) == len(TRAIT_GRID)
    assert isinstance(result["mixed_sign_geometry"], bool)
    assert all(row["mean_sign"] in {-1, 0, 1} for row in result["trait_rows"])


def test_build_pairs_seed_ensemble_across_parameter_values_and_is_fail_honest():
    payload = build(replicates=1, seed=20260826)
    assert payload["status"] == "scientific_reassessment_gate_phase1"
    assert payload["design"]["empirical_inputs_loaded"] == []
    assert payload["design"]["matched_pollinator_realizations_across_trait_grid"] is True
    assert payload["design"]["paired_seed_ensemble_across_parameter_values"] is True
    assert "does not estimate natural prevalence" in payload["claim_boundary"]
    assert "joint multi-parameter" in payload["next_gate"]
    assert payload["robustness_summary"]["one_factor_parameter_settings"] == sum(
        len(values) for values in SWEEPS.values()
    )
