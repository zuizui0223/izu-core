"""Original-birth reconstruction and conditional I-response accounting, no new futures."""
from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np

FREEZE = '97435b5aa1d0072d7ad4b2ea050ab323366d74425e640cfee32cca54be8f97b7'
CASE_RECORDS = '8cda8bfb12eb5424e6e5b4029277160983ac1b96075ccbdf5d8ce55ed4990a5f'
NATIVE_PINS = {
    'population.py':'c03fc6fccdf4efb660ece8fa5ee016d4de14f84f3b234dfb6322666b89ec34c1',
    'randomness.py':'35305f37429c2d46239bed125736d8168c26bbd66aeefc68319615f3f620cefe',
    'history.py':'87407dd301ee7c9c793ff5fd25963b470ebf4674a61a0385ab7adcca8d354d04',
}
TERM_NAMES = ('maternal_selection','paternal_selection','self_selection',
              'parent_choice','mendelian_transmission','birth_mutation','observed_change')


def sha(b): return hashlib.sha256(b).hexdigest()


def nonresponse_class(adequate, hit, reopening, event):
    adequate, hit = np.asarray(adequate, bool), np.asarray(hit, bool)
    if adequate.shape != (201,) or hit.shape != (201,) or (hit & ~adequate).any():
        raise ValueError('mean predicate without necessary support')
    found = np.flatnonzero(np.convolve(hit.astype(int), np.ones(20, int), 'valid') == 20)
    if (int(found[0]) if len(found) else None) != event:
        raise ValueError('event inventory differs from saved means')
    if reopening is None: return 'never_reopened'
    if not 0 <= reopening <= 200: raise ValueError('invalid reopening time')
    if event is not None:
        return 'completed_before_reopening' if event+19 < reopening else 'completed_after_reopening'
    if reopening > 181: return 'late_reopening'
    run = longest = 0
    for present in adequate[reopening:]:
        run = run+1 if present else 0
        longest = max(longest, run)
    if longest < 20: return 'no_support_window'
    return 'mean_not_sustained' if hit[reopening:].any() else 'mean_never_reached'


def price_terms(resident, components, selected, premutation, actual):
    components = np.asarray(components, float)
    if components.shape != (3,) or not np.isfinite([resident,selected,premutation,actual,*components]).all():
        raise ValueError('invalid response-accounting inputs')
    expected = resident+components.sum()
    terms = np.r_[components, selected-expected, premutation-selected,
                  actual-premutation, actual-resident]
    if abs(terms[:6].sum()-terms[6]) > 1e-12:
        raise ValueError('conditional response identity does not close')
    return terms


def replay_children(alleles, origins, flags, mothers, fathers, segregation, mutation):
    mothers, fathers = np.asarray(mothers, int), np.asarray(fathers, int)
    n = len(mothers); loci = np.arange(3)[None, :]
    maternal = segregation.integers(0, 2, size=(n, 3))
    paternal = segregation.integers(0, 2, size=(n, 3))
    def transmit(a):
        return np.stack([a[mothers[:,None], loci, maternal],
                         a[fathers[:,None], loci, paternal]], axis=-1)
    premutation = transmit(alleles)
    inherited_origins, inherited_flags = transmit(origins), transmit(flags)
    hits = mutation.random(premutation.shape) < .01
    hits &= np.array([False, True, True])[None, :, None]
    steps = mutation.normal(0, .05, premutation.shape)
    child = premutation.copy()
    child[hits] = 1-np.abs(np.mod(child[hits]+steps[hits], 2)-1)
    return premutation, child, inherited_origins, inherited_flags | hits, 18*n


