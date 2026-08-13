from channel_id.virtual_izu_abm import default_islands, generate_founders, run_abm


def test_default_scaffold_has_declared_regime_boundary():
    islands = default_islands()
    assert islands[1].ardens > 0
    assert all(island.ardens == 0 for island in islands[2:])


def test_abm_is_reproducible():
    a = run_abm(scenario="environment_plus_pollinator", generations=12, founders=60, seed=9)
    b = run_abm(scenario="environment_plus_pollinator", generations=12, founders=60, seed=9)
    assert a["final"] == b["final"]


def test_all_scenarios_run_and_report_southern_lineages():
    scenarios = (
        "environment_only",
        "distance_only",
        "pollinator_regime",
        "environment_plus_pollinator",
        "small_bee_substitution",
    )
    for scenario in scenarios:
        result = run_abm(scenario=scenario, generations=8, founders=50, seed=3)
        assert result["scenario"] == scenario
        assert result["final"]["southern_lineages"] >= 0
        assert len(result["trajectory"]) == 3


def test_founder_traits_stay_bounded():
    founders = generate_founders(30, seed=4)
    for plant in founders:
        assert 0 <= plant.specialization <= 1
        assert 0 <= plant.autonomous_selfing <= 1
        assert 0 <= plant.dispersal <= 1
