import json
import zipfile
import pytest
from scripts.q3_archive160_20261019 import pack, restore


def test_roundtrip_and_no_replace(tmp_path):
    root=tmp_path/'source';(root/'states').mkdir(parents=True)
    (root/'RUN.json').write_text('{}')
    (root/'states'/'one.npz').write_bytes(b'fixture')
    archive=tmp_path/'a.zip'
    assert pack(root,archive)['bytes']>0
    dest=tmp_path/'destination';restore(archive,dest)
    assert (dest/'states'/'one.npz').read_bytes()==b'fixture'
    with pytest.raises(ValueError):restore(archive,dest)
    with pytest.raises(FileExistsError):pack(root,archive)


def test_reject_member_escape_before_writing(tmp_path):
    archive=tmp_path/'bad.zip'
    with zipfile.ZipFile(archive,'w') as z:
        z.writestr('../escaped','x')
        z.writestr('ARCHIVE_MANIFEST.json',json.dumps({'../escaped':'bad'}))
    with pytest.raises(ValueError):restore(archive,tmp_path/'dest')
    assert not (tmp_path/'dest').exists()
