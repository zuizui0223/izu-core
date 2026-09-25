"""Prospective 2 x 2 x 2 response-rule attribution, not an evolution model."""
from __future__ import annotations

import argparse
import itertools
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np

from scripts.chapter2_simulation_integrity import verify_model
from scripts.chapter2_rng import scenario_copy_seeds
from scripts.audit_trait_adjustment_system_size_rank_crossover import pooled_trajectory_from_seeds
from scripts.audit_chapter2_postfreeze_grid_update_rule import _encounter_matrix, _service_from_encounters
from scripts.run_chapter2_conditional_why_diagnostics import two_way_decomposition, realization_class_counts
from scripts.run_response_geometry_parameter_robustness import BASE, EPS

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / 'data/design/chapter2_update_factorial_20260925.json'
RULES = {
    f't{int(t)}_{target}_d{int(d)}': {'threshold': t, 'target': target, 'damping': d}
    for t, target, d in itertools.product((False, True), ('best', 'centroid'), (False, True))
}
RULES['fixed'] = {'threshold': False, 'target': 'fixed', 'damping': False}
COMPONENTS = ['starting_position', 'community_realization', 'starting_position_by_community_nonadditivity']


def endpoints(grid, trajectory, cfg, *, threshold, target, damping):
    if target not in ('best', 'centroid', 'fixed'):
        raise ValueError('unknown target')
    x = np.asarray(grid, dtype=float).copy()
    if target != 'fixed':
        for visitors in trajectory:
            if not visitors:
                continue
            matches = _encounter_matrix(x, visitors, cfg)
            services = _service_from_encounters(matches, cfg)
            z = np.asarray([p.trait for p in visitors])
            mask = services < .45 if threshold else np.ones(x.shape, dtype=bool)
            if target == 'best':
                destination = z[matches.argmax(axis=1)]
            else:
                weights = matches.sum(axis=1)
                mask &= weights > EPS
                destination = (matches @ z) / np.maximum(weights, EPS)
            factor = 1 - services if damping else np.ones(x.shape)
            x[mask] += cfg.trait_adjustment * factor[mask] * (destination[mask] - x[mask])
            x = np.clip(x, 0, 1)
    visitors = trajectory[-1] if trajectory else ()
    return x, _service_from_encounters(_encounter_matrix(x, visitors, cfg), cfg)


def trait_metrics(grid, final):
    centered = grid - grid.mean()
    return {
        'mean_absolute_displacement': float(np.abs(final - grid[:, None]).mean()),
        'mean_within_history_variance_across_starts': float(final.var(axis=0).mean()),
        'mean_initial_terminal_slope': float((centered[:, None] * final).mean() / centered.var()),
    }


def batch(seed, k, design, destination):
    # Each process independently checks the exact locked inputs before computation.
    verify_model(BASE)
    grid = np.linspace(0, 1, design['grid_points'])
    n = design['realizations']
    arrays = {name: np.empty((3, len(grid), n)) for name in RULES}
    for rep in range(n):
        histories = [pooled_trajectory_from_seeds(scenario, scenario_copy_seeds(seed, rep, i, k), BASE)
                     for i, scenario in enumerate((BASE.mainland, BASE.island))]
        for name, rule in RULES.items():
            mx, ms = endpoints(grid, histories[0], BASE, **rule)
            ix, ins = endpoints(grid, histories[1], BASE, **rule)
            arrays[name][:, :, rep] = np.array([ins - ms, mx, ix])
    rows = []
    for name, data in arrays.items():
        decomposition = two_way_decomposition(data[0])
        row = {'rule': name, 'seed': seed, 'k': k,
               'mean_delta_service': float(data[0].mean()),
               'classes': realization_class_counts(data[0]),
               'mainland_traits': trait_metrics(grid, data[1]),
               'island_traits': trait_metrics(grid, data[2])}
        for short, long in zip('SCI', COMPONENTS):
            row[short] = decomposition['sum_of_squares_fraction'][long]
            row[short + '_ss_per_cell'] = decomposition['sum_of_squares'][long] / data[0].size
        rows.append(row)
    # Persist cell-level outputs, including terminal traits; never overwrite an earlier run.
    with (Path(destination) / f'seed{seed}_k{k}.npz').open('xb') as handle:
        np.savez_compressed(handle, grid=grid, **arrays)
    return rows


def paired_effects(rows):
    lookup = {(r['seed'], r['k'], r['rule']): r for r in rows}
    result = []
    for seed, k in sorted({(r['seed'], r['k']) for r in rows}):
        for factor in ('threshold', 'target', 'damping'):
            for name, rule in RULES.items():
                if name == 'fixed' or rule[factor] not in (False, 'best'):
                    continue
                changed = dict(rule)
                changed[factor] = 'centroid' if factor == 'target' else True
                other = next(n for n, v in RULES.items() if n != 'fixed' and v == changed)
                left, right = lookup[(seed, k, name)], lookup[(seed, k, other)]
                entry = {'seed': seed, 'k': k, 'factor': factor, 'from': name, 'to': other}
                for metric in ('S', 'C', 'I', 'S_ss_per_cell', 'C_ss_per_cell', 'I_ss_per_cell'):
                    if metric in left:
                        entry['delta_' + metric] = right[metric] - left[metric]
                for scenario in ('mainland_traits', 'island_traits'):
                    if scenario in left:
                        entry['delta_' + scenario] = {m: right[scenario][m] - left[scenario][m] for m in left[scenario]}
                result.append(entry)
    return result


def run(destination, workers=2):
    provenance = verify_model(BASE)
    design = json.loads(DESIGN.read_text(encoding='utf-8'))
    if design['status'] != 'frozen_before_execution':
        raise ValueError('factorial design must be frozen')
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    (destination / 'execution_contract.json').write_text(json.dumps({'design': design, 'integrity': provenance}, indent=2), encoding='utf-8')
    rows = []
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(batch, seed, k, design, str(destination)) for seed in design['seeds'] for k in design['k']]
        for future in as_completed(futures):
            completed = future.result()
            rows.extend(completed)
            print(f"Completed seed={completed[0]['seed']} k={completed[0]['k']} ({len(rows)//9}/30)", flush=True)
    verify_model(BASE)
    rows.sort(key=lambda r: (r['seed'], r['k'], r['rule']))
    output = {'status': 'complete_additional_factorial', 'design': design, 'integrity': provenance,
              'rows': rows, 'paired_effects': paired_effects(rows)}
    (destination / 'results.json').write_text(json.dumps(output, indent=2), encoding='utf-8')
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--workers', type=int, default=2)
    args = parser.parse_args()
    run(args.out, args.workers)
