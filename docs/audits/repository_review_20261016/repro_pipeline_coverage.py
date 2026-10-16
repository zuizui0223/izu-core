"""Synthetic admission-layer reproduction. Pinned hash check is mocked explicitly;
no assertion is made about the absent original archives or existing scientific results."""
import hashlib, importlib.util, json, tempfile, zipfile
from pathlib import Path
from unittest.mock import patch
import numpy as np
ROOT=Path(__file__).resolve().parents[2]/"work/repository_review_20261016"
def digest_override(expected):
    class D:
        def hexdigest(self): return expected
    return lambda *args,**kwargs:D()
with tempfile.TemporaryDirectory() as temp:
    t=Path(temp)
    source=ROOT/"scripts/verify_existing_response_clocks_independent_20261013.py"
    spec=importlib.util.spec_from_file_location("clock_verify",source)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    archive=t/"raw.zip"
    with zipfile.ZipFile(archive,"w") as z:
        z.writestr("one.json",json.dumps({"rows":[{"selection":[0,0,0],"observed_change":[0,0,0]}]*200}))
    scalar={"first_favorable_window":None,"selection_crossing":None,"actual_crossing":None,"snapshots":{str(i):{"selection_contribution":0,"observed_change":0} for i in [1,20,100,200]}}
    readout=t/"readout.json";readout.write_text(json.dumps({"records":[{"task":{"key":"one"},"A":scalar,"I":scalar}]*320}))
    with patch.object(m.hashlib,"sha256",digest_override("115636a338c847fdf1f80ae9e39cdfc622fcf38c7f70575e37d245bf7c41b098")):
        clock=m.verify(archive,readout)
    kernel_source=ROOT/"scripts/kernel_expression_accounting_20261013/verify_kernel_expression_independent.py"
    fake=t/"scripts/kernel_expression_accounting_20261013";fake.mkdir(parents=True)
    (fake/"extracted").mkdir();(fake/"extracted/READOUT.json").write_text('{"comparisons":[]}')
    f=fake/kernel_source.name;f.write_bytes(kernel_source.read_bytes())
    raw=fake.parent/"four_question_unresolved_20261013/duration_actual_github_38280177062";raw.mkdir(parents=True)
    np.savez(raw/"native_regenerated_kernels_and_state_curves.npz",keys=np.array([],dtype=str),kernels=np.empty((0,1,1)),states=np.zeros((1,3)),probabilities=np.empty((0,1,1)))
    np.savez(fake/"extracted/ALL_STATE_TIME_CONTRIBUTIONS.npz",endpoint=np.array([]),duration=np.array([]))
    with patch.object(hashlib,"sha256",digest_override("d34fc60c389775f88fa8a54051fdfe90a76ef7864b8f5a813b99d5f0b68ca172")):
        exec(compile(f.read_text(),str(f),"exec"),{"__file__":str(f),"__name__":"__main__"})
    kernel=json.loads((fake/"INDEPENDENT_REVIEW.json").read_text())
    print(json.dumps({"fixture_only_hash_admission_mocked":True,"clock_unique_keys":1,"clock":clock,"kernel_empty_comparisons":True,"kernel":{k:kernel[k] for k in ["status","pairs","state_time_checks","switch_time_checks"]}},indent=2))
