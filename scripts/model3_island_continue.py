"""Explicit compute-only continuation; frozen model and original receipts unchanged."""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import time
import numpy as np
import psutil
from threadpoolctl import threadpool_limits
from scripts.model3_island.design import canonical, digest, compile_design, source_hashes
from scripts.model3_island.run import atomic_json, execute_case, verify_snapshot
from scripts.model3_island.storage import pack_result


def pending_cases(cases, output, manifest_hash):
    output = Path(output)
    expected_ids = {c['case_id'] for c in cases}
    if any(p.parent.name not in expected_ids for p in output.glob('*/receipt.json')):
        raise ValueError('unexpected completed case')
    pending = []
    for case in cases:
        folder = output / case['case_id']
        receipt = folder / 'receipt.json'
        if not receipt.exists():
            if (folder / 'input.json').exists() and json.loads((folder / 'input.json').read_text()) != case:
                raise ValueError('interrupted input differs')
            pending.append(case)
            continue
        r = json.loads(receipt.read_text())
        expected = {'case_hash': digest(case), 'manifest_hash': manifest_hash,
                    'mode': 'production', 'status': 'complete'}
        if any(r.get(k) != v for k, v in expected.items()):
            raise ValueError('receipt identity mismatch')
        if json.loads((folder / 'input.json').read_text()) != case:
            raise ValueError('completed input differs')
        if sha256((folder / 'arrays.npz').read_bytes()).hexdigest() != r['arrays_sha256']:
            raise ValueError('completed arrays differ')
    return pending


def run(design, output, amendment):
    output = Path(output)
    doc = json.loads(Path(design).read_text(encoding='utf-8-sig'))
    change = json.loads(Path(amendment).read_text(encoding='utf-8-sig'))
    mh = digest(doc)
    if change['manifest_hash'] != mh or source_hashes() != doc['source_hashes']:
        raise ValueError('frozen design/source differs')
    if sha256(Path(__file__).read_bytes()).hexdigest() != change['runner_sha256']:
        raise ValueError('continuation runner differs')
    if json.loads((output / 'manifest.json').read_text()) != {'identity': {'manifest_hash': mh, 'mode': 'production'}, 'design': doc}:
        raise ValueError('stored manifest differs')
    verify_snapshot(output, doc, current_runtime=True)
    status_path = output / 'campaign_status.json'
    original = status_path.read_bytes()
    if sha256(original).hexdigest() != change['original_status_sha256']:
        raise ValueError('terminal STOP differs')
    status = json.loads(original)
    if status['complete'] or status['stop_reason'] != 'runtime_budget':
        raise ValueError('requires original runtime STOP')
    cases = [c for c in compile_design(doc) if c['cohort'] != 'pilot']
    pending = pending_cases(cases, output, mh)
    if len(pending) != change['missing_cases'] or len(cases)-len(pending) != status['completed']:
        raise ValueError('continuation coverage differs')
    archive = output / 'continuations' / change['id']
    archive.mkdir(parents=True, exist_ok=False)  # one attempt; no silent budget reset
    (archive / 'original_campaign_status.json').write_bytes(original)
    atomic_json(archive / 'amendment.json', change)
    atomic_json(archive / 'pending_case_ids.json', [c['case_id'] for c in pending])
    for path in output.glob('*/interruption.json'):
        (archive / (path.parent.name + '-interruption.json')).write_bytes(path.read_bytes())
    atomic_json(archive / 'process.json', {'pid': os.getpid(), 'started_unix': time.time()})
    start = time.monotonic()
    limits = doc['resource_limits']
    output_bytes = sum(p.stat().st_size for p in output.rglob('*') if p.is_file())
    def check():
        if time.monotonic()-start >= change['additional_runtime_seconds']:
            raise TimeoutError('amendment_runtime_budget')
        if psutil.Process().memory_info().rss > limits['memory_mb']*1024**2:
            raise TimeoutError('memory_budget')
        if output_bytes > limits['output_mb']*1024**2:
            raise TimeoutError('output_budget')
        if psutil.disk_usage(str(output)).free < limits['min_free_mb']*1024**2:
            raise TimeoutError('free_disk_budget')
    completed = status['completed']; executed = 0; reason = None
    try:
        with threadpool_limits(limits=1):
            for case in pending:
                check()
                folder = output / case['case_id']; folder.mkdir(exist_ok=True)
                atomic_json(folder / 'input.json', case)
                begin = time.monotonic()
                result = execute_case(case, doc, check)
                check()
                with (folder / 'arrays.npz.tmp').open('wb') as handle:
                    np.savez_compressed(handle, **pack_result(result, doc['storage']))
                os.replace(folder / 'arrays.npz.tmp', folder / 'arrays.npz')
                atomic_json(folder / 'receipt.json', {'case_hash': digest(case), 'manifest_hash': mh,
                    'mode': 'production', 'status': 'complete', 'arrays_sha256': sha256((folder / 'arrays.npz').read_bytes()).hexdigest(),
                    'elapsed_seconds': time.monotonic()-begin, 'compute_amendment': change['id']})
                output_bytes += sum(p.stat().st_size for p in folder.iterdir() if p.is_file())
                completed += 1; executed += 1
    except TimeoutError as exc:
        reason = str(exc)
    except Exception as exc:
        atomic_json(archive / 'failure.json', {'type': type(exc).__name__, 'detail': str(exc)})
        raise
    terminal = {'expected': len(cases), 'completed': completed, 'executed': executed,
                'complete': completed == len(cases), 'manifest_hash': mh, 'stop_reason': reason,
                'compute_amendment': change['id']}
    atomic_json(archive / 'terminal.json', terminal)
    atomic_json(status_path, terminal)
    return terminal

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--design', required=True); p.add_argument('--output', required=True)
    p.add_argument('--amendment', required=True)
    a = p.parse_args()
    result = run(a.design, a.output, a.amendment)
    print(json.dumps(result), flush=True)
    raise SystemExit(0 if result['complete'] else 2)
