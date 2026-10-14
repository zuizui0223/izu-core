"""Admit frozen originals and register deterministic seeds; no RNG or futures."""
import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import zipfile

import numpy as np

from q3_triangle_contract_20261014 import build_plan, require

ARCHIVE_SHA = '8a2462910025b4a386e789583578cb1380349097393916dac4e50d01c9637b7e'
PREFLIGHT_SHA = '165a0d39f6f226ac4ccfbfb65fef4b2189fde272ccb0c0f33d840d542ae2760b'


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest()


def first_trigger(raw):
    offsets, a = raw['offsets'], raw['alleles']
    require(a.ndim == 3 and a.shape[1:] == (3, 2) and np.isfinite(a).all(), 'finite allele shape')
    require(offsets.ndim == 1 and len(offsets) >= 2 and np.issubdtype(offsets.dtype, np.integer), 'offset schema')
    require(offsets[0] == 0 and offsets[-1] == len(a) and np.all(np.diff(offsets) >= 0), 'offset coverage')
    for t, (lo, hi) in enumerate(zip(offsets[:-1], offsets[1:])):
        copies = a[lo:hi, 1, :]
        if copies.size and copies.min() == copies.max():
            return t
    return None


def source_inventory(actual, registered):
    require(set(registered) <= set(actual), 'missing registered source')
    ignored = sorted(set(actual)-set(registered))
    for name in ignored:
        path = PurePosixPath(name)
        match = re.fullmatch(r'(.+)\.cpython-311\.pyc', path.name)
        require(path.parent.name == '__pycache__' and match is not None, 'foreign source member')
        require(str(path.parent.parent / (match.group(1)+'.py')) in registered, 'unregistered cache module')
    return ignored


def main():
    parser = argparse.ArgumentParser()
    for name in ('archive', 'preflight', 'design', 'out'):
        parser.add_argument('--'+name, type=Path, required=True)
    args = parser.parse_args()
    require(digest(args.archive) == ARCHIVE_SHA, 'archive SHA256')
    require(digest(args.preflight) == PREFLIGHT_SHA, 'original preflight SHA256')
    previous = json.loads(args.preflight.read_text(encoding='utf-8'))
    cases = previous['cases']
    source_hashes = {}
    with zipfile.ZipFile(args.archive) as z:
        names = z.namelist()
        require(len(names) == len(set(names)) == 12042, 'archive inventory')
        manifest = json.loads(z.read('MANIFEST.json'))
        require(set(names) == set(manifest) | {'MANIFEST.json'}, 'manifest inventory')
        for name, expected in previous['frozen_source_sha256'].items():
            actual_name = name.replace('FROZEN_SOURCE/', 'frozen_source/', 1)
            got = hashlib.sha256(z.read(actual_name)).hexdigest()
            require(got == expected == manifest[actual_name], 'frozen source hash '+actual_name)
            source_hashes[actual_name] = got
        ignored_cache = source_inventory({n for n in names if n.startswith('frozen_source/')}, set(source_hashes))
        ignored_cache_hashes = {n: hashlib.sha256(z.read(n)).hexdigest() for n in ignored_cache}
        require(all(manifest[n] == h for n, h in ignored_cache_hashes.items()), 'ignored cache inventory hashes')
        campaign_hash = hashlib.sha256(z.read('campaign.json')).hexdigest()
        require(campaign_hash == manifest['campaign.json'], 'campaign identity')
        admitted_metadata_bytes = sum(z.getinfo(n).file_size for n in names if n.startswith(('frozen_source/', 'original/')) or n == 'campaign.json')
        require(admitted_metadata_bytes < 128*1024**2, 'shard original/source metadata allowance')
        for c in cases:
            raw = z.read('original/'+c['key']+'.npz')
            require(hashlib.sha256(raw).hexdigest() == c['original_npz_sha256'], 'original record identity')
            with np.load(io.BytesIO(raw), allow_pickle=False) as npz:
                a = {f: npz[f] for f in npz.files}
            require(len(a['offsets']) == 202, 'original 201-census coverage')
            require(first_trigger(a) == c['trigger'], 'earliest trigger agreement')
            meta = json.loads(str(a['metadata']))
            c['original_metadata_sha256'] = hashlib.sha256(json.dumps(meta, sort_keys=True).encode()).hexdigest()
            c['fixed_I'] = None
            if c['trigger'] is not None:
                lo, hi = a['offsets'][c['trigger']:c['trigger']+2]
                require(hi-lo == 48, 'trigger population admission')
                v = float(a['alleles'][lo, 1, 0])
                require(1/8 <= v <= 7/8, 'unclipped wide policy domain')
                c['fixed_I'] = v
    plan = build_plan(cases)
    plan.update(archive_sha256=ARCHIVE_SHA, prior_preflight_sha256=PREFLIGHT_SHA,
                design_sha256=digest(args.design), frozen_source_sha256=source_hashes,
                excluded_bytecode_sha256=ignored_cache_hashes,
                campaign_sha256=campaign_hash, admitted_original_source_bytes=admitted_metadata_bytes,
                planning_code_sha256={p.name: digest(p) for p in (Path(__file__), Path(__file__).with_name('q3_triangle_contract_20261014.py'))})
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(plan, f, indent=2, allow_nan=False)
        f.write('\n')
    print(json.dumps({k: plan[k] for k in ('status', 'approved', 'new_trajectories', 'triplets', 'max_native_updates', 'max_hosted_runner_minutes', 'archive_bound_per_shard', 'remote_two_copy_bound', 'local_reservation_per_shard')}, indent=2))
    print('preflight_sha256='+digest(args.out))


if __name__ == '__main__':
    main()
