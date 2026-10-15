"""Describe all paired frozen ecological outcomes; never advance a model."""
from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import subprocess

from scipy.stats import beta

PRIMARY_SHA = '4a0b6ab3edf90b21c9513feecab0bec59bfc550f1af8350964ac3b3201220ce5'
SUPPORT_SHA = '8cda8bfb12eb5424e6e5b4029277160983ac1b96075ccbdf5d8ce55ed4990a5f'
SUPPORT_READOUT_SHA = '08211287952abb99d34f43c43943a3cbb1241b50b3ca87db1c63f40cd5559202'
BLOCKS = {'main': 27200701, 'confirmation': 27210701}
CONTEXTS = [(0., 'empty')] + [(s, c) for s in (.03125, .125, .5, 1.) for c in ('matched', 'separated')]
CATEGORIES = ('assurance_first', 'investment_first', 'near_simultaneous', 'assurance_only', 'investment_only', 'neither')
SUPPORT_CLASSES = ('I_completed', 'I_absent_no_deficit', 'I_absent_deficit_by181', 'I_absent_deficit_after181')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def classify(a, i):
    for t in (a, i):
        if t is not None and (type(t) is not int or not 0 <= t <= 181):
            raise ValueError('invalid event onset')
    if a is None:
        return 'neither' if i is None else 'investment_only'
    if i is None:
        return 'assurance_only'
    return 'near_simultaneous' if abs(a-i) <= 5 else ('assurance_first' if a < i else 'investment_first')


def checked(e):
    if e['category'] != classify(e['A'], e['I']):
        raise ValueError('event category mismatch')
    return e


def pair_counts(left, right, n=128):
    if set(left) != set(range(n)) or set(right) != set(range(n)):
        raise ValueError('missing/shifted paired replicate')
    matrix = [[0]*6 for _ in CATEGORIES]
    c = Counter()
    for k in range(n):
        a, b = checked(left[k]), checked(right[k])
        ac, bc = a['category'], b['category']
        matrix[CATEGORIES.index(ac)][CATEGORIES.index(bc)] += 1
        c['strict_A_to_I'] += ac == 'assurance_first' and bc == 'investment_first'
        c['strict_I_to_A'] += ac == 'investment_first' and bc == 'assurance_first'
        both_a, both_b = all(a[t] is not None for t in ('A', 'I')), all(b[t] is not None for t in ('A', 'I'))
        c['both_to_nonboth'] += both_a and not both_b
        c['nonboth_to_both'] += both_b and not both_a
        for t in ('A', 'I'):
            c[t+'_gained'] += a[t] is None and b[t] is not None
            c[t+'_lost'] += a[t] is not None and b[t] is None
    return dict(starts=n, category_order=list(CATEGORIES), transition_matrix=matrix, **dict(c))


def support_status(e, s):
    checked(e)
    if e['I'] != s['event_onset']:
        raise ValueError('support/event mismatch')
    t = s['first_deficit']
    if t is not None and (type(t) is not int or not 0 <= t <= 200):
        raise ValueError('invalid support deficit time')
    if e['I'] is not None:
        return 'I_completed'
    return 'I_absent_no_deficit' if t is None else ('I_absent_deficit_by181' if t <= 181 else 'I_absent_deficit_after181')


def key(task):
    return task['block'], task['context'], task['replicate']


def inventory(rows):
    table = {key(r['task']): r for r in rows}
    expected = {(b, c, r) for b in BLOCKS for c in range(9) for r in range(128)}
    if len(rows) != 2304 or len(table) != 2304 or set(table) != expected:
        raise ValueError('incomplete/duplicate full source inventory')
    for (b, c, r), row in table.items():
        s, comp = CONTEXTS[c]
        if row['task'] != dict(block=b, block_seed=BLOCKS[b], context=c, supply=s, composition=comp, replicate=r):
            raise ValueError('task configuration mismatch')
    return table


