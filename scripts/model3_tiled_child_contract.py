"""Exact child-core contraction with bounded binary output tiles."""
from math import prod
import numpy as np


def tiled_child_contract(dc, rc, transforms, *, budget):
    if not isinstance(budget, int) or budget < 1:
        raise ValueError('positive integer budget required')
    arrays=[np.asarray(dc),np.asarray(rc),*[np.asarray(t) for t in transforms]]
    if len(arrays)!=5 or any(a.ndim!=3 for a in arrays):
        raise ValueError('two cores and three three-dimensional transforms required')
    if any(not np.isfinite(a).all() for a in arrays):
        raise ValueError('finite arrays required')
    for k,t in enumerate(arrays[2:]):
        if t.shape[1:]!=(arrays[0].shape[k],arrays[1].shape[k]):
            raise ValueError('parent rank mismatch')
    shape=tuple(t.shape[0] for t in arrays[2:])
    if prod(shape)>budget:raise MemoryError('output exceeds budget')
    result=np.empty(shape,dtype=np.result_type(*arrays));tiles=0;peak=0
    equation='abc,def,iad,jbe,kcf->ijk'
    def assemble(bounds):
        nonlocal tiles,peak
        args=arrays[:2]+[t[s:e] for t,(s,e) in zip(arrays[2:],bounds)]
        path,_=np.einsum_path(equation,*args,optimize=('greedy',budget))
        labels=[set(s) for s in equation.split('->')[0].split(',')]
        dims={s:n for lab,a in zip(['abc','def','iad','jbe','kcf'],args) for s,n in zip(lab,a.shape)}
        sizes=[];valid=all(len(p)==2 for p in path[1:])
        for indices in path[1:]:
            selected=set().union(*(labels[i] for i in indices))
            remaining=[s for i,s in enumerate(labels) if i not in indices]
            retained=selected & set().union(set('ijk'),*remaining)
            sizes.append(prod(dims[s] for s in retained));labels=remaining+[retained]
        valid=valid and max(sizes,default=0)<=budget
        if valid:
            result[tuple(slice(s,e) for s,e in bounds)]=np.einsum(equation,*args,optimize=path)
            tiles+=1;peak=max(peak,max(sizes,default=0));return
        lengths=[e-s for s,e in bounds];axis=int(np.argmax(lengths))
        if lengths[axis]<=1:raise MemoryError('no bounded binary scalar tile contraction')
        start,end=bounds[axis];middle=(start+end)//2
        for pair in [(start,middle),(middle,end)]:
            child=list(bounds);child[axis]=pair;assemble(child)
    assemble([(0,n) for n in shape])
    return result,dict(tiles=tiles,max_intermediate_values=peak,output_values=result.size,
        scope='exact tiled algebra; floating point roundoff not bounded')
