"""Verify unchanged t0 Model3 reproduction across genotype-hidden factorial arms.

Calls ONLY archived exact reproduction.reproduce on founding diploid genotypes,
never offspring inheritance, population advancement, new histories, or outcome
selection. Use an original source-verified Python module (git blob fixed).
"""
from __future__ import annotations
import argparse
from hashlib import sha256,sha1
import io
import json
from pathlib import Path
from types import SimpleNamespace
import zipfile

import numpy as np

from scripts.audit_chapter2_clock_factorial_feasibility_20261013 import (
    transform,A_HALF_WIDTHS,I_HOMOLOG_SCALE,FOUNDER_BLOCKS,
)

ORIGINAL_NATIVE_REPRO_GIT_BLOB="95314698a3296b6f13b8c053c36f2df0b7b744ca"
ORIGINAL_SHARD_SHA={
    0:"5b850eaad6104f572f56df2a37da00fbc8473503a827703c82f6870a87e9a881",
    3:"676e84ff0729ba88dcd91cb161efeb2dc63f10b6679458695c5d2909c017e9c2",
    4:"900d3d22a36fa59241a933b8efc4b2fb8f320e4b25637e592640f31c529314fe",
}
SOURCE_FIELDS=("outcross","self_raw","self_viable","ovules","exported","delivered","lost","maternal","paternal")
ARCHIVED_TOTAL_FIELDS=("maternal","paternal","self_raw","self_viable","ovules","exported","delivered","outcross")
CONTEXTS={
  0:{"supply":0.0,"composition":"empty","optima":[]},
  3:{"supply":0.125,"composition":"matched","optima":[.5,.5,.5,.5]},
  4:{"supply":0.125,"composition":"separated","optima":[.3,.3,.7,.7]},
}


def git_blob_digest(p:Path)->str:
    raw=p.read_bytes()
    return sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()


def source_ledger(reproduction,state,visitor,cfg)->dict:
    l=reproduction.reproduce(state,visitor,cfg)
    return {key:np.asarray(getattr(l,key)) for key in SOURCE_FIELDS}


def checksum_ledger(ledger)->str:
    h=sha256()
    for key in SOURCE_FIELDS:
        x=np.asarray(ledger[key],dtype=np.float64)
        h.update(key.encode()+b"\0")
        h.update(np.asarray(x.shape,dtype=np.int64).tobytes())
        h.update(x.tobytes(order="C"))
    return h.hexdigest()


def original_totals(ledger)->np.ndarray:
    return np.array([np.asarray(ledger[key]).sum() for key in ARCHIVED_TOTAL_FIELDS],dtype=np.float64)


