"""Admission regression tests; tiny fixtures, no biological simulation."""
import hashlib
import json
import shutil
import numpy as np
import pytest
from scripts.summarize_model3_ch2_bridge_prospective import summarize, PAIR_ARMS
from scripts.model3_island.design import digest

@pytest.fixture
def campaign(tmp_path):
    arms = [arm for pair in PAIR_ARMS.values() for arm in pair]
    design = dict(status="frozen", cases=32, history_seeds=[1,2], starts=[.2,.8], demographic_seeds=[3], arms=arms, thresholds=[0])
    for arm in arms:
        for history in design["history_seeds"]:
            for start in design["starts"]:
                cid=f"{arm}-s{int(round(start*10))}-h{history}-d3"
                folder=tmp_path/cid
                folder.mkdir()
                case=dict(id=cid,cell=dict(founders=dict(means=[.5,start,.5])),history_seed=history,demographic_seed=3,manifest_hash=digest(design))
                (folder/"input.json").write_text(json.dumps(case))
                np.savez(folder/"arrays.npz",population=[48,48],density_mass=[48.,48.],trait_mean=[[.5,start,.5],[.5,start+.1,.5]],density_traits=[[.5,start,.5],[.5,start+.1,.5]],visitor_count=[4,4])
                (folder/"receipt.json").write_text(json.dumps(dict(status="complete",case_hash=digest(case),manifest_hash=digest(design),arrays_sha256=hashlib.sha256((folder/"arrays.npz").read_bytes()).hexdigest())))
    return design,tmp_path

def test_complete_domain(campaign):
    design,root=campaign
    result=summarize(design,root)
    assert result["cases_checked"]==32
    assert result["reports"][0]["pair_occupancy"]==1

@pytest.mark.parametrize("fault",["duplicate","missing","foreign","wrong_manifest"])
def test_bad_domain_rejected(campaign,fault):
    design,root=campaign
    source=root/"near-s2-h1-d3"
    if fault=="duplicate":
        shutil.rmtree(root/"near-s8-h1-d3")
        shutil.copytree(source,root/"duplicate-folder")
    elif fault=="missing":
        shutil.rmtree(root/"near-s8-h1-d3")
    else:
        case=json.loads((source/"input.json").read_text())
        if fault=="foreign":case["history_seed"]=99
        else:case["manifest_hash"]="other-design"
        (source/"input.json").write_text(json.dumps(case))
        receipt=json.loads((source/"receipt.json").read_text())
        receipt["case_hash"]=digest(case)
        (source/"receipt.json").write_text(json.dumps(receipt))
    with pytest.raises(ValueError):summarize(design,root)


def test_recorded_extinction_is_not_missing_case(campaign):
    design,root=campaign
    folder=root/"near-s8-h1-d3"
    path=folder/"arrays.npz"
    with np.load(path) as source:
        arrays={key:source[key].copy() for key in source.files}
    arrays["population"][-1]=0
    arrays["trait_mean"][-1]=np.nan
    np.savez(path,**arrays)
    receipt=json.loads((folder/"receipt.json").read_text())
    receipt["arrays_sha256"]=hashlib.sha256(path.read_bytes()).hexdigest()
    (folder/"receipt.json").write_text(json.dumps(receipt))
    result=summarize(design,root)
    assert result["cases_checked"]==32
    assert result["reports"][0]["pair_occupancy"]==.75
