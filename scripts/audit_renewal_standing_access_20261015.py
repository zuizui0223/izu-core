"""Read all frozen original/renewal arrays; no producer import or biological calls."""
from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np

FREEZE = '97435b5aa1d0072d7ad4b2ea050ab323366d74425e640cfee32cca54be8f97b7'
READOUT = '9251c9a78f3790648bd8041d9ae8bebe244a9dd673c1893776114db86c7c8776'


def sha(body):
    return hashlib.sha256(body).hexdigest()


def summarize(n, offsets, alleles, flags, means, *, mutable):
    n, offsets = np.asarray(n), np.asarray(offsets)
    if (n.ndim != 1 or len(n) < 1 or n[0] < 1 or (n < 0).any()
            or offsets.shape != (len(n)+1,) or offsets[0] != 0
            or not np.array_equal(np.diff(offsets), n)
            or alleles.shape != (offsets[-1], 3, 2)
            or flags.shape != alleles.shape or means.shape != (len(n), 3)
            or not np.isfinite(alleles).all()
            or ((alleles < 0) | (alleles > 1)).any()):
        raise ValueError('invalid saved layout')
    if (n == 0).any() and (n[np.flatnonzero(n == 0)[0]:] != 0).any():
        raise ValueError('extinct history reoccupied')
    first_deficit = first_reopening = onset = None
    streak = occupied = deficits = reopenings = 0
    previous_deficit = False
    initial = float(means[0, 1])
    for t, count in enumerate(n):
        if count == 0:
            if not np.isnan(means[t]).all():
                raise ValueError('extinct saved means are not missing')
            streak = 0
            continue
        lo, hi = offsets[t:t+2]
        a = alleles[lo:hi]
        if not np.array_equal(a.mean(axis=(0, 2)), means[t]):
            raise ValueError('saved means differ from raw homologs')
        copies = a[:, 1, :]
        adequate = bool(initial - copies.min() >= .05)
        hit = bool(initial - means[t, 1] >= .05)
        if hit and not adequate:
            raise ValueError('mean event lacks necessary standing support')
        deficit = not adequate
        occupied += 1
        deficits += int(deficit)
        if deficit and first_deficit is None:
            first_deficit = t
        if previous_deficit and adequate:
            if not mutable:
                raise ValueError('original support reopened without mutation')
            capable = initial - copies >= .05
            if not flags[lo:hi, 1, :][capable].all():
                raise ValueError('unflagged reopening homolog')
            previous = alleles[offsets[t-1]:offsets[t], 1, :]
            if any(value in previous for value in copies[capable]):
                raise ValueError('reopening allele already present')
            reopenings += 1
            if first_reopening is None:
                first_reopening = t
        previous_deficit = deficit
        streak = streak + 1 if hit else 0
        if onset is None and streak == 20:
            onset = t-19
    complete = None if onset is None else onset+19
    return dict(first_deficit=first_deficit, first_reopening=first_reopening,
                reopening_transitions=reopenings, event_onset=onset,
                event_completion=complete, occupied_censuses=occupied,
                deficit_censuses=deficits, occupied_final=bool(n[-1] > 0),
                event_before_deficit=bool(complete is not None and first_deficit is not None
                                         and complete < first_deficit),
                event_after_reopening=bool(complete is not None and first_reopening is not None
                                          and complete >= first_reopening))


