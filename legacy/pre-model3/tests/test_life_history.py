from channel_id.life_history import (
    LifeHistoryParameters,
    Metric,
    ObservationInterval,
    ParameterGrid,
    Regime,
    SimulationCase,
    TraitState,
    assess_compatibility,
    retain_compatible_candidates,
    simulate_life_history,
)


def test_life_history_factorisation_holds() -> None:
    result = simulate_life_history(
        TraitState(attraction=0.5, assurance=0.5),
        Regime(pollinator_service=0.5, establishment_multiplier=1.0),
        LifeHistoryParameters(
            seed_budget=10.0,
            baseline_outcross_fraction=0.2,
            attraction_pollination_gain=0.4,
            attraction_cost=0.0,
            assurance_cost=0.0,
            selfing_viability=0.5,
            baseline_establishment=0.2,
        ),
    )

    assert result.local_viable_seed_output == (
        result.outcross_viable_seeds + result.selfed_viable_seeds
    )
    assert result.retained_recruits == (
        result.local_viable_seed_output * result.establishment
    )


def test_compatibility_reports_failed_measurement() -> None:
    parameters = LifeHistoryParameters(
        seed_budget=5.0,
        baseline_outcross_fraction=0.0,
        attraction_pollination_gain=0.0,
        attraction_cost=0.0,
        assurance_cost=0.0,
        selfing_viability=1.0,
        baseline_establishment=0.5,
    )
    case = SimulationCase(
        name="low_service",
        trait=TraitState(attraction=0.0, assurance=1.0),
        regime=Regime(pollinator_service=0.0),
        observations=(
            ObservationInterval(Metric.RETAINED_RECRUITS, 3.0, 4.0),
        ),
    )

    report = assess_compatibility(parameters, [case])

    assert not report.compatible
    assert "retained_recruits" in report.failures[0]


def test_grid_retains_only_compatible_candidates() -> None:
    case = SimulationCase(
        name="known",
        trait=TraitState(attraction=0.0, assurance=1.0),
        regime=Regime(pollinator_service=0.0),
        observations=(
            ObservationInterval(Metric.LOCAL_VIABLE_SEED_OUTPUT, 4.9, 5.1),
        ),
    )
    grid = ParameterGrid(
        seed_budget=(5.0,),
        baseline_outcross_fraction=(0.0,),
        attraction_pollination_gain=(0.0,),
        attraction_cost=(0.0,),
        assurance_cost=(0.0,),
        selfing_viability=(0.5, 1.0),
        baseline_establishment=(0.5,),
    )

    reports = retain_compatible_candidates(grid, [case])

    assert len(reports) == 1
    assert reports[0].parameters.selfing_viability == 1.0
