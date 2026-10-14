"""Pre-execution technical synthetic founder-state check using original Model3 types.

NO biological futures, births, fitness inference, new ecological histories, or
registered scientific experiments. Every virtual allele is marked synthetic.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import numpy as np

from scripts.model3_island import reproduction, types

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / 'data/design/chapter2_colonisation_genetic_access_draft_20261014.json'
PINNED_MODULE_BLOBS = {
    'types.py': '0bc427b3261e7baf1651648ee879b368f9bf935b',
    'reproduction.py': '95314698a3296b6f13b8c053c36f2df0b7b744ca',
}
LEDGER_FIELDS = ('outcross', 'self_raw', 'self_viable', 'ovules',
                 'exported', 'delivered', 'lost', 'maternal', 'paternal')
SOURCE_SALT = 'izu-core-512-synthetic-source-TECHNICAL-NOT-REGISTERED'
DRAW_SALT = 'izu-core-512-synthetic-draw-TECHNICAL-NOT-REGISTERED'


def _blob_sha(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def native_gate() -> None:
    for name, module in (('types.py', types), ('reproduction.py', reproduction)):
        if _blob_sha(Path(module.__file__).read_bytes()) != PINNED_MODULE_BLOBS[name]:
            raise ValueError('frozen native Model3 module changed: ' + name)


def design_gate() -> dict:
    d = json.loads(SPEC.read_text(encoding='utf-8'))
    if (d.get('status') != 'DESIGN_CANDIDATE_NO_EXECUTION_NO_CONFIRMATION'
            or d.get('approval', {}).get('author_approval_for_new_biology') is not False
            or d.get('approval', {}).get('new_biological_histories') != 0
            or d.get('approval', {}).get('source_genotypes_and_rng_frozen') is not False
            or d.get('illustrative_mainland_source', {}).get('real_observed_mainland_data') is not False
            or d.get('candidate_founder_samples') != [2, 8, 24, 48]):
        raise ValueError('Synthetic design is not a scientific execution permission')
    return d


def ordered_ids(ids: np.ndarray, seed: int, salt: str) -> np.ndarray:
    if type(seed) is not int or not 0 <= seed < 2**63:
        raise ValueError('Unregistered synthetic source/draw seed')
    # SHA ranking avoids shared RNG state and pins paired draws across arms.
    labels = [(hashlib.sha256(f'{salt}|{seed}|{int(i)}'.encode()).digest(), int(i))
              for i in ids]
    return np.array([i for _, i in sorted(labels)], dtype=np.int64)


def synthetic_reference() -> types.PlantState:
    """Artificial N=48 input; NOT measured mainland or canonical original founders."""
    ids = np.arange(48, dtype=np.int64)
    means = np.empty((48, 3), dtype=np.float64)
    means[:, 0] = 0.5 + ((ids % 5) - 2) / 64  # M: virtual matching variance
    means[:, 1] = 0.5 + ((ids % 7) - 3) / 64  # I: virtual expressed heterogeneity
    means[:, 2] = 0.5
    return types.PlantState(
        alleles=np.repeat(means[:, :, None], 2, axis=2),
        allele_origin=np.broadcast_to(ids[:, None, None], (48, 3, 2)).copy(),
        mutation_flags=np.zeros((48, 3, 2), dtype=bool),
        ids=ids,
        birth_years=np.zeros(48, dtype=np.int64),
    )


def _require_virtual_reference(reference: types.PlantState) -> None:
    if not isinstance(reference, types.PlantState) or len(reference.ids) != 48:
        raise ValueError('Only an explicit synthetic 48-individual source fixture is allowed')
    if not np.array_equal(reference.ids, np.arange(48)) or np.any(reference.birth_years != 0):
        raise ValueError('Virtual source ID or original-founder year changed')
    if not np.array_equal(reference.allele_origin,
                          np.broadcast_to(reference.ids[:, None, None], (48, 3, 2))):
        raise ValueError('Synthetic ancestry must be explicitly labelled by source individual')
    if np.any(reference.mutation_flags):
        raise ValueError('Virtual source cannot silently inherit historical mutations')
    if (np.any(reference.alleles[:, :, 0] != reference.alleles[:, :, 1])
            or np.any(reference.alleles[:, 2, :] != 0.5)):
        raise ValueError('Virtual reference must be symmetric homozygotes with A=0.5')


@dataclass(frozen=True)
class Source:
    state: types.PlantState
    A_ids: tuple[int, ...]
    I_ids: tuple[int, ...]
    source_seed: int
    co_carriers: int


def construct_virtual_source(reference: types.PlantState, *, co_carriers: int,
                             source_seed: int, halfwidth_A: float = 0.0625,
                             halfwidth_I: float = 0.0625) -> Source:
    """Create synthetic standing A/I homologs, preserving adult phenotype."""
    design_gate()
    _require_virtual_reference(reference)
    if type(co_carriers) is not int or not 0 <= co_carriers <= 12:
        raise ValueError('Invalid A/I source carrier overlap')
    if (halfwidth_A, halfwidth_I) != (0.0625, 0.0625):
        raise ValueError('Illustrative allele halfwidths are not frozen native experiments')
    order = ordered_ids(reference.ids, source_seed, SOURCE_SALT)
    ai = order[:12]
    ii = np.concatenate((order[:co_carriers], order[12:24-co_carriers]))
    if len(np.unique(ii)) != 12 or len(set(ai) & set(ii)) != co_carriers:
        raise AssertionError('Synthetic allele carrier overlap is not exact')
    updated = reference.alleles.copy()
    for trait, carriers, halfwidth in ((2, ai, halfwidth_A), (1, ii, halfwidth_I)):
        centers = reference.alleles[:, trait, :].mean(axis=1)
        updated[carriers, trait, 0] = centers[carriers] - halfwidth
        updated[carriers, trait, 1] = centers[carriers] + halfwidth
    if np.any((updated < 0) | (updated > 1)):
        raise ValueError('Synthetic heterozygotes violate Model3 allele bounds')
    if not np.array_equal(updated.mean(axis=2), reference.alleles.mean(axis=2)):
        raise ValueError('Synthetic hidden genetics changed source adult phenotypes')
    state = types.PlantState(
        alleles=updated,
        allele_origin=reference.allele_origin,
        mutation_flags=reference.mutation_flags,
        ids=reference.ids,
        birth_years=reference.birth_years,
    )
    if not np.array_equal(state.alleles[:, 0, :], reference.alleles[:, 0, :]):
        raise AssertionError('M locus must remain untouched')
    return Source(state, tuple(map(int, ai)), tuple(map(int, ii)), source_seed, co_carriers)


def subset_founders(state: types.PlantState, founders: int, draw_seed: int) -> types.PlantState:
    if type(founders) is not int or founders not in (2, 8, 24, 48):
        raise ValueError('Unregistered technical founder-count option')
    if len(state.ids) != 48 or not np.array_equal(np.sort(state.ids), np.arange(48)):
        raise ValueError('Only the complete virtual source can be sampled')
    chosen_ids = np.sort(ordered_ids(state.ids, draw_seed, DRAW_SALT)[:founders])
    indices = np.searchsorted(state.ids, chosen_ids)
    if not np.array_equal(state.ids[indices], chosen_ids):
        raise ValueError('Source IDs are not sorted for paired founder draw')
    return types.PlantState(**{field: getattr(state, field)[indices]
                               for field in ('alleles', 'allele_origin',
                                             'mutation_flags', 'ids', 'birth_years')})


def static_config() -> types.Config:
    """Declared technical settings only; never pass to population.advance."""
    arrival = types.ArrivalConfig(0., 1., 1., 'exponential', 0., 0.)
    return types.Config(1, types.EVENT_ORDER, 'reproductive_year', 48, 200, 0.,
                        8., 20., .5, 1., .5, .01, .05, 'evolving', .5,
                        'delayed', 0., .5, .4, 'count_scaled', 4., 1., 1.,
                        arrival, arrival, 'founding', 4, .2, 1., (.5, .5, .5), .15)


def static_visitor_state(optima: tuple[float, ...]) -> types.VisitorState:
    n = len(optima)
    return types.VisitorState(np.arange(n, dtype=np.int64),
                              np.array(optima, dtype=float),
                              np.full(n, .2), np.ones(n))


def static_return_parity(reference: types.PlantState, variant: types.PlantState,
                         visitor: types.VisitorState, config: types.Config) -> str:
    """Compute exactly one expected ledger on each state; no inheritance/future."""
    if not np.array_equal(reference.ids, variant.ids):
        raise ValueError('Matched founder IDs changed')
    if not np.array_equal(reference.alleles.mean(axis=2), variant.alleles.mean(axis=2)):
        raise ValueError('Individual phenotype mismatch before static returns')
    l0 = reproduction.reproduce(reference, visitor, config)
    l1 = reproduction.reproduce(variant, visitor, config)
    digest = hashlib.sha256()
    for field in LEDGER_FIELDS:
        a, b = getattr(l0, field), getattr(l1, field)
        if a.shape != b.shape or not np.array_equal(a, b):
            raise ValueError('Initial expected parental return mismatch: ' + field)
        digest.update(field.encode() + b'\0' + np.ascontiguousarray(a).tobytes())
    return digest.hexdigest()


def technical_receipt() -> dict:
    """16 synthetic founding draws and 32 matching static ledgers; zero births."""
    native_gate()
    design_gate()
    reference = synthetic_reference()
    visitors = [static_visitor_state(x) for x in ((), (.5, .5, .5, .5))]
    config = static_config()
    rows = []
    for overlap in (0, 3, 6, 12):
        virtual = construct_virtual_source(reference, co_carriers=overlap, source_seed=20261014)
        for n in (2, 8, 24, 48):
            source_n = subset_founders(virtual.state, n, draw_seed=20261014)
            matched_n = subset_founders(reference, n, draw_seed=20261014)
            static_ledger_sha = [static_return_parity(matched_n, source_n, v, config)
                                 for v in visitors]
            a_carriers = set(virtual.A_ids) & set(map(int, source_n.ids))
            i_carriers = set(virtual.I_ids) & set(map(int, source_n.ids))
            rows.append({'m_source_overlap': overlap, 'n_founders': n,
                         'selected_ids': [int(v) for v in source_n.ids],
                         'A_heterozygous_founder_count': len(a_carriers),
                         'I_heterozygous_founder_count': len(i_carriers),
                         'both_retained': bool(a_carriers and i_carriers),
                         'static_ledger_sha256_by_visitor': static_ledger_sha,
                         'initial_genotype_sha256': hashlib.sha256(
                             np.ascontiguousarray(source_n.alleles).tobytes()).hexdigest()})
    return {'status': 'SYNTHETIC_NATIVE_INITIAL_STATE_TECHNICAL_ONLY',
            'native_biology_source_pinned': True,
            'new_genetic_or_demographic_histories': 0,
            'offspring_or_future_update_calls': 0,
            'virtual_mainland_sources': 4,
            'paired_founder_subsets': len(rows),
            'static_return_parity_checks': len(rows)*len(visitors),
            'rows': rows,
            'limitations': ['I and A carriers synthetically assigned, not observed mainland genetics',
                            'ancestry IDs are synthetic founder labels, not reconstructed natural history',
                            'original stored Model3 founders not reconstituted',
                            'no genetic-only n48 cloning/transplant intervention',
                            'no response-order or persistence outcomes']}


def main() -> None:
    print(json.dumps(technical_receipt(), sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
