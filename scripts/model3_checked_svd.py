"""Alternate LAPACK driver on nonconvergence, with explicit fallback checks."""
import numpy as np
import scipy.linalg


def checked_svd(matrix):
    a=np.asarray(matrix,dtype=float)
    if a.ndim!=2 or not a.size or not np.isfinite(a).all():raise ValueError('finite nonempty matrix required')
    try:
        u,s,v=np.linalg.svd(a,full_matrices=False)
        return u,s,v,dict(driver='numpy_default',fallback=False)
    except np.linalg.LinAlgError:
        u,s,v=scipy.linalg.svd(a,full_matrices=False,lapack_driver='gesvd',check_finite=True)
    norm=float(np.linalg.norm(a));error=float(np.linalg.norm((u*s)@v-a))
    relative=error/max(norm,np.finfo(float).tiny)
    orth=max(float(np.linalg.norm(u.T@u-np.eye(len(s)))),float(np.linalg.norm(v@v.T-np.eye(len(s)))))
    if not np.isfinite([relative,orth]).all() or relative>1e-10 or orth>1e-10 or np.any(s<0) or np.any(np.diff(s)>0):
        raise ArithmeticError('fallback SVD failed reconstruction or orthogonality check')
    return u,s,v,dict(driver='gesvd',fallback=True,relative_residual=relative,orthogonality_residual=orth,scope='numerical factorization checks; not an ecological tolerance change')
