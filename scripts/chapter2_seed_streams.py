from __future__ import annotations

import numpy as np


def _seed_int(sequence: np.random.SeedSequence) -> int:
    """Convert a SeedSequence node into a stable integer seed."""
    return int(sequence.generate_state(1, dtype=np.uint64)[0])


def paired_copy_seeds(master_seed: int, replicate: int, copies: int = 1) -> tuple[list[int], list[int]]:
    """Return independent mainland/island seed streams for one replicate.

    The hierarchy is master seed -> replicate -> scenario -> copy. Rebuilding the
    same hierarchy for different system sizes preserves common-random-number
    prefixes across copy counts without reusing a stream between scenarios or
    replicates.
    """
    if copies < 1:
        raise ValueError("copies must be >= 1")
    root = np.random.SeedSequence([int(master_seed), int(replicate)])
    mainland_sequence, island_sequence = root.spawn(2)
    mainland = [_seed_int(child) for child in mainland_sequence.spawn(copies)]
    island = [_seed_int(child) for child in island_sequence.spawn(copies)]
    return mainland, island


def paired_seeds(master_seed: int, replicate: int) -> tuple[int, int]:
    mainland, island = paired_copy_seeds(master_seed, replicate, copies=1)
    return mainland[0], island[0]
