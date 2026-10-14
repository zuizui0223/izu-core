import itertools
import subprocess
import sys
from pathlib import Path
import numpy as np
import pytest
from audit_channels import construct, recover, factorial


def fixture():
    states = np.array([(a,b,n-a-b) for n in range(9) for a in range(n+1) for b in range(n-a+1)])
    mu = np.r_[0., np.full(len(states)-1, 3.)]
    q = np.tile([.2,.5,.3], (len(states),1)); q[0] = [1.,0.,0.]
    return states, mu, q


def test_channels_recover_with_capped_tail_and_genotype_compositions():
    states, mu, q = fixture()
    result = recover(construct(mu, q, states), states)
    np.testing.assert_allclose(result[0], mu, atol=1e-12, rtol=0)
    np.testing.assert_allclose(result[1], q, atol=1e-12, rtol=0)


def test_arbitrary_stochastic_law_is_not_admitted_as_channel_factorization():
    states, mu, q = fixture()
    t = construct(mu,q,states)
    # Preserve extinction and N1 masses while breaking conditional N2 genotype law.
    cols = np.flatnonzero(states.sum(axis=1)==2)
    t[1,cols[0]] += .001; t[1,cols[1]] -= .001
    with pytest.raises(ValueError, match='row-factorization'):
        recover(t,states)


def test_nonidentifiable_extinction_row_stops():
    states, mu, q = fixture()
    t = construct(mu,q,states); t[1] = t[0]
    with pytest.raises(ValueError, match='unrecoverable'):
        recover(t,states)


def test_nonfinite_outside_identifying_cells_stops():
    states,mu,q=fixture()
    t=construct(mu,q,states);t[1,-1]=np.nan
    with pytest.raises(ValueError,match='nonstochastic'):
        recover(t,states)


def test_interaction_is_not_allocated_to_either_channel():
    x=factorial({'00':0.,'10':2.,'01':3.,'11':9.})
    assert x['interaction']==4 and x['full']==9
    assert x['recruitment_only']==2 and x['recruitment_native_reference']==6


@pytest.mark.parametrize('script', ['audit_channels.py','verify_channels.py'])
def test_incomplete_frozen_manifest_stops_before_inputs(tmp_path,script):
    manifest=tmp_path/'frozen.json';manifest.write_text('{}')
    args=['--input-dir',str(tmp_path/'absent'),'--frozen-manifest',str(manifest)]
    if script=='audit_channels.py':args+=['--out',str(tmp_path/'out')]
    else:args+=['--output-dir',str(tmp_path/'absent'),'--receipt',str(tmp_path/'receipt')]
    run=subprocess.run([sys.executable,str(Path(__file__).with_name(script)),*args],capture_output=True,text=True)
    assert run.returncode!=0 and 'frozen manifest inventory differs' in run.stderr
