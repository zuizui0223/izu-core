"""Synthetic coverage tests; only the unavailable original archive hash is mocked."""
import copy
import json
import zipfile
import pytest
from scripts import verify_existing_response_clocks_independent_20261013 as verifier

@pytest.fixture
def inputs(tmp_path, monkeypatch):
    archive=tmp_path/'original.zip'
    names=[f'case{i}_evolving' for i in range(320)]
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
        raw=json.dumps({'rows':[{'selection':[0,0,0],'observed_change':[0,0,0]}]*200})
        for name in names:z.writestr(name+'.json',raw)
    original_sha=verifier.hashlib.sha256
    raw_archive=archive.read_bytes()
    class Pinned:
        def hexdigest(self):return '115636a338c847fdf1f80ae9e39cdfc622fcf38c7f70575e37d245bf7c41b098'
    monkeypatch.setattr(verifier.hashlib,'sha256',lambda data: Pinned() if data==raw_archive else original_sha(data))
    scalar={'first_favorable_window':None,'selection_crossing':None,'actual_crossing':None,'snapshots':{str(i):{'selection_contribution':0,'observed_change':0} for i in [1,20,100,200]}}
    records=[{'task':{'key':name},'A':copy.deepcopy(scalar),'I':copy.deepcopy(scalar)} for name in names]
    return archive,tmp_path/'readout.json',records

def test_complete_original_inventory(inputs):
    archive,path,rows=inputs;path.write_text(json.dumps({'records':rows}))
    result=verifier.verify(archive,path)
    assert result['cases']==320 and result['checks']==7040

@pytest.mark.parametrize('mutation',['duplicate','missing','foreign','extra','empty'])
def test_incomplete_or_duplicate_readout_is_rejected(inputs,mutation):
    archive,path,rows=inputs
    if mutation=='duplicate':rows[-1]=copy.deepcopy(rows[0])
    elif mutation=='missing':rows.pop()
    elif mutation=='foreign':rows[-1]['task']['key']='foreign'
    elif mutation=='extra':rows.append(copy.deepcopy(rows[0]))
    else:rows=[]
    path.write_text(json.dumps({'records':rows}))
    with pytest.raises(ValueError,match='inventory'):verifier.verify(archive,path)
