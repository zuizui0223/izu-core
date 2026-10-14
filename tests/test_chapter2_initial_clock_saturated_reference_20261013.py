"""Guard saturated known-cell reference against leakage and missing outcomes."""
import copy
import json
from pathlib import Path
import pytest

from scripts.audit_chapter2_initial_clock_saturated_reference_20261013 import run,lookup


def source_if_available():
    # Published source files remain base PR #491, not always materialized in
    # isolated tests; the source workflow runs this test with real files.
    compact=Path('data/results/ecological_order_boundary_20261013.json')
    paired=Path('data/results/chapter2_initial_clock_paired_events_20261013.json')
    if not compact.is_file() or not paired.is_file():
        pytest.skip('Pinned PR491 raw summary and PR494 paired file not mounted')
    return json.loads(compact.read_text()),json.loads(paired.read_text())


def test_full_saturated_six_class_folds():
    summary,paired=source_if_available()
    result=run(summary,paired)
    assert result['paired_clusters']==256
    assert result['source_profiles']==18
    assert len(result['scores'])==4
    v=result['scores'][1]
    assert v['smoothing']==0.5
    assert v['n']==2304
    assert v['correct']==1088
    assert abs(v['log_loss']-1.1399286597052283)<1e-10
    assert abs(v['brier']-0.6207427493431876)<1e-10
    assert abs(v['argmax_accuracy']-1088/2304)<1e-12


def test_reject_corrupted_or_missing_paired_originals():
    summary,paired=source_if_available()
    with pytest.raises(ValueError,match='Positive'):
        lookup(summary,paired,0)
    corrupted=copy.deepcopy(paired)
    corrupted['data'][0]['sequence']='NNNNNNNNN'
    with pytest.raises(ValueError,match='counts'):
        lookup(summary,corrupted)
    corrupted=copy.deepcopy(paired)
    corrupted['data'].pop()
    with pytest.raises(ValueError,match='cardinality'):
        lookup(summary,corrupted)
