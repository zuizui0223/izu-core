"""Independent raw-only verifier. No imports from the production reader."""
import argparse
from collections import Counter
import csv
import hashlib
import io
from itertools import groupby
import json
from pathlib import Path
import zipfile

import numpy as np

ARCHIVE_SHA = '8a2462910025b4a386e789583578cb1380349097393916dac4e50d01c9637b7e'
PREFLIGHT_SHA = '165a0d39f6f226ac4ccfbfb65fef4b2189fde272ccb0c0f33d840d542ae2760b'
PROTOCOL_SHA = 'b3baf3a7909a1557451f4197398870b1574121b6533489381fef0744601264a0'
EXECUTION_SHA = '54549eeec37a225526883fad4f08ae11a417a87b12adede05346425114d83c93'
PROTOCOL_COMMIT = 'aef793872e1b79b150e204e298b39b8026cb071c'
STATE_FIELDS = 'key block trigger baseline fixed_I support_class preexisting prefix_start trailing remaining window_excluded native_event_predicted original_event_start pairs native_events restored_events gains losses terminal_mean_difference trigger_population'.split()
PAIR_FIELDS = 'key block replicate support_class preexisting native_start native_completion native_longest native_event restored_start restored_completion restored_longest restored_event refix_year refix_endpoint refix_remaining refix_event_complete_at_refixation refix_absorbing joint terminal_mean_difference'.split()


