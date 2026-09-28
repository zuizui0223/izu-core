"""Read-only reconstruction of a complete locked factorial artifact package."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np

from scripts.audit_chapter2_update_factorial import DESIGN, RULES, COMPONENTS, paired_effects, trait_metrics
from scripts.chapter2_simulation_integrity import canonical_bytes, verify_model
from scripts.run_response_geometry_parameter_robustness import BASE
from scripts.run_chapter2_conditional_why_diagnostics import two_way_decomposition, realization_class_counts


def validate(directory, *, require_manifest=True):
    directory = Path(directory)
    provenance = verify_model(BASE)
    design = json.loads(DESIGN.read_text(encoding='utf-8'))
    pairs = list(itertools.product(design['seeds'], design['k']))
    batch_names = {f'seed{s}_k{k}.npz' for s, k in pairs}
    if {p.name for p in directory.glob('*.npz')} != batch_names:
        raise ValueError('missing or unexpected batch files')
    files = batch_names | {'results.json', 'execution_contract.json'}
    hashes = {name: hashlib.sha256((directory/name).read_bytes() if name.endswith('.npz')
                                  else canonical_bytes(directory/name)).hexdigest() for name in sorted(files)}
    manifest_path = directory/'verification.json'
    if require_manifest and not manifest_path.exists():
        raise ValueError('missing verification manifest')
    if manifest_path.exists():
        old = json.loads(manifest_path.read_text(encoding='utf-8'))
        if set(old['sha256']) != files:
            raise ValueError('artifact hash inventory mismatch')
        for name in files:
            accepted = {hashes[name]}
            if name.endswith('.json'):
                # Original receipts hashed Windows CRLF text. Accept only the
                # two documented checkout representations, never arbitrary edits.
                crlf = canonical_bytes(directory/name).replace(b'\n', b'\r\n')
                accepted.add(hashlib.sha256(crlf).hexdigest())
            if old['sha256'][name] not in accepted:
                raise ValueError('artifact hash mismatch; refusing to re-certify changed data')
        hashes = old['sha256']
    contract = json.loads((directory/'execution_contract.json').read_text(encoding='utf-8'))
    result = json.loads((directory/'results.json').read_text(encoding='utf-8'))
    if contract != {'design': design, 'integrity': provenance}:
        raise ValueError('execution contract differs from locked design or sources')
    if result['design'] != design or result['integrity'] != provenance:
        raise ValueError('result provenance mismatch')
    if result['status'] != 'complete_additional_factorial':
        raise ValueError('result not complete')
    identities = [(r['seed'], r['k'], r['rule']) for r in result['rows']]
    expected = {(s, k, rule) for s, k in pairs for rule in RULES}
    if len(identities) != len(expected) or set(identities) != expected:
        raise ValueError('missing or duplicated rule rows')
    lookup = dict(zip(identities, result['rows']))
    recomputed = []
    grid = np.linspace(0, 1, design['grid_points'])
    max_error = 0.
    for seed, k in pairs:
        with np.load(directory/f'seed{seed}_k{k}.npz', allow_pickle=False) as arrays:
            if set(arrays.files) != set(RULES) | {'grid'} or not np.array_equal(arrays['grid'], grid):
                raise ValueError('batch grid or rules mismatch')
            for rule in RULES:
                data = arrays[rule]
                if data.shape != (3, len(grid), design['realizations']) or not np.isfinite(data).all():
                    raise ValueError('invalid cell array')
                if (np.abs(data[0]) > 1).any() or (data[1:] < 0).any() or (data[1:] > 1).any():
                    raise ValueError('out-of-range cell array')
                decomposition = two_way_decomposition(data[0])
                row = {'seed': seed, 'k': k, 'rule': rule,
                       'mean_delta_service': float(data[0].mean()),
                       'classes': realization_class_counts(data[0]),
                       'mainland_traits': trait_metrics(grid, data[1]),
                       'island_traits': trait_metrics(grid, data[2])}
                for short, long in zip('SCI', COMPONENTS):
                    row[short] = decomposition['sum_of_squares_fraction'][long]
                    row[short+'_ss_per_cell'] = decomposition['sum_of_squares'][long]/data[0].size
                archived = lookup[(seed, k, rule)]
                if row['classes'] != archived['classes']:
                    raise ValueError('class-count mismatch')
                numbers = [(row[key], archived[key]) for key in ['mean_delta_service', 'S', 'C', 'I', 'S_ss_per_cell', 'C_ss_per_cell', 'I_ss_per_cell']]
                numbers += [(row[sc][key], archived[sc][key]) for sc in ['mainland_traits', 'island_traits'] for key in row[sc]]
                error = max(abs(a-b) for a, b in numbers)
                if not all(np.isfinite(b) and np.isclose(a, b, rtol=1e-12, atol=1e-14) for a, b in numbers):
                    raise ValueError('reconstructed cell statistics mismatch')
                max_error = max(max_error, error)
                recomputed.append(row)
    # Generate contrasts from checked archived rows; exact JSON values must agree.
    if paired_effects(result['rows']) != result['paired_effects']:
        raise ValueError('paired-contrast mismatch')
    return {'verified_batches': len(pairs), 'verified_rule_rows': len(expected),
            'verified_contrasts': len(result['paired_effects']), 'max_cell_statistic_error': max_error,
            'sha256': hashes}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    print(json.dumps({k:v for k,v in validate(args.directory).items() if k != 'sha256'}, indent=2))
