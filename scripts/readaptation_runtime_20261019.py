"""Single-writer checkpoint primitives; no production dispatch or batch runner.

The caller must admit sources/contract, count existing output bytes at startup,
and update that counter after each publication. This module never kills processes.
"""
import hashlib
from pathlib import Path
import shutil

import psutil

from scripts.audit_readaptation_raw_20261019 import load_future,audit_identity,audit_future,require
from scripts.readaptation_storage_20261019 import save_future


GiB=2**30
MAX_FUTURE_BYTES=16*2**20


class ResourceStop(RuntimeError):
    """Leave all allocations intact; resume later using existing checkpoints."""


def measure_resources(directory):
    return dict(available_memory=int(psutil.virtual_memory().available),
                free_disk=int(shutil.disk_usage(directory).free))


def resource_gate(directory,used_bytes,*,reserve_bytes=MAX_FUTURE_BYTES):
    require(type(used_bytes) is int and used_bytes>=0 and
            type(reserve_bytes) is int and reserve_bytes>=0,'invalid byte accounting')
    measured=measure_resources(directory)
    if measured['available_memory']<GiB:
        raise ResourceStop('available physical memory below 1 GiB')
    if measured['free_disk']<10*GiB:
        raise ResourceStop('disk free space below 10 GiB')
    if used_bytes+reserve_bytes>8*GiB:
        raise ResourceStop('output budget would exceed 8 GiB')
    return measured


def complete_future(path,key,contract,base_config,cohort_sha256,used_bytes,produce,*,receipt=None):
    """Admit/reuse a checkpoint, or publish one new audited trajectory.

    `produce` is called only for a missing, previously unreceipted task. The
    proposal remains unauthorized for production; this primitive is tested on
    synthetic fixtures only. A later dispatch layer must enforce that gate.
    """
    path=Path(path)
    exists=path.exists()
    if receipt is not None and not exists:
        raise ValueError('receipted checkpoint is missing; recover it before resuming')
    require(not path.is_symlink(),'checkpoint must not be a symlink')
    resource_gate(path.parent,used_bytes,reserve_bytes=0 if exists else MAX_FUTURE_BYTES)
    if exists:
        require(path.is_file() and path.stat().st_size<=MAX_FUTURE_BYTES,'checkpoint file size/type')
        observed=dict(key=list(key),file=path.name,
                      sha256=hashlib.sha256(path.read_bytes()).hexdigest(),bytes=path.stat().st_size)
        if receipt is not None:
            require(receipt==observed,'checkpoint receipt mismatch')
        raw=load_future(path,observed['sha256'],key)
        audit_identity(raw,key,contract,base_config,cohort_sha256)
        summary=audit_future(raw)
        return dict(state='resumed' if receipt is not None else 'recovered',
                    receipt=observed,added_bytes=0,summary=summary)
    raw=produce()
    audit_identity(raw,key,contract,base_config,cohort_sha256)
    audit_future(raw)
    resource_gate(path.parent,used_bytes)
    saved=save_future(path,key,raw)
    del raw
    # Read the published bytes rather than treating in-memory validation as I/O evidence.
    loaded=load_future(path,saved['sha256'],key)
    audit_identity(loaded,key,contract,base_config,cohort_sha256)
    summary=audit_future(loaded)
    return dict(state='created',receipt=saved,added_bytes=saved['bytes'],summary=summary)
