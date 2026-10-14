import copy
import hashlib
import importlib
import json
from pathlib import Path
import sys
import time
import zipfile

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from test_q3_triangle_contract_20261014 import cases, records
from q3_triangle_contract_20261014 import summarize


def verifier():
    return importlib.import_module('verify_q3_triangle_archives_20261014')


def test_independent_summary_checks_means_weights_intervals_and_opposed_signs():
    cs = cases();rr = records(cs)
    blocks = {c['key']: c['block'] for c in cs}
    for r in rr:
        main = blocks[r['key']] == 'causal_main'
        r['arms']['A'].update(I=.4375 if main else .5625, event=main)
        r['arms']['B']['event'] = not main
    answer = summarize(rr, cs)
    assert verifier().verify_summary(answer, rr, cs)['status'] == 'INDEPENDENT_SUMMARY_MATCH'
    assert answer['directional_replication']['D_A'] == 'opposed'
    for defect in ('estimate', 'half_width', 'direction', 'practical'):
        bad = copy.deepcopy(answer)
        item = bad['blocks']['causal_main']['contrasts']['D_A']
        item[defect] = 0 if defect in ('estimate', 'half_width') else 'unresolved'
        with pytest.raises(ValueError):
            verifier().verify_summary(bad, rr, cs)


def test_independent_summary_extinction_is_family_wide_and_keeps_events():
    cs = cases();rr = records(cs)
    rr[0]['arms']['C'].update(I=None, survived=False, event=True)
    answer = summarize(rr, cs)
    verifier().verify_summary(answer, rr, cs)
    bad = copy.deepcopy(answer);bad['raw_event_counts']['causal_main']['C'] = 0
    with pytest.raises(ValueError):
        verifier().verify_summary(bad, rr, cs)
    with pytest.raises(ValueError):
        verifier().verify_summary(answer, rr[:-1], cs)


def test_cross_shard_inventory_requires_one_run_and_exact_coverage():
    rows = [dict(shard=s, run_id='123', execution_sha256='d'*64,
                 triplets=488, trajectories=1464, production_updates=185760,
                 replay_updates=185760, fixture_updates=0, reserved_native_updates=371520)
            for s in range(18)]
    assert verifier().verify_campaign(rows)['native_updates'] == 6687360
    for kind in ('missing', 'duplicate', 'foreign_run', 'wrong_count', 'fixture_overrun'):
        bad = copy.deepcopy(rows)
        if kind == 'missing': bad.pop()
        elif kind == 'duplicate': bad[-1] = bad[0]
        elif kind == 'foreign_run': bad[0]['run_id'] = '124'
        elif kind == 'wrong_count': bad[0]['replay_updates'] = 1
        else: bad[0]['fixture_updates'] = 33
        with pytest.raises(ValueError):
            verifier().verify_campaign(bad)


def test_raw_readback_recomputes_endpoints_and_rejects_receipt_tampering(tmp_path, monkeypatch):
    from test_q3_triangle_paths_20261014 import prepared
    run, check, case, calls = prepared(tmp_path, monkeypatch)
    (tmp_path/'triplets').mkdir()
    receipt = run.run_triplet(case, 0, tmp_path, 'd'*64, time.monotonic()+30)
    assert len(calls) == 6  # Stand-in transitions only; archive reader adds none.
    names = [p for p in tmp_path.rglob('*') if p.is_file()]
    manifest = {p.relative_to(tmp_path).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in names}
    for altered in (False, True):
        path = tmp_path/('bad.zip' if altered else 'good.zip')
        with zipfile.ZipFile(path, 'w') as z:
            for p in names:
                if altered and p.name == 'synthetic__r000.json':
                    changed = copy.deepcopy(receipt);changed['arms']['A']['event'] = True
                    z.writestr(p.relative_to(tmp_path).as_posix(), json.dumps(changed))
                else:
                    z.write(p, p.relative_to(tmp_path).as_posix())
        with zipfile.ZipFile(path) as z:
            if altered:
                with pytest.raises(ValueError, match='endpoints'):
                    verifier().read_triplet(z, case, 0, 'd'*64, manifest)
            else:
                result = verifier().read_triplet(z, case, 0, 'd'*64, manifest)
                assert result['arms'] == {p: dict(I=.5, survived=True, event=False) for p in 'ABC'}
    assert len(calls) == 6


def test_archive_endpoint_definition_does_not_share_replay_calculator(monkeypatch):
    import numpy as np
    import verify_q3_triangle_paths_20261014 as paths
    monkeypatch.setattr(paths, 'read_endpoints', lambda *a:dict(I=999, survived=True, event=False))
    original = dict(alleles=np.full((201, 3, 2), .5), offsets=np.arange(202))
    original['alleles'][181:199, 1] = .375
    future = dict(alleles=np.full((2, 3, 2), .375), offsets=np.array([0, 1, 2]))
    assert verifier().archive_endpoints(original, future, 199) == dict(I=.375, survived=True, event=True)
    original['alleles'][181, 1] = .5
    assert verifier().archive_endpoints(original, future, 199)['event'] is False
    original['alleles'][1:21, 1] = .375
    future['offsets'] = np.array([0, 1, 1]);future['alleles'] = future['alleles'][:1]
    assert verifier().archive_endpoints(original, future, 199) == dict(I=None, survived=False, event=True)
