"""Publish every factorial cell, keeping primary results separate."""
import hashlib
import json
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / 'data/results/update_factorial_20260925'


def build():
    from scripts.validate_chapter2_update_factorial import validate
    validation = validate(DIRECTORY, require_manifest=False)
    p = json.loads((DIRECTORY / 'results.json').read_text())
    rows = p['rows']
    if len(rows) != 270 or len(p['paired_effects']) != 360:
        raise ValueError('incomplete factorial')
    old = json.loads((ROOT / 'data/results/chapter2_postfreeze_grid_update_rule_challenge_receipt_20260925.json').read_text())
    names = ['starting_position', 'community_realization', 'starting_position_by_community_nonadditivity']
    errors = [abs(median(r[c] for r in rows if r['k'] == k and r['rule'] == rule)
                  - old['selected_median_results'][key][f'k{k}_fraction'][full])
              for rule, key in [('t1_best_d0', 'threshold_best_grid21'), ('t0_centroid_d1', 'smooth_weighted_grid21')]
              for k in [1, 4, 16] for c, full in zip('SCI', names)]
    if max(errors) > 1e-12:
        raise ValueError('primary or smooth replay mismatch')
    lines = ['# Additional response-rule factorial — 2026-09-25', '',
             'Parent: c788c740. Additional frozen diagnostic; not replacement of the original result.',
             'Eight rules plus fixed state; 6 seeds × 5 k × 96 histories × 21 starts. Histories shared across rules.',
             'All 270 rule/seed/k rows, 360 paired conditional contrasts and 30 NPZ cell-array files are retained.', '',
             f'Primary/smooth reported median replay maximum absolute error: {max(errors):.3g}.', '',
             '## All conditions at k=16', '',
             't: service threshold enabled; d: response damping by (1-service); best/centroid: response target.',
             'Fractions are separately computed six-seed medians, not causal contributions or guaranteed to sum to 100%.', '',
             '| Rule | S % | C % | I % | Initial-terminal slope, mainland | island |',
             '|---|---:|---:|---:|---:|---:|']
    for rule in sorted({r['rule'] for r in rows}):
        selected = [r for r in rows if r['rule'] == rule and r['k'] == 16]
        values = [100 * median(r[c] for r in selected) for c in 'SCI']
        slopes = [median(r[s]['mean_initial_terminal_slope'] for r in selected) for s in ['mainland_traits', 'island_traits']]
        lines.append('| ' + rule + ' | ' + ' | '.join(f'{v:.2f}' for v in values + slopes) + ' |')
    lines += ['', '## Median winner at every audited k', '', '| Rule | 1 | 2 | 4 | 8 | 16 |', '|---|---|---|---|---|---|']
    for rule in sorted({r['rule'] for r in rows}):
        winners = [max('SCI', key=lambda c: median(r[c] for r in rows if r['rule'] == rule and r['k'] == k)) for k in p['design']['k']]
        lines.append('| ' + rule + ' | ' + ' | '.join(winners) + ' |')
    effects = [e for e in p['paired_effects'] if e['k'] == 16 and e['factor'] == 'target']
    lines += ['', '## Interpretation', '',
              f"At k=16, best→centroid reduces S fraction in {sum(e['delta_S'] < 0 for e in effects)}/{len(effects)} conditional contrasts (4 settings × 6 seeds; these are not 24 independent seeds). Range: {min(e['delta_S'] for e in effects):.4f} to {max(e['delta_S'] for e in effects):.4f}.",
              'Removing the threshold alone does not remove S dominance. Under the tested parameters, target choice is the clearest determinant of high-k S dominance.',
              'This does not prove that loss of initial-trait memory causes loss of S: fixed state has slope 1 but is I-dominated. S concerns expected service contrasts, not trait retention.',
              'Continuous centroid movement without damping remains C-dominated by median at every audited k. C/I reversal is therefore not universal across all response operators; preserve this additional narrowing.',
              'These are within-model interventions, not evidence for historical regional selection, genetic evolution, or a calibrated plasticity mechanism.', '',
              '## Replay and integrity', '',
              '`python -m scripts.audit_chapter2_update_factorial --out <new-directory> --workers 3`',
              'Output directory must be new. Resolved configuration and canonical-LF source hashes are checked before and after execution and in each batch.',
              'The integrity maintenance modifies no biological equations; prior source correction identifiers remain archived. Changed files require explicit revised locks, never name-only exemptions.',
              'Terminal arrays: layer 0 service difference, layer 1 mainland final trait, layer 2 island final trait; axes layers × starts × histories.']
    (ROOT / 'docs/CHAPTER2_UPDATE_FACTORIAL_RESULTS_20260925.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    manifest = {'status':'complete', 'batches':30, 'rule_rows':270, 'conditional_contrasts':360,
                'max_reference_median_error':max(errors),
                'sha256':validation['sha256']}
    if not (DIRECTORY/'verification.json').exists():
        with (DIRECTORY/'verification.json').open('x', encoding='utf-8') as handle:
            handle.write(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({k:v for k,v in manifest.items() if k!='sha256'}))


if __name__ == '__main__':
    build()
