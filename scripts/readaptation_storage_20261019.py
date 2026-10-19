"""Publish one compressed future without overwriting an existing checkpoint."""
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

import numpy as np


def save_future(path,key,record):
    path=Path(path)
    if path.exists():
        raise FileExistsError(path)
    arrays={}; metadata={}
    for name,value in record.items():
        if not isinstance(name,str) or not re.fullmatch('[a-z][a-z0-9_]*',name):
            raise ValueError('invalid record field')
        if isinstance(value,np.ndarray):
            if value.dtype.kind not in 'biuf':
                raise ValueError('only numeric non-pickle arrays may be stored')
            arrays[name]=value
        else:
            metadata[name]=value
    header=dict(format='readaptation_npz_v1',key=list(key),metadata=metadata,
                arrays=sorted(arrays))
    arrays['__metadata__']=np.frombuffer(json.dumps(header,sort_keys=True,
        separators=(',',':'),allow_nan=False).encode('utf8'),dtype=np.uint8)
    temp=None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent,prefix='.future-',suffix='.tmp',delete=False) as f:
            temp=Path(f.name)
            np.savez_compressed(f,**arrays)
            f.flush(); os.fsync(f.fileno())
        digest=hashlib.sha256(temp.read_bytes()).hexdigest()
        size=temp.stat().st_size
        # Same-directory hard link publishes the completed file atomically and
        # fails if another writer already owns the destination. Never replace.
        os.link(temp,path)
        return dict(key=list(key),file=path.name,sha256=digest,bytes=size)
    finally:
        if temp is not None and temp.exists():
            temp.unlink()