def check(shards:dict[int,Path])->dict:
    import scripts.model3_island.reproduction as reproduction
    if git_blob_digest(Path(reproduction.__file__))!=ORIGINAL_NATIVE_REPRO_GIT_BLOB:
        raise ValueError("wrong original Model3 reproduction source; do not admit source substitute")
    zips={};receipts=[];rows=[]
    try:
        for context,p in shards.items():
            if context not in ORIGINAL_SHARD_SHA:raise ValueError("unexpected original visitor context")
            data=p.read_bytes()
            h=sha256(data).hexdigest()
            if h!=ORIGINAL_SHARD_SHA[context]:raise ValueError("original provider SHA changed")
            zips[context]=zipfile.ZipFile(io.BytesIO(data))
            receipts.append({"context":context,"provider_sha256":h,"bytes":len(data)})
        if set(zips)!=set(CONTEXTS):raise ValueError("must supply all three source contexts")
        for block in FOUNDER_BLOCKS:
            reference_founder=None
            for context in sorted(CONTEXTS):
                z=zips[context]
                with np.load(io.BytesIO(z.read(f"{block}_c{context}_r0.npz")),allow_pickle=False) as a:
                    first=int(a['offsets'][1]-a['offsets'][0]);original=np.asarray(a['alleles'][:first])
                    archive_totals=np.asarray(a['returns'][0],dtype=np.float64)
                    metadata=json.loads(str(a['metadata'].item()))
                    if first!=48 or original.shape!=(48,3,2):raise ValueError("source population changed")
                    c=CONTEXTS[context]
                    task=metadata['task']
                    if task['block']!=block or task['context']!=context or task['replicate']!=0 or task['supply']!=c['supply'] or task['composition']!=c['composition']:
                        raise ValueError("source task mismatch")
                    if reference_founder is None:reference_founder=original
                    elif not np.array_equal(reference_founder,original):raise ValueError("initial founder drift by visitor context")
                    config=SimpleNamespace(**metadata['config'])
                    if config.capacity!=48 or config.mutation_rate!=.01 or config.mutation_sd!=.05 or config.assurance_mode!='evolving' or config.investment_cost!=.5 or config.assurance_cost!=.5 or config.depression!=.5:
                        raise ValueError("original fixed source config not the planned factorial")
                    if not np.isclose(config.activity,.4*c['supply'],atol=0,rtol=0):raise ValueError("activity context mismatch")
                    optics=np.array(c['optima'],dtype=float)
                    visitor=SimpleNamespace(ids=np.arange(len(optics),dtype=np.int64),optima=optics,breadths=np.full(len(optics),config.visitor_breadth),effectiveness=np.full(len(optics),config.visitor_effectiveness))
                    model_state=SimpleNamespace(ids=np.asarray(a['ids'][:48]),alleles=original)
                    original_ledger=source_ledger(reproduction,model_state,visitor,config)
                    oldtot=original_totals(original_ledger)
                    err=float(np.max(np.abs(archive_totals-oldtot)))
                    if err>1e-12:
                        raise ValueError("exact source reproductive ledger does not reproduce archived original totals")
                    baseline=checksum_ledger(original_ledger)
                    for w in A_HALF_WIDTHS:
                        for h in I_HOMOLOG_SCALE:
                            changed,transformed=transform(original,w,h)
                            new_state=SimpleNamespace(ids=model_state.ids.copy(),alleles=changed)
                            ledger=source_ledger(reproduction,new_state,visitor,config)
                            score=checksum_ledger(ledger)
                            if score!=baseline:
                                raise ValueError("genotype transformation altered t0 maternal/paternal/self/pollen ledger")
                            rows.append({"block":block,"original_context":context,"A_half_width":w,"I_homolog_scale":h,
                                         "source_original_ledger_sha256":baseline,"source_new_ledger_sha256":score,
                                         "t0_all_individual_expressed_traits_preserved":transformed['I_individual_expressed_traits_all_preserved'],
                                         "exact_ledger_bitwise_equal":True,
                                         "original_recorded_total_max_error":err})
    finally:
        for z in zips.values():z.close()
    assert len(rows)==2*3*4
    return {"schema":"chapter2_clock_factorial_original_t0_reproductive_ledger_v1",
            "status":"SIX_ORIGINAL_SOURCE_STATES_TWENTY_FOUR_GENOTYPE_CONTRAST_LEDGERS_EXACT",
            "original_reproduction_git_blob":ORIGINAL_NATIVE_REPRO_GIT_BLOB,
            "original_provider_receipts":sorted(receipts,key=lambda x:x['context']),
            "original_founder_by_context_source_states":6,
            "genotype_adjusted_fixed_state_ledger_calls":24,
            "original_source_reference_ledger_calls":6,
            "new_biological_histories":0,"population_advance_called":False,
            "all_original_totals_match":True,"all_adjusted_ledger_hashes_match_original":True,
            "max_recorded_total_error":max(r['original_recorded_total_max_error'] for r in rows),
            "records":rows,
            "limitations":["Original SHA-locked reproduction.py executed with source config and original restored visitor functional values; technical SimpleNamespace receivers do not replace the source model class validations.",
                           "This check stops before any population advance, mutation or stochastic offspring production and is not evidence of future evolutionary equivalence.",
                           "Original archive source is validated by archived totals and immutable biological-commit reproduction SHA; future pilot must validate full genotype/parentage birth operator and orchestrator separately."]}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for c in sorted(CONTEXTS):p.add_argument('--original-shard-'+str(c),type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    paths={c:getattr(a,'original_shard_'+str(c)) for c in CONTEXTS}
    out=check(paths)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    with a.out.open('x',encoding='utf8',newline='\n') as f:
        json.dump(out,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({"status":out['status'],"ledger_calls":out['genotype_adjusted_fixed_state_ledger_calls'],"max_error":out['max_recorded_total_error']}))

if __name__=='__main__':main()
