import json
from pathlib import Path
import pytest
from scripts.run_model3_ch2_bridge import run_campaign, sources

def tiny():
    d=json.loads(Path('data/design/model3_ch2_bridge_candidate_20260927.json').read_text())
    d.update(status='frozen',history_seeds=[74909],demographic_seeds=[101],starts=[.5],arms=['near','far'],cases=2)
    d['base_config']['years']=2;d['years']=2;d['source_hashes']=sources()
    return d

def test_resume_verifies_and_never_reruns_complete_cases(tmp_path):
    d=tiny();a=run_campaign(d,tmp_path/'run');assert a['complete'] and a['executed']==2
    b=run_campaign(d,tmp_path/'run');assert b['executed']==0
    f=next((tmp_path/'run').glob('*/arrays.npz'));f.write_bytes(b'corrupt')
    with pytest.raises(ValueError):run_campaign(d,tmp_path/'run')

def test_source_and_unfrozen_rejected(tmp_path):
    d=tiny();d['status']='candidate'
    with pytest.raises(ValueError):run_campaign(d,tmp_path/'run')
    d=tiny();d['source_hashes']={}
    with pytest.raises(ValueError):run_campaign(d,tmp_path/'run')

def test_budget_stop_preserves_attempts(tmp_path):
    d=tiny();d['resource_limits']['runtime_seconds']=1e-12
    out=tmp_path/'run'
    a=run_campaign(d,out);assert not a['complete'] and a['stop_reason']=='runtime_budget'
    b=run_campaign(d,out);assert not b['complete']
    record=json.loads(next(out.glob('*/interruption.json')).read_text())
    assert len(record['attempts'])==2
    assert record['elapsed_seconds']==sum(x['elapsed_seconds'] for x in record['attempts'])

def test_unclosed_attempt_is_fail_closed(tmp_path):
    d=tiny();out=tmp_path/'run';run_campaign(d,out)
    p=tmp_path/'run.attempts.json';book=json.loads(p.read_text());book['attempts'][-1]['closed']=False;p.write_text(json.dumps(book))
    with pytest.raises(ValueError,match='unclosed attempt'):run_campaign(d,out)

def test_unexpected_exception_is_charged(tmp_path,monkeypatch):
    import scripts.run_model3_ch2_bridge as mod
    d=tiny();out=tmp_path/'run'
    def fail(*a,**kw):raise RuntimeError('fixture interruption')
    monkeypatch.setattr(mod,'simulate',fail)
    with pytest.raises(RuntimeError):run_campaign(d,out)
    book=json.loads((tmp_path/'run.attempts.json').read_text())
    assert book['attempts'][-1]['closed'] and book['attempts'][-1]['elapsed_seconds']>0

def test_serialization_limit_is_not_success(tmp_path):
    d=tiny();d['resource_limits']['output_mb']=.045
    r=run_campaign(d,tmp_path/'run')
    assert not r['complete'] and r['stop_reason']=='output_budget'

def test_missing_attempt_ledger_cannot_reset_budget(tmp_path):
    d=tiny();out=tmp_path/'run';run_campaign(d,out)
    (tmp_path/'run.attempts.json').unlink()
    with pytest.raises(ValueError,match='missing attempt ledger'):run_campaign(d,out)
