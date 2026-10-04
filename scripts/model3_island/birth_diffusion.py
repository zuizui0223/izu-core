"""Conservative no-flux heat PDE on an allele axis, applied to gametes at birth."""
import numpy as np
from scipy.linalg import eigh_tridiagonal


def reflecting_heat_matrix(nodes, diffusion_time):
    x=np.asarray(nodes,dtype=float)
    if (x.ndim!=1 or len(x)<1 or not np.isfinite(x).all() or
        (np.diff(x)<=0).any() or (x<0).any() or (x>1).any() or
        not np.isfinite(diffusion_time) or diffusion_time<0):
        raise ValueError('invalid heat grid or diffusion time')
    if diffusion_time==0:return np.eye(len(x))
    if len(x)<2 or x[0]!=0 or x[-1]!=1:
        raise ValueError('positive heat diffusion requires full [0,1] axis')
    h=np.diff(x)
    volume=np.diff(np.r_[0,(x[:-1]+x[1:])/2,1])
    left=np.r_[0,1/h]/volume
    right=np.r_[1/h,0]/volume
    off=1/(h*np.sqrt(volume[:-1]*volume[1:]))
    eigen,vectors=eigh_tridiagonal(-(left+right),off)
    symmetric=(vectors*np.exp(diffusion_time*eigen))@vectors.T
    p=symmetric*np.sqrt(volume[None,:]/volume[:,None])
    if p.min() < -1e-12 or not np.allclose(p.sum(axis=1),1,atol=1e-10,rtol=0):
        raise ArithmeticError('heat semigroup lost positivity or conservation')
    p=np.maximum(p,0)
    p/=p.sum(axis=1,keepdims=True)
    return p
