"""Read-only audit of the existing 64-pair restoration; never advances biology.

All ZIP arguments are existing published artifacts, admitted by immutable hash.
Expected response is checked against the independently audited saved accounting;
this script recomputes genotype moments and realized parent/transmission terms.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import zipfile

import numpy as np

SOURCE_COMMIT = '688bcdf563d4150e6f3618e27967469cbbaa341e'
HASHES = {
    'restoration': '90b9d063c564edf97f12d3a3917819486f72d4ecb8281a20ebdaf39ad7de14c6',
    'accounting': '07e86248551b1dce24ea91f1566c54e6a8c7f8932ac96479e2cd78e708ce572d',
    'source_input': 'f0fd126f638e1c6bd130e640ce4491b3bb47aac3da1838359a902776c9a4e037',
    'cohort': '7ae00916ed2cbb38323c3fb9ffc5824de3e8272df1f5a35785842c316191f918',
}
STATE_FIELDS = ('ids', 'alleles', 'allele_origin', 'mutation_flags', 'birth_years')
TERMS = ('selection', 'parent_sampling', 'transmission', 'observed_change')
BLOCKS = ('causal_main', 'causal_confirmation')
SOURCE_PREFIX = 'work/EL_order_boundary_20261007/'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def file_sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for part in iter(lambda: f.read(1024 * 1024), b''):
            h.update(part)
    return h.hexdigest()


def close(a, b, label):
    require(np.allclose(a, b, atol=1e-12, rtol=0, equal_nan=False), label)


def unique_by_key(rows):
    out = {r['key']: r for r in rows}
    require(len(out) == len(rows), 'duplicate case inventory')
    return out


def moments(genes):
    genes = np.asarray(genes)
    require(genes.ndim == 2 and genes.shape[1] == 2, 'diploid I shape')
    require(np.isfinite(genes).all() and (genes >= 0).all() and (genes <= 1).all(), 'invalid alleles')
    if not len(genes):
        return dict(mean=None, minimum=None, maximum=None, allele_variance=None,
                    expressed_variance=None, fixed=None)
    return dict(mean=float(genes.mean()), minimum=float(genes.min()), maximum=float(genes.max()),
                allele_variance=float(genes.var()), expressed_variance=float(genes.mean(1).var()),
                fixed=bool(np.all(genes == genes.flat[0])))


def supports_target(minimum, initial):
    return None if minimum is None else bool(initial - minimum >= .05)


def event_start(means, initial, start=0):
    """Earliest start of twenty censuses at original >=0.05 decrease."""
    run = 0
    for year in range(start, len(means)):
        value = means[year]
        run = run + 1 if value is not None and np.isfinite(value) and initial - value >= .05 else 0
        if run == 20:
            return year - 19
    return None


def trajectory(a, censuses):
    offsets = a['offsets']
    require(np.issubdtype(offsets.dtype, np.integer) and offsets.shape == (censuses + 1,), 'census offsets')
    require(offsets[0] == 0 and offsets[-1] == len(a['alleles']) and (np.diff(offsets) >= 0).all(), 'offset coverage')
    require(a['alleles'].shape == (offsets[-1], 3, 2), 'three diploid loci')
    return [moments(a['alleles'][lo:hi, 1, :]) for lo, hi in zip(offsets[:-1], offsets[1:])]


def state(a, t):
    lo, hi = a['offsets'][t:t + 2]
    return {k: a[k][lo:hi] for k in STATE_FIELDS}


def check_state_equal(a, b):
    for k in STATE_FIELDS:
        require(np.array_equal(a[k], b[k]), 'state differs: ' + k)


def arrays(raw):
    with np.load(io.BytesIO(raw), allow_pickle=False) as f:
        return {k: f[k] for k in f.files}


def first_year(rows, predicate, start=0):
    return next((i for i in range(start, len(rows)) if predicate(rows[i])), None)


def pathwise(a, meta, ref):
    require(len(ref['annual']) == len(meta['rows']) - 1 == ref['updates'], 'accounting update inventory')
    totals = {k: 0. for k in TERMS}
    for i, saved in enumerate(ref['annual']):
        parent, child = state(a, i), state(a, i + 1)
        pl, ph = a['parent_offsets'][i:i + 2]
        edges = a['parentage'][pl:ph]
        require(edges.shape == (len(child['ids']), 3), 'parentage shape')
        require(np.array_equal(edges[:, 0], child['ids']), 'offspring identity')
        require(len(set(parent['ids'])) == len(parent['ids']), 'duplicate parents')
        index = {int(v): j for j, v in enumerate(parent['ids'])}
        mi = [index[int(v)] for v in edges[:, 1]]
        fi = [index[int(v)] for v in edges[:, 2]]
        g = parent['alleles'][:, 1, :]
        h = child['alleles'][:, 1, :]
        require(len(g) > 0 and len(h) > 0, 'extinct path is not a finite mean')
        require(not child['mutation_flags'][:, 1, :].any(), 'I mutation')
        require((h[:, 0, None] == g[mi]).any(1).all() and (h[:, 1, None] == g[fi]).any(1).all(), 'I inheritance')
        traits = g.mean(1)
        selected = (traits[mi] + traits[fi]).mean() / 2
        expected = meta['rows'][i]['expected_response'][1]
        values = dict(selection=expected, parent_sampling=selected-traits.mean()-expected,
                      transmission=h.mean()-selected, observed_change=h.mean()-traits.mean())
        require(saved['year'] == meta['rows'][i]['year'], 'accounting year')
        for k in TERMS:
            close(values[k], saved[k], 'annual ' + k)
            totals[k] += values[k]
    for k in TERMS:
        close(totals[k], ref[k], 'cumulative ' + k)
    return totals


def audit_case(original_raw, restored_raw, original_receipt, restored_receipt, ref):
    o, r = arrays(original_raw), arrays(restored_raw)
    om, rm = [json.loads(str(a['metadata'].item())) for a in (o, r)]
    task = om['task']
    require(task == rm['task'] == original_receipt['task'] == restored_receipt['task'], 'paired task')
    require(not om['technical'] and not original_receipt['technical'], 'technical case')
    require(om['identity'] == original_receipt['identity'], 'original identity')
    require(sha(original_raw) == original_receipt['sha256'] == rm['original_case_sha256'], 'original raw binding')
    require(sha(restored_raw) == restored_receipt['raw_sha256'] == ref['raw_sha256'], 'restored raw binding')
    require(om['mutation_mask'] == [False, False, True], 'standing I mutation mask')
    require(task['supply'] == .125 and task['composition'] == 'matched' and task['capacity'] == 48 and task['arm'] == 'evolving', 'context')
    require(om['config']['years'] == 200 and om['config']['survival'] == 0 and om['config']['seed_arrival']['supply'] == 0, 'horizon/closed annual model')
    ot = trajectory(o, 201)
    tr = first_year(ot, lambda x: x['fixed'] is True)
    require(tr == rm['trigger'] == restored_receipt['trigger'] == ref['trigger'], 'first occupied fixation trigger')
    start = 200 if tr is None else tr
    require(tr is None or tr < 200, 'trigger has no future')
    rt = trajectory(r, 201-start)
    require([x['year'] for x in rm['rows']] == list(range(start, 201)), 'saved years')
    require(rm == {k: v for k, v in restored_receipt.items() if k != 'raw_sha256'}, 'metadata/receipt')
    require(np.array_equal(np.diff(o['offsets']), o['population']), 'original census')
    close(np.array([x['mean'] for x in ot]), o['means'][:, 1], 'original mean reconstruction')
    for i, m in enumerate(rt):
        row = rm['rows'][i]
        require(row['census'] == r['offsets'][i+1]-r['offsets'][i], 'restored census')
        require(m['mean'] is not None, 'extinct trait cannot be dropped')
        for k in ('mean', 'allele_variance', 'expressed_variance'):
            close(m[k], row[k][1], 'restored ' + k)
    if tr is None:
        check_state_equal(state(o, 200), state(r, 0))
        require(rm['half_width'] is None, 'no-trigger width')
        full = ot
    else:
        before, after = state(o, tr), state(r, 0)
        expected = {k: v.copy() for k, v in before.items()}
        v = ot[tr]['mean']
        require(1/16 <= v <= 15/16 and rm['half_width'] == 1/16, 'fixed restoration width')
        expected['alleles'][:, 1, 0] = v-1/16
        expected['alleles'][:, 1, 1] = v+1/16
        check_state_equal(expected, after)
        close(before['alleles'].mean(2), after['alleles'].mean(2), 'individual means preserved')
        require(rt[0]['expressed_variance'] == 0 and rt[0]['allele_variance'] == 1/256, 'restoration type')
        full = ot[:tr] + rt
    close(rm['original_I'], ot[-1]['mean'], 'original terminal')
    close(rm['restored_I'], rt[-1]['mean'], 'restored terminal')
    sums = pathwise(r, rm, ref)
    effect = ot[-1]['mean'] - rt[-1]['mean']
    close(sums['observed_change'], -effect, 'terminal/pathwise correspondence')
    initial = ot[0]['mean']
    refix = first_year(rt, lambda x: x['fixed'] is True, start=1) if tr is not None else None
    expressed = first_year(rt, lambda x: x['expressed_variance'] is not None and x['expressed_variance'] > 0, start=1) if tr is not None else None
    excluded = first_year(rt, lambda x: supports_target(x['minimum'], initial) is False) if tr is not None else None
    original_event = event_start([x['mean'] for x in ot], initial)
    full_event = event_start([x['mean'] for x in full], initial)
    post_event = event_start([x['mean'] for x in full], initial, start=tr) if tr is not None else None
    return dict(key=task['key'], block=task['block'], replicate=task['replicate'],
        original_raw_sha256=sha(original_raw), restored_raw_sha256=sha(restored_raw),
        initial_I=initial, event_target_I=initial-.05, trigger_year=tr, remaining_updates=200-start,
        trigger_I=ot[start]['mean'] if tr is not None else None,
        restored_min_I=rt[0]['minimum'] if tr is not None else None,
        restored_max_I=rt[0]['maximum'] if tr is not None else None,
        restored_supports_target=supports_target(rt[0]['minimum'], initial) if tr is not None else None,
        target_previously_reachable=supports_target(ot[start]['minimum'], initial) if tr is not None else None,
        first_expressed_variance_year=start+expressed if expressed is not None else None,
        first_refixation_year=start+refix if refix is not None else None,
        time_to_refixation=refix,
        first_post_target_exclusion_year=start+excluded if excluded is not None else None,
        post_censuses_with_allele_variance=sum(x['allele_variance'] > 0 for x in rt) if tr is not None else None,
        post_censuses_with_expressed_variance=sum(x['expressed_variance'] > 0 for x in rt) if tr is not None else None,
        original_event_year=original_event, restored_event_year=full_event, post_event_year=post_event,
        event_completed_before_trigger=(original_event is not None and original_event+19 < tr) if tr is not None else None,
        original_terminal_I=ot[-1]['mean'], restored_terminal_I=rt[-1]['mean'],
        terminal_effect_original_minus_restored=effect,
        restored_terminal_fixed=rt[-1]['fixed'], **sums)


def run(paths):
    for key, path in paths.items():
        require(file_sha(path) == HASHES[key], 'ZIP identity: ' + key)
    with zipfile.ZipFile(paths['restoration']) as z, zipfile.ZipFile(paths['accounting']) as az, \
            zipfile.ZipFile(paths['source_input']) as sz, zipfile.ZipFile(paths['cohort']) as cz:
        for archive in (z, az, sz, cz):
            require(len(archive.namelist()) == len(set(archive.namelist())), 'duplicate ZIP members')
        manifest = json.loads(z.read('MANIFEST.json'))
        require(set(z.namelist()) == set(manifest) | {'MANIFEST.json'}, 'manifest coverage')
        for name, h in manifest.items():
            require(sha(z.read(name)) == h, 'member identity: ' + name)
        source_manifest = json.loads(sz.read('work/EL_next_20261007/extension_source_manifest.json'))
        for name, h in source_manifest['files'].items():
            require(sha(z.read('FROZEN_SOURCE/'+name)) == h, 'frozen biology identity')
        design = json.loads(sz.read(SOURCE_PREFIX+'natural_campaign_design.json'))
        require(design['order'] == dict(thresholds=[.025, .05, .1], primary=.05, sustained=20, tie=5), 'original event definition')
        readout = json.loads(z.read('RESTORATION/READOUT.json'))
        cases = unique_by_key(readout['cases'])
        expected_keys = {f'{b}_s0.125_matched_n48_standing_MI_new_A_r{i}_evolving' for b in BLOCKS for i in range(32)}
        require(set(cases) == expected_keys, '64 original block/replicate inventory')
        accounting = json.loads(az.read('RESTORED_PATHWISE_ACCOUNTING_AUDITED_20261013.json'))
        require(sha(az.read('RESTORED_PATHWISE_ACCOUNTING_AUDITED_20261013.json')) == 'c1604c9b7ed8c814d0219cef951e9f4da835db7ccbbc7b85bb00aaa95f36a52f', 'accounting identity')
        refs = unique_by_key(accounting['rows'])
        require(set(refs) == expected_keys, 'accounting coverage')
        rows = []
        for key in sorted(cases):
            orig, restored = [z.read(prefix+'/'+key+'.npz') for prefix in ('ORIGINAL64', 'RESTORATION')]
            matches = [n for n in cz.namelist() if n.endswith('/'+key+'.npz')]
            require(len(matches) == 1 and cz.read(matches[0]) == orig, 'original full-cohort member identity')
            receipts = [json.loads(z.read(prefix+'/'+key+'.json')) for prefix in ('ORIGINAL64', 'RESTORATION')]
            require(cases[key]['raw_sha256'] == sha(restored), 'primary readout member')
            rows.append(audit_case(orig, restored, *receipts, refs[key]))
        for b in BLOCKS:
            group = [r for r in rows if r['block'] == b]
            for k in TERMS:
                close(np.mean([r[k] for r in group]), accounting['blocks'][b][k], 'block pathwise mean')
            close(np.mean([r['terminal_effect_original_minus_restored'] for r in group]), readout['primary']['block_estimates'][b], 'primary block')
        close(np.mean([r['terminal_effect_original_minus_restored'] for r in rows]), readout['primary']['estimate'], 'primary mean')
        require(readout['primary']['decision'] == 'unresolved', 'frozen primary')
        tr = [r for r in rows if r['trigger_year'] is not None]
        require(len(tr) == 61 and sum(r['remaining_updates'] for r in rows) == 7740, 'trigger/update inventory')
        summary = dict(source_commit=SOURCE_COMMIT, input_sha256=HASHES, original_event_definition=design['order'],
            event_source_sha256=sha(sz.read(SOURCE_PREFIX+'order_events.py')),
            cases=64, triggers=len(tr), no_trigger=3, primary_preserved=readout['primary'],
            primary_interval_note='Existing frozen interval retained; no new bootstrap or inference family.',
            counts=dict(restored_support=sum(r['restored_supports_target'] for r in tr),
                already_supported_at_trigger=sum(r['target_previously_reachable'] for r in tr),
                newly_supported=sum(r['restored_supports_target'] and not r['target_previously_reachable'] for r in tr),
                excluded_despite_restoration=sum(not r['restored_supports_target'] for r in tr),
                expressed_variance_next_census=sum(r['first_expressed_variance_year'] == r['trigger_year']+1 for r in tr),
                refixed_by_200=sum(r['first_refixation_year'] is not None for r in tr),
                original_events_all64=sum(r['original_event_year'] is not None for r in rows),
                restored_events_all64=sum(r['restored_event_year'] is not None for r in rows),
                new_events_among_original_none=sum(r['original_event_year'] is None and r['restored_event_year'] is not None for r in rows),
                lost_events=sum(r['original_event_year'] is not None and r['restored_event_year'] is None for r in rows),
                triggered_with_at_least_20_censuses=sum(r['remaining_updates']+1 >= 20 for r in tr)),
            trigger_range=[min(r['trigger_year'] for r in tr), max(r['trigger_year'] for r in tr)],
            remaining_updates_range=[min(r['remaining_updates'] for r in tr), max(r['remaining_updates'] for r in tr)],
            pathwise_blocks=accounting['blocks'], no_new_histories=True,
            checks=['four ZIP hashes', 'all restoration manifest members', 'original64 byte identity against full cohort',
                'source-manifest biology identity', '64 paired raw receipts', 'annual genotype moments',
                'first fixation and exact intervention fields', '7740 raw parent/transmission updates against saved expected response',
                'all64 primary mean and both blocks'],
            limitation='Support is necessary, not sufficient; expected response is the authenticated saved quantity, not freshly recomputed reproduction. Descriptive post hoc audit, no unique cause, equivalence or natural-process intervention claim.')
    return rows, summary


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for key in HASHES:
        p.add_argument('--'+key.replace('_', '-'), type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    require(not args.out.exists(), 'output directory exists; inspect it instead of overwriting')
    rows, summary = run({key: getattr(args, key) for key in HASHES})
    summary['audit_script_sha256'] = file_sha(__file__)
    args.out.mkdir(parents=True)
    with (args.out/'restoration_access_cases_20261014.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary['case_table_sha256'] = file_sha(args.out/'restoration_access_cases_20261014.csv')
    (args.out/'restoration_access_audit_20261014.json').write_text(json.dumps(summary, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
