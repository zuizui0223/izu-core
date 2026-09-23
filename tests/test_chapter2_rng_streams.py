from __future__ import annotations

from scripts.chapter2_rng import paired_scenario_seeds, scenario_copy_seeds


SEEDS = (20260826, 20250101, 20260833, 20260827, 999983, 12345)


def test_baseline_streams_are_unique_across_scenarios_and_replicates() -> None:
    generated = []
    for master_seed in SEEDS:
        for replicate in range(96):
            generated.extend(paired_scenario_seeds(master_seed, replicate))
    assert len(generated) == 6 * 96 * 2
    assert len(generated) == len(set(generated))


def test_system_size_stream_prefix_is_stable() -> None:
    for master_seed in SEEDS:
        for replicate in (0, 1, 10, 95):
            for scenario_index in (0, 1):
                one = scenario_copy_seeds(master_seed, replicate, scenario_index, 1)
                two = scenario_copy_seeds(master_seed, replicate, scenario_index, 2)
                sixteen = scenario_copy_seeds(master_seed, replicate, scenario_index, 16)
                assert one == two[:1] == sixteen[:1]
                assert two == sixteen[:2]


def test_declared_six_seed_k16_design_has_no_stream_collisions() -> None:
    generated = []
    for master_seed in SEEDS:
        for replicate in range(96):
            for scenario_index in (0, 1):
                generated.extend(
                    scenario_copy_seeds(master_seed, replicate, scenario_index, 16)
                )
    assert len(generated) == 6 * 96 * 2 * 16
    assert len(generated) == len(set(generated))
