"""Independent algebra-versus-invasion check of the joint local cost thresholds."""
import hashlib
import itertools
import json
from pathlib import Path
import numpy as np
from scripts.audit_model3_joint_syndrome_vector import _settings, invasion_gradient
from scripts.audit_model3_unified_reduction import _visitors
from scripts.model3_island.selection import syndrome_thresholds
from scripts.model3_island.types import Config

ROOT=Path(__file__).resolve().parents[1]

def run_audit():
    paths=['data/design/model3_ch2_bridge_20260927.json',
           'data/design/model3_joint_syndrome_rare_mutant_20261004.json',
           'data/design/model3_unified_reduction_audit_20260927.json']
    bridge,decision,controlled=[json.loads((ROOT/p).read_text(encoding='utf-8')) for p in paths]
    states=list(itertools.product(*(decision['resident_states'][k] for k in ['access','investment','assurance'])))
    rows=[]
    for setting,cfg in _settings(Config.from_dict(bridge['base_config']),decision).items():
        for name,optima in controlled['communities'].items():
            visitors=_visitors(optima)
            for state in states:
                t=syndrome_thresholds(state,visitors,cfg)
                numeric=[invasion_gradient(np.array(state),visitors,cfg,trait_index=k,step=1e-5) for k in [1,2]]
                row=dict(setting=setting,community=name,state=list(state),
                         **{k:bool(v) if k=='local_syndrome_direction' else float(v) for k,v in t.items()},
                         numerical_investment_gradient=numeric[0],numerical_assurance_gradient=numeric[1])
                rows.append(row)
    error=max(max(abs(r['investment_gradient']-r['numerical_investment_gradient']),
                  abs(r['assurance_gradient']-r['numerical_assurance_gradient'])) for r in rows)
    paths+=['scripts/model3_island/selection.py','scripts/audit_model3_joint_syndrome_vector.py',
            'scripts/audit_model3_joint_thresholds.py']
    return dict(status='passed' if error<2e-8 else 'failed',n_cells=len(rows),
                maximum_gradient_error=error,rows=rows,
                source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},
                claim_boundary='controlled local gradient validation, not frozen-history threshold crossing or evolved endpoints')

if __name__=='__main__':
    result=run_audit()
    (ROOT/'data/results/model3_joint_thresholds_20261004.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print({k:result[k] for k in ['status','n_cells','maximum_gradient_error']})
    if result['status']!='passed':
        raise SystemExit(1)
