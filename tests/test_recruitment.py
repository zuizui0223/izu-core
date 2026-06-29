from channel_id.recruitment import BevertonHoltEstablishment, ConstantEstablishment


def test_constant_establishment_preserves_the_baseline_factorisation() -> None:
    model = ConstantEstablishment(0.25)
    result = model.recruit(8.0)

    assert result.establishment_probability == 0.25
    assert result.retained_recruits == 2.0


def test_beverton_holt_establishment_makes_e_seed_supply_dependent() -> None:
    model = BevertonHoltEstablishment(
        low_density_probability=0.4,
        half_saturation_viable_seeds=3.0,
    )
    low = model.recruit(2.0)
    high = model.recruit(8.0)

    assert high.establishment_probability < low.establishment_probability
    assert high.retained_recruits > low.retained_recruits
    assert high.retained_recruits / low.retained_recruits < high.viable_seeds / low.viable_seeds


def test_half_saturation_has_the_declared_interpretation() -> None:
    model = BevertonHoltEstablishment(
        low_density_probability=0.4,
        half_saturation_viable_seeds=3.0,
    )

    assert model.establishment_probability(3.0) == 0.2
