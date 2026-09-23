from __future__ import annotations

import numpy as np


def _seed_sequence_to_int(sequence: np.random.SeedSequence) -> int:
    """Convert a SeedSequence child into a stable 128-bit Python integer seed."""
    words = sequence.generate_state(4, dtype=np.uint32)
    value = 0
    for word in words:
        value = (value << 32) | int(word)
    return value


def scenario_copy_seeds(
    master_seed: int,
    replicate_index: int,
    scenario_index: int,
    copies: int = 1,
) -> tuple[int, ...]:
    """Return disjoint deterministic child streams for one replicate/scenario.

    The hierarchy is master seed -> replicate -> scenario -> copy. Calling this
    function with larger copies preserves the prefix, so k=1,2,4,... audits
    intentionally share common random numbers without mainland/island stream
    collisions.
    """
    if replicate_index < 0:
        raise ValueError("replicate_index must be non-negative")
    if scenario_index not in (0, 1):
        raise ValueError("scenario_index must be 0 (mainland) or 1 (island)")
    if copies < 1:
        raise ValueError("copies must be positive")

    root = np.random.SeedSequence([int(master_seed), int(replicate_index)])
    scenario = root.spawn(2)[scenario_index]
    return tuple(_seed_sequence_to_int(child) for child in scenario.spawn(copies))


def paired_scenario_seeds(master_seed: int, replicate_index: int) -> tuple[int, int]:
    """Return one mainland and one island seed from disjoint child streams."""
    return (
        scenario_copy_seeds(master_seed, replicate_index, 0, 1)[0],
        scenario_copy_seeds(master_seed, replicate_index, 1, 1)[0],
    )
