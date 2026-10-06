"""Exploratory resident-state coupling; no biological parameter changes."""
from pathlib import Path
import hashlib
import json
import numpy as np
from scripts.audit_model3_joint_syndrome_vector import _settings, invasion_gradient
from scripts.audit_model3_unified_reduction import _visitors
from scripts.model3_island.selection import syndrome_thresholds
from scripts.model3_island.types import Config

ROOT=Path(__file__).resolve().parents[1]

def run():
    read=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
    design=read('data/design/model3_reciprocal_selection_20261005.json')
    base=read('data/design/model3_ch2_bridge_20260927.json')
    decision=read('data/design/model3_joint_syndrome_rare_mutant_20261004.json')
    communities=read('data/design/model3_unified_reduction_audit_20260927.json')['communities']
    settings=_settings(Config.from_dict(base['base_config']),decision)
    axis=np.linspace(.02,.98,49); inv,cap=np.meshgrid(axis,axis)
    arrays={'axis':axis}; rows=[]; maxerr=0.; inv_error=0.; sign_disagreements=0; max_relative_step_error=0.
    for setting,cfg in settings.items():
        for community,optima in communities.items():
            visitors=_visitors(optima)
            for matching in design['matching']:
                z=np.stack([np.full_like(inv,matching),inv,cap],axis=-1)
                t=syndrome_thresholds(z,visitors,cfg)
                gi=t['investment_gradient'];ga=t['assurance_gradient']
                cross=[]
                for field,k in [('investment_gradient',2),('assurance_gradient',1)]:
                    estimates=[]
                    for h in design['derivative_steps']:
                        zp=z.copy();zm=z.copy();zp[...,k]+=h;zm[...,k]-=h
                        estimates.append((syndrome_thresholds(zp,visitors,cfg)[field]-syndrome_thresholds(zm,visitors,cfg)[field])/(2*h))
                    maxerr=max(maxerr,float(np.max(np.abs(estimates[0]-estimates[1]))))
                    sign_disagreements+=int(np.count_nonzero(np.sign(estimates[0])!=np.sign(estimates[1])))
                    max_relative_step_error=max(max_relative_step_error,float(np.max(np.abs(estimates[0]-estimates[1])/np.maximum(np.abs(estimates[1]),1e-12))))
                    cross.append(estimates[-1])
                state=np.array([matching,.5,.5]);tt=syndrome_thresholds(state,visitors,cfg)
                for field,k in [('investment_gradient',1),('assurance_gradient',2)]:
                    inv_error=max(inv_error,abs(float(tt[field])-invasion_gradient(state,visitors,cfg,trait_index=k,step=1e-5)))
                key=f'{setting}__{community}__x{matching}'
                arrays[key]=np.stack([gi,ga,*cross])
                assert np.isfinite(arrays[key]).all()
                row=dict(setting=setting,community=community,matching=matching,n_states=gi.size,
                         joint_direction_fraction=float(np.mean((gi<0)&(ga>0))))
                for label,values in zip(['capacity_effect_on_investment_selection','investment_effect_on_capacity_selection'],cross):
                    row[label]=dict(minimum=float(values.min()),maximum=float(values.max()),
                                    negative_grid_fraction=float(np.mean(values < -1e-7)),positive_grid_fraction=float(np.mean(values > 1e-7)))
                rows.append(row)
    out=ROOT/'outputs/model3_reciprocal_selection_20261005';out.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(out/'fields.npz',**arrays)
    result=dict(classification=design['classification'],n_fields=len(rows),n_states=sum(r['n_states'] for r in rows),
                derivative_step_max_difference=maxerr,independent_gradient_max_error=inv_error,
                derivative_sign_disagreements=sign_disagreements,max_relative_step_error=max_relative_step_error,
                rows=rows,claim_boundary=design['interpretation'],
                array_sha256=hashlib.sha256((out/'fields.npz').read_bytes()).hexdigest(),
                design_sha256=hashlib.sha256((ROOT/'data/design/model3_reciprocal_selection_20261005.json').read_bytes()).hexdigest())
    result['status']='passed_diagnostic_checks' if maxerr<1e-3 and inv_error<2e-8 else 'failed_diagnostic_checks'
    (ROOT/'data/results/model3_reciprocal_selection_20261005.json').write_text(json.dumps(result,indent=2,allow_nan=False),encoding='utf-8')
    print({k:v for k,v in result.items() if k!='rows'})
    if result['status'].startswith('failed'):raise SystemExit(1)

if __name__=='__main__':run()
