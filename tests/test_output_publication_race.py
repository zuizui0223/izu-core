import sys
from pathlib import Path
import pytest
import scripts.audit_chapter2_initial_clock_identifiability_20261013 as aggregate
import scripts.audit_chapter2_initial_clock_raw_20261013 as raw

def test_aggregate_preserves_a_result_created_during_computation(tmp_path,monkeypatch):
    out=tmp_path/'audit.json';original=aggregate.analyze
    def concurrent_publication(*args):
        out.write_text('first validated writer',encoding='utf-8')
        return original(*args)
    monkeypatch.setattr(aggregate,'analyze',concurrent_publication)
    monkeypatch.setattr(sys,'argv',['audit','--input',str(Path('data/results/ecological_order_boundary_20261013.json')),'--out',str(out)])
    with pytest.raises(FileExistsError):aggregate.main()
    assert out.read_text()=='first validated writer'

def test_raw_reader_preserves_a_result_created_during_long_validation(tmp_path,monkeypatch):
    out=tmp_path/'raw.json'
    def concurrent_publication(*args):
        out.write_text('first validated writer',encoding='utf-8')
        return {'status':'technical publication-test only'}
    # The race is at output publication, so the expensive byte audit is isolated;
    # actual filesystem writes remain real and no source data is changed.
    monkeypatch.setattr(raw,'audit',concurrent_publication)
    monkeypatch.setattr(sys,'argv',['audit','--outer','unused.zip','--compact','unused.json','--out',str(out)])
    with pytest.raises(FileExistsError):raw.main()
    assert out.read_text()=='first validated writer'
