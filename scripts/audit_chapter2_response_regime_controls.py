"""Additional declared rule-by-control audit; no changes to the frozen model."""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import replace
import hashlib
import json
from pathlib import Path

import numpy as np

from scripts.audit_chapter2_update_factorial import RULES, endpoints, COMPONENTS
from scripts.audit_chapter2_realized_richness_matching import match_trajectories, verify_design
from scripts.chapter2_rng import paired_scenario_seeds
from scripts.chapter2_simulation_integrity import verify_model, canonical_bytes
from scripts.run_chapter2_conditional_why_diagnostics import (
    classify_matrix, realization_class_counts, two_way_decomposition,
)
from scripts.run_response_geometry_parameter_robustness import BASE, TRAIT_GRID, pollinator_trajectory

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / 'data/design/chapter2_response_regime_controls_20260925.json'
MATCH_DESIGN = ROOT / 'data/design/chapter2_realized_richness_matching_freeze_20260907.json'


def describe(data):
    delta = data[0]
    decomp = two_way_decomposition(delta)
    return {
        'classes': realization_class_counts(delta),
        'mean_geometry': classify_matrix(delta),
        'grand_mean': float(delta.mean()),
        'min_start_mean': float(delta.mean(axis=1).min()),
        'max_start_mean': float(delta.mean(axis=1).max()),
        'fractions': decomp['sum_of_squares_fraction'],
        'ss_per_cell': {name: decomp['sum_of_squares'][name] / delta.size for name in COMPONENTS},
    }


def batch(control, community_seed, matching_seed, destination):
    verify_model(BASE)
    design = json.loads(MATCH_DESIGN.read_text(encoding='utf-8'))
    verify_design(design)
    grid = np.asarray(TRAIT_GRID)
    n = design['baseline']['matched_community_realizations']
    arrays = {rule: np.empty((3, len(grid), n)) for rule in RULES}
    counts = np.empty((n, BASE.steps, 4), dtype=np.int64)
    island = BASE.island
    if control == 'equal_turnover':
        island = replace(island, partner_arrival=BASE.mainland.partner_arrival,
                         partner_loss=BASE.mainland.partner_loss)
    elif control != 'richness_matched':
        raise ValueError(control)
    for rep in range(n):
        sm, si = paired_scenario_seeds(community_seed, rep)
        tm = pollinator_trajectory(BASE.mainland, sm, BASE)
        ti = pollinator_trajectory(island, si, BASE)
        counts[rep, :, 0] = [len(x) for x in tm]
        counts[rep, :, 1] = [len(x) for x in ti]
        if control == 'richness_matched':
            tm, ti, audit = match_trajectories(tm, ti, matching_seed=matching_seed,
                                              replicate_index=rep, design=design)
            if audit['unequal_after_matching']:
                raise ValueError('richness mismatch')
        counts[rep, :, 2] = [len(x) for x in tm]
        counts[rep, :, 3] = [len(x) for x in ti]
        for rule, spec in RULES.items():
            mx, ms = endpoints(grid, tm, BASE, **spec)
            ix, ins = endpoints(grid, ti, BASE, **spec)
            arrays[rule][:, :, rep] = np.array([ins-ms, mx, ix])
    name = f'{control}_community{community_seed}_matching{matching_seed}.npz'
    path = Path(destination) / name
    with path.open('xb') as handle:
        np.savez_compressed(handle, grid=grid, counts=counts, **arrays)
    # Reconstruct every reported row from the actual saved arrays.
    rows = []
    with np.load(path, allow_pickle=False) as saved:
        for rule in RULES:
            if not np.isfinite(saved[rule]).all():
                raise ValueError('nonfinite endpoint')
            rows.append(dict(control=control, community_seed=community_seed,
                             matching_seed=matching_seed, rule=rule, **describe(saved[rule])))
    return {'file': name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'snapshot_pairs': int(counts.shape[0]*counts.shape[1]),
            'unequal_after': int((counts[:,:,2] != counts[:,:,3]).sum()), 'rows': rows}


def run(destination, workers):
    contract = json.loads(DESIGN.read_text(encoding='utf-8'))
    if contract['status'] != 'frozen_before_new_control_execution':
        raise ValueError('unfrozen contract')
    for name, expected in contract['source_sha256'].items():
        if hashlib.sha256(canonical_bytes(ROOT/name)).hexdigest() != expected:
            raise ValueError(f'changed source {name}')
    integrity = verify_model(BASE)
    destination.mkdir(parents=True, exist_ok=False)
    (destination/'execution_contract.json').write_text(
        json.dumps({'design':contract, 'integrity':integrity},indent=2),encoding='utf-8')
    jobs = [('richness_matched', contract['matching_community_seed'], seed)
            for seed in contract['matching_seeds']]
    jobs += [('equal_turnover', seed, None) for seed in contract['community_seeds']]
    outputs = []
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(batch,*job,str(destination)) for job in jobs]
        for future in as_completed(futures):
            out = future.result()
            outputs.append(out)
            print(f'Completed {len(outputs)}/{len(jobs)}: {out["file"]}',flush=True)
    verify_model(BASE)
    outputs.sort(key=lambda x:x['file'])
    result = {'status':'complete_additional_controls', 'design':contract,
              'batches': outputs, 'rows':[row for out in outputs for row in out['rows']]}
    if len(result['rows']) != 108:
        raise ValueError('incomplete outputs')
    (destination/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--workers',type=int,default=3)
    args=parser.parse_args()
    run(args.out,args.workers)
