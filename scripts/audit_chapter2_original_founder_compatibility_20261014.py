"""Read-only Model3 ORIGINAL t0 genome -> intervened founder-state compatibility.

This is a *technical* initial-state source audit, not future Model3 biology.
Historical genomes stay immutable; edited I/A homologs are explicitly artificial.
"""
from __future__ import annotations

import base64
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path

import numpy as np

from scripts.model3_island import reproduction, types
from scripts.audit_chapter2_native_founder_source_20261014 import (
    PINNED_MODULE_BLOBS, LEDGER_FIELDS, native_gate,
    ordered_ids, SOURCE_SALT, DRAW_SALT,
)

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / 'data/design/chapter2_clock_original_t0_typed_fixture_20261013.json'
ORIGINAL_BLOB = '4b529cce12bc44e06d43a22b10c325a52bbd967b'
ORIGINAL_BIOLOGY_COMMIT = '328548612e93469fcc8663f24548530a57399b9a'
EXPECTED_DTYPE = {
    'ids': '<i8',
    'alleles': '<f8',
    'allele_origin': '<i8',
    'mutation_flags': '|b1',
    'birth_years': '<i8',
}
EXPECTED_SHAPE = {
    'ids': (48,),
    'alleles': (48, 3, 2),
    'allele_origin': (48, 3, 2),
    'mutation_flags': (48, 3, 2),
    'birth_years': (48,),
}
ORIGINAL_SOURCE_SHA = {
    'main': {
        'ids': '852c80a269cfde9f6b8cc6c4f19f4e92c636218d0620fedda0d379e77abc224b',
        'alleles': '1e2f173e46c20af3ecc811c81f95a38a5b09bf539e834542a6bdaf1281634930',
        'allele_origin': 'ba1b53cae912da6d52ef63ea1bc6596d368e11e463348612a15dea36c45b41fc',
        'mutation_flags': '2d5565fb483d8ea4525a7a9229677d1038ad34b6e22c8d5152e1d7f7b9817597',
        'birth_years': 'a1a4f5721c1c4610af7f71078f3a68c330536d679803b0e0507ee8dc10c5dfca',
    },
    'confirmation': {
        'ids': '852c80a269cfde9f6b8cc6c4f19f4e92c636218d0620fedda0d379e77abc224b',
        'alleles': '13cbb1c08a8da3d79db6c6cacf7443a6c865f170c7f7639dbed114',
        'allele_origin': 'ba1b53cae912da6d52ef63ea1bc6596d368e11e463348612a15dea36c45b41fc',
        'mutation_flags': '2d5565fb483d8ea4525a7a9229677d1038ad34b6e22c8d5152e1d7f7b9817597',
        'birth_years': 'a1a4f5721c1c4610af7f71078f3a68c330536d679803b0e0507ee8dc10c5dfca',
    },
}
CONTEXTS = {0: (), 3: (.5, .5, .5, .5), 4: (.3, .3, .7, .7)}
SOURCE_BIOMARK = 10**12  # reserved artificial origin namespace, NEVER original genealogy
SOURCE_SEED = 20261014
DRAW_SEED = 20261014
H = .0625


