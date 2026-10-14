"""Saved-kernel identity verification via independent switch-time rewards and separate products."""
import hashlib
import json
from pathlib import Path
import numpy as np

root=Path(__file__).resolve().parent
source=root.parent/'four_question_unresolved_20261013/duration_actual_github_38280177062/native_regenerated_kernels_and_state_curves.npz'
assert hashlib.sha256(source.read_bytes()).hexdigest()=='d34fc60c389775f88fa8a54051fdfe90a76ef7864b8f5a813b99d5f0b68ca172'
readout=json.loads((root/'extracted/READOUT.json').read_bytes())
with np.load(source,allow_pickle=False) as data:
    keys=data['keys'].tolist();matrices=data['kernels'];states=data['states'];original_p=data['probabilities']
with np.load(root/'extracted/ALL_STATE_TIME_CONTRIBUTIONS.npz',allow_pickle=False) as data:
    recorded_e=data['endpoint'];recorded_d=data['duration']
index={key:i for i,key in enumerate(keys)};alive=(states.sum(1)>0).astype(float)
max_state_error=0.;max_switch_error=0.;state_checks=0;switch_checks=0
one_step=[]
for case_no,row in enumerate(readout['comparisons']):
    stem=f"{row['mismatch_fraction']}_{row['setting']}_{row['budget']}"
    ni=index[stem+'_native_'+row['visitor_arm']];fi=index[stem+'_fixed_expression_'+row['visitor_arm']]
    native,fixed=matrices[ni],matrices[fi];p0=original_p[ni,0]
    p=[];v=[];g=[]
    for matrix in (native,fixed):
        pp=np.zeros((81,165));pp[0]=p0
        vv=np.zeros_like(pp);vv[0]=alive
        for t in range(80):pp[t+1]=pp[t]@matrix;vv[t+1]=matrix@vv[t]
        gg=np.zeros_like(pp);gg[1:]=np.cumsum(vv[:-1],axis=0)
        p.append(pp);v.append(vv);g.append(gg)
    assert max(abs(p[0]-original_p[ni]).max(),abs(p[1]-original_p[fi]).max())<1e-10
    for ref in range(2):
        prefix=ref;future=1-ref
        hybrid_endpoint=[];hybrid_duration=[]
        prefix_rewards=np.r_[0.,np.cumsum(p[prefix][:-1]@alive)]
        for t in range(81):
            hybrid_endpoint.append(float(p[prefix][t]@v[future][80-t]))
            hybrid_duration.append(float(prefix_rewards[t]+p[prefix][t]@g[future][80-t]))
        direction=1 if ref==0 else -1
        expected_e=direction*np.diff(hybrid_endpoint)
        expected_d=direction*np.diff(hybrid_duration)
        err=max(abs(expected_e-recorded_e[case_no,ref].sum(1)).max(),abs(expected_d-recorded_d[case_no,ref].sum(1)).max())
        assert err<1e-10;max_switch_error=max(max_switch_error,float(err));switch_checks+=160
        for t in range(80):
            end=p[prefix][t]*(native@v[future][79-t]-fixed@v[future][79-t])
            duration=p[prefix][t]*(native@g[future][79-t]-fixed@g[future][79-t])
            err=max(abs(end-recorded_e[case_no,ref,t]).max(),abs(duration-recorded_d[case_no,ref,t]).max())
            assert err<1e-10;max_state_error=max(max_state_error,float(err));state_checks+=330
    # Additional descriptive row properties, all original48 pairs/no new condition:
    # pure investment-genotype states retain their alleles; recruit counts are demographic.
    for name,mask in [('low_fixed',(states[:,0]>0)&(states[:,1:]==0).all(1)),('high_fixed',(states[:,2]>0)&(states[:,:2]==0).all(1))]:
        for i in np.flatnonzero(mask):
            one_step.append(dict(pair=case_no,original_reversal=row['original_reversal'],investment_genotype=name,census=int(states[i].sum()),
                one_update_occupancy_change=float((native[i]-fixed[i])@alive),
                expected_recruit_census_change=float((native[i]-fixed[i])@states.sum(1))))
receipt=dict(status='ALL48_TWO_REFERENCE_STATE_TIME_AND_SWITCH_REWARD_IDENTITIES_INDEPENDENTLY_MATCH',
    pairs=48,state_time_checks=state_checks,switch_time_checks=switch_checks,max_state_error=max_state_error,max_switch_error=max_switch_error,
    new_biological_histories=0,producer_imported=False,
    readout_sha256=hashlib.sha256((root/'extracted/READOUT.json').read_bytes()).hexdigest(),
    all_terms_sha256=hashlib.sha256((root/'extracted/ALL_STATE_TIME_CONTRIBUTIONS.npz').read_bytes()).hexdigest(),
    verifier_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    descriptive_one_step_all48_pairs=one_step,
    limits=['Single-update pure-genotype recruit/occupancy changes are descriptive row properties, not a new confirmatory family.','No unique fixation or natural-order mediator identified.'])
with (root/'INDEPENDENT_REVIEW.json').open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k not in ('descriptive_one_step_all48_pairs','limits')}))
