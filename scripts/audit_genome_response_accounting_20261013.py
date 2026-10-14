"""Retrospective genetic-response accounting; no new biological trajectories.

CLI uses the exact archived source and existing parentage. Only seeded birth
transmission is replayed; all child genotype/state fields must match originals.
"""
from __future__ import annotations
import argparse
import copy
from concurrent.futures import ProcessPoolExecutor,as_completed
from dataclasses import replace
import hashlib
import io
import json
from pathlib import Path
import sys
import zipfile

import numpy as np

INPUT_SHA="f0fd126f638e1c6bd130e640ce4491b3bb47aac3da1838359a902776c9a4e037"
COHORT_SHA="7ae00916ed2cbb38323c3fb9ffc5824de3e8272df1f5a35785842c316191f918"
SOURCE_PREFIX="work/EL_next_20261007/extension_source/"
RECIPE_PREFIX="work/EL_order_boundary_20261007/"
FIELDS=("ids","alleles","allele_origin","mutation_flags","birth_years")


def _valid(a,shape,label):
    a=np.asarray(a,dtype=float)
    if (a.shape!=shape or not np.isfinite(a).all() or (a<0).any() or (a>1).any()):
        raise ValueError("Invalid genetic input: "+label)
    return a


def decompose_step(source_traits,mothers,fathers,expected,premut,actual):
    source_traits=np.asarray(source_traits,dtype=float)
    if source_traits.ndim!=2 or source_traits.shape[1]!=3 or not len(source_traits):
        raise ValueError("Occupied source genotype state required")
    source_traits=_valid(source_traits,source_traits.shape,"source")
    actual=np.asarray(actual,dtype=float)
    if actual.ndim!=3 or actual.shape[1:]!=(3,2):
        raise ValueError("Diploid offspring shape")
    n=len(actual)
    actual=_valid(actual,(n,3,2),"actual")
    premut=_valid(premut,(n,3,2),"premutation")
    mothers=_valid(mothers,(n,3),"mothers")
    fathers=_valid(fathers,(n,3),"fathers")
    expected=_valid(expected,(3,),"expected parent return")
    if not n:
        return {"eligible":False,"reason":"no_offspring_trait_mean","source_census":len(source_traits),"offspring_census":0}
    resident=source_traits.mean(axis=0)
    selected=(mothers+fathers).mean(axis=0)/2
    transmitted=premut.mean(axis=(0,2));final=actual.mean(axis=(0,2))
    values={"selection":expected-resident,"parent_sampling":selected-expected,
            "transmission":transmitted-selected,"birth_mutation":final-transmitted,
            "observed_change":final-resident}
    error=float(np.max(np.abs(sum(values[k] for k in values if k!="observed_change")-values["observed_change"])))
    if error>1e-10:raise ValueError("Response closure failed")
    return {"eligible":True,"source_census":len(source_traits),"offspring_census":n,
            **{k:v.tolist() for k,v in values.items()},"closure_error":error}


def digest(raw):return hashlib.sha256(raw).hexdigest()


def check_recorded_ledger(ledger,record):
    fields={"maternal_total":"maternal","paternal_total":"paternal","outcross_total":"outcross",
            "self_viable":"self_viable","self_raw":"self_raw","pollen_export":"exported",
            "pollen_delivered":"delivered","pollen_lost":"lost"}
    maximum=0.
    for key,attribute in fields.items():
        observed=record.get(key)
        if (isinstance(observed,(bool,np.bool_)) or not isinstance(observed,(int,float,np.number))
            or not np.isfinite(observed) or observed<0):
            raise ValueError("Original ledger field missing/nonfinite: "+key)
        value=float(getattr(ledger,attribute).sum())
        if not np.isfinite(value) or value<0:raise ValueError("Invalid reconstructed ledger: "+key)
        error=abs(value-observed);maximum=max(maximum,error)
        if error>1e-10:raise ValueError("Original reproductive ledger differs: "+key)
    return maximum


