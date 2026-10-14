"""Verify and publish one fixed shard at a time; no biological work or retries."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

from q3_triangle_contract_20261014 import require, summarize
from q3_triangle_execution_gate_20261014 import authorize, digest, exclusive_json, LIMITS, job_deadline
from verify_q3_triangle_archives_20261014 import verify_shard, verify_campaign, verify_summary

REPO = 'zuizui0223/izu-core'
TAG = 'q3-distribution-triangle-20261014'


def publish_campaign(out, plan, execution_sha, identity, cli, guard):
    """Authorized caller supplies the exact plan and run; transport is injectable for tests."""
    out = Path(out)
    stage, readback = out/'staging', out/'readback'
    stage.mkdir();readback.mkdir()
    notes = out/'RELEASE_NOTES.md'
    notes.write_text('Frozen Q3 distribution-policy experiment. Complete raw paths, independent replay '
                     'and simultaneous conditional readouts. Original primary remains unresolved. '
                     'Identity is by SHA256; platform immutability is not asserted.\n', encoding='utf-8')
    # Create the new lightweight tag explicitly: draft releases need not create
    # their Git tag until publication. Never reuse or force-update an old tag.
    created_tag = json.loads(cli(['api', f'repos/{REPO}/git/refs', '--method', 'POST',
                                 '-f', 'ref=refs/tags/'+TAG, '-f', 'sha='+identity['head']]))
    require(created_tag['object']['sha'] == identity['head'], 'created release tag identity')
    cli(['release', 'create', TAG, '--repo', REPO, '--draft', '--latest=false',
         '--target', identity['head'], '--title', 'Q3 distribution triangle 20261014', '--notes-file', str(notes)])
    tag = json.loads(cli(['api', f'repos/{REPO}/git/ref/tags/{TAG}']))
    require(tag['object']['sha'] == identity['head'], 'release tag must identify this activation')
    headers, records, published = [], [], []
    for shard in range(18):
        guard()
        require(not list(stage.iterdir()) and not list(readback.iterdir()), 'one-archive-at-a-time storage')
        cli(['run', 'download', identity['run_id'], '--repo', REPO,
             '--name', f"q3-triangle-shard-{shard:02d}-{identity['run_id']}", '--dir', str(stage)])
        filename = f'Q3_TRIANGLE_SHARD_{shard:02d}.zip'
        archive = stage/filename
        receipt_path = stage/f'SHARD_{shard:02d}_RECEIPT.json'
        require({p.name for p in stage.iterdir()} == {filename, receipt_path.name}, 'artifact transport inventory')
        receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
        require(receipt['shard'] == shard and receipt['run_id'] == identity['run_id'] and
                receipt['execution_sha256'] == execution_sha, 'artifact transport identity')
        require(archive.stat().st_size == receipt['bytes'] <= LIMITS['archive_bound_per_shard'] and
                digest(archive) == receipt['archive_sha256'], 'artifact transport bytes/hash')
        header, rows = verify_shard(archive, plan, execution_sha, identity['run_id'], guard)
        require(header['shard'] == shard, 'downloaded shard identity')
        headers.append(header);records.extend(rows)
        cli(['release', 'upload', TAG, str(archive), '--repo', REPO])
        archive.unlink()  # Only this known file; retain compact receipt until remote readback passes.
        cli(['release', 'download', TAG, '--repo', REPO, '--pattern', filename, '--dir', str(readback)])
        require({p.name for p in readback.iterdir()} == {filename}, 'external archive inventory')
        remote = readback/filename
        require(remote.stat().st_size == receipt['bytes'] and digest(remote) == receipt['archive_sha256'],
                'external release byte readback')
        published.append(dict(shard=shard, filename=filename, bytes=receipt['bytes'],
                              sha256=receipt['archive_sha256'], triplets=488, trajectories=1464))
        remote.unlink();receipt_path.unlink()
        require(2*sum(p['bytes'] for p in published)+16*1024**2 < LIMITS['max_remote_bytes'], 'remote two-copy ceiling')
    accounting = verify_campaign(headers)
    claim = summarize(records, plan['cases'])
    independent = verify_summary(claim, records, plan['cases'])
    manifest = dict(status='COMPLETE_ALL_RAW_EXTERNAL_BYTES_VERIFIED', run_id=identity['run_id'],
                    execution_sha256=execution_sha, head=identity['head'], release_tag=TAG,
                    archives=published, accounting=accounting, native_updates_during_publication=0)
    documents = {'CAMPAIGN_MANIFEST.json': manifest, 'READOUT.json': claim,
                 'INDEPENDENT_VERIFICATION.json': independent}
    expected_assets = {p['filename']:p['bytes'] for p in published}
    for name, value in documents.items():
        guard();path = out/name;exclusive_json(path, value)
        expected_assets[name] = path.stat().st_size
        cli(['release', 'upload', TAG, str(path), '--repo', REPO])
        cli(['release', 'download', TAG, '--repo', REPO, '--pattern', name, '--dir', str(readback)])
        require(digest(readback/name) == digest(path), 'external document byte readback')
        (readback/name).unlink()
    assets = json.loads(cli(['release', 'view', TAG, '--repo', REPO, '--json', 'assets']))['assets']
    require(len(assets) == len(expected_assets) and {a['name']:a['size'] for a in assets} == expected_assets,
            'complete release inventory')
    guard()
    cli(['release', 'edit', TAG, '--repo', REPO, '--draft=false', '--latest=false'])
    return accounting


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True, type=Path);p.add_argument('--out', required=True, type=Path)
    a = p.parse_args()
    execution, execution_sha, identity = authorize(a.repo)
    out = a.out.resolve();out.mkdir(parents=True, exist_ok=False)
    deadline = job_deadline(os.environ, minutes=30, tail_seconds=180)
    def guard():
        require(time.monotonic() < deadline, 'aggregate readback deadline')
    def cli(args):
        guard()
        return subprocess.check_output(['gh', *args], text=True, timeout=max(1, min(180, deadline-time.monotonic())))
    try:
        require(shutil.disk_usage(out).free >= LIMITS['minimum_free_local_bytes'], 'aggregate free space')
        plan = json.loads((a.repo/'data/designs/q3_triangle_preflight_20261014.json').read_text(encoding='utf-8'))
        publish_campaign(out, plan, execution_sha, identity, cli, guard)
    except BaseException as exc:
        exclusive_json(out/'HOLD.json', dict(status='TECHNICAL_HOLD_PUBLICATION', exception=type(exc).__name__,
                       reason=str(exc), execution_sha256=execution_sha, run_id=identity['run_id']))
        raise


if __name__ == '__main__':
    main()