def audit(base, standing, output):
    base, standing, output = Path(base), Path(standing), Path(output)
    frozen_bytes = (base/'EXECUTION_FREEZE.json').read_bytes()
    if sha(frozen_bytes) != FREEZE: raise ValueError('native execution freeze changed')
    frozen = json.loads(frozen_bytes)
    for filename, pin in NATIVE_PINS.items():
        p = base/'original_native_source/scripts/model3_island'/filename
        if sha(p.read_bytes()) != pin: raise ValueError('native replay arithmetic source changed')
    record_bytes = gzip.decompress((standing/'CASES.json.gz').read_bytes())
    if sha(record_bytes) != CASE_RECORDS: raise ValueError('standing case records changed')
    prior = json.loads(record_bytes)
    key = lambda x: f"{x['task']['block']}_c{x['task']['context']}_r{x['task']['replicate']}"
    prod = json.loads((base/'run/PRODUCTION_COMPLETE.json').read_bytes())['records']
    replay = json.loads((base/'run/REPLAY_COMPLETE.json').read_bytes())['records']
    pm, rm = {key(x):x for x in prod}, {key(x):x for x in replay}
    expected = {f'{b}_c{c}_r{i}' for b in ('main','confirmation') for c in range(9) for i in range(128)}
    if not (len(prior) == len(prod) == len(replay) == 2304 and {x['case'] for x in prior} == set(pm) == set(rm) == expected):
        raise ValueError('original case inventory changed')
    rows = []; draws = transitions = 0; max_closure = 0.; census_min = 48; census_max = 0
    for old in sorted(prior, key=lambda x:x['case']):
        k = old['case']; raw = (base/'run/paths'/(k+'.npz')).read_bytes()
        if sha(raw) != pm[k]['sha256'] or sha(raw) != rm[k]['sha256']:
            raise ValueError('raw renewal hash changed')
        with np.load(base/'run/paths'/(k+'.npz'), allow_pickle=False) as z:
            a = {f:z[f] for f in ('ids','alleles','allele_origin','mutation_flags','birth_years',
                                   'offsets','means','population','parentage','parent_offsets','sexual_selection')}
            m = json.loads(str(z['metadata'].item())); cfg = m['config']; task = m['task']
        # The final field is the literal technical-replay flag 0, separated by NUL.
        seed = int.from_bytes(hashlib.sha256(b'\0'.join([b'ecological-order-v1-20261013', task['block'].encode(), str(task['replicate']).encode(), b'0'])).digest()[:16], 'big')
        if (m['seed'] != seed or m['mutation_mask'] != [False,True,True] or task != old['task']
                or cfg['survival'] != 0 or cfg['seed_arrival']['supply'] != 0
                or cfg['mutation_rate'] != .01 or cfg['mutation_sd'] != .05 or cfg['assurance_mode'] == 'fixed'):
            raise ValueError('original replay configuration changed')
        n, off, po = a['population'], a['offsets'], a['parent_offsets']
        if (n.shape != (201,) or (n <= 0).any() or (n > 48).any()
                or not np.array_equal(np.diff(off), n) or not np.array_equal(np.diff(po), n[1:])
                or a['sexual_selection'].shape != (200,3,3)):
            raise ValueError('invalid birth/census inventory')
        seg = np.random.default_rng(np.random.SeedSequence([seed,8,0]))
        mut = np.random.default_rng(np.random.SeedSequence([seed,9,0]))
        adequate = np.array([a['means'][0,1]-a['alleles'][off[t]:off[t+1],1,:].min() >= .05 for t in range(201)])
        hit = a['means'][0,1]-a['means'][:,1] >= .05
        r = old['renewal']['first_reopening']
        group = nonresponse_class(adequate, hit, r, old['renewal']['event_onset'])
        steps = []
        for t in range(200):
            lo, hi, end = off[t:t+3]; parents = a['parentage'][po[t]:po[t+1]]
            if not np.array_equal(parents[:,0], a['ids'][hi:end]): raise ValueError('saved parent-child IDs changed')
            lookup = {int(pid):i for i,pid in enumerate(a['ids'][lo:hi])}
            mothers = np.array([lookup[int(pid)] for pid in parents[:,1]], int)
            fathers = np.array([lookup[int(pid)] for pid in parents[:,2]], int)
            pre, child, origins, flags, scalar_draws = replay_children(
                a['alleles'][lo:hi], a['allele_origin'][lo:hi], a['mutation_flags'][lo:hi], mothers, fathers, seg, mut)
            for x, field in ((child,'alleles'), (origins,'allele_origin'), (flags,'mutation_flags')):
                if not np.array_equal(x, a[field][hi:end]): raise ValueError('original-birth reconstruction mismatch: '+field)
            traits = a['alleles'][lo:hi,1,:].mean(axis=1)
            selected = (traits[mothers]+traits[fathers]).mean()/2
            row = price_terms(a['means'][t,1], a['sexual_selection'][t,:,1],
                              selected, pre[:,1,:].mean(), a['means'][t+1,1])
            max_closure = max(max_closure, float(abs(row[:6].sum()-row[6])))
            steps.append(row); draws += scalar_draws; transitions += 1
        steps = np.array(steps)
        phase = None if r is None else steps[r:].sum(axis=0)
        rows.append(dict(case=k, task=task, raw_sha256=sha(raw), group=group,
                         first_reopening=r, event_onset=old['renewal']['event_onset'],
                         phase_updates=None if r is None else 200-r,
                         whole_path=dict(zip(TERM_NAMES,steps.sum(axis=0).tolist())),
                         post_reopening=None if phase is None else dict(zip(TERM_NAMES,phase.tolist()))))
        census_min = min(census_min,int(n.min())); census_max = max(census_max,int(n.max()))
    cells = []
    for b in ('main','confirmation'):
        for c in range(9):
            selected = [x for x in rows if x['task']['block'] == b and x['task']['context'] == c]
            if len(selected) != 128: raise ValueError('incomplete fixed cell')
            cells.append(dict(block=b, context=c, starts=128, classes=dict(Counter(x['group'] for x in selected))))
    groups = {}
    for name in sorted({x['group'] for x in rows}):
        selected = [x for x in rows if x['group'] == name]; phase = [x['post_reopening'] for x in selected if x['post_reopening'] is not None]
        groups[name] = dict(starts=len(selected), mean_post_reopening=None if not phase else {
            key:float(np.mean([p[key] for p in phase])) for key in TERM_NAMES},
            cumulative_selection_negative=sum(sum(p[key] for key in TERM_NAMES[:3]) < -1e-12 for p in phase),
            negative_selection_observed_nonnegative=sum(sum(p[key] for key in TERM_NAMES[:3]) < -1e-12 and p['observed_change'] >= -1e-12 for p in phase))
    raw = json.dumps(rows, sort_keys=True, separators=(',',':')).encode()
    result = dict(status='ALL2304_ORIGINAL_BIRTH_RECONSTRUCTIONS_EXACT', cases=2304,
                  replayed_birth_transitions=transitions, regenerated_original_scalar_variates=draws,
                  new_biological_histories=0, native_advance_calls=0, case_records_sha256=sha(raw),
                  source_freeze_sha256=FREEZE, prior_case_records_sha256=CASE_RECORDS,
                  reader_sha256=sha(Path(__file__).read_bytes()), native_source_pins=NATIVE_PINS,
                  numpy_version=np.__version__, maximum_step_closure_error=max_closure,
                  observed_census_range=[census_min,census_max], groups=groups, cells=cells,
                  scope='Retrospective conditional observed-path accounting; not causal shares or a density counterfactual.')
    output.mkdir(parents=True, exist_ok=True)
    (output/'CASES.json.gz').write_bytes(gzip.compress(raw, mtime=0))
    (output/'READOUT.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('base','standing','output'): p.add_argument('--'+name, type=Path, required=True)
    a = p.parse_args()
    print(json.dumps(audit(a.base, a.standing, a.output), indent=2))
