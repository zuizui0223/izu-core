"""Re-express locked natural evidence; no model fitting or new field inference."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = 'data/results/chapter2_natural_regime_six_source_checkpoint_20260915.json'
PROJECTION = 'data/results/chapter2_unified_model3_real_island_projection_20260927.json'
MATRIX = 'data/results/island_system_propagation_matrix_v1.json'
STATE = 'data/results/chapter2_natural_regime_current_state_20260915.json'
PREFIX = 'data/predictive_meta/hiraiwa_ushimaru_'


def validate_coordinate(row: dict) -> None:
    for key in ('breadth_D1', 'phi'):
        value = float(row[key])
        lo, hi = map(float, row[key + '_ci95'])
        if not all(math.isfinite(v) for v in (value, lo, hi)) or lo > hi:
            raise ValueError(f'invalid {key} or interval')
        if key == 'breadth_D1' and min(value, lo) <= 0:
            raise ValueError('D1 must be positive')
        if key == 'phi' and not (0 <= min(value, lo) <= max(value, hi) <= 1):
            raise ValueError('synchrony outside [0,1]')


def build_atlas(root: Path = ROOT) -> dict:
    hashes = {}

    def read(rel: str):
        raw = (root / rel).read_bytes()
        # Canonical text hash survives Git newline conversion; originals untouched.
        hashes[rel] = hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest()
        return json.loads(raw)

    checkpoint = read(CHECKPOINT)
    rows = []
    for rel in checkpoint['source_result_files']:
        payload = read(rel)
        current = payload.get('systems')
        if current is None:
            current = [payload['coordinate']]
        for i, original in enumerate(current):
            row = dict(original)
            source = payload.get('source') or {}
            row.setdefault('source_study_id', source.get('source_study_id'))
            row.setdefault('archipelago_id', source.get('archipelago_id'))
            row.setdefault('system_id', source.get('system_id') or f'{row["source_study_id"]}:source-row-{i+1}')
            if not row['source_study_id']:
                raise ValueError('source identity missing')
            validate_coordinate(row)
            rows.append(row)
    counts = {s: sum(r['source_study_id'] == s for r in rows) for s in {r['source_study_id'] for r in rows}}
    if counts != checkpoint['source_system_counts'] or len(rows) != 42:
        raise ValueError('locked observation roster changed')
    if len({(r['source_study_id'], r['system_id']) for r in rows}) != len(rows):
        raise ValueError('duplicate source-system identity')
    projection = read(PROJECTION)
    matrix = read(MATRIX)
    state = read(STATE)
    matching = read(PREFIX + 'continuous_functional_exposure.json')
    pollen = read(PREFIX + 'matching_to_pollen.json')
    concordance = read(PREFIX + 'cross_channel_concordance.json')
    rel = PREFIX + 'cross_channel_concordance.csv'
    raw = (root / rel).read_bytes()
    hashes[rel] = hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest()
    species = list(csv.DictReader(raw.decode('utf-8-sig').splitlines()))
    if len(species) != concordance['n_shared_targets'] or len({r['plant'] for r in species}) != len(species):
        raise ValueError('species roster changed')
    for row in species:
        for key in ('matching_delta_post_minus_oshima', 'tube_delta_mm_post_minus_oshima', 'pollen_delta_post_minus_oshima'):
            if not math.isfinite(float(row[key])):
                raise ValueError('nonfinite species contrast')

    def stage(payload, coef, name):
        full = payload['fixed_effect_subsets']['izu_five_islands']
        omitted = payload['leave_one_site_sensitivity']['izu_five_islands'][coef + '_coefficients_by_omitted_site']
        if set(omitted) != {'hachijo', 'kozu', 'miyake', 'niijima', 'oshima'}:
            raise ValueError('Izu omitted-site roster changed')
        if not all(math.isfinite(float(v)) for v in [full[coef + '_coefficient'], *omitted.values()]):
            raise ValueError('nonfinite Izu stage coefficient')
        return {'label': name, 'full_coefficient': full[coef + '_coefficient'],
                'leave_one_out': omitted,
                'n_sites': full['n_sites'], 'n_seasons': full['n_seasons'],
                'n_analysis_rows': full['n_site_season_rows'] if coef == 'fdq' else full['n_cells'],
                'n_plant_taxa': full.get('n_plants'),
                'analysis_unit': 'site x season community' if coef == 'fdq' else payload['aggregation_unit'],
                'coefficient_unit': 'standardized matching / FDQ unit' if coef == 'fdq' else 'standardized pollen / standardized matching',
                'source_model': payload['source_native_model'],
                'uncertainty': 'site-deletion sensitivity, not confidence intervals; stage-specific scales'}

    return {'status': 'retrospective_source_locked_context_projection',
            'units': {'network_observations': len(rows), 'network_studies': len(counts),
                      'network_island_groups': checkpoint['archipelago_groups'],
                      'literature_entries': projection['breadth_context']['descriptive_research_entries'],
                      'literature_geographic_labels': projection['breadth_context']['exact_geographic_labels'],
                      'propagation_layers': len(matrix['rows'])},
            'coordinates': rows, 'source_system_counts': counts,
            'natural_plane_robustness': state,
            'izu': {'matching': stage(matching, 'fdq', 'FDQ to matching'),
                    'pollen': stage(pollen, 'tm', 'Matching to pollen receipt'),
                    'species': species, 'unit': 'species contrasts are cross-sectional, not evolutionary trajectories'},
            'empirical_k_mapping': None, 'inherited_trajectory_validation': False,
            'source_sha256': hashes, 'hash_convention': 'SHA256 of UTF-8 source bytes with CRLF normalized to LF',
            'claim_boundary': 'observed context and partial functional links; no parameter calibration, phase allocation or causal island-evolution validation'}


def write_outputs(root: Path, out: Path) -> dict:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np

    atlas = build_atlas(root)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'atlas.json').write_text(json.dumps(atlas, indent=2) + '\n', encoding='utf-8')
    fig = plt.figure(figsize=(13, 14), constrained_layout=True)
    grid = fig.add_gridspec(3, 2, height_ratios=[1.2, .9, 1.2])
    ax = fig.add_subplot(grid[0, :])
    labels = ['Hawaii', 'Mallorca', 'Tenerife', 'Cabrera', 'Martinique', 'Great Britain']
    sources = list(dict.fromkeys(r['source_study_id'] for r in atlas['coordinates']))
    for source, label, marker in zip(sources, labels, ['o', 's', '^', 'D', 'v', 'P']):
        rr = [r for r in atlas['coordinates'] if r['source_study_id'] == source]
        line, = ax.plot([r['breadth_D1'] for r in rr], [r['phi'] for r in rr], marker, label=f'{label} (n={len(rr)})', ms=5)
        for r in rr:
            ax.hlines(r['phi'], *r['breadth_D1_ci95'], color=line.get_color(), alpha=.35, lw=.7)
            ax.vlines(r['breadth_D1'], *r['phi_ci95'], color=line.get_color(), alpha=.35, lw=.7)
    ax.set(xscale='log', xlabel='Partner diversity, Hill D1', ylabel='Temporal synchrony, phi', ylim=(0, 1), title='A  Actual community contexts: 42 systems / 6 studies')
    ax.legend(frameon=False, fontsize=8, ncol=2)
    sites = ['hachijo', 'kozu', 'miyake', 'niijima', 'oshima']
    for j, key in enumerate(['matching', 'pollen']):
        ax = fig.add_subplot(grid[1, j]); stage = atlas['izu'][key]
        values = [stage['full_coefficient']] + [stage['leave_one_out'][s] for s in sites]
        ax.scatter(values, range(6), c=['#173f4f'] + ['#ba5b36'] * 5, s=35)
        ax.axvline(0, color='gray', ls='--', lw=1)
        ax.set_yticks(range(6), ['All 5 islands'] + ['Omit ' + s.title() for s in sites], fontsize=8)
        ax.invert_yaxis(); ax.set_xlabel('Slope: ' + stage['coefficient_unit'], fontsize=8)
        count_label = '25 site-season rows' if j == 0 else '78 plant-site-season cells; 10 taxa'
        ax.set_title(('B  ' if j == 0 else 'C  ') + stage['label'] + '\n' + count_label, fontsize=10)
        ax.spines[['top', 'right']].set_visible(False)
    ax = fig.add_subplot(grid[2, :])
    rows = atlas['izu']['species']
    keys = ['matching_delta_post_minus_oshima', 'tube_delta_mm_post_minus_oshima', 'pollen_delta_post_minus_oshima']
    data = np.array([[np.sign(float(r[k])) for k in keys] for r in rows])
    from matplotlib.colors import ListedColormap
    ax.imshow(data, cmap=ListedColormap(['#5797aa', '#eeeeee', '#da9566']), vmin=-1, vmax=1, aspect='auto')
    ax.set_yticks(range(len(rows)), [r['plant'] for r in rows], fontsize=9)
    ax.set_xticks(range(3), ['Corrected matching', 'Tube length', 'Pollen receipt'])
    for i in range(len(rows)):
        for j in range(3):
            ax.text(j, i, {-1: 'Lower / shorter', 0: 'Unchanged', 1: 'Higher / longer'}[int(data[i,j])], ha='center', va='center', fontsize=9)
    ax.set_title('D  Izu species contrasts: post-Oshima minus Oshima (8 shared targets)', loc='left')
    fig.suptitle('Islands as natural experiments: community context to plant response', fontsize=16)
    fig.supxlabel('A: source bootstrap intervals. B–C: deletion diagnostics, not confidence intervals; do not compare slope magnitudes.\nD: descriptive cross-sectional directions, not significance or inherited evolution. No synthetic phase boundaries assigned.', fontsize=10)
    for suffix in ('png', 'pdf'):
        fig.savefig(out / ('natural_island_atlas.' + suffix), dpi=200, bbox_inches='tight')
    plt.close(fig)
    provenance = {'source_sha256': atlas['source_sha256'], 'builder_sha256': hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n', b'\n')).hexdigest(),
                  'outputs': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.name in {'atlas.json', 'natural_island_atlas.png', 'natural_island_atlas.pdf'}},
                  'visual_review': 'pending'}
    (out / 'provenance.json').write_text(json.dumps(provenance, indent=2) + '\n', encoding='utf-8')
    return atlas


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT / 'outputs/chapter2_island_atlas_20260928')
    args = parser.parse_args()
    result = write_outputs(ROOT, args.out)
    print(json.dumps({'status': result['status'], 'units': result['units']}))