def audit(base, output):
    base, output = Path(base), Path(output)
    freeze_bytes = (base/'EXECUTION_FREEZE.json').read_bytes()
    if sha(freeze_bytes) != FREEZE:
        raise ValueError('execution freeze hash changed')
    frozen = json.loads(freeze_bytes)
    root = base/'run'
    readout_bytes = (root/'READOUT.json').read_bytes()
    if sha(readout_bytes) != READOUT:
        raise ValueError('original result hash changed')
    prod = json.loads((root/'PRODUCTION_COMPLETE.json').read_bytes())['records']
    replay = json.loads((root/'REPLAY_COMPLETE.json').read_bytes())['records']
    def key(x):
        t = x['task']
        return f"{t['block']}_c{t['context']}_r{t['replicate']}"
    pm, rm, old = ({key(x):x for x in rows} for rows in (prod, replay, frozen['baselines']))
    expected = {f'{b}_c{c}_r{i}' for b in ('main', 'confirmation')
                for c in range(9) for i in range(128)}
    if any(len(rows) != 2304 for rows in (prod, replay, frozen['baselines'])) or not (set(pm) == set(rm) == set(old) == expected):
        raise ValueError('missing, duplicate or extra frozen case')
    if {p.stem for p in (root/'paths').glob('*.npz')} != expected:
        raise ValueError('unexpected original raw-file set')
    cases, counts = [], {}
    for k in sorted(expected):
        task = pm[k]['task']
        if rm[k]['task'] != task or old[k]['task'] != task:
            raise ValueError('task source mismatch')
        arrays, summaries = [], {}
        for arm, path, pin in (
            ('original', Path(frozen['original_dir'])/(k+'.npz'), old[k]['sha256']),
            ('renewal', root/'paths'/(k+'.npz'), pm[k]['sha256']),
        ):
            raw = path.read_bytes()
            if sha(raw) != pin or (arm == 'renewal' and pin != rm[k]['sha256']):
                raise ValueError('case source hash mismatch')
            with np.load(path, allow_pickle=False) as z:
                meta = json.loads(str(z['metadata'].item()))
                if meta['task'] != task or meta['mutation_mask'] != [False, arm == 'renewal', True] or z['population'].shape != (201,):
                    raise ValueError('case metadata mismatch')
                arrays.append(z['alleles'][:48].copy())
                d = summarize(*(z[f] for f in ('population','offsets','alleles','mutation_flags','means')), mutable=arm == 'renewal')
                reference_event = old[k]['events'] if arm == 'original' else pm[k]['events']
                if d['event_onset'] != reference_event['I']:
                    raise ValueError('original investment-event definition mismatch')
                summaries[arm] = d
                cell = counts.setdefault((task['block'], task['context'], arm), Counter())
                cell.update(starts=1, ever_deficit=int(d['first_deficit'] is not None),
                            ever_reopened=int(d['first_reopening'] is not None),
                            event=int(d['event_onset'] is not None),
                            event_before_deficit=int(d['event_before_deficit']),
                            event_after_reopening=int(d['event_after_reopening']),
                            deficit_censuses=d['deficit_censuses'], occupied_censuses=d['occupied_censuses'],
                            occupied_final=int(d['occupied_final']),
                            reopening_transitions=d['reopening_transitions'])
        if not np.array_equal(*arrays):
            raise ValueError('paired initial alleles changed')
        cases.append(dict(case=k, task=task, **summaries))
    cells = [dict(block=b, context=c, arm=a, **counts[b,c,a])
             for b in ('main','confirmation') for c in range(9) for a in ('original','renewal')]
    paired = Counter(f"{int(x['original']['event_onset'] is not None)}{int(x['renewal']['event_onset'] is not None)}" for x in cases)
    result = dict(status='ALL2304_SOURCE_PAIRED_STANDING_SUPPORT_HISTORIES_READ',
                  scope='Retrospective saved-state accounting, no causal mediation or new test.',
                  cases=2304, source_freeze_sha256=FREEZE, original_readout_sha256=READOUT,
                  production_receipt_sha256=sha((root/'PRODUCTION_COMPLETE.json').read_bytes()),
                  replay_receipt_sha256=sha((root/'REPLAY_COMPLETE.json').read_bytes()),
                  script_sha256=sha(Path(__file__).read_bytes()), cells=cells,
                  paired_event_status=dict(paired), new_native_updates=0, new_random_draws=0)
    output.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(cases, sort_keys=True, separators=(',',':')).encode()
    result['case_records_sha256'] = sha(raw)
    (output/'CASES.json.gz').write_bytes(gzip.compress(raw, mtime=0))
    (output/'READOUT.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--base', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    args = p.parse_args()
    print(json.dumps(audit(args.base, args.output), indent=2))