def prepare_source(input_zip,destination):
    raw=Path(input_zip).read_bytes()
    if digest(raw)!=INPUT_SHA:raise ValueError("Original source-input ZIP identity")
    root=Path(destination);root.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        manifest_raw=z.read("work/EL_next_20261007/extension_source_manifest.json")
        manifest=json.loads(manifest_raw)
        for name,h in manifest["files"].items():
            data=z.read(SOURCE_PREFIX+name)
            if digest(data)!=h:raise ValueError("Original source member drift: "+name)
            target=(root/name).resolve()
            if not target.is_relative_to(root.resolve()):raise ValueError("Unsafe source member")
            target.parent.mkdir(parents=True,exist_ok=True)
            if target.exists() and target.read_bytes()!=data:raise ValueError("Existing source differs")
            target.write_bytes(data)
        local={n: z.read(RECIPE_PREFIX+n) for n in
               ("campaign_inputs.py","campaign_runner.py","natural_trace.py","trace_archive.py","order_observer.py","natural_campaign_design.json")}
        causal={n:z.read(RECIPE_PREFIX+n) for n in
                ("assurance_causal_design.json","assurance_causal_inputs.py","assurance_causal_runner.py")}
    return {"root":str(root.resolve()),"manifest_sha256":digest(manifest_raw),
            "files":manifest["files"],"local_sha256":{n:digest(b) for n,b in local.items()},
            "producer_sha256":{n:digest(b) for n,b in causal.items()},
            "campaign_design":json.loads(local["natural_campaign_design.json"]),
            "causal_design":json.loads(causal["assurance_causal_design.json"])}


def load_native(source):
    sys.path.insert(0,source["root"])
    import scripts.model3_island.types as types
    import scripts.model3_island.population as pop
    import scripts.model3_island.reproduction as reproduction
    import scripts.model3_island.randomness as randomness
    for module in (types,pop,reproduction,randomness):
        p=Path(module.__file__).resolve()
        if not p.is_relative_to(Path(source["root"])):
            raise ValueError("Native imports resolved to unrelated current checkout")
    return types,pop,reproduction,randomness