def check(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest()


def events(values, base):
    """Windows, independent of the reader's run-counter algorithm."""
    eligible = [x is not None and base - x >= 0.05 for x in values]
    starts = [i for i in range(len(eligible) - 19) if all(eligible[i:i + 20])]
    longest = max((sum(1 for _ in group) for yes, group in groupby(eligible) if yes), default=0)
    return dict(start=starts[0] if starts else None,
                completion=starts[0] + 19 if starts else None, longest=longest)


def geometry(base, v):
    flags = [base - x >= 0.05 for x in (v - 0.0625, v, v + 0.0625)]
    check(flags == sorted(flags, reverse=True), 'nonmonotone support')
    return ['support_excluded', 'gain_possible', 'loss_possible', 'all_support_eligible'][sum(flags)]


def describe_history(means, trigger):
    prefix = means[:trigger + 1]
    observed = events(prefix, means[0])
    failures = [i for i, x in enumerate(prefix) if means[0] - x < 0.05]
    trailing = len(prefix) - 1 - max(failures, default=-1)
    preexisting = observed['start'] is not None
    return dict(preexisting=preexisting, prefix_start=observed['start'], trailing=trailing,
                remaining=200-trigger, window_excluded=not preexisting and trailing+200-trigger < 20,
                native_event_predicted=events(list(prefix)+[means[trigger]]*(200-trigger), means[0])['start'] is not None)


def read_path(z, name, n, allowed=None):
    with np.load(io.BytesIO(z.read(name)), allow_pickle=False) as raw:
        alleles, offsets = raw['alleles'], raw['offsets']
        meta = json.loads(str(raw['metadata']))
    check(offsets.ndim == 1 and len(offsets) == n+1 and np.issubdtype(offsets.dtype, np.integer), 'offset schema')
    check(offsets[0] == 0 and offsets[-1] == len(alleles) and np.all(np.diff(offsets)>0), 'occupied offset coverage')
    check(alleles.ndim == 3 and alleles.shape[1:] == (3,2), 'allele dimensions')
    copies = alleles[:,1,:]
    check(np.isfinite(copies).all(), 'finite I')
    if allowed is not None:
        check(np.isin(copies, allowed).all(), 'foreign I support')
    # Flatten each census explicitly; test fixation via min/max rather than equality to first copy.
    chunks = [copies[a:b].reshape(-1) for a,b in zip(offsets[:-1], offsets[1:])]
    means = [float(x.sum()/len(x)) for x in chunks]
    fixed = [float(x.min()) if x.min()==x.max() else None for x in chunks]
    return means, fixed, np.diff(offsets), copies[:offsets[1]], meta


def first_fixation(fixed, trigger, v, completion):
    candidates = [i for i in range(1,len(fixed)) if fixed[i] is not None]
    if not candidates:
        return dict(refix_year=None, refix_endpoint='unfixed', refix_remaining=None,
                    refix_event_complete_at_refixation=None, refix_absorbing=None)
    i = candidates[0]
    check(fixed[i] in (v-0.0625,v+0.0625), 'fixation support')
    check(set(fixed[i:]) == {fixed[i]}, 'fixation not absorbing')
    year = trigger+i
    return dict(refix_year=year, refix_endpoint='lower' if fixed[i]<v else 'upper',
                refix_remaining=200-year, refix_event_complete_at_refixation=completion is not None and completion<=year,
                refix_absorbing=True)


def logical_check(state, native, restored):
    cls = state['support_class']
    check(not state['preexisting'] or (native and restored), 'lost shared event')
    check(not state['window_excluded'] or not(native or restored), 'time exclusion')
    allowed = {'support_excluded':{'00','11'}, 'gain_possible':{'00','01','11'},
               'loss_possible':{'00','10','11'}, 'all_support_eligible':{'00','11'}}
    check(f'{int(native)}{int(restored)}' in allowed[cls], 'forbidden joint event')
    check(native == state['native_event_predicted'], 'native geometric prediction')


def compare_csv(path, expected, fields):
    with path.open(newline='',encoding='utf-8') as f:
        reader = csv.DictReader(f)
        check(reader.fieldnames == fields, f'{path.name}: schema')
        actual = list(reader)
    check(len(actual)==len(expected), f'{path.name}: row count')
    # Order is part of this declared output schema; exact scalar strings include nulls and booleans.
    for i,(a,e) in enumerate(zip(actual,expected)):
        for field in fields:
            value = '' if e[field] is None else str(e[field])
            check(a[field] == value, f'{path.name} row {i} field {field}: {a[field]} != {value}')


def verify(archive, preflight, protocol, output, reader):
    for path, expected in [(archive,ARCHIVE_SHA),(preflight,PREFLIGHT_SHA),(protocol,PROTOCOL_SHA)]:
        check(sha(path)==expected, f'{path.name}: frozen SHA256')
    cases = json.loads(preflight.read_text(encoding='utf-8'))['cases']
    check(len(cases)==64 and len({c['key'] for c in cases})==64, '64 unique slots')
    check(Counter(c['block'] for c in cases)=={'causal_main':32,'causal_confirmation':32}, 'block slots')
    states, pairs = [], []
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        manifest = json.loads(z.read('MANIFEST.json'))
        check(len(names)==12042 and len(names)==len(set(names)), 'archive unique inventory')
        check(set(names)==set(manifest)|{'MANIFEST.json'}, 'manifest inventory')
        triggered = [c for c in cases if c['trigger'] is not None]
        check(len(triggered)==61, '61 triggered slots')
        for prefix, expected in [
            ('original/', {f"original/{c['key']}.npz" for c in cases}),
            ('raw/', {f"raw/{c['key']}__r{r:02d}__{a}.npz" for c in triggered for r in range(64) for a in ('native','restored')}),
            ('pairs/', {f"pairs/{c['key']}__r{r:02d}.json" for c in triggered for r in range(64)})]:
            check({n for n in names if n.startswith(prefix)}==expected, prefix+' inventory')
        for c in cases:
            key,t = c['key'],c['trigger']
            name = f'original/{key}.npz'
            check(hashlib.sha256(z.read(name)).hexdigest()==c['original_npz_sha256'], 'original digest')
            original, fixed, sizes, _, _ = read_path(z,name,201)
            b = original[0]
            s = dict.fromkeys(STATE_FIELDS)
            s.update(key=key,block=c['block'],trigger=t,baseline=b,support_class='not_triggered',
                     original_event_start=events(original,b)['start'],pairs=0,native_events=0,restored_events=0,
                     gains=0,losses=0,terminal_mean_difference=0.0)
            if t is None:
                states.append(s)
                continue
            v = fixed[t]
            check(v is not None, 'trigger fixation')
            s.update(fixed_I=v,support_class=geometry(b,v),trigger_population=int(sizes[t]),**describe_history(original,t))
            local = []
            for r in range(64):
                p = dict(key=key,block=c['block'],replicate=r,support_class=s['support_class'],preexisting=s['preexisting'])
                terminal = {}
                for arm in ('native','restored'):
                    means, fixation, _, trigger_copies, m = read_path(z,f'raw/{key}__r{r:02d}__{arm}.npz',201-t,
                                                                     [v] if arm=='native' else [v-0.0625,v+0.0625])
                    check((m['key'],m['replicate'],m['arm'],m['trigger'])==(key,r,arm,t), 'raw metadata identity')
                    check(str(m['seed'])==str(c['pair_seeds'][r]), 'raw metadata seed')
                    check(m['original_sha256']==c['original_npz_sha256'] and m['execution_sha256']==EXECUTION_SHA, 'raw metadata provenance')
                    check(means[0]==v and np.all(trigger_copies.sum(axis=1)/2==v), 'shared trigger expression')
                    e = events(original[:t]+means,b)
                    p.update({arm+'_'+k:value for k,value in e.items()})
                    p[arm+'_event'] = e['start'] is not None
                    terminal[arm] = means[-1]
                    if arm=='restored':
                        p.update(first_fixation(fixation,t,v,e['completion']))
                logical_check(s,p['native_event'],p['restored_event'])
                p['joint'] = f"{int(p['native_event'])}{int(p['restored_event'])}"
                p['terminal_mean_difference'] = terminal['native']-terminal['restored']
                local.append(p)
            s.update(pairs=len(local),native_events=sum(p['native_event'] for p in local),
                     restored_events=sum(p['restored_event'] for p in local),gains=sum(p['joint']=='01' for p in local),
                     losses=sum(p['joint']=='10' for p in local),
                     terminal_mean_difference=float(np.asarray([p['terminal_mean_difference'] for p in local]).mean()))
            states.append(s)
            pairs.extend(local)
    compare_csv(output/'STATES.csv',states,STATE_FIELDS)
    compare_csv(output/'PAIRS.csv',pairs,PAIR_FIELDS)
    blocks = {}
    for block in ('causal_main','causal_confirmation'):
        ss = [s for s in states if s['block']==block]
        pp = [p for p in pairs if p['block']==block]
        joint = {j:sum(p['joint']==j for p in pp) for j in ('00','01','10','11')}
        native, restored = sum(p['native_event'] for p in pp),sum(p['restored_event'] for p in pp)
        check(restored-native==joint['01']-joint['10'], 'joint reconciliation')
        blocks[block] = dict(original_slots=len(ss),triggered_slots=sum(s['trigger'] is not None for s in ss),
            policy_zero_slots=sum(s['trigger'] is None for s in ss),pairs=len(pp),support_classes=dict(Counter(s['support_class'] for s in ss)),
            preexisting_states=sum(s['preexisting'] is True for s in ss),window_excluded_states=sum(s['window_excluded'] is True for s in ss),
            gain_capable_states=sum(s['support_class']=='gain_possible' and not s['preexisting'] and not s['window_excluded'] for s in ss),
            native_events=native,restored_events=restored,joint=joint,
            refixation_by_joint={j:dict(Counter(p['refix_endpoint'] for p in pp if p['joint']==j)) for j in joint},
            terminal_mean_difference=float(np.asarray([s['terminal_mean_difference'] for s in ss]).mean()))
    expected = dict(status='ALL_DECLARED_PATH_RESTRICTIONS_PASS',exploratory=True,biological_updates=0,original_slots=64,
                    triggered_pairs=3904,nontrigger_policy_zero_slots=3,all_observed_censuses_occupied=True,
                    all_native_and_restored_supports_checked=True,all_native_event_predictions_match=True,
                    all_observed_refixations_absorbing=True,original_primary='unresolved',confirmation_margin_0_01='unresolved',blocks=blocks)
    check(json.loads((output/'SUMMARY.json').read_text())==expected, 'every summary field')
    provenance = json.loads((output/'PROVENANCE.json').read_text())
    expected_provenance = dict(archive_sha256=ARCHIVE_SHA,preflight_sha256=PREFLIGHT_SHA,protocol_sha256=PROTOCOL_SHA,
        protocol_commit=PROTOCOL_COMMIT,reader_sha256=sha(reader),biological_updates=0,new_random_draws=0,
        outputs={name:sha(output/name) for name in ('STATES.csv','PAIRS.csv','SUMMARY.json')})
    check(provenance==expected_provenance, 'every provenance field')
    return dict(status='INDEPENDENT_RAW_RECOMPUTATION_PASS',states=len(states),pairs=len(pairs),
                verified_state_fields=len(STATE_FIELDS),verified_pair_fields=len(PAIR_FIELDS),
                biological_updates=0,new_random_draws=0,verifier_sha256=sha(__file__))


def main():
    parser = argparse.ArgumentParser()
    for flag in ('archive','preflight','protocol','output','reader'):
        parser.add_argument('--'+flag,type=Path,required=True)
    args = parser.parse_args()
    print(json.dumps(verify(**vars(args)),indent=2))


if __name__=='__main__':
    main()
