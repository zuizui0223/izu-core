"""Frozen-plant local investment returns across actual visitor exposures."""
from pathlib import Path
import hashlib,json,zipfile
import numpy as np
from scripts.run_model3_assurance_intervention import founders,config
from scripts.run_model3_persistent_isolation import exposure
from scripts.model3_island.assays import investment_assay
from scripts.model3_island.reproduction import reproduce
from scripts.model3_pollen_assay import assay_totals


def main():
    root=Path(__file__).resolve().parents[1]
    out=root/'outputs/model3_fixedplant_returns_20261005';out.mkdir(parents=True,exist_ok=True)
    destination=root/'data/results/model3_fixedplant_returns_20261005.json'
    if destination.exists() or (out/'individual_arrays.npz').exists():raise ValueError('preserve completed audit')
    sources=list((root/'scripts/model3_island').glob('*.py'))+[Path(__file__),root/'scripts/run_model3_assurance_intervention.py',
        root/'scripts/run_model3_persistent_isolation.py',root/'scripts/model3_pollen_assay.py',
        root/'data/design/model3_ch2_bridge_20260927.json',root/'data/design/model3_fixedplant_returns_20261005.json']
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    hashes={p.relative_to(root).as_posix():sha(p) for p in sources}
    manifest=out/'sources.json'
    if manifest.exists():assert json.loads(manifest.read_text())==hashes
    else:
        manifest.write_text(json.dumps(hashes,indent=2)+'\n',encoding='utf-8')
        with zipfile.ZipFile(out/'sources.zip','w',zipfile.ZIP_DEFLATED) as z:
            for p in sources:z.write(p,p.relative_to(root).as_posix())
    state=founders();rows=[];arrays={};failed=0
    for setting in ['assurance_cost','prior_selfing']:
        c=config(setting,.01,'fixed')
        for seed in range(76001,76065):
            for arm in ['near','far']:
                history=exposure(seed,arm)
                for period in [0,200,400]:
                    visitors=history.visitors[period]
                    coarse=investment_assay(state,visitors,c,step=.001)
                    fine=investment_assay(state,visitors,c,step=.0005)
                    error=np.abs(coarse['total_gradient']-fine['total_gradient'])
                    passed=bool(np.all(error<=1e-4+1e-3*np.abs(fine['total_gradient'])))
                    failed+=not passed
                    ledger=reproduce(state,visitors,c)
                    pollen=assay_totals(ovules=ledger.ovules,outcross=ledger.outcross.sum(axis=0),
                        capacity=np.full(48,.5),depression=c.depression,timing=c.assurance_timing)
                    key=f'{setting}_h{seed}_{arm}_t{period}'
                    arrays[key]=np.stack([fine['total_gradient'],fine['outcross_gradient'],error])
                    rows.append(dict(setting=setting,history_seed=seed,arm=arm,period=period,
                        visitors=len(visitors.ids),mean_gradient=float(fine['total_gradient'].mean()),
                        negative_fraction=float((fine['total_gradient']<0).mean()),
                        mean_outcross_gradient=float(fine['outcross_gradient'].mean()),
                        max_step_error=float(error.max()),precision_passed=passed,
                        received_pollen=float(ledger.delivered.sum()),**pollen))
            if seed%8==0:print(setting,seed,'cases',len(rows),flush=True)
    assert len(rows)==768
    np.savez_compressed(out/'individual_arrays.npz',**arrays)
    (out/'records.json').write_text(json.dumps(rows,allow_nan=False)+'\n',encoding='utf-8')
    result=dict(status='precision_passed' if failed==0 else 'precision_failed',cases=len(rows),failed_cases=failed,
        sources_sha256=sha(manifest),records_sha256=sha(out/'records.json'),arrays_sha256=sha(out/'individual_arrays.npz'),
        claim_ceiling='Fixed-state local contribution diagnostic, no realized evolution or field effect estimate. Require full precision pass before readout.')
    destination.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))


if __name__=='__main__':main()
