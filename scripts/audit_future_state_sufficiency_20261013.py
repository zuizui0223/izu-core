"""Frozen technical annotation-invariance audit; no biological effect inference."""
from dataclasses import replace
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
from scripts import persistence_expression_mechanism_20261012 as native
from scripts import initial_assurance_mean_20261013 as design
from scripts.model3_island.types import Config, PlantState, VisitorState


def technical_tasks():
    return [dict(block=b,replicate=0,origin=o,target=t,policy='native')
            for b in native.BLOCKS for o in native.ORIGINS for t in native.TARGETS]


def relabel(state):
    return replace(state,allele_origin=state.allele_origin+1000000,
                   mutation_flags=~state.mutation_flags,ids=state.ids+1000000000)


def assert_dynamics_equal(first,second):
    for field in ('population','offsets','alleles','means','diagnostics'):
        if field in first or field in second:
            np.testing.assert_array_equal(first[field],second[field],err_msg=field)


def run(input_path,out):
    design.source_gate()
    manifest,states,baseline=native.read_inputs(input_path,design.INPUT_SHA)
    lookup={(r['block'],r['replicate'],r['origin']):i for i,r in enumerate(manifest['states'])}
    expected={(b,r,o) for b in native.BLOCKS for r in range(512) for o in native.ORIGINS}
    if len(lookup)!=2048 or set(lookup)!=expected:raise ValueError('complete initial-state domain required')
    future_pairs=0
    for b in native.BLOCKS:
        for r in range(512):
            for t in native.TARGETS:
                a=dict(block=b,replicate=r,target=t,origin=native.ORIGINS[0],policy='native')
                z=dict(a,origin=native.ORIGINS[1])
                if native.future_seed(a)!=native.future_seed(z):raise ValueError('origin alters future seed')
                future_pairs+=1
    out=Path(out)
    if out.exists():raise ValueError('refuse overwrite')
    out.mkdir(parents=True)
    visitors=VisitorState(np.arange(4),np.full(4,.5),np.full(4,.2),np.ones(4));records=[]
    for task in technical_tasks():
        i=lookup[task['block'],task['replicate'],task['origin']]
        state=PlantState(**{f:states[f][i].copy() for f in native.FIELDS})
        cfg=Config.from_dict(manifest['configs'][str(task['target'])])
        if cfg.survival!=0:raise ValueError('zero adult survival required')
        first=native.trajectory(state,visitors,cfg,native.future_seed(task),'native',horizon=200)
        native.verify_native(first,baseline,i*2+native.TARGETS.index(task['target']))
        second=native.trajectory(relabel(state),visitors,cfg,native.future_seed(task),'native',horizon=200)
        assert_dynamics_equal(first,second)
        key=native.case_key(task)
        np.savez_compressed(out/(key+'.npz'),**{'native_'+k:v for k,v in first.items()},**{'relabeled_'+k:v for k,v in second.items()})
        raw=(out/(key+'.npz')).read_bytes()
        records.append(dict(task=task,archive=key+'.npz',sha256=native.digest(raw),exact_dynamics_equal=True,original_native_admitted=True))
    source=Path(__file__).read_bytes()
    readout=dict(status='TECHNICAL_CONDITIONAL_STATE_INVARIANCE_ADMITTED',input_sha256=design.INPUT_SHA,
        operator_sha256=design.OPERATOR_SHA,producer_sha256=native.digest(source),states=2048,
        origin_free_future_pairs=future_pairs,technical_pairs=8,technical_traces=16,horizon=200,
        biological_effect_cases=0,records=records,
        inference='Same ordered genotype/census/future law has no direct ancestry-label effect. No natural-order benefit or future-selection decomposition identified.')
    (out/'READOUT.json').write_text(json.dumps(readout,indent=2)+'\n',encoding='utf-8')
    return readout


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();print(json.dumps(run(a.input,a.out),indent=2))


if __name__=='__main__':main()
