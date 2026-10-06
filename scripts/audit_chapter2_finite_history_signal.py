"""Exploratory exact-source diagnostic for finite history signal in the Chapter 2 bridge.

Reads the compact verified shard exports from the original prospective bridge
workflow. No simulation is rerun. This diagnostic is explicitly post-hoc.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np

PAIRS={
    "natural":("near","far"),
    "richness_matched":("matched_near","matched_far"),
    "visitor_pooled":("pool_near","pool_far"),
    "large_plant_capacity":("large_near","large_far"),
}

def _load(folder: Path):
    docs=[]
    for p in sorted(folder.glob("shard-*.json")):
        d=json.loads(p.read_text())
        if d["status"]!="complete_verified_shard_export":
            raise ValueError(f"incomplete shard {p}")
        docs.append(d)
    if len(docs)!=16:
        raise ValueError(f"expected 16 verified shard exports, got {len(docs)}")
    histories=sorted(h for d in docs for h in d["history_seeds"])
    if len(histories)!=128 or len(set(histories))!=128:
        raise ValueError("history support mismatch")
    starts=docs[0]["starts"]; demos=docs[0]["demographic_seeds"]
    shape=(len(starts),len(histories),len(demos)); hi={h:i for i,h in enumerate(histories)}
    values={k:np.full(shape,np.nan) for k in docs[0]["values"]}
    for d in docs:
        hs=d["history_seeds"]
        for key,raw in d["values"].items():
            a=np.asarray(raw,float)
            if a.shape!=(len(starts),len(hs),len(demos)):
                raise ValueError((key,a.shape))
            for j,h in enumerate(hs):
                values[key][:,hi[h],:]=a[:,j,:]
    return histories,starts,demos,values

def _varcomp(x):
    x=np.asarray(x,float); a,b,n=x.shape
    gm=x.mean(); ms=x.mean(axis=(1,2)); mh=x.mean(axis=(0,2)); msh=x.mean(axis=2)
    ss_h=a*n*np.sum((mh-gm)**2)
    ss_sh=n*np.sum((msh-ms[:,None]-mh[None,:]+gm)**2)
    ss_e=np.sum((x-msh[:,:,None])**2)
    mh_ms=ss_h/(b-1); sh_ms=ss_sh/((a-1)*(b-1)); e_ms=ss_e/(a*b*(n-1))
    sig_h=max(0.0,(mh_ms-sh_ms)/(a*n))
    sig_sh=max(0.0,(sh_ms-e_ms)/n)
    hist=sig_h+sig_sh
    icc=hist/(hist+e_ms)
    rel=hist/(hist+e_ms/n)
    first=x[:,:,:n//2].mean(axis=(0,2)); last=x[:,:,n//2:].mean(axis=(0,2))
    corr=float(np.corrcoef(first,last)[0,1])
    return np.array([sig_h,sig_sh,e_ms,icc,rel,corr],float)

def _label(v,eps):
    pos=np.any(v>eps); neg=np.any(v<-eps)
    return "mixed" if pos and neg else "positive" if pos else "negative" if neg else "neutral"

def _all_balanced_split_half(x):
    from itertools import combinations
    idx=range(x.shape[2]); out=[]
    # Keep only combinations containing repeat index 0 to avoid duplicate complements.
    for comb in combinations(idx,x.shape[2]//2):
        if 0 not in comb:
            continue
        a=np.asarray(comb,int)
        b=np.asarray([i for i in idx if i not in comb],int)
        va=x[:,:,a].mean(axis=(0,2))
        vb=x[:,:,b].mean(axis=(0,2))
        out.append(float(np.corrcoef(va,vb)[0,1]))
    if len(out)!=35:
        raise ValueError(f"expected 35 unique balanced splits, got {len(out)}")
    return np.asarray(out,float)

def _sign(x,eps):
    labels=[]; disagree=0
    for h in range(x.shape[1]):
        b=x[:,h,:]
        labels.append(_label(b.mean(axis=1),eps))
        labs=[_label(b[:,hrep],eps) for hrep in range(x.shape[2])]
        disagree+=int(len(set(labs))>1)
    return {"mixed":labels.count("mixed"),"repeat_disagreement":disagree}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input-dir",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    a=ap.parse_args()
    histories,starts,demos,values=_load(a.input_dir)
    tensors={name:values[f"{far}|individual"]-values[f"{near}|individual"] for name,(near,far) in PAIRS.items()}
    point={}
    for name,x in tensors.items():
        vc=_varcomp(x)
        point[name]={
            "mean_effect":float(x.mean()),
            "sigma_history":float(vc[0]),
            "sigma_start_by_history":float(vc[1]),
            "sigma_demographic_residual":float(vc[2]),
            "single_trajectory_icc":float(vc[3]),
            "eight_repeat_reliability":float(vc[4]),
            "split_half_history_correlation":float(vc[5]),
            "sign_eps0":_sign(x,0.0),
            "sign_eps0_01":_sign(x,0.01),
        }
    rng=np.random.default_rng(927032); boots={k:[] for k in tensors}
    for _ in range(1999):
        ix=rng.integers(0,len(histories),len(histories))
        for name,x in tensors.items():
            boots[name].append(_varcomp(x[:,ix,:]))
    for name in boots:
        b=np.vstack(boots[name])
        for j,key in enumerate(("sigma_history","sigma_start_by_history","sigma_demographic_residual","single_trajectory_icc","eight_repeat_reliability","split_half_history_correlation")):
            point[name][key+"_ci95"]=np.quantile(b[:,j],[.025,.975]).tolist()
    split={name:_all_balanced_split_half(x) for name,x in tensors.items()}
    def ss(v):
        return {
            "min":float(v.min()),"q05":float(np.quantile(v,.05)),
            "median":float(np.median(v)),"mean":float(v.mean()),
            "q95":float(np.quantile(v,.95)),"max":float(v.max()),
        }
    robust={name:ss(v) for name,v in split.items()}
    robust["paired_difference_vs_natural"]={}
    for name in ("large_plant_capacity","visitor_pooled"):
        d=split[name]-split["natural"]
        robust["paired_difference_vs_natural"][name]={
            **ss(d),"positive_splits":int(np.sum(d>0)),"total_splits":int(len(d))
        }
    out={
        "status":"complete_posthoc_exact_source_finite_history_signal_diagnostic",
        "histories":len(histories),"starts":starts,"demographic_seeds":demos,
        "estimates":point,
        "balanced_split_half_robustness":{
            "method":"all 35 unique 4-versus-4 demographic-repeat partitions",
            **robust,
        },
        "claim_boundary":"exploratory post-hoc diagnostic; not a preregistered test or natural variance-component estimate",
    }
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