def _blob_sha(raw: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def _source_field(field: dict, name: str, block: str) -> np.ndarray:
    if (field.get('sha256') != ORIGINAL_SOURCE_SHA[block][name]
            or field.get('dtype') != EXPECTED_DTYPE[name]
            or tuple(field.get('shape', [])) != EXPECTED_SHAPE[name]):
        raise ValueError('Original t0 typed field identity invalid: ' + block + '/' + name)
    try:
        raw = base64.b64decode(field['data_b64'], validate=True)
    except (KeyError, ValueError, base64.binascii.Error) as exc:
        raise ValueError('Original typed base64 is unreadable') from exc
    dt = np.dtype(EXPECTED_DTYPE[name])
    if (len(raw) != int(np.prod(EXPECTED_SHAPE[name])) * dt.itemsize or
            hashlib.sha256(raw).hexdigest() != ORIGINAL_SOURCE_SHA[block][name]):
        raise ValueError('Original t0 source array bytes/hash failed: ' + name)
    return np.frombuffer(raw, dtype=dt).reshape(EXPECTED_SHAPE[name]).copy()


def original_fixture() -> dict:
    native_gate()
    raw = ORIGINAL.read_bytes()
    if _blob_sha(raw) != ORIGINAL_BLOB:
        raise ValueError('Original typed fixture Git blob differs from approved source')
    d = json.loads(raw)
    if (d.get('schema') != 'clock_original_t0_typed_fixture_20261013_v1'
            or d.get('scope') != 'ONLY_ORIGINAL_HISTORICAL_T0_NOT_SIMULATED'
            or d.get('original_biological_commit') != ORIGINAL_BIOLOGY_COMMIT
            or d.get('new_biological_histories') != 0
            or d.get('original_full_file_admitted_from_source_archives') is not True
            or set(d.get('original_founders', {})) != {'main', 'confirmation'}):
        raise ValueError('Historical original t0 fixture contract changed')
    if set(d.get('original_provider_sha256', {})) != {'0', '3', '4'}:
        raise ValueError('Original provider archive inventory changed')
    return d


def source_state(d: dict, block: str) -> types.PlantState:
    if block not in ORIGINAL_SOURCE_SHA:
        raise ValueError('Unregistered founder block')
    fields = d['original_founders'][block]['source_state_arrays']
    if set(fields) != set(EXPECTED_DTYPE):
        raise ValueError('Original typed founder state inventory changed')
    state = types.PlantState(**{k: _source_field(fields[k], k, block) for k in fields})
    if not np.array_equal(state.ids, np.arange(48, dtype=np.int64)):
        raise ValueError('Original source individual IDs no longer 0..47')
    if np.any(state.birth_years != 0) or np.any(state.mutation_flags):
        raise ValueError('Unexpected birth/mutation marker in historical t0')
    if np.any(state.alleles[:, 2, :].mean(axis=1) != 0.5):
        raise ValueError('Original A adult phenotype not held at 0.5')
    return state


@dataclass(frozen=True)
class Intervention:
    state: types.PlantState
    A_ids: tuple[int, ...]
    I_ids: tuple[int, ...]
    m: int
    source_block: str
    original_f0_alleles_sha256: str


def manipulate_homologs(state: types.PlantState, *, block: str, overlap: int,
                        source_seed: int = SOURCE_SEED) -> Intervention:
    """Intervene on original I/A homologs preserving adult M/I/A exactly."""
    if block not in ORIGINAL_SOURCE_SHA or not isinstance(state, types.PlantState):
        raise ValueError('Cannot intervene on unregistered original block')
    if type(overlap) is not int or overlap not in (0, 3, 6, 12):
        raise ValueError('Unregistered original-source A/I overlap')
    if not np.array_equal(state.ids, np.arange(48)):
        raise ValueError('Model3 original founder ID roster changed')
    if hashlib.sha256(state.alleles.tobytes()).hexdigest() != ORIGINAL_SOURCE_SHA[block]['alleles']:
        raise ValueError('Input is not exact original source genome')
    ranked = ordered_ids(state.ids, source_seed, SOURCE_SALT)
    a_ids = ranked[:12]
    i_ids = np.concatenate((ranked[:overlap], ranked[12:24-overlap]))
    if len(i_ids) != 12 or len(np.intersect1d(a_ids, i_ids)) != overlap:
        raise AssertionError('A/I carrier intervention indexing changed')
    alleles = state.alleles.copy()
    origins = state.allele_origin.copy()
    block_id = 0 if block == 'main' else 1
    for trait, carriers in ((1, i_ids), (2, a_ids)):
        means = state.alleles[:, trait, :].mean(axis=1)
        alleles[:, trait, :] = means[:, None]
        alleles[carriers, trait, 0] = means[carriers] - H
        alleles[carriers, trait, 1] = means[carriers] + H
        for copy in (0, 1):
            origins[:, trait, copy] = (SOURCE_BIOMARK + block_id * 1_000_000
                                      + state.ids * 10 + trait * 2 + copy)
    edited = types.PlantState(
        alleles=alleles, allele_origin=origins,
        mutation_flags=state.mutation_flags, ids=state.ids,
        birth_years=state.birth_years,
    )
    if (not np.array_equal(edited.alleles.mean(axis=2), state.alleles.mean(axis=2))
            or not np.array_equal(edited.alleles[:, 0], state.alleles[:, 0])
            or not np.array_equal(edited.allele_origin[:, 0], state.allele_origin[:, 0])
            or not np.array_equal(edited.mutation_flags, state.mutation_flags)
            or not np.array_equal(edited.ids, state.ids)
            or not np.array_equal(edited.birth_years, state.birth_years)
            or np.any(edited.allele_origin[:, 1:, :] < SOURCE_BIOMARK)):
        raise ValueError('Synthetic intervention did not preserve original adult/ID state')
    return Intervention(edited, tuple(map(int, a_ids)), tuple(map(int, i_ids)),
                        overlap, block, ORIGINAL_SOURCE_SHA[block]['alleles'])


def matched_draw(original: types.PlantState, treated: types.PlantState, n: int,
                 draw_seed: int = DRAW_SEED) -> tuple[types.PlantState, types.PlantState]:
    if type(n) is not int or n not in (2, 8, 24, 48):
        raise ValueError('Unregistered founder-sample count')
    if not np.array_equal(original.ids, treated.ids):
        raise ValueError('Original/engineered founder ID mismatch')
    selected = np.sort(ordered_ids(original.ids, draw_seed, DRAW_SALT)[:n])
    indices = np.searchsorted(original.ids, selected)
    if not np.array_equal(original.ids[indices], selected):
        raise ValueError('Invalid founder draw/source order')
    names = ('alleles', 'allele_origin', 'mutation_flags', 'ids', 'birth_years')
    construct = lambda x: types.PlantState(**{key: getattr(x, key)[indices] for key in names})
    return construct(original), construct(treated)


def original_context(d: dict, block: str, context: int) -> tuple[types.Config, types.VisitorState]:
    if block not in ORIGINAL_SOURCE_SHA or context not in CONTEXTS:
        raise ValueError('Unregistered original ecology')
    c = types.Config.from_dict(d['original_founders'][block]['contexts'][str(context)]['config'])
    if (c.capacity != 48 or c.years != 200 or c.survival != 0
            or c.seed_arrival.supply != 0 or c.assurance_mode != 'evolving'
            or c.mutation_rate != .01 or c.mutation_sd != .05):
        raise ValueError('Original ecological config/horizon changed')
    optima = np.asarray(CONTEXTS[context], dtype=np.float64)
    v = types.VisitorState(
        ids=np.arange(len(optima), dtype=np.int64), optima=optima,
        breadths=np.full(len(optima), c.visitor_breadth),
        effectiveness=np.full(len(optima), c.visitor_effectiveness),
    )
    return c, v


def ledger_parity(original: types.PlantState, engineered: types.PlantState,
                  config: types.Config, visitors: types.VisitorState) -> str:
    if not np.array_equal(original.ids, engineered.ids):
        raise ValueError('Not a same-founder counterfactual')
    if not np.array_equal(original.alleles.mean(axis=2),
                          engineered.alleles.mean(axis=2)):
        raise ValueError('Hidden genotype changes expressed initial phenotypes')
    l0 = reproduction.reproduce(original, visitors, config)
    l1 = reproduction.reproduce(engineered, visitors, config)
    h = hashlib.sha256()
    for field in LEDGER_FIELDS:
        a = getattr(l0, field)
        b = getattr(l1, field)
        if a.shape != b.shape or not np.array_equal(a, b):
            raise ValueError('Original native t0 ledger differs after intervention: ' + field)
        h.update(field.encode() + b'\0' + np.asarray(a).tobytes())
    return h.hexdigest()


def archive_return_gate(d: dict, original: types.PlantState,
                        block: str, context: int,
                        config: types.Config, visitors: types.VisitorState) -> None:
    """Old published eight *aggregated* returns are a separate source anchor."""
    rec = d['original_founders'][block]['contexts'][str(context)]
    actual = reproduction.reproduce(original, visitors, config)
    fields = ('maternal', 'paternal', 'self_raw', 'self_viable',
              'ovules', 'exported', 'delivered', 'outcross')
    observed = np.asarray(rec['original_returns_t0'], dtype=float)
    measured = np.array([float(getattr(actual, name).sum()) for name in fields])
    if (observed.shape != (8,) or not np.isfinite(observed).all()
            or np.max(np.abs(observed-measured)) > 1e-12):
        raise ValueError('Authentic old t0 source recorded returns do not match')


def technical_report() -> dict:
    """Six historical original source states, 96 technical comparisons, zero futures."""
    d = original_fixture()
    cells = []
    original_return_validations = 0
    for block in ('main', 'confirmation'):
        original = source_state(d, block)
        contexts = {k: original_context(d, block, k) for k in CONTEXTS}
        for context, (config, visitors) in contexts.items():
            archive_return_gate(d, original, block, context, config, visitors)
            original_return_validations += 1
        for overlap in (0, 3, 6, 12):
            engineered = manipulate_homologs(original, block=block, overlap=overlap)
            for n in (2, 8, 24, 48):
                raw_sample, intervention_sample = matched_draw(original, engineered.state, n)
                for context, (config, visitors) in contexts.items():
                    digest = ledger_parity(raw_sample, intervention_sample, config, visitors)
                    cells.append({
                        'founder_block': block, 'co_carriers': overlap,
                        'founder_sample_n': n, 'ecological_context': context,
                        'selected_original_IDs': [int(z) for z in raw_sample.ids],
                        'A_carriers_retained': len(set(engineered.A_ids) & set(map(int, raw_sample.ids))),
                        'I_carriers_retained': len(set(engineered.I_ids) & set(map(int, raw_sample.ids))),
                        'expected_reproductive_ledger_sha256': digest,
                        'intervened_source_alleles_sha256': hashlib.sha256(
                            intervention_sample.alleles.tobytes()).hexdigest(),
                    })
    if len(cells) != 96 or original_return_validations != 6:
        raise AssertionError('Original-source matched access inventory incomplete')
    return {
        'status': 'ORIGINAL_T0_PINNED_COUNTERFACTUAL_TECHNICAL_ONLY',
        'original_fixture_git_blob': ORIGINAL_BLOB,
        'original_source_commit': ORIGINAL_BIOLOGY_COMMIT,
        'original_historical_founder_blocks': 2,
        'original_full48_return_checks': original_return_validations,
        'technical_t0_reproductive_ledger_parity_checks': len(cells),
        'source_modification_types': ['I_homolog_pairs', 'A_homolog_pairs'],
        'genetically_intervened_origin_namespace': SOURCE_BIOMARK,
        'all_biology_futures_or_new_evolutionary_histories': 0,
        'cells': cells,
        'interpretation': [
            'Original t0 typed fixture matches source Git blob and exact individual-array digests',
            'Reference originates from previous authenticated source, not fresh independent raw ZIP replay',
            'Allele changes are artificial interventions and ancestry namespace is explicitly artificial',
            'Initial per-adult phenotypes and all expected return matrices are held, not future evolution',
            'Founder n contrasts change actual initial population count; genetic-only fixed-N48 control unresolved',
            'No natural island genotype or Q2 clock confirmation or Q4 mediation shown',
        ],
    }


def main() -> None:
    print(json.dumps(technical_report(), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
