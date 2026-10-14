"""Deterministic genotype-construction feasibility only; no future simulation."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import zipfile

import numpy as np

from q3_event_conditions_20261014 import ARCHIVE_SHA, PREFLIGHT_SHA, digest, require

POLICIES = {
    'A': dict(width=1/16, heterozygotes=24, variance=1/512),
    'B': dict(width=1/16, heterozygotes=12, variance=1/1024),
    'C': dict(width=1/8, heterozygotes=3, variance=1/1024),
}
FIELDS = ('alleles', 'allele_origin', 'mutation_flags', 'ids', 'birth_years')


def construct(state, name, indices):
    require(name in POLICIES, 'unknown policy')
    policy = POLICIES[name]
    a = np.asarray(state['alleles'])
    require(a.shape == (48, 3, 2) and np.isfinite(a).all(), '48 finite diploid states required')
    v = float(a[0, 1, 0])
    require(np.all(a[:, 1] == v), 'complete I fixation required')
    w = policy['width']
    require(0 <= v-w and v+w <= 1 and np.all((0 <= a) & (a <= 1)), 'allele domain')
    require(len(indices) == policy['heterozygotes'], 'subset size')
    require(all(isinstance(i, (int, np.integer)) and not isinstance(i, (bool, np.bool_)) for i in indices), 'integer indices')
    require(len(set(indices)) == len(indices) and all(0 <= i < 48 for i in indices), 'unique admitted indices')
    out = {field: np.asarray(state[field]).copy() for field in FIELDS}
    out['alleles'] = out['alleles'].astype(float)
    out['alleles'][indices, 1, :] = [v-w, v+w]
    b = out['alleles']
    require(np.array_equal(a.mean(axis=2), b.mean(axis=2)), 'individual expression preserved')
    require(b[:, 1, :].var() == policy['variance'], 'exact target variance')
    require(set(b[:, 1, :].flat) == {v-w, v, v+w}, 'three-point support')
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--preflight', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    require(digest(args.archive) == ARCHIVE_SHA, 'archive identity')
    require(digest(args.preflight) == PREFLIGHT_SHA, 'preflight identity')
    cases = json.loads(args.preflight.read_text(encoding='utf-8'))['cases']
    rows = []
    with zipfile.ZipFile(args.archive) as z:
        source = z.read('frozen_source/scripts/model3_island/types.py')
        source_sha = hashlib.sha256(source).hexdigest()
        for case in cases:
            if case['trigger'] is None:
                continue
            raw = z.read('original/' + case['key'] + '.npz')
            require(hashlib.sha256(raw).hexdigest() == case['original_npz_sha256'], 'original identity')
            with np.load(io.BytesIO(raw), allow_pickle=False) as npz:
                lo, hi = npz['offsets'][case['trigger']:case['trigger']+2]
                state = {field: npz[field][lo:hi].copy() for field in FIELDS}
            checks = {}
            for name, policy in POLICIES.items():
                # Existence witness only: this is not a randomised future allocation policy.
                indices = list(range(policy['heterozygotes']))
                out = construct(state, name, indices)
                require(all(np.array_equal(state[f], out[f]) for f in FIELDS if f != 'alleles'), 'nonallele fields unchanged')
                require(np.array_equal(state['alleles'][:, (0, 2), :], out['alleles'][:, (0, 2), :]), 'M/A unchanged')
                checks[name] = dict(policy, indices=indices, support=sorted(set(out['alleles'][:, 1, :].flat)),
                    allele_array_sha256=hashlib.sha256(out['alleles'].astype('<f8').tobytes()).hexdigest())
            rows.append(dict(key=case['key'], trigger=case['trigger'], original_sha256=case['original_npz_sha256'],
                             fixed_I=float(state['alleles'][0, 1, 0]), population=len(state['ids']), policies=checks))
    require(len(rows) == 61, 'all 61 triggered states')
    result = dict(status='ALL_61_STATES_THREE_POLICY_CONSTRUCTIONS_FEASIBLE',
        scope='existence_witness_not_future_outcomes_or_random_allocation', archive_sha256=ARCHIVE_SHA,
        preflight_sha256=PREFLIGHT_SHA, constructor_sha256=digest(__file__),
        frozen_domain_source='frozen_source/scripts/model3_island/types.py', frozen_domain_source_sha256=source_sha,
        native_calls=0, new_random_draws=0, constructed_states=183, rows=rows)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open('x', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'rows'}, indent=2))


if __name__ == '__main__':
    main()
