import importlib.util
from pathlib import Path
import math

import numpy as np
import pytest


def api():
    path = Path(__file__).parents[1] / 'scripts/q3_futures_contract_20261014.py'
    assert path.exists(), 'approved Q3 execution contract missing'
    spec = importlib.util.spec_from_file_location('q3_contract_test', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def inventory():
    cases = []
    for block, count in [('causal_main', 31), ('causal_confirmation', 30)]:
        for j in range(32):
            cases.append(dict(key=f'{block}_{j}', block=block, trigger=50 if j<count else None))
    return cases


def records():
    return [dict(key=c['key'], replicate=r, native_I=.5, restored_I=.48,
                 native_survived=True, restored_survived=True,
                 native_event=None, restored_event=None)
            for c in inventory() if c['trigger'] is not None for r in range(64)]


def test_original_slot_denominators_and_fixed_precision():
    result = api().summarize(records(), inventory())
    assert result['means']['all64']['estimate'] == pytest.approx(.02*61/64)
    assert result['means']['causal_main']['estimate'] == pytest.approx(.02*31/32)
    assert result['means']['causal_confirmation']['estimate'] == pytest.approx(.02*30/32)
    assert result['means']['all64']['half_width'] == pytest.approx(.00295014926963976)
    assert result['directional_replication'] == 'positive'


@pytest.mark.parametrize('damage', ['missing', 'duplicate', 'foreign', 'replicate', 'outside', 'nan', 'missing_mean', 'false_survival'])
def test_corruption_is_technical_failure_not_selected_subset(damage):
    rows = records()
    if damage == 'missing': rows.pop()
    elif damage == 'duplicate': rows[-1] = dict(rows[0])
    elif damage == 'foreign': rows[-1]['key'] = 'alien'
    elif damage == 'replicate': rows[-1]['replicate'] = 64
    elif damage == 'outside': rows[-1]['restored_I'] = .1
    elif damage == 'nan': rows[-1]['restored_I'] = math.nan
    elif damage == 'missing_mean': rows[-1]['restored_I'] = None
    elif damage == 'false_survival': rows[-1]['restored_survived'] = False
    with pytest.raises(ValueError): api().summarize(rows, inventory())


def test_single_extinction_invalidates_all_means_without_imputation():
    rows=records();rows[0].update(restored_I=None, restored_survived=False)
    result=api().summarize(rows, inventory())
    assert result['decision']=='not_evaluable'
    assert result['means'] is None
    assert result['survival']['native_only']==1
    assert result['pairs']==3904


def test_direction_is_distinct_from_practical_class_and_both_blocks_required():
    m=api()
    assert m.classify(.001,.009)==dict(direction='positive', practical='operationally_equivalent')
    assert m.classify(0,.01)==dict(direction='unresolved', practical='operationally_equivalent')
    rows=records()
    for row in rows:
        if row['key'].startswith('causal_confirmation'):row['restored_I']=.5
    assert m.summarize(rows,inventory())['directional_replication']=='unresolved'


def test_event_keeps_original_baseline_and_pretrigger_history():
    m=api()
    assert m.event_start([.5]*4+[.4]*20, .5)==4
    assert m.event_start([.4]*19+[None]+[.4]*19, .5) is None
    assert m.event_start([.4]*20+[None]*5, .5)==0
    assert m.event_start([.48]*25, .5) is None


def test_restoration_is_mean_preserving_and_no_clipping():
    m=api(); a=np.full((2,3,2),.5);b=m.restore(a)
    np.testing.assert_array_equal(a.mean(2),b.mean(2))
    np.testing.assert_array_equal(b[:,[0,2]],a[:,[0,2]])
    assert np.all(b[:,1]==[.4375,.5625])
    for values in ([0,0],[1,1],[.4,.5]):
        a[:,1]=values
        with pytest.raises(ValueError):m.restore(a)


def test_budget_reservation_counts_failed_attempts_and_never_overshoots(tmp_path):
    m=api();b=m.Budget(tmp_path/'budget.json', max_calls=10)
    b.reserve(6,'attempt1')
    with pytest.raises(ValueError):b.reserve(5,'attempt2')
    assert b.calls==6
    b.reserve(4,'attempt2')
    with pytest.raises(ValueError):b.reserve(1,'retry')
    with pytest.raises(FileExistsError):m.Budget(tmp_path/'budget.json',max_calls=10)


def test_hash_failure_before_any_source_import(tmp_path):
    p=tmp_path/'bad.zip';p.write_bytes(b'wrong')
    with pytest.raises(ValueError, match='SHA256'):api().checked_bytes(p,'0'*64)
