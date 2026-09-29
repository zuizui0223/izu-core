from pathlib import Path

from channel_id.island_source_level import load_source_level_evidence
from channel_id.source_level_profile import (
    ProfileSearchConfig,
    _mutate_draw,
    profile_source_level_scenarios,
)
from channel_id.island_multichannel import IslandScenario, draw_scenario_parameters


ROOT = Path(__file__).parents[1]


def evidence():
    return load_source_level_evidence(
        island_summary_path=ROOT / "data" / "inoue_literature_island_traits.csv",
        outcrossing_path=ROOT / "data" / "two_breakpoint_evidence" / "inoue1990_outcrossing.csv",
        bagging_path=ROOT / "data" / "two_breakpoint_evidence" / "inoue1988_bagging.csv",
        flower_path=ROOT / "data" / "two_breakpoint_evidence" / "inoue1995_flower_length.csv",
    )


def test_mutation_keeps_effectiveness_bounds_and_scenario_restrictions() -> None:
    rng = __import__("random").Random(8)
    base = draw_scenario_parameters(IslandScenario.ARDENS_BRIDGE_LOSS, 3, rng)
    mutated = _mutate_draw(base, IslandScenario.ARDENS_BRIDGE_LOSS, 2.0, rng)

    assert 0.0 <= mutated.large_bombus_effectiveness <= 1.0
    assert 0.0 <= mutated.small_bee_effectiveness <= 1.0
    assert 0.0 <= mutated.ardens_effectiveness <= 1.0
    assert mutated.ardens_effectiveness >= mutated.small_bee_effectiveness + 0.03 - 1e-12


def test_profile_search_is_deterministic_and_ranks_all_scenarios() -> None:
    config = ProfileSearchConfig(population_size=60, iterations=4, elite_fraction=0.20)
    first = profile_source_level_scenarios(evidence(), config=config, seed=101)
    second = profile_source_level_scenarios(evidence(), config=config, seed=101)

    assert first == second
    assert [result.profile_rank for result in first] == [1, 2, 3, 4]
    assert all(result.best_log_likelihood >= result.terminal_elite_mean_log_likelihood for result in first)
