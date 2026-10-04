import numpy as np
from scripts.model3_island.birth_diffusion import reflecting_heat_matrix


def test_finite_volume_heat_preserves_mass_and_constant_density():
    x=np.linspace(0,1,41)
    p=reflecting_heat_matrix(x,.0000125)
    volume=np.r_[.5,np.ones(39),.5]/40
    assert p.min()>=0
    np.testing.assert_allclose(p.sum(axis=1),1,atol=1e-12)
    np.testing.assert_allclose(volume@p,volume,atol=1e-12)
    assert p[20,19]>.001


def test_heat_pde_cosine_converges_and_time_semigroup():
    errors=[]
    for n in [21,41,81]:
        x=np.linspace(0,1,n);tau=.001
        p=reflecting_heat_matrix(x,tau)
        f=np.cos(2*np.pi*x)
        errors.append(np.max(np.abs(p@f-np.exp(-4*np.pi**2*tau)*f)))
        np.testing.assert_allclose(p@p,reflecting_heat_matrix(x,2*tau),atol=2e-12)
    assert errors[2]<errors[1]<errors[0]
    assert errors[0]/errors[1]>3.5
