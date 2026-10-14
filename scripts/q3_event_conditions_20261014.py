"""Exploratory Q3 event geometry from frozen raw records; zero biological calls."""
import argparse
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path
import zipfile

import numpy as np

ARCHIVE_SHA = '8a2462910025b4a386e789583578cb1380349097393916dac4e50d01c9637b7e'
PREFLIGHT_SHA = '165a0d39f6f226ac4ccfbfb65fef4b2189fde272ccb0c0f33d840d542ae2760b'
EXECUTION_SHA = '54549eeec37a225526883fad4f08ae11a417a87b12adede05346425114d83c93'
PROTOCOL_SHA = 'b3baf3a7909a1557451f4197398870b1574121b6533489381fef0744601264a0'
PROTOCOL_COMMIT = 'aef793872e1b79b150e204e298b39b8026cb071c'
H = 1 / 16


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def event(means, baseline):
    run = longest = 0
    start = None
    for year, value in enumerate(means):
        run = run + 1 if value is not None and baseline - value >= 0.05 else 0
        longest = max(longest, run)
        if run == 20 and start is None:
            start = year - 19
    return dict(start=start, completion=None if start is None else start + 19, longest=longest)


def support_class(baseline, v):
    pattern = tuple(bool(baseline - a >= 0.05) for a in (v - H, v, v + H))
    classes = {(False, False, False): 'support_excluded',
               (True, False, False): 'gain_possible',
               (True, True, False): 'loss_possible',
               (True, True, True): 'all_support_eligible'}
    require(pattern in classes, 'nonmonotone support')
    return classes[pattern]


def history(original, trigger):
    baseline, v = original[0], original[trigger]
    prefix = original[:trigger + 1]
    before = event(prefix, baseline)
    preexisting = before['start'] is not None
    trailing = 0
    for value in reversed(prefix):
        if baseline - value < 0.05:
            break
        trailing += 1
    native = event(list(prefix) + [v] * (200 - trigger), baseline)
    return dict(preexisting=preexisting, prefix_start=before['start'],
                trailing=trailing, window_excluded=not preexisting and 200 - trigger + trailing < 20,
                native_event=native['start'] is not None)


def restrictions(cls, hist, native, restored):
    if hist['preexisting']:
        require(native and restored, 'preexisting event lost')
    if hist['window_excluded']:
        require(not native and not restored, 'window impossibility violated')
    if cls in ('support_excluded', 'all_support_eligible'):
        require(native == restored, 'extreme support discordance')
    if cls in ('support_excluded', 'gain_possible'):
        require(not (native and not restored), 'forbidden event loss')
    else:
        require(not (not native and restored), 'forbidden event gain')


def inventory(names, expected):
    require(len(names) == len(set(names)) and set(names) == set(expected), 'member inventory')


def investment_path(raw, allowed, censuses):
    offsets, alleles = raw['offsets'], raw['alleles']
    require(offsets.ndim == 1 and len(offsets) == censuses + 1, 'census count')
    require(np.issubdtype(offsets.dtype, np.integer), 'integer offsets')
    require(offsets[0] == 0 and offsets[-1] == len(alleles), 'offset coverage')
    require(np.all(np.diff(offsets) > 0), 'every census must be occupied')
    require(alleles.ndim == 3 and alleles.shape[1:] == (3, 2), 'allele shape')
    values = alleles[:, 1, :]
    require(np.isfinite(values).all(), 'finite investment alleles')
    if allowed is not None:
        require(np.isin(values, allowed).all(), 'investment support violation')
    means, fixed = [], []
    for lo, hi in zip(offsets[:-1], offsets[1:]):
        copies = values[lo:hi]
        means.append(float(copies.mean()))
        fixed.append(float(copies[0, 0]) if np.all(copies == copies[0, 0]) else None)
    return np.asarray(means), fixed


def refixation(fixed, trigger, v, completion):
    for index in range(1, len(fixed)):
        allele = fixed[index]
        if allele is not None:
            require(allele in (v - H, v + H), 'refixation endpoint')
            require(all(later == allele for later in fixed[index:]), 'fixation must be absorbing')
            year = trigger + index
            return dict(year=year, endpoint='lower' if allele < v else 'upper',
                        remaining=200 - year, event_complete_at_refixation=completion is not None and completion <= year,
                        absorbing=True)
    return dict(year=None, endpoint='unfixed', remaining=None, event_complete_at_refixation=None, absorbing=None)


