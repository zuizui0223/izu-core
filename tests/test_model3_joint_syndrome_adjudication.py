import json
import hashlib
from pathlib import Path
import pytest
from scripts import adjudicate_model3_joint_syndrome as module
from scripts.run_model3_joint_syndrome_finite_followup import _summarize_start

@pytest.fixture(autouse=True)
def reviewed_input_manifest(tmp_path,monkeypatch):
    p=tmp_path/"provenance.json"
    p.write_text(json.dumps({"inputs":[]}))
    monkeypatch.setattr(module,"PROVENANCE",p)

@pytest.fixture
def complete_response(tmp_path,monkeypatch):
    s=json.loads(module.SELECTION.read_text())
    s["full_G_beta_response"]["frozen_gate_pass_cells"]=48
    p=tmp_path/"selection.json";p.write_text(json.dumps(s))
    monkeypatch.setattr(module,"SELECTION",p)

def _write(tmp_path, setting, *, syndrome=0., outcross=0., **unused):
    design=json.loads(module.FINITE_DESIGN.read_text())
    bridge=json.loads((module.ROOT/design["source_bridge"]).read_text())
    records=[]
    for start in design["initial_states"]:
        histories=[]
        for idx,seed in enumerate(bridge["history_seeds"]):
            cls="syndrome" if idx<round(128*syndrome) else ("outcross" if idx<round(128*(syndrome+outcross)) else "intermediate")
            di,da={"syndrome":(-.125,.125),"outcross":(.125,-.125),"intermediate":(0.,0.)}[cls]
            histories.append(dict(history_seed=seed,eligible=True,far_minus_near_investment=di,far_minus_near_assurance=da,**{"class":cls},per_repeat=[
                dict(demographic_seed=ds,paired_occupied=True,near_investment=.5,near_assurance=.5,far_investment=.5+di,far_assurance=.5+da) for ds in design["demographic_seeds"]]))
        records.append(dict(initial_state=start,histories=histories))
    summaries={r["initial_state"]["id"]:_summarize_start(r["histories"],design["branching"]["split_halves"]) for r in records}
    branched=any(x["history_branching"] for x in summaries.values())
    p=tmp_path/f"{setting}.json"
    p.write_text(json.dumps(dict(status="finite_joint_syndrome_followup_complete",setting=setting,cases=3072,records=records,terminal_occupancy_fraction_all_trajectories=1.,
        summary_by_initial_state=summaries,any_history_branching=branched,any_reproducible_history_branching=branched)))
    m=json.loads(module.PROVENANCE.read_text())
    m["inputs"].append({"setting":setting,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()})
    module.PROVENANCE.write_text(json.dumps(m))
    return str(p)

def test_adjudication_requires_realized_endpoint_for_mechanistic_promotion(tmp_path,complete_response):
    paths=[_write(tmp_path,s,syndrome=.2 if s=="pollen_discount" else 0) for s in ("delayed_control","prior_selfing","pollen_discount","assurance_cost")]
    assert module.adjudicate(paths)["overall_promotion"]=="mechanistic_core"

def test_reproducible_branching_outranks_mechanistic_core(tmp_path,complete_response):
    paths=[_write(tmp_path,s,syndrome=.2 if s=="prior_selfing" else 0,outcross=.2 if s=="prior_selfing" else 0) for s in ("delayed_control","prior_selfing","pollen_discount","assurance_cost")]
    assert module.adjudicate(paths)["overall_promotion"]=="repeatability_core_or_next_paper"

def test_frozen_incomplete_response_does_not_promote(tmp_path):
    paths=[_write(tmp_path,s,syndrome=.2) for s in ("delayed_control","prior_selfing","pollen_discount","assurance_cost")]
    r=module.adjudicate(paths)
    assert r["overall_promotion"]=="si_only"
    assert r["response_gate_all_cells_pass"] is False

@pytest.mark.parametrize("damage",["missing_repeat","bad_mean","branch_flag","wrong_start","nan"])
def test_corrupt_records_rejected(tmp_path,damage):
    p=Path(_write(tmp_path,"prior_selfing",syndrome=.2))
    r=json.loads(p.read_text())
    h=r["records"][0]["histories"][0]
    if damage=="missing_repeat":h["per_repeat"].pop()
    elif damage=="bad_mean":h["far_minus_near_investment"]=.8
    elif damage=="branch_flag":r["any_reproducible_history_branching"]=True
    elif damage=="wrong_start":r["records"][0]["initial_state"]["investment"]=.1
    else:h["per_repeat"][0]["far_investment"]=float("nan")
    with pytest.raises(ValueError):
        module.validate_finite(r,json.loads(module.FINITE_DESIGN.read_text()))


def test_wrong_source_identity_rejected(tmp_path,complete_response):
    paths=[_write(tmp_path,s,syndrome=.2) for s in ("delayed_control","prior_selfing","pollen_discount","assurance_cost")]
    p=Path(paths[0])
    p.write_text(p.read_text()+" ")
    with pytest.raises(ValueError,match="source identity"):
        module.adjudicate(paths)
