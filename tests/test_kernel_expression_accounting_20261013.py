import numpy as np
from scripts.kernel_expression_accounting_20261013.audit_kernel_expression import decompose


def test_small_absorbing_model_exact_endpoint_duration_and_last_update():
    native=np.array([[1.,0.],[.2,.8]])
    fixed=np.array([[1.,0.],[.4,.6]])
    p0=np.array([0.,1.]);alive=np.array([0.,1.])
    for prefix,future in [(native,fixed),(fixed,native)]:
        end,duration=decompose(native,fixed,p0,alive,3,prefix,future)
        assert abs(end.sum()-(.8**3-.6**3))<1e-14
        assert abs(duration.sum()-((1+.8+.8**2)-(1+.6+.6**2)))<1e-14
        assert np.all(duration[-1]==0)
        assert np.all(end[:,0]==0)


def test_same_kernel_has_zero_contributions():
    t=np.array([[1.,0.],[.2,.8]]);p=np.array([0.,1.]);r=np.array([0.,1.])
    a,b=decompose(t,t,p,r,4,t,t)
    assert np.array_equal(a,np.zeros((4,2)))
    assert np.array_equal(b,np.zeros((4,2)))


def test_noncommuting_kernels_close_in_both_reference_orders():
    native=np.array([[1.,0.,0.],[.1,.6,.3],[.2,.5,.3]])
    fixed=np.array([[1.,0.,0.],[.4,.2,.4],[.05,.3,.65]])
    assert not np.allclose(native@fixed,fixed@native)
    p=np.array([0.,1.,0.]);r=np.array([0.,1.,1.]);h=7
    endpoint=p@(np.linalg.matrix_power(native,h)-np.linalg.matrix_power(fixed,h))@r
    duration=sum(p@(np.linalg.matrix_power(native,t)-np.linalg.matrix_power(fixed,t))@r for t in range(h))
    contributions=[]
    for prefix,future in [(native,fixed),(fixed,native)]:
        e,d=decompose(native,fixed,p,r,h,prefix,future)
        assert abs(e.sum()-endpoint)<1e-14
        assert abs(d.sum()-duration)<1e-14
        contributions.append(e)
    assert not np.allclose(contributions[0],contributions[1])