def load_npz(z, name):
    with np.load(io.BytesIO(z.read(name)), allow_pickle=False) as f:
        return {key: f[key] for key in ('alleles', 'offsets', 'metadata')}


def write_csv(path, rows):
    with path.open('x', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def extract(archive, preflight_path, protocol_path, out):
    require(digest(archive) == ARCHIVE_SHA, 'archive SHA256')
    require(digest(preflight_path) == PREFLIGHT_SHA, 'preflight SHA256')
    require(digest(protocol_path) == PROTOCOL_SHA, 'published protocol SHA256')
    cases = json.loads(preflight_path.read_text(encoding='utf-8'))['cases']
    require(len(cases) == len({c['key'] for c in cases}) == 64, '64 original slots')
    require(Counter(c['block'] for c in cases) == {'causal_main': 32, 'causal_confirmation': 32}, 'two 32-slot blocks')
    states, pairs = [], []
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        manifest = json.loads(z.read('MANIFEST.json'))
        inventory(names, set(manifest) | {'MANIFEST.json'})
        require(len(names) == 12042, 'archive member count')
        triggered = [c for c in cases if c['trigger'] is not None]
        require(len(triggered) == 61, '61 triggered slots')
        expected_raw = {f"raw/{c['key']}__r{r:02d}__{arm}.npz" for c in triggered for r in range(64) for arm in ('native', 'restored')}
        inventory([n for n in names if n.startswith('raw/')], expected_raw)
        inventory([n for n in names if n.startswith('original/')], {f"original/{c['key']}.npz" for c in cases})
        inventory([n for n in names if n.startswith('pairs/')], {f"pairs/{c['key']}__r{r:02d}.json" for c in triggered for r in range(64)})
        for case in cases:
            key, block, trigger = case['key'], case['block'], case['trigger']
            name = f'original/{key}.npz'
            require(hashlib.sha256(z.read(name)).hexdigest() == case['original_npz_sha256'], 'original hash')
            original_raw = load_npz(z, name)
            original, fixed_original = investment_path(original_raw, None, 201)
            base = float(original[0])
            row = dict(key=key, block=block, trigger=trigger, baseline=base,
                       fixed_I=None, support_class='not_triggered', preexisting=None, prefix_start=None,
                       trailing=None, remaining=None, window_excluded=None, native_event_predicted=None,
                       original_event_start=event(original, base)['start'], pairs=0,
                       native_events=0, restored_events=0, gains=0, losses=0,
                       terminal_mean_difference=0.0, trigger_population=None)
            if trigger is None:
                states.append(row)
                continue
            require(fixed_original[trigger] is not None, 'trigger is complete fixation')
            v = fixed_original[trigger]
            cls = support_class(base, v)
            hist = history(original, trigger)
            row.update(fixed_I=v, support_class=cls, preexisting=hist['preexisting'], prefix_start=hist['prefix_start'],
                       trailing=hist['trailing'], remaining=200-trigger, window_excluded=hist['window_excluded'],
                       native_event_predicted=hist['native_event'],
                       trigger_population=int(np.diff(original_raw['offsets'])[trigger]))
            state_pairs = []
            for replicate in range(64):
                p = dict(key=key, block=block, replicate=replicate, support_class=cls, preexisting=hist['preexisting'])
                endpoints = {}
                for arm in ('native', 'restored'):
                    raw = load_npz(z, f'raw/{key}__r{replicate:02d}__{arm}.npz')
                    meta = json.loads(str(raw['metadata']))
                    require((meta['key'], meta['replicate'], meta['arm'], meta['trigger']) == (key, replicate, arm, trigger), 'raw identity')
                    require(str(meta['seed']) == str(case['pair_seeds'][replicate]), 'raw seed')
                    require(meta['original_sha256'] == case['original_npz_sha256'] and meta['execution_sha256'] == EXECUTION_SHA, 'raw provenance')
                    means, fixed = investment_path(raw, (v,) if arm == 'native' else (v-H, v+H), 201-trigger)
                    require(means[0] == v, 'shared trigger mean')
                    at_trigger = raw['alleles'][:raw['offsets'][1], 1, :]
                    require(np.all(at_trigger.mean(axis=1) == v), 'shared trigger individual expression')
                    whole = np.concatenate((original[:trigger], means))
                    result = event(whole, base)
                    for field, value in result.items():
                        p[f'{arm}_{field}'] = value
                    p[f'{arm}_event'] = result['start'] is not None
                    endpoints[arm] = float(means[-1])
                    if arm == 'restored':
                        for field, value in refixation(fixed, trigger, v, result['completion']).items():
                            p['refix_' + field] = value
                require(p['native_event'] == hist['native_event'], 'native event prediction')
                restrictions(cls, hist, p['native_event'], p['restored_event'])
                p['joint'] = str(int(p['native_event'])) + str(int(p['restored_event']))
                p['terminal_mean_difference'] = endpoints['native'] - endpoints['restored']
                state_pairs.append(p)
            row.update(pairs=64, native_events=sum(p['native_event'] for p in state_pairs),
                       restored_events=sum(p['restored_event'] for p in state_pairs),
                       gains=sum(p['joint'] == '01' for p in state_pairs), losses=sum(p['joint'] == '10' for p in state_pairs),
                       terminal_mean_difference=float(np.mean([p['terminal_mean_difference'] for p in state_pairs])))
            states.append(row)
            pairs.extend(state_pairs)
    require(len(states) == 64 and len(pairs) == 3904, 'complete coverage')
    blocks = {}
    for block in ('causal_main', 'causal_confirmation'):
        ss = [s for s in states if s['block'] == block]
        pp = [p for p in pairs if p['block'] == block]
        joint = {j: sum(p['joint'] == j for p in pp) for j in ('00', '01', '10', '11')}
        native, restored = sum(p['native_event'] for p in pp), sum(p['restored_event'] for p in pp)
        require(restored-native == joint['01']-joint['10'], 'gain/loss reconciliation')
        blocks[block] = dict(original_slots=len(ss), triggered_slots=sum(s['trigger'] is not None for s in ss),
            policy_zero_slots=sum(s['trigger'] is None for s in ss), pairs=len(pp),
            support_classes=dict(Counter(s['support_class'] for s in ss)),
            preexisting_states=sum(s['preexisting'] is True for s in ss),
            window_excluded_states=sum(s['window_excluded'] is True for s in ss),
            gain_capable_states=sum(s['support_class'] == 'gain_possible' and not s['preexisting'] and not s['window_excluded'] for s in ss),
            native_events=native, restored_events=restored, joint=joint,
            refixation_by_joint={j: dict(Counter(p['refix_endpoint'] for p in pp if p['joint'] == j)) for j in joint},
            terminal_mean_difference=float(np.mean([s['terminal_mean_difference'] for s in ss])))
    require((blocks['causal_main']['native_events'], blocks['causal_main']['restored_events']) == (640, 1108), 'main frozen readout match')
    require((blocks['causal_confirmation']['native_events'], blocks['causal_confirmation']['restored_events']) == (1280, 1208), 'confirmation frozen readout match')
    summary = dict(status='ALL_DECLARED_PATH_RESTRICTIONS_PASS', exploratory=True, biological_updates=0,
        original_slots=64, triggered_pairs=3904, nontrigger_policy_zero_slots=3,
        all_observed_censuses_occupied=True, all_native_and_restored_supports_checked=True,
        all_native_event_predictions_match=True, all_observed_refixations_absorbing=True,
        original_primary='unresolved', confirmation_margin_0_01='unresolved', blocks=blocks)
    write_csv(out / 'STATES.csv', states)
    write_csv(out / 'PAIRS.csv', pairs)
    (out / 'SUMMARY.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    provenance = dict(archive_sha256=ARCHIVE_SHA, preflight_sha256=PREFLIGHT_SHA,
        protocol_sha256=PROTOCOL_SHA, protocol_commit=PROTOCOL_COMMIT, reader_sha256=digest(__file__),
        outputs={p.name: digest(p) for p in sorted(out.iterdir()) if p.is_file()},
        biological_updates=0, new_random_draws=0)
    (out / 'PROVENANCE.json').write_text(json.dumps(provenance, indent=2) + '\n', encoding='utf-8')
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--preflight', type=Path, required=True)
    parser.add_argument('--protocol', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    try:
        result = extract(args.archive, args.preflight, args.protocol, args.out)
    except Exception as error:
        (args.out / 'TECHNICAL_FAILURE.json').write_text(json.dumps(dict(error_type=type(error).__name__, message=str(error)), indent=2) + '\n', encoding='utf-8')
        raise
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
