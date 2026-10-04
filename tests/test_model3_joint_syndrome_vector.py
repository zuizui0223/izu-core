import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.audit_model3_joint_syndrome_vector import (
    rare_mutant_components,
)
from scripts.model3_island.density import density_step, make_grid
from scripts.model3_island.types import Config, PlantState
from scripts.model3_island_bridge_ops import prepare_arms

ROOT = Path(__file__).resolve().parents[1]


def _empty_state():
    return PlantState(
        alleles=np.empty((0, 3, 2), dtype=float),
        allele_origin=np.empty((0, 3, 2), dtype=np.int64),
        mutation_flags=np.empty((0, 3, 2), dtype=bool),
        ids=np.empty(0, dtype=np.int64),
        birth_years=np.empty(0, dtype=np.int64),
    )


def _base():
    design = json.loads(
        (ROOT / "data/design/model3_ch2_bridge_20260927.json").read_text()
    )
    return design, Config.from_dict(design["base_config"])


def test_decision_rules_were_frozen_before_rare_mutant_execution():
    design = json.loads(
        (ROOT / "data/design/model3_joint_syndrome_rare_mutant_20261004.json")
        .read_text()
    )
    assert design["status"] == "frozen_before_rare_mutant_execution"
    assert design["vector_definitions"]["gradient_shift_deadband"] == 0.05
    assert set(design["settings"]) == {
        "delayed_control",
        "prior_selfing",
        "pollen_discount",
        "assurance_cost",
    }


def test_rare_mutant_genome_contribution_matches_density_low_frequency_limit():
    design, base = _base()
    config = replace(
        base,
        assurance_mode="evolving",
        assurance_timing="delayed",
        pollen_discount=1.0,
        assurance_cost=0.5,
    )
    arms = prepare_arms(
        base,
        seed=int(design["history_seeds"][0]),
        pool_size=int(design["pool_size"]),
    )
    visitors = arms["near"][1].visitors[0]

    resident = (0.5, 0.5, 0.5)
    mutant = (0.5, 0.5, 0.5001)
    analytic = rare_mutant_components(
        resident, mutant, visitors, config
    )["parental_genome_contribution"]

    grid = make_grid(([0.5], [0.5], [0.5, 0.5001]))
    means = grid.genotypes.mean(axis=2)
    resident_ix = int(np.where(
        np.all(np.isclose(means, resident), axis=1)
    )[0][0])
    mutant_ix = int(np.where(
        np.all(np.isclose(means, mutant), axis=1)
    )[0][0])

    frac = 1e-7
    counts = np.zeros(len(grid.genotypes))
    counts[resident_ix] = config.capacity * (1.0 - frac)
    counts[mutant_ix] = config.capacity * frac

    _, ledger = density_step(
        counts,
        grid,
        visitors,
        _empty_state(),
        config,
        immigration_mode="source",
    )
    paternal = ledger.outcross.sum(axis=1)
    maternal_outcross = ledger.maternal - ledger.self_viable
    genome = (
        0.5 * maternal_outcross
        + 0.5 * paternal
        + ledger.self_viable
    )
    density_per_capita = genome[mutant_ix] / counts[mutant_ix]
    assert abs(density_per_capita - analytic) < 2e-6


def test_selfed_seed_counts_as_two_half_transmissions():
    design, base = _base()
    config = replace(
        base,
        assurance_mode="evolving",
        assurance_timing="delayed",
        pollen_discount=0.0,
        assurance_cost=0.0,
    )
    empty_visitors = prepare_arms(
        base,
        seed=int(design["history_seeds"][0]),
        pool_size=int(design["pool_size"]),
    )["far"][1].visitors[0]
    # This test only uses the identity if the selected year is empty.
    if len(empty_visitors.ids):
        return
    comp = rare_mutant_components(
        (0.5, 0.5, 0.5),
        (0.5, 0.5, 0.5),
        empty_visitors,
        config,
    )
    assert comp["maternal_outcross"] == 0
    assert comp["paternal_outcross"] == 0
    assert comp["parental_genome_contribution"] == comp["self_viable"]
