"""User-authorized long validation from the active seventh-step checkpoint.

Starts after that existing producer completes; no duplicate step7. Local checks
are retained, but this run is not yet admitted for ecological interpretation.
"""
from pathlib import Path
from itertools import combinations_with_replacement
import ctypes
import hashlib
import json
import time
import zipfile
import numpy as np
from scripts.model3_restart_checkpoint import save_checkpoint
from scripts.model3_batched_weight_integration import bounded_step
from scripts.model3_birth_marginal_reference import exact_next_marginals
from scripts.run_model3_full_mutation import config, exposure, atomic_json
from scripts.model3_weighted_slab_core import exact_core
import scripts.model3_weighted_block_read as reader
import scripts.model3_batched_weight_core as projector


def producer_alive(pid):
    kernel=ctypes.WinDLL('kernel32',use_last_error=True)
    kernel.OpenProcess.restype=ctypes.c_void_p
    kernel.OpenProcess.argtypes=[ctypes.c_ulong,ctypes.c_int,ctypes.c_ulong]
    kernel.GetExitCodeProcess.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_ulong)]
    kernel.CloseHandle.argtypes=[ctypes.c_void_p]
    handle=kernel.OpenProcess(0x1000,False,pid)
    if not handle:return False
    try:
        code=ctypes.c_ulong()
        return bool(kernel.GetExitCodeProcess(handle,ctypes.byref(code))) and code.value==259
    finally:kernel.CloseHandle(handle)


def main():
    reader.exact_core=exact_core;projector.exact_core=exact_core
    root=Path.cwd();source=root/'slab_weight_seventh65_recovery1'
    out=root/'highgrid_long_from7_20261005'
    out.mkdir(exist_ok=False)
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    files=list((root/'scripts').glob('*.py'))+list((root/'scripts/model3_island').glob('*.py'))+[root/'data/design/model3_ch2_bridge_20260927.json']
    manifest={p.relative_to(root).as_posix():sha(p) for p in files}
    atomic_json(out/'sources.json',manifest)
    with zipfile.ZipFile(out/'sources.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in files:z.write(p,p.relative_to(root).as_posix())
    source_hash=sha(out/'sources.json')
    case='assurance_cost_near_jump'
    status=dict(case=case,target_period=1000,status='waiting_for_existing_step7',producer_pid=20152,records=[],interpretation='unadmitted long validation')
    atomic_json(out/'progress.json',status)
    try:
        while not (source/'summary.json').exists():
            if not producer_alive(20152):raise RuntimeError('step7 producer stopped without completion receipt')
            time.sleep(10)
        receipt=json.loads((source/'summary.json').read_text(encoding='utf-8'))
        if receipt['status']!='passed_marginals' or sha(source/'state.npz')!=receipt['npz_sha256']:
            raise ValueError('step7 not verified')
        previous=json.loads((source/'sources.json').read_text(encoding='utf-8'))
        with zipfile.ZipFile(source/'sources.zip') as z:
            for name,digest in previous.items():
                if sha(root/name)!=digest or hashlib.sha256(z.read(name)).hexdigest()!=digest:
                    raise ValueError('producer source changed')
        for name,digest in manifest.items():
            if sha(root/name)!=digest:raise ValueError('long runner source changed')
        with np.load(source/'state.npz',allow_pickle=False) as z:
            state=z['core'],tuple(z[f'factor{k}'] for k in range(3))
        save_checkpoint(out/'period0007',state,period=7,case=case,source_hash=source_hash)
        axis=np.linspace(0,1,65)
        means=np.array([(a+b)/2 for a,b in combinations_with_replacement(axis,2)])
        cfg=config('assurance_cost',.01);visitors=exposure(76001,'near').visitors
        status.update(status='running',completed_period=7)
        atomic_json(out/'progress.json',status)
        for t in range(7,1000):
            start=time.monotonic()
            expected=exact_next_marginals(state,(axis,)*3,visitors[t],cfg)
            candidate,certificates=bounded_step(state,(axis,)*3,visitors[t],cfg,budget=16_000_000)
            core,fs=candidate;sums=[f.sum(axis=0) for f in fs];actual=[]
            for k in range(3):
                other=[j for j in range(3) if j!=k]
                vector=np.einsum('abc,'+','.join('abc'[j] for j in other)+'->'+'abc'[k],core,*[sums[j] for j in other],optimize=True)
                actual.append(fs[k]@vector)
            masses=np.array([a.sum() for a in actual])
            if not np.isfinite(masses).all() or (masses<=0).any():raise ArithmeticError('invalid mass; not classified as extinction')
            l1=max(float(abs(a-b).sum()/b.sum()) for a,b in zip(actual,expected))
            gap=max(float(abs(a@means/a.sum()-b@means/b.sum())) for a,b in zip(actual,expected))
            passed=bool(np.isfinite([l1,gap]).all() and l1<=1e-5 and gap<=1e-6)
            row=dict(period=t+1,relative_marginal_l1=l1,trait_gap=gap,mass=masses.tolist(),ranks=list(core.shape),seconds=time.monotonic()-start,passed=passed,certificates=certificates)
            atomic_json(out/f'diagnostic{t+1:04d}.json',row)
            if not passed:raise ArithmeticError('local comparison failed')
            save_checkpoint(out/f'period{t+1:04d}',candidate,period=t+1,case=case,source_hash=source_hash)
            state=candidate;status['records'].append({k:v for k,v in row.items() if k!='certificates'})
            status['completed_period']=t+1;atomic_json(out/'progress.json',status)
            print(t+1,l1,gap,row['seconds'],flush=True)
        status['status']='completed_local_checks_only'
    except Exception as exc:
        status.update(status='stopped',error=f'{type(exc).__name__}: {exc}')
        atomic_json(out/'progress.json',status)
        raise
    atomic_json(out/'progress.json',status)


if __name__=='__main__':main()