def original_interval(a, i):
    # Recheck the frozen original bounds; this is not another inferential family.
    alpha = .05/36
    def cp(k):
        return (0. if k == 0 else float(beta.ppf(alpha/2, k, 129-k)),
                1. if k == 128 else float(beta.ppf(1-alpha/2, k+1, 128-k)))
    al, ah = cp(a); il, ih = cp(i)
    return [al-ih, ah-il]


def audit(primary_path, support_path, support_readout_path, output):
    if output.exists():
        raise ValueError('refuse result replacement')
    pb, sb, rb = primary_path.read_bytes(), gzip.decompress(support_path.read_bytes()), support_readout_path.read_bytes()
    if (sha(pb), sha(sb), sha(rb)) != (PRIMARY_SHA, SUPPORT_SHA, SUPPORT_READOUT_SHA):
        raise ValueError('frozen source SHA mismatch')
    primary, sr = json.loads(pb), json.loads(rb)
    if sr['case_records_sha256'] != SUPPORT_SHA or sr['cases'] != 2304:
        raise ValueError('standing-support receipt mismatch')
    records, support = inventory(primary['records']), inventory(json.loads(sb))
    original_cells = {(x['block'], x['context']): x for x in primary['cells']}
    if len(primary['cells']) != 18 or len(original_cells) != 18:
        raise ValueError('original cell inventory')
    cells, pairs = [], []
    for block in BLOCKS:
        for context in range(9):
            counts, ss = Counter(), Counter()
            for replicate in range(128):
                k = block, context, replicate
                e = checked(records[k]['events'])
                counts[e['category']] += 1
                ss[support_status(e, support[k]['original'])] += 1
            original = original_cells[block, context]
            cats = {c: counts[c] for c in CATEGORIES}
            a, i = counts['assurance_first'], counts['investment_first']
            ci = original_interval(a, i)
            if cats != original['categories'] or original['D'] != (a-i)/128 or any(abs(x-y) > 1e-14 for x, y in zip(ci, original['simultaneous_interval'])):
                raise ValueError('original primary decision changed')
            if len(original['simultaneous_interval']) != 2:
                raise ValueError('invalid original bounds')
            cells.append(dict(**original, both_events=sum(counts[c] for c in CATEGORIES[:3]),
                              support_status={c: ss[c] for c in SUPPORT_CLASSES}))
        for left, right in itertools.combinations(range(9), 2):
            ls, lc = CONTEXTS[left]; rs, rc = CONTEXTS[right]
            kind = 'empty_to_positive' if left == 0 else ('same_composition_supply' if lc == rc else ('same_supply_composition' if ls == rs else 'mixed'))
            l = {r: records[block, left, r]['events'] for r in range(128)}
            r = {r: records[block, right, r]['events'] for r in range(128)}
            pairs.append(dict(block=block, left_context=left, right_context=right, contrast_kind=kind, **pair_counts(l, r)))
    result = dict(status='ALL2304_ORIGINAL_EVENTS_18_CELLS_72_PAIRED_CONTEXT_MATRICES',
                  primary_sha256=sha(pb), support_cases_sha256=sha(sb), support_readout_sha256=sha(rb),
                  reader_sha256=sha(Path(__file__).read_bytes()),
                  execution_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
                  trajectories=2304, paired_comparisons=9216, cells=cells, pairs=pairs,
                  original_supported_supply_pairs=primary['supported_supply_pairs'],
                  original_supported_composition_pairs=primary['supported_composition_pairs'],
                  new_biological_histories=0, native_calls=0, random_draws=0,
                  scope='Retrospective descriptive paired input contrasts; reused trajectories, no new intervals, boundary or natural-order benefit. Support timing is not a mediator share; no fresh rawNPZ admission.')
    output.mkdir(parents=True)
    (output/'READOUT.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('primary', 'support', 'support-readout', 'output'):
        p.add_argument('--'+name, required=True, type=Path)
    args = p.parse_args()
    r = audit(args.primary, args.support, args.support_readout, args.output)
    print(json.dumps({k: v for k, v in r.items() if k not in ('cells', 'pairs')}, indent=2))
