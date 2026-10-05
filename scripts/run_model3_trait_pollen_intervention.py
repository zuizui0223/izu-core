"""Execute the predeclared whole-population trait factorial at fixed exposures."""
from pathlib import Path
import hashlib,json,zipfile
from itertools import product
from scripts.run_model3_assurance_intervention import founders,config
from scripts.run_model3_persistent_isolation import exposure
from scripts.model3_trait_pollen_intervention import assay


def main():
    root=Path(__file__).resolve().parents[1]
    planpath=root/'data/design/model3_trait_pollen_intervention_20261005.json'
    plan=json.loads(planpath.read_text(encoding='utf-8'))
    out=root/'outputs/model3_trait_pollen_intervention_20261005'
    out.mkdir(parents=True,exist_ok=True)
    result=root/'data/results/model3_trait_pollen_intervention_20261005.json'
    if result.exists() or (out/'records.json').exists():
        raise ValueError('preserve existing execution')
    sources=list((root/'scripts/model3_island').glob('*.py'))+[Path(__file__),planpath,
        root/'scripts/model3_trait_pollen_intervention.py',root/'scripts/model3_pollen_assay.py',
        root/'scripts/run_model3_assurance_intervention.py',root/'scripts/run_model3_persistent_isolation.py',
        root/'data/design/model3_ch2_bridge_20260927.json']
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    hashes={p.relative_to(root).as_posix():sha(p) for p in sources}
    if (out/'sources.json').exists():
        assert json.loads((out/'sources.json').read_text(encoding='utf-8'))==hashes
    else:
        (out/'sources.json').write_text(json.dumps(hashes,indent=2)+'\n',encoding='utf-8')
        with zipfile.ZipFile(out/'sources.zip','w',zipfile.ZIP_DEFLATED) as z:
            for p in sources:z.write(p,p.relative_to(root).as_posix())
    state=founders();rows=[];seen=set();initial={}
    for seed in range(plan['histories']['first'],plan['histories']['last']+1):
        for arm in plan['arms']:
            history=exposure(seed,arm)
            for setting in plan['settings']:
                cfg=config(setting,.01,'evolving')
                for period,investment,capacity in product(plan['visitor_snapshots'],plan['investment_values'],plan['capacity_values']):
                    key=(setting,seed,arm,period,investment,capacity)
                    assert key not in seen;seen.add(key)
                    metrics=assay(state,history.visitors[period],cfg,investment=investment,capacity=capacity)
                    if period==0:
                        baseline=(setting,seed,investment,capacity)
                        if arm=='near':initial[baseline]=metrics
                        else:assert metrics==initial[baseline]
                    rows.append(dict(setting=setting,history_seed=seed,arm=arm,period=period,
                        investment=investment,capacity=capacity,**metrics))
        if seed%8==0:print('Completed',len(rows),'/',plan['expected_records'],flush=True)
    assert len(rows)==len(seen)==plan['expected_records']==6912
    with zipfile.ZipFile(out/'sources.zip') as z:
        for name,digest in hashes.items():assert sha(root/name)==hashlib.sha256(z.read(name)).hexdigest()==digest
    (out/'records.json').write_text(json.dumps(rows,allow_nan=False)+'\n',encoding='utf-8')
    receipt=dict(status='completed_validated_execution',records=len(rows),records_sha256=sha(out/'records.json'),
        source_manifest_sha256=sha(out/'sources.json'),design_sha256=sha(planpath),limits=plan['limits'])
    result.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt))


if __name__=='__main__':main()
