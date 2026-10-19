import copy
import numpy as np
import pytest
from scripts import q3_production160_20261019 as p
from scripts import q3_native_runner_20261019 as n
from scripts import q3_archive160_20261019 as archive


def test_production_plan_preserves_candidate_and_old_cap(tmp_path):
    plan = p.plan(False)
    assert len(plan['founders']) == len(plan['visitors']) == 160
    assert plan['founders'][0] == 501001
    assert plan['namespace'].endswith('planning-only')
    with pytest.raises(ValueError):
        n.initialize(tmp_path/'forbidden', plan)


def test_native_equivalence_restart_and_collection(tmp_path):
    native = tmp_path/'native'
    n.initialize(native, n.technical_plan())
    n.run(native, save_every=80)
    root = tmp_path/'production_adapter_technical'
    p.initialize(root, technical=True)
    p.run(root, max_updates=48)
    archive.pack(root,tmp_path/'partial.zip')
    root=tmp_path/'restored'
    archive.restore(tmp_path/'partial.zip',root)
    p.run(root)
    assert p.run(root)['new_updates'] == 0
    for file in (native/'states').glob('*.npz'):
        a, aa = n.read_snapshot(file)
        b, bb = n.read_snapshot(root/'states'/file.name)
        assert a['rng'] == b['rng']
        for key in aa:
            np.testing.assert_array_equal(aa[key], bb[key])
    rows = p.seal(root)['records']
    summary = p.aggregate([p.seal(root)], technical=True)
    assert len(rows) == 9
    assert summary['genetic_loss_inputs'] == n.collect(native)['genetic_loss_inputs']
    assert summary['occupancy_inputs'] == n.collect(native)['occupancy_inputs']
    with pytest.raises(ValueError, match='duplicate'):
        p.aggregate([p.seal(root), p.seal(root)], technical=True)
    broken = p.seal(root)
    broken['records'] = broken['records'][:-1]
    with pytest.raises(ValueError):
        p.aggregate([broken], technical=True)
    for mode in ('missing', 'duplicate'):
        broken = copy.deepcopy(p.seal(root))
        arms = broken['records'][0]['arms']
        if mode == 'missing': arms.pop()
        else: arms[-1] = copy.deepcopy(arms[0])
        broken['seal_sha256'] = n.digest(n.canonical({k:v for k,v in broken.items() if k!='seal_sha256'}))
        with pytest.raises(ValueError, match='arm'):
            p.aggregate([broken], technical=True)
    broken = copy.deepcopy(p.seal(root))
    broken['contract']['contract_sha256'] = 'invalid'
    broken['seal_sha256'] = n.digest(n.canonical({k:v for k,v in broken.items() if k!='seal_sha256'}))
    with pytest.raises(ValueError, match='contract'):
        p.aggregate([broken], technical=True)
    file = next((root/'states').glob('*.npz'))
    file.write_bytes(b'broken')
    with pytest.raises((ValueError, OSError)):
        p.seal(root)
