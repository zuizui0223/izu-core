"""Approved, all-start descriptive mean intervention; no natural-order causal test."""
from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path
import zipfile

import numpy as np

from scripts import persistence_expression_mechanism_20261012 as native
from scripts.initial_assurance_mean_20261013 import equalize_mean

BANK_SHA = 'ec15316f234ec6f28c50d93bb099ad9db6f64b84a82f6c1a88370482f6f6d8b2'
BLOCKS = ('main', 'confirmation')
TARGETS = (1.05, 1.5)
CATEGORIES = ('assurance_first', 'investment_first', 'near_simultaneous',
              'assurance_only', 'investment_only', 'neither')
UPDATE_CAP = 820832
PATH_UPDATES = 200


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def future_seed(task):
    if task['block'] not in BLOCKS or type(task['replicate']) is not int or not 0 <= task['replicate'] < 512:
        raise ValueError('unregistered source task')
    original = dict(study='history', block=task['block'], replicate=task['replicate'])
    text = 'resolution-v1-20261011:challenge' + json.dumps(original, sort_keys=True)
    return int.from_bytes(hashlib.sha256(text.encode()).digest()[:16], 'big')


def reserve_updates(used, amount):
    if type(used) is not int or type(amount) is not int or used < 0 or amount < 0 or used + amount > UPDATE_CAP:
        raise ValueError('frozen cumulative native-update cap')
    return used + amount


def read_bank(path):
    raw = Path(path).read_bytes()
    if digest(raw) != BANK_SHA:
        raise ValueError('source bank digest mismatch')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        if sorted(z.namelist()) != ['MANIFEST.json', 'states.npz']:
            raise ValueError('bank inventory')
        manifest = json.loads(z.read('MANIFEST.json'))
        data = z.read('states.npz')
    if digest(data) != manifest['states_sha256']:
        raise ValueError('bank state digest')
    with np.load(io.BytesIO(data), allow_pickle=False) as a:
        states = {f: a[f].copy() for f in a.files}
    if set(states) != set(native.FIELDS) or len(manifest['cases']) != 1024:
        raise ValueError('bank state inventory')
    seen = set()
    for ix, row in enumerate(manifest['cases']):
        t = row['task']
        if t['study'] != 'history' or t['arm'] != 'both_access' or row['category'] not in CATEGORIES:
            raise ValueError('bank source scope')
        future_seed(t)
        seen.add((t['block'], t['replicate']))
        for f in native.FIELDS:
            if states[f][ix].shape != ((8, 3, 2) if f in native.FIELDS[:3] else (8,)):
                raise ValueError('bank field layout')
        equalize_mean(native.PlantState(**{f: states[f][ix] for f in native.FIELDS}))
    if seen != {(b, r) for b in BLOCKS for r in range(512)}:
        raise ValueError('bank cohort incomplete or duplicated')
    return manifest, states


def check_inventory(records):
    keys = [(r['block'], r['replicate'], r['target']) for r in records]
    expected = {(b, r, t) for b in BLOCKS for r in range(512) for t in TARGETS}
    if len(keys) != 2048 or set(keys) != expected:
        raise ValueError('complete2048 unique all-start outcomes required')
    for b in BLOCKS:
        for r in range(512):
            categories = {x['category'] for x in records if x['block'] == b and x['replicate'] == r}
            if len(categories) != 1:
                raise ValueError('historical category changed with future challenge')


def describe(records):
    for r in records:
        if r['block'] not in BLOCKS or r['target'] not in TARGETS or r['category'] not in CATEGORIES:
            raise ValueError('unregistered outcome group')
        for p in ('native', 'normalized'):
            if r[p] not in (0, 1) or not np.isfinite(r[p]):
                raise ValueError('binary all-start occupancy required')
            d = r[p + '_duration']
            if not np.isfinite(d) or d != int(d) or not 0 <= d <= 200:
                raise ValueError('occupied-census duration outside fixed horizon')
    groups = []
    for b in (*BLOCKS, 'pooled_descriptive'):
        for t in TARGETS:
            for c in CATEGORIES:
                rows = [r for r in records if (b == 'pooled_descriptive' or r['block'] == b)
                        and r['target'] == t and r['category'] == c]
                n = len(rows)
                a = dict(block=b, target=t, category=c, starts=n)
                for p in ('native', 'normalized'):
                    count = sum(r[p] for r in rows)
                    duration = sum(r[p + '_duration'] for r in rows)
                    a.update({p + '_survivors': count, p + '_fraction': count/n if n else None,
                              p + '_duration_sum': duration, p + '_mean_duration': duration/n if n else None})
                a['paired_gains'] = sum(r['normalized'] == 1 and r['native'] == 0 for r in rows)
                a['paired_losses'] = sum(r['normalized'] == 0 and r['native'] == 1 for r in rows)
                a['occupancy_change'] = (a['normalized_fraction']-a['native_fraction']) if n else None
                a['duration_change'] = (a['normalized_mean_duration']-a['native_mean_duration']) if n else None
                groups.append(a)
    gaps = []
    for b in (*BLOCKS, 'pooled_descriptive'):
        for t in TARGETS:
            af = next(r for r in groups if r['block'] == b and r['target'] == t and r['category'] == 'assurance_first')
            inv = next(r for r in groups if r['block'] == b and r['target'] == t and r['category'] == 'investment_first')
            d = dict(block=b, target=t, assurance_first_n=af['starts'], investment_first_n=inv['starts'])
            for endpoint, field in [('occupancy', 'fraction'), ('duration', 'mean_duration')]:
                for p in ('native', 'normalized'):
                    d[p + '_' + endpoint + '_gap'] = af[p+'_'+field]-inv[p+'_'+field] if af['starts'] and inv['starts'] else None
                v, u = d['native_'+endpoint+'_gap'], d['normalized_'+endpoint+'_gap']
                d[endpoint+'_attenuation'] = v-u if v is not None and u is not None else None
            gaps.append(d)
    return dict(groups=groups, strict_gaps=gaps, inference='Retrospective fixed-founder descriptive policy comparison; no new primary family, significance test, or causal effect of past natural order.')
