"""Technical negative control for the Q1 assurance-evolvability intervention.

This is a *short debug fixture*, not a registered new evolutionary cohort.
Allowing mutations at a genetically silent A locus while keeping expressed
assurance fixed at A=0.5 must NOT change either X/I genomic history or the
realised demographic lottery. This probes leaked A alleles, mutation-stream
coupling and accidental cross-locus effects that the original zero-mutation
fixed/evolving control could not reveal.
"""
from __future__ import annotations

import numpy as np
import pytest

from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config, founders, load_design,
)
from scripts.run_model3_persistent_isolation import exposure
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.model3_island.reproduction import reproduce


@pytest.fixture(scope="module")
def original_design():
    return load_design(DEFAULT_DESIGN)


def _sham_steps(design, setting: str, arm: str, *, silent_a_mutation: bool):
    """Different mutation PERMISSION in inheritance, identical expressed A.

    The sham condition uses evolving-A *only* for the inheritance operation.
    Reproduction ALWAYS uses the frozen fixed-A configuration. Original Model3
    inherited alleles and separate random streams are used without changing any
    production file; these eight updates are test fixtures, not result histories.
    """
    reproductive_cfg = config(design, setting, .01, "fixed")
    inherited_cfg = config(
        design, setting, .01,
        "evolving" if silent_a_mutation else "fixed",
    )
    history_seed = 26110601
    repeat_seed = 26111601
    env = exposure(history_seed, arm)
    pop = founders(design)
    assert np.array_equal(pop.alleles[:, 2, :],
                          np.full_like(pop.alleles[:, 2, :], .5))
    master = int(np.random.SeedSequence(
        [history_seed, repeat_seed]
    ).generate_state(1)[0])
    streams = {name: stream(master, name, 0) for name in STREAM_IDS}
    trajectory = []
    saw_a_mutation = False
    for year in range(8):
        # Frozen, expressed A=0.5 for both arms, even if the *sham* has
        # accumulated unexpressed A mutations in its diploid genotype.
        ledger = reproduce(pop, env.visitors[year], reproductive_cfg)
        pop, _ = advance(
            pop, ledger, env.seed_candidates[year], inherited_cfg,
            streams, year=year, mutation_traits=(True, True, True),
        )
        trajectory.append((
            pop.ids.copy(),
            pop.alleles[:, :2, :].copy(),
            pop.alleles[:, 2, :].copy(),
            pop.mutation_flags[:, :2, :].copy(),
        ))
        saw_a_mutation |= bool(np.any(pop.mutation_flags[:, 2, :]))
    return trajectory, saw_a_mutation


@pytest.mark.parametrize("setting", (
    "delayed_control", "prior_selfing", "pollen_discount", "assurance_cost",
))
@pytest.mark.parametrize("arm", ("near", "far"))
def test_silent_a_mutation_cannot_change_finite_flower_investment(
    original_design, setting, arm,
):
    reference, _ = _sham_steps(
        original_design, setting, arm, silent_a_mutation=False,
    )
    sham, sham_mutated_a = _sham_steps(
        original_design, setting, arm, silent_a_mutation=True,
    )
    assert sham_mutated_a, "technical fixture did not actually mutate silent A"
    assert len(reference) == len(sham) == 8
    for (ids0, loci0, a0, flags0), (ids1, loci1, a1, flags1) in zip(
        reference, sham
    ):
        assert np.array_equal(ids0, ids1)
        # This equality tests the WHOLE diploid matching/investment genotypes,
        # not only the final means or the sign of the treatment interaction.
        assert np.array_equal(loci0, loci1)
        assert np.array_equal(flags0, flags1)
        assert np.all(a0 == .5)
    assert any(
        not np.array_equal(a0, a1)
        for (_, _, a0, _), (_, _, a1, _) in zip(reference, sham)
    )


def test_t0_fixed_and_evolving_reproduction_are_identical_in_all_settings(
    original_design,
):
    pop = founders(original_design)
    visitors = exposure(26110601, "near").visitors[0]
    for setting in original_design["settings"]:
        fixed = reproduce(pop, visitors, config(original_design, setting, .01, "fixed"))
        evolving = reproduce(pop, visitors, config(original_design, setting, .01, "evolving"))
        for field in ("outcross", "self_viable", "maternal", "paternal", "ovules"):
            assert np.array_equal(getattr(fixed, field), getattr(evolving, field))
