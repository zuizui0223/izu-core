"""Source-bound completed mean-control evidence. No model import or random draws."""
import gzip
import hashlib
import json
import math
from pathlib import Path

FOLDER = Path('data/results/natural_order_mean_20261015')
PINS = {'INDEPENDENT_ADMISSION.json': 'e794ff3512bab789f2927d686459d2603f8e29c52535df1240cf828868112f71', 'PUBLIC_READBACK.json': '671d48180f058f130a6bae44d722315fa1c2befbcba05ece9f981dd9efd03d07', 'READOUT.json.gz': '2f6849fff2aa0c64a3ed0ed1123a221d3171e39ce44b7ac179fe2579b5d5e5ad'}
READOUT_SHA = '40a3cc176e60c4f0d58087610b4717bab4f95048a5475c92c125d8ecf6d18096'
FREEZE_SHA = 'c2f988abb1222288e4db1b47fb30d08e71e9f17476987e2a9c4e91a1a8dfb7ea'
ARCHIVE_SHA = '79f9e7d27f0337653a7ce9cc48ab8203f77bedaaf5a05eb87395bb3a29aa9e1f'

def materials(root):
    bodies = {}
    for name, digest in PINS.items():
        raw = (root / FOLDER / name).read_bytes()
        canonical = raw if name.endswith('.gz') else raw.replace(b'\r\n', b'\n')
        if hashlib.sha256(canonical).hexdigest() != digest:
            raise ValueError('frozen mean-control evidence differs: ' + name)
        bodies[name] = canonical
    raw = gzip.decompress(bodies['READOUT.json.gz'])
    if hashlib.sha256(raw).hexdigest() != READOUT_SHA:
        raise ValueError('frozen mean-control evidence raw readout differs')
    r = json.loads(raw)
    a = json.loads(bodies['INDEPENDENT_ADMISSION.json'])
    p = json.loads(bodies['PUBLIC_READBACK.json'])
    full = a['NATURAL_ORDER_MEAN_FULL_ARRAY_INDEPENDENT_ADMISSION_20261015.json']
    second = a['NATURAL_ORDER_MEAN_FINAL_RESULT_INDEPENDENT_REVIEW_20261015.json']
    f, s = full['summary'], second['summary']
    if (r['status'] != 'ALL2048_PRODUCTION_AND_INDEPENDENT_REPLAY_VERIFIED'
            or r['scientific_paths'] != 2048 or r['independent_replays'] != 2048
            or r['references'] != 8 or r['completed_updates'] != 820804
            or r['cumulative_reserved_updates'] != 820804 or r['cap'] != 820832
            or r['source_freeze_sha256'] != FREEZE_SHA
            or f['status'] != 'ALL2048_RAW_GENOME_SEED_PARENTAGE_AND36_GROUPS_INDEPENDENTLY_VERIFIED'
            or s['status'] != 'PASS_INDEPENDENT_ALL2048_ENDPOINTS_DURATIONS_36GROUPS_6GAPS'
            or s['review_findings'] != [] or s['original_archives'] != 2048
            or len(r['groups']) != 36 or len(r['strict_gaps']) != 6
            or f['new_biological_updates'] != 0 or s['new_biological_updates'] != 0
            or p['status'] != 'PUBLIC_DOWNLOAD_ALL6184_MEMBERS_BYTE_IDENTICAL'
            or p['members_verified'] != 6184 or p['archive_sha256'] != ARCHIVE_SHA):
        raise ValueError('independent mean-control admission incomplete')
    for entry in (full, second):
        v = entry['summary']
        if (v['archives'] != 2048 or v['readout_sha256'] != READOUT_SHA
                or v['source_freeze_sha256'] != FREEZE_SHA):
            raise ValueError('independent mean-control admission identity differs')
    for name, entry in a.items():
        if p['assets'][name]['sha256'] != entry['original_sha256']:
            raise ValueError('independent mean-control admission public identity differs')
    categories = {'assurance_first', 'investment_first', 'near_simultaneous', 'assurance_only', 'investment_only', 'neither'}
    expected = {(t,b,c) for t in (1.05,1.5) for b in ('main','confirmation','pooled_descriptive') for c in categories}
    if {(g['target'],g['block'],g['category']) for g in r['groups']} != expected:
        raise ValueError('independent mean-control admission groups differ')
    for g in r['groups']:
        n = g['starts']
        for arm in ('native','normalized'):
            if not (0 <= g[arm+'_survivors'] <= n and 0 <= g[arm+'_duration_sum'] <= 200*n):
                raise ValueError('independent mean-control admission counts differ')
            if not math.isclose(g[arm+'_fraction'],g[arm+'_survivors']/n,abs_tol=1e-12):
                raise ValueError('independent mean-control admission fraction differs')
    for t, old, new in ((1.05,123,4),(1.5,986,882)):
        groups = [g for g in r['groups'] if g['target']==t and g['block']=='pooled_descriptive']
        if (sum(g['starts'] for g in groups),sum(g['native_survivors'] for g in groups),sum(g['normalized_survivors'] for g in groups)) != (1024,old,new):
            raise ValueError('independent mean-control admission all-start totals differ')
    members, derivations = {}, {}
    for name, raw in bodies.items():
        key = 'EVIDENCE/NATURAL_ORDER_MEAN_' + name
        if not name.endswith('.gz'):
            raw = raw.replace(b'https://github.com/zuizui0223/izu-core/', b'PUBLIC_REPOSITORY_SOURCE/')
        members[key] = raw
        derivations[key] = dict(canonical_lf_sha256=PINS[name], derived_sha256=hashlib.sha256(raw).hexdigest(),
            public_companion_sha256=ARCHIVE_SHA,
            transformation='Exact frozen gzip or canonical LF with identifying repository prefix replaced. Complete36 groups; two fixed founders, attained-mean policy, extinction floor, no natural-order causal or unique-mediation claim.')
    return members, derivations
