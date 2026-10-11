"""Infrastructure-only continuation of an immutable Windows experiment."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import zipfile

BASE = Path(r'C:\Users\zuizui\Documents\Codex\2026-09-24\https-github-com-zuizui0223-izu-core')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def extract(bundle, expected):
    if digest(bundle) != expected:
        raise ValueError('input bundle SHA256 mismatch')
    with zipfile.ZipFile(bundle) as z:
        for item in z.infolist():
            dest = (BASE / item.filename).resolve()
            if not dest.is_relative_to(BASE.resolve()):
                raise ValueError('unsafe archive path')
        z.extractall(BASE)
    manifest = json.loads((BASE / 'remote_transfer_manifest.json').read_text())
    for name, sha in manifest['files'].items():
        if digest(BASE / name) != sha:
            raise ValueError('transfer file drift: ' + name)
    return manifest


def run(bundle, expected, shard, shards):
    if shards != 4 or shard not in range(4):
        raise ValueError('registered four-shard inventory required')
    manifest = extract(bundle, expected)
    root = BASE / 'work/resolution_20261011'
    sys.path.insert(0, str(root))
    import atom_campaign as campaign
    identity = campaign.identity()
    registration = json.loads((campaign.NUM / 'registration.json').read_text())
    if identity != registration['identity'] or campaign.jobs() != registration['jobs']:
        raise ValueError('frozen source/runtime/job identity mismatch')
    all_jobs = campaign.jobs()
    missing = [j for j in all_jobs if not (campaign.NUM / 'archives' / (campaign.previous.key(j) + '.json')).exists()]
    if [campaign.previous.key(j) for j in missing] != manifest['remaining_job_keys']:
        raise ValueError('remaining job inventory mismatch')
    # Check every cached archive before reusing it, without recomputing it.
    for j in all_jobs:
        if j not in missing:
            campaign.compute(j, identity)
    # Remote platform must reproduce a frozen technical archive before production.
    reference = all_jobs[0]
    import numpy as np
    import tempfile
    original = campaign.NUM
    with tempfile.TemporaryDirectory() as tmp:
        campaign.NUM = Path(tmp)
        replay = campaign.compute(reference, identity, horizon=3, technical=True)
    campaign.NUM = original
    technical = original / 'technical' / (campaign.previous.key(reference) + '.npz')
    with np.load(technical, allow_pickle=False) as stored:
        for key in ('trace', 'cdf', 'axis2'):
            np.testing.assert_allclose(replay[key], stored[key], atol=1e-12, rtol=1e-12, equal_nan=True)
    selected = missing[shard::shards]
    output = Path(os.environ.get('REMOTE_OUTPUT', 'remote-output')).resolve()
    output.mkdir(parents=True, exist_ok=True)
    try:
        for job in selected:
            campaign.compute(job, identity)
            key = campaign.previous.key(job)
            for suffix in ('.npz', '.json'):
                source = original / 'archives' / (key + suffix)
                import shutil
                shutil.copy2(source, output / source.name)
        if campaign.identity() != identity:
            raise ValueError('source drift during execution')
    finally:
        (output / 'remote_execution.json').write_text(json.dumps(dict(
            shard=shard, source_identity=identity, bundle_sha256=expected,
            selected_job_keys=[campaign.previous.key(j) for j in selected],
            completed_archive_sha256={p.name: digest(p) for p in output.glob('*.npz')},
            platform=sys.platform, python=sys.version,
            scope='remote continuation, not full numerical admission'), indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--bundle', type=Path, required=True)
    p.add_argument('--sha256', required=True)
    p.add_argument('--shard', type=int, required=True)
    a = p.parse_args()
    run(a.bundle, a.sha256, a.shard, 4)
