import numpy as np

from scripts.audit_readaptation_raw_20261019 import support_diagnostics


def fields():
    return dict(population=np.ones(81,dtype=int),allele_min=np.full((81,3),.5),
                allele_max=np.full((81,3),.5))


def test_strict_and_tolerant_targets_are_not_conflated():
    result=support_diagnostics(fields(),dict(I=.51,A=.49))
    assert [r['epsilon'] for r in result['rows']]==[0,.005,.01,.02,.05]
    assert result['rows'][0]['first_I_exclusion']==0
    assert result['rows'][0]['first_A_exclusion']==0
    assert result['rows'][2]['final_I_support'] is True
    assert result['rows'][2]['final_A_support'] is True
    assert result['rows'][2]['first_I_exclusion'] is None
    assert result['targets']==dict(I=.51,A=.49)


def test_extinction_does_not_become_genetic_exclusion():
    d=fields(); d['population'][4:]=0
    d['allele_min'][4:]=np.nan; d['allele_max'][4:]=np.nan
    result=support_diagnostics(d,dict(I=.5,A=.5))
    assert result['first_extinction']==4
    for row in result['rows']:
        assert row['first_I_exclusion'] is None
        assert row['final_I_support'] is None
        assert row['final_A_support'] is None


def test_equal_endpoints_retain_different_loss_times():
    results=[]
    for t in (7,19):
        d=fields(); d['allele_max'][t:,1]=.4
        results.append(support_diagnostics(d,dict(I=.5,A=.5)))
    assert [r['rows'][0]['first_I_exclusion'] for r in results]==[7,19]
    assert all(r['rows'][0]['final_I_support'] is False for r in results)