def audit_case(raw,receipt,source,*,max_updates=None):
    if digest(raw)!=receipt["sha256"]:raise ValueError("Original case SHA")
    types,pop,reproduction,randomness=load_native(source)
    with np.load(io.BytesIO(raw),allow_pickle=False) as z:
        a={k:z[k].copy() for k in z.files}
    m=json.loads(str(a["metadata"].item()))
    expected_source={"source_manifest":source["manifest_sha256"],"local":source["local_sha256"],"numpy":np.__version__}
    if m["identity"]["source"]!=expected_source or m["identity"]["producer"]!=source["producer_sha256"]:
        raise ValueError("Original source/producer/runtime record differs")
    if receipt["task"]!=m["task"] or receipt["identity"]!=m["identity"] or receipt["technical"] or m["technical"]:
        raise ValueError("Case receipt/task admission")
    task=m["task"];c=dict(m["config"])
    paired=int.from_bytes(hashlib.sha256(('izu-assurance-causal-v1-28470909\0'+task['pair_key']).encode()).digest()[:16],'big')
    if m['seed']!=paired:raise ValueError('Original keyed biological seed differs')
    c["visitor_arrival"]=types.ArrivalConfig(**c["visitor_arrival"])
    c["seed_arrival"]=types.ArrivalConfig(**c["seed_arrival"])
    c=types.Config(**c)
    if c.survival!=0 or c.seed_arrival.supply!=0 or c.years!=200:
        raise ValueError("No-adult/no-immigration accounting scope differs")
    optima=[] if task["supply"]==0 else source["campaign_design"]["compositions"][task["composition"]]
    v=types.VisitorState(np.arange(len(optima),dtype=np.int64),np.array(optima,dtype=float),np.full(len(optima),.2),np.ones(len(optima)))
    d=json.loads(str(a["diagnostics"].item()))
    if len(a["population"])!=201 or len(a["offsets"])!=202 or len(a["parent_offsets"])!=201 or len(d)!=201:
        raise ValueError("Incomplete annual inventory")
    streams={n:randomness.stream(m["seed"],n,0) for n in randomness.STREAM_IDS}
    output=[];max_record_error=0.;max_birth_error=0.
    updates=200 if max_updates is None else min(200,max_updates)
    for t in range(updates):
        lo,hi=a["offsets"][t:t+2];nxlo,nxhi=a["offsets"][t+1:t+3]
        state=types.PlantState(**{k:a[k][lo:hi] for k in FIELDS})
        next_state=types.PlantState(**{k:a[k][nxlo:nxhi] for k in FIELDS})
        if len(state.ids)!=a["population"][t] or len(next_state.ids)!=a["population"][t+1]:raise ValueError("Annual census offsets")
        ledger=reproduction.reproduce(state,v,c)
        if not len(state.ids):
            if len(next_state.ids):raise ValueError("Extinction not absorbing")
            output.append({"year":t,"eligible":False,"reason":"extinct_source"});continue
        max_record_error=max(max_record_error,check_recorded_ledger(ledger,d[t]))
        weights=np.stack([ledger.outcross.sum(axis=0)/2,ledger.outcross.sum(axis=1)/2,ledger.self_viable])
        traits=state.alleles.mean(axis=2);total=weights.sum()
        if total<=0 and len(next_state.ids):raise ValueError("Recruitment without parental return")
        components=weights@(traits-traits.mean(axis=0))/total if total else np.zeros((3,3))
        recorded=d[t]["premutation_mean_response_components"]
        if recorded is not None:
            err=float(np.max(np.abs(components-np.asarray(recorded))));max_record_error=max(max_record_error,err)
            if err>1e-10:raise ValueError("Original Price components differ")
        start,end=a["parent_offsets"][t:t+2];parentage=a["parentage"][start:end]
        if parentage.shape!=(len(next_state.ids),3) or not np.array_equal(parentage[:,0],next_state.ids):
            raise ValueError("Parentage/offspring census mismatch")
        index={int(pid):i for i,pid in enumerate(state.ids)}
        try:
            mothers=np.array([index[int(x)] for x in parentage[:,1]],dtype=int)
            fathers=np.array([index[int(x)] for x in parentage[:,2]],dtype=int)
        except KeyError as exc:raise ValueError("Unknown original parent ID") from exc
        shadow_seg=copy.deepcopy(streams["segregation"])
        premut=pop.inherit(state,mothers,fathers,replace(c,mutation_rate=0.),
                          segregation_rng=shadow_seg,mutation_rng=copy.deepcopy(streams["mutation"]),
                          year=t+1,mutation_traits=tuple(m["mutation_mask"]))
        child=pop.inherit(state,mothers,fathers,c,segregation_rng=streams["segregation"],
                          mutation_rng=streams["mutation"],year=t+1,mutation_traits=tuple(m["mutation_mask"]))
        for field in FIELDS:
            actual=getattr(next_state,field);replayed=getattr(child,field)
            if field=="alleles":
                err=float(np.max(np.abs(actual-replayed))) if len(actual) else 0.;max_birth_error=max(max_birth_error,err)
                if err>1e-12:raise ValueError("Original birth allele replay differs")
            elif not np.array_equal(actual,replayed):raise ValueError("Original birth state replay differs: "+field)
        expected=traits.mean(axis=0)+components.sum(axis=0)
        row=decompose_step(traits,traits[mothers],traits[fathers],expected,premut.alleles,child.alleles)
        row.update(year=t,sexual_selection_components=components.tolist())
        output.append(row)
    return {"task":task,"updates":updates,"status":"original_birth_and_ledger_replayed",
            "case_sha256":digest(raw),"max_record_error":max_record_error,"max_birth_error":max_birth_error,
            "source_manifest_sha256":source['manifest_sha256'],"auditor_sha256":digest(Path(__file__).read_bytes()),
            "rows":output,"scope":"Source-matched retrospective accounting; not independent biological histories or causal density-effect allocation"}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cohort",type=Path,required=True);p.add_argument("--source-input",type=Path,required=True)
    p.add_argument("--source-dir",type=Path,required=True);p.add_argument("--out",type=Path,required=True)
    p.add_argument("--technical",action="store_true")
    p.add_argument("--workers",type=int,default=2)
    args=p.parse_args();source=prepare_source(args.source_input,args.source_dir)
    auditor_hash=digest(Path(__file__).read_bytes())
    if digest(args.cohort.read_bytes())!=COHORT_SHA:raise ValueError("Original complete cohort ZIP identity")
    args.out.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(args.cohort) as z:
        names=sorted(n for n in z.namelist() if "/assurance_causal_campaign_" in n and n.endswith('.npz'))
        if len(names)!=320:raise ValueError("Complete320 ABM case inventory")
        cases=[(n,json.loads(z.read(n[:-4]+'.json'))) for n in names]
        if args.technical:
            contexts={}
            for name,receipt in cases:
                t=receipt['task'];key=(t['block'],t['supply'],t['composition'])
                contexts.setdefault(key,(name,receipt))
            if len(contexts)!=10:raise ValueError('Original ten-context coverage')
            cases=list(contexts.values())
        if args.workers not in (1,2,4):raise ValueError('Bounded audit worker count')
        task_keys=[r['task']['key'] for _,r in cases]
        if len(task_keys)!=len(set(task_keys)):raise ValueError('Duplicate original task identity')
        for _,receipt in cases:
            if (args.out/(receipt['task']['key']+'.json')).exists():
                raise ValueError('Existing derived readout must be inspected, never overwritten or rerun blindly')
        completed=[]
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            pending=[pool.submit(audit_case,z.read(name),receipt,source) for name,receipt in cases]
            for i,future in enumerate(as_completed(pending),1):
                r=future.result()
                if r['auditor_sha256']!=auditor_hash:raise ValueError('Audit code changed during execution')
                target=args.out/(r['task']['key']+'.json')
                payload=(json.dumps(r,indent=2,allow_nan=False)+'\n').encode('utf-8')
                target.write_bytes(payload)
                completed.append({'key':r['task']['key'],'sha256':digest(payload),'updates':r['updates'],
                                  'max_record_error':r['max_record_error'],'max_birth_error':r['max_birth_error']})
                print(json.dumps({'case':i,'total':len(cases),'key':r['task']['key'],'status':r['status'],
                                  'updates':r['updates'],'max_birth_error':r['max_birth_error']}),flush=True)
        if len(completed)!=len(cases) or digest(Path(__file__).read_bytes())!=auditor_hash:
            raise ValueError('Incomplete audit or changed auditor')
        envelope={'status':'COMPLETE_TECHNICAL_SOURCE_MATCHED' if args.technical else 'COMPLETE_RETROSPECTIVE_320_RESPONSE_ACCOUNTING',
                  'cases':len(completed),'audited_updates':sum(r['updates'] for r in completed),
                  'original_cohort_sha256':COHORT_SHA,'original_input_sha256':INPUT_SHA,
                  'original_source_manifest_sha256':source['manifest_sha256'],'auditor_sha256':auditor_hash,
                  'no_new_biological_histories':True,'all_birth_fields_replayed':list(FIELDS),
                  'scope':'Existing source-matched genetic-response accounting; no unique causal density allocation or natural-order survival claim',
                  'records':sorted(completed,key=lambda r:r['key'])}
        (args.out/'_COMPLETION.json').write_bytes((json.dumps(envelope,indent=2)+'\n').encode('utf-8'))


if __name__=='__main__':main()
