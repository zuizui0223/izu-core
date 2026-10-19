"""Immutable single-future files, with an independent non-pickle reader."""
import hashlib
import zipfile

import numpy as np
import pytest

from scripts.readaptation_storage_20261019 import save_future
from scripts.audit_readaptation_raw_20261019 import load_future


KEY=[0,0,'fixed',0,0,.5,0]


def test_byte_roundtrip_and_no_overwrite(tmp_path):
    path=tmp_path/'future.npz'
    raw={'state':np.array([[.2,np.nan]],dtype=np.float64),'count':2,'assays':{'80':None}}
    receipt=save_future(path,KEY,raw)
    assert receipt['sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
    assert receipt['bytes']==path.stat().st_size
    got=load_future(path,receipt['sha256'],KEY)
    assert got['state'].dtype==raw['state'].dtype
    assert got['state'].tobytes()==raw['state'].tobytes()
    assert got['assays']==raw['assays'] and got['count']==2
    with pytest.raises(FileExistsError):
        save_future(path,KEY,raw)
    assert receipt['sha256']==hashlib.sha256(path.read_bytes()).hexdigest()


def test_hash_and_key_binding(tmp_path):
    path=tmp_path/'future.npz'
    receipt=save_future(path,KEY,{'a':np.zeros(2)})
    with pytest.raises(ValueError,match='hash'):
        load_future(path,'0'*64,KEY)
    with pytest.raises(ValueError,match='key'):
        load_future(path,receipt['sha256'],KEY[:-1]+[1])


def test_no_pickle_and_no_partial_publication(tmp_path):
    path=tmp_path/'future.npz'
    with pytest.raises(ValueError):
        save_future(path,KEY,{'bad':np.array([object()],dtype=object)})
    assert not path.exists()
    with pytest.raises(ValueError):
        save_future(path,KEY,{'bad':float('nan')})
    assert not path.exists()


def test_extra_archive_member_rejected_even_with_updated_hash(tmp_path):
    path=tmp_path/'future.npz'
    save_future(path,KEY,{'a':np.zeros(2)})
    with zipfile.ZipFile(path,'a') as archive:
        archive.writestr('unlisted.npy',b'bad')
    with pytest.raises(ValueError,match='inventory'):
        load_future(path,hashlib.sha256(path.read_bytes()).hexdigest(),KEY)
