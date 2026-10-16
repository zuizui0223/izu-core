import sys,tempfile
from pathlib import Path
from dataclasses import dataclass
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"work/repository_review_20261016"))
from scripts import chapter2_timed_self_viability_future as m
from scripts.compare_model3_bridge_clean_rerun import _maxdiff
@dataclass
class Task:
    value:int=1
def fake_future(task,eight,d,bio,K,B,gate,visitor,budget):
    s=1.0 if gate in ("baseline","self_half_late") else .5
    if visitor=="near" and gate=="self_half_late":s=99.0
    return dict(arm=f"K{K}_B{B}",K=K,B=B,gate=gate,visitor=visitor,budget=budget,t0_population=1,t0=dict(selfed_viable=s,outcrossed_viable=2.,exported_pollen=3.))
with tempfile.TemporaryDirectory() as tmp,patch.object(m,"case_key",return_value="synthetic"),patch.object(m,"restore_prehistory",return_value=(None,"digest")),patch.object(m,"selected_eight",return_value=None),patch.object(m,"state_fingerprint",return_value="fp"),patch.object(m,"source_hashes",return_value={}),patch.object(m,"one_future",side_effect=fake_future):
    m.one_source(Path(tmp),Path(tmp),Task(),{"postshock":{"budgets":[.5,1,2,3,4,5,8]}},{},{"protocol_sha256":"p"})
    print("TIMED_NEAR_CORRUPTION_ACCEPTED")
print("NAN_COMPARISON",_maxdiff({"mean":float("nan")},{"mean":1.0}))
