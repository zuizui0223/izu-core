"""Fixed-N48 donor-homolog projection onto authenticated ORIGINAL Model3 founders.

TECHNICAL COUNTERFACTUAL ONLY: transfer I/A homolog offsets from n sampled
donors, not whole plants or historical alleles. No reproduction/update futures.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import numpy as np

from scripts.model3_island import types
from scripts.audit_chapter2_native_founder_source_20261014 import ordered_ids
from scripts.audit_chapter2_original_founder_compatibility_20261014 import (
    CONTEXTS, SOURCE_BIOMARK, SOURCE_SEED, DRAW_SEED,
    Intervention, archive_return_gate, ledger_parity, matched_draw,
    manipulate_homologs, original_context, original_fixture, source_state,
)

RECIPIENT_SALT = 'izu-core-512-T0-I-A-donor-projection-no-biology-v1'
PROJECTION_PROVENANCE_BASE = 2 * SOURCE_BIOMARK


@dataclass(frozen=True)
class Projection:
    state: types.PlantState
    n_original_donors: int
    donor_by_recipient_id: tuple[int, ...]
    original_block: str
    co_carriers: int


def fixed48_projection(original: types.PlantState, intervention: Intervention,
                       n: int, *, recipient_seed: int = 20261014) -> Projection:
    """Balance n donor homologs into 48 recipient plants without changing phenotypes."""
    if intervention.source_block not in ('main', 'confirmation'):
        raise ValueError('Unregistered founder source')
    if len(original.ids) != 48 or not np.array_equal(original.ids, np.arange(48)):
        raise ValueError('Not authenticated original founder numbering')
    if intervention.original_f0_alleles_sha256 != hashlib.sha256(
            original.alleles.tobytes()).hexdigest():
        raise ValueError('Wrong original F0 genome for projection')
    if not isinstance(n, int) or type(n) is not int or n not in (2, 8, 24, 48):
        raise ValueError('Unregistered donor number')
    if not np.array_equal(original.alleles.mean(axis=2),
                          intervention.state.alleles.mean(axis=2)):
        raise ValueError('Donor intervention changed starting adult phenotypes')

    _, donor_state = matched_draw(original, intervention.state, n, DRAW_SEED)
    donors = donor_state.ids
    if n == 48:
        assignments = original.ids.copy()  # genuine same-source ID and no redundant permutation
    else:
        receivers = ordered_ids(original.ids, recipient_seed, RECIPIENT_SALT)
        assignments = np.full(48, -1, dtype=np.int64)
        for pos, receiver_id in enumerate(receivers):
            assignments[int(receiver_id)] = int(donors[pos % n])
    unique, counts = np.unique(assignments, return_counts=True)
    if (len(unique) != n or not np.array_equal(unique, donors)
            or not np.all(counts == 48 // n)):
        raise AssertionError('Unbalanced fixed-census founder homolog projection')

    altered = original.alleles.copy()
    origins = original.allele_origin.copy()
    block_index = 0 if intervention.source_block == 'main' else 1
    source_alleles = intervention.state.alleles
    for locus in (1, 2):
        recipient_mean = original.alleles[:, locus, :].mean(axis=1)
        source_offsets = (source_alleles[assignments, locus, 1] -
                          source_alleles[assignments, locus, 0]) / 2
        altered[:, locus, 0] = recipient_mean - source_offsets
        altered[:, locus, 1] = recipient_mean + source_offsets
        for copy in (0, 1):
            origins[:, locus, copy] = (PROJECTION_PROVENANCE_BASE +
                                     block_index * 1_000_000 +
                                     original.ids * 10 + locus * 2 + copy)
    projected = types.PlantState(
        alleles=altered, allele_origin=origins,
        mutation_flags=original.mutation_flags,
        ids=original.ids, birth_years=original.birth_years,
    )
    if (not np.array_equal(projected.alleles.mean(axis=2),
                           original.alleles.mean(axis=2))
            or not np.array_equal(projected.alleles[:, 0, :],
                                  original.alleles[:, 0, :])
            or not np.array_equal(projected.allele_origin[:, 0, :],
                                  original.allele_origin[:, 0, :])
            or np.any(projected.allele_origin[:, 1:, :] < PROJECTION_PROVENANCE_BASE)):
        raise ValueError('Genetic-only technical projection fails initial phenotype or provenance')
    if n == 48 and not np.array_equal(projected.alleles, intervention.state.alleles):
        raise ValueError('All-founder projection fails original engineered donor identity')
    return Projection(projected, n, tuple(map(int, assignments)),
                      intervention.source_block, intervention.m)


def technical_report() -> dict:
    """96 extra native static parity checks at N=48; no evolution simulation."""
    d = original_fixture()
    rows = []
    checks = 0
    for block in ('main', 'confirmation'):
        original = source_state(d, block)
        contexts = {k: original_context(d, block, k) for k in CONTEXTS}
        for overlap in (0, 3, 6, 12):
            intervention = manipulate_homologs(
                original, block=block, overlap=overlap, source_seed=SOURCE_SEED)
            for n in (2, 8, 24, 48):
                projected = fixed48_projection(original, intervention, n)
                if len(projected.state.ids) != 48:
                    raise AssertionError('Fixed-census projection count differs')
                for context, (config, visitors) in contexts.items():
                    digest = ledger_parity(original, projected.state, config, visitors)
                    checks += 1
                    rows.append({
                        'original_block': block,
                        'overlap_A_I_original_carriers': overlap,
                        'n_donor_founders': n,
                        'fixed_plant_census': 48,
                        'ecological_context': context,
                        'original_donor_ids': list(sorted(set(projected.donor_by_recipient_id))),
                        'artificial_homolog_donor_by_recipient': list(projected.donor_by_recipient_id),
                        'initial_return_ledger_sha256': digest,
                        'edited_full48_genome_sha256': hashlib.sha256(
                            projected.state.alleles.tobytes()).hexdigest(),
                    })
    if checks != 96 or len(rows) != 96:
        raise AssertionError('Not all registered source-paired contexts audited')
    return {
        'status': 'ORIGINAL_T0_DONOR_HOMOLOG_PROJECTION_TECHNICAL_ONLY',
        'original_source_fixture_verified': True,
        'provenance_namespace': PROJECTION_PROVENANCE_BASE,
        'original_source_blocks': 2,
        'same_phenotype_fixed_N48_technical_returns': checks,
        'biological_futures_or_new_population_histories': 0,
        'rows': rows,
        'interpretation': [
            'This is *not* real source-plant cloning or island founding.',
            'I/A homolog offsets are duplicated across otherwise distinct adults.',
            'Projection preserves adult M/I/A phenotype but constructs artificial relationships.',
            'Changing n in source subpopulation and projecting to fixed 48 are distinct interventions.',
            'No natural-order survival effect or genomic mediation can be inferred.',
        ],
    }


def main() -> None:
    print(json.dumps(technical_report(), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
