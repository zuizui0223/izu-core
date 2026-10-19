"""Raw-only post-outcome comparison of paired A/I endpoint repeatability.

Reads already executed artifacts; imports no producer or biological model.
No p-values, new significance criteria, biological updates or trait ranking.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
from statistics import mean, variance
import subprocess
import zipfile

ROOT=Path(__file__).resolve().parents[1]


def require(condition,message):
    if not condition: raise ValueError(message)


def label(value,epsilon):
    if value==0: return 0
    if value>=epsilon: return 1
    if value<=-epsilon: return -1
    return 0


def summarize_records(records):
    result={}
    for record in records:
        start=record['initial_state']['id']
        require(start not in result,'duplicate initial state')
        histories=record['histories']
        require(len({h['history_seed'] for h in histories})==len(histories),'duplicate history')
        eligible=[]; occupied=0
        for h in histories:
            per=h['per_repeat']
            require(len(per)==4 and len({r['demographic_seed'] for r in per})==4,'repeat inventory')
            for r in per:
                arm_occ=[]
                for arm in ('near','far'):
                    values=[r[arm+'_'+trait] for trait in ('assurance','investment')]
                    require(all(v is None for v in values) or all(
                        isinstance(v,(int,float)) and not isinstance(v,bool)
                        and math.isfinite(v) and 0<=v<=1 for v in values),'invalid/missing trait')
                    arm_occ.append(values[0] is not None)
                occupied+=sum(arm_occ)
                require(type(r['paired_occupied']) is bool and r['paired_occupied']==all(arm_occ),
                        'paired occupancy mismatch')
            ok=all(r['paired_occupied'] for r in per)
            require(type(h['eligible']) is bool and h['eligible']==ok,'eligibility mismatch')
            for trait in ('assurance','investment'):
                value=h['far_minus_near_'+trait]
                if ok:
                    expected=mean(r['far_'+trait]-r['near_'+trait] for r in per)
                    require(value is not None and math.isclose(value,expected,abs_tol=1e-12,rel_tol=0),
                            'source contrast mean mismatch')
                else: require(value is None,'ineligible contrast must be undefined')
            if ok: eligible.append(h)
        row=dict(allocated_contexts=len(histories),allocated_arm_trajectories=len(histories)*8,
                 occupied_arm_trajectories=occupied,paired_eligible_contexts=len(eligible))
        for short,trait in [('A','assurance'),('I','investment')]:
            stats={}
            for arm in ('near','far'):
                vectors=[[r[arm+'_'+trait] for r in h['per_repeat']] for h in eligible]
                stats[arm+'_mean_within_context_sample_variance']=mean(map(variance,vectors)) if vectors else None
                stats[arm+'_mean_endpoint']=mean(map(mean,vectors)) if vectors else None
                stats[arm+'_identical_endpoint_contexts']=sum(len(set(v))==1 for v in vectors)
            differences=[[r['far_'+trait]-r['near_'+trait] for r in h['per_repeat']] for h in eligible]
            stats['contrast_mean_within_context_sample_variance']=mean(map(variance,differences)) if differences else None
            stats['contrast_labels']={}
            for epsilon in (0.,.05):
                labels=[[label(x,epsilon) for x in values] for values in differences]
                stats['contrast_labels'][str(epsilon)]=dict(
                    unanimous_contexts=sum(len(set(v))==1 for v in labels),
                    all_neutral_contexts=sum(set(v)=={0} for v in labels),
                    all_positive_contexts=sum(set(v)=={1} for v in labels),
                    all_negative_contexts=sum(set(v)=={-1} for v in labels),
                    discordant_contexts=sum(len(set(v))>1 for v in labels))
            row[short]=stats
        result[start]=row
    return result


def audit(directory):
    source=ROOT/'data/results/model3_joint_syndrome_finite_frozen_20261004.json'
    design_path=ROOT/'data/design/model3_joint_syndrome_finite_followup_20261004.json'
    bridge_path=ROOT/'data/design/model3_ch2_bridge_20260927.json'
    receipt=json.loads(source.read_text())
    for path in (design_path,bridge_path):
        original=subprocess.check_output(['git','show',receipt['provenance']['head_sha']+':'+path.relative_to(ROOT).as_posix()],cwd=ROOT)
        require(original==path.read_bytes(),'design differs from recorded source head')
    design=json.loads(design_path.read_text())
    bridge=json.loads(bridge_path.read_text())
    findings={}; sources={}
    for name,meta in receipt['provenance']['artifacts'].items():
        path=Path(directory)/(name+'.zip')
        require(hashlib.sha256(path.read_bytes()).hexdigest()==meta['digest_sha256'],'artifact hash mismatch')
        with zipfile.ZipFile(path) as z:
            member='finite_'+name+'.json'
            raw=z.read(member); d=json.loads(raw)
        require(d['setting']==name and d['cases']==3072,'setting/case mismatch')
        require(len(d['records'])==3,'initial state inventory')
        expected_starts={s['id']:s for s in design['initial_states']}
        for r in d['records']:
            require(r['initial_state']==expected_starts[r['initial_state']['id']],'initial state mismatch')
            require({h['history_seed'] for h in r['histories']}==set(bridge['history_seeds']),
                    'history seed inventory')
            for h in r['histories']:
                require({p['demographic_seed'] for p in h['per_repeat']}==set(design['demographic_seeds']),
                        'demographic seed inventory')
        report=summarize_records(d['records'])
        occupancy=sum(r['occupied_arm_trajectories'] for r in report.values())/3072
        require(math.isclose(occupancy,d['terminal_occupancy_fraction_all_trajectories'],abs_tol=1e-12),
                'source occupancy mismatch')
        findings[name]=report
        sources[name]=dict(artifact_id=meta['id'],archive_sha256=meta['digest_sha256'],
                           json_member=member,json_sha256=hashlib.sha256(raw).hexdigest())
    return dict(status='EXPLORATORY_MATCHED_AI_ENDPOINT_READBACK_NO_NEW_SIMULATION',
                source_run=receipt['provenance']['workflow_run_id'],
                source_head=receipt['provenance']['head_sha'],sources=sources,
                design_files_match_recorded_source_head=True,
                input_sha256={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in (source,design_path,bridge_path)},
                original_arm_trajectories=12288,new_biological_updates=0,
                horizon=design['years'],repeats_per_context=4,
                endpoint='terminal trait and far-minus-near terminal contrast, not initial-to-final change',
                labels='epsilon 0 and .05; equality at nonzero boundaries is directional; exact zero neutral',
                denominator='trait statistics use contexts with all four paired near/far survivors; all-start counts retained',
                limitations=['post-outcome descriptive comparison, no confirmatory trait ranking',
                             'four repeats per context cannot certify deterministic evolution',
                             'coarse five-node I/A genetic grid; M fixed at .5; no mutation',
                             'endpoint dispersion depends on starting variation, boundaries and selection',
                             'no event timing or ancestral-change direction recovered from endpoint JSON',
                             'not a new independent biological replay'],settings=findings)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--source-dir',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    if args.out.exists(): parser.error('refuse overwrite')
    result=audit(args.source_dir)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open('x',encoding='utf8',newline='\n') as handle:
        json.dump(result,handle,indent=2,allow_nan=False);handle.write('\n')
    print(result['status'])
