"""Reject incomplete experiments before interpreting stationarity."""
import itertools
import json
from pathlib import Path
import pytest
from scripts.summarize_chapter2_long_horizon_stationarity import summarize
ROOT=Path(__file__).resolve().parents[1]

@pytest.fixture
def experiment(tmp_path):
    design=json.loads((ROOT/"data/design/chapter2_long_horizon_stationarity_20261003.json").read_text(encoding="utf-8"))
    parent=json.loads((ROOT/design["backbone"]["parent_design"]).read_text(encoding="utf-8"))
    years=design["checkpoints"]
    backbone=[dict(history_seed=h,start_investment=s,year=y,effect_far_minus_near=-.1) for h,s,y in itertools.product(parent["history_seeds"],design["backbone"]["starts"],years)]
    m=design["mutation_accessibility"]
    mutation=[dict(standing_regime=c["standing_regime"],standing_sd_investment=c["standing_sd_investment"],target_VM_over_VG0=c["VM_over_VG0"],capacity=k,founder_seed=f,demographic_seed=d,visitor_history=v,reports=[dict(year=y,investment_response=.2 if c["standing_regime"]=="high_reference" else .1,investment_va_proxy=.1) for y in years]) for c,k,f,d,v in itertools.product(m["comparison"],m["capacities"],m["founder_seeds"],m["demographic_seeds"],m["visitor_histories"])]
    return design,tmp_path,backbone,mutation

def write_run(root,backbone,mutation):
    for kind,rows in (("backbone",backbone),("mutation",mutation)):
        (root/f"{kind}-shard-0.json").write_text(json.dumps(dict(status=f"complete_long_horizon_{kind}_shard",rows=rows)))

def test_complete_domain(experiment):
    design,root,b,m=experiment;write_run(root,b,m)
    result=summarize(design,root)
    assert result["backbone"]["n_histories"]==128
    assert result["mutation_accessibility"]["n_trajectories"]==64

@pytest.mark.parametrize("fault",["backbone_subset","duplicate_backbone","foreign_history","missing_mutation","duplicate_mutation","missing_checkpoint"])
def test_invalid_domain(experiment,fault):
    design,root,b,m=experiment
    if fault=="backbone_subset":b=b[:6]
    elif fault=="duplicate_backbone":b[-1]=b[0]
    elif fault=="foreign_history":b[0]["history_seed"]=-1
    elif fault=="missing_mutation":m.pop()
    elif fault=="duplicate_mutation":m[-1]=m[0]
    else:m[0]["reports"].pop()
    write_run(root,b,m)
    with pytest.raises(ValueError):summarize(design,root)
