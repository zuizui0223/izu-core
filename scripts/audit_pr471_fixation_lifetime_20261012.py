"""Retrospective first-fixation and finite-horizon lifetime accounting for PR471.

No new biology or random histories. Reads the immutable saved-matrix ZIP;
new quantities do not replace the original 80-update endpoint. A probability
conditional on fixation is descriptive, not an independent causal effect.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import itertools
import json
from pathlib import Path
import platform
import zipfile
import numpy as np

ARCHIVE_SHA = '1f58a0f0988d1215a53ea50aa30ece049a37da4a0cd459a72a44f2f05065a783'
KERNEL_SHA = '9d13fe6d116e2c0ef7e08658fa9d9488cb7320e8e7cab2ecc9946e0780a852c3'
NATIVE_SHA = 'b7f3814d682095e91783db0e4cebef2f0eb235835ff71de68e3ad28bb3c3ca84'
SETTINGS = ('delayed_control','prior_selfing','pollen_discount','assurance_cost')
ARMS = ('shifted4','original4_statewise_equal_delivery')
HORIZON = 80
TOL = 1e-12


def masks_and_validate(T, states, p0, horizon):
    s=np.asarray(states)
    if type(horizon) is not int or horizon < 1:
        raise ValueError('positive integer horizon required')
    if s.ndim!=2 or s.shape[1]!=3 or not np.issubdtype(s.dtype,np.integer):
        raise ValueError('integer low/heterozygote/high genotype states required')
    if (s<0).any() or len(np.unique(s,axis=0))!=len(s):
        raise ValueError('nonnegative unique genotype states required')
    n=len(s); census=s.sum(1)
    if census[0]!=0 or np.count_nonzero(census==0)!=1:
        raise ValueError('unique extinction state must be first')
    if T.shape!=(n,n) or not np.isfinite(T).all() or (T<0).any():
        raise ValueError('invalid kernel entries')
    if not np.allclose(T.sum(1),1.,atol=1e-11,rtol=0):
        raise ValueError('kernel row probability mass differs from one')
    if not np.array_equal(T[0],np.eye(n)[0]):
        raise ValueError('extinction must be absorbing')
    if p0.shape!=(n,) or not np.isfinite(p0).all() or (p0<0).any():
        raise ValueError('invalid initial probabilities')
    if abs(p0.sum()-1)>TOL or p0[0]!=0:
        raise ValueError('all initial starts must be living')
    low=(s[:,0]>0)&(s[:,1:]==0).all(1)
    high=(s[:,2]>0)&(s[:,:2]==0).all(1)
    seg=(census>0)&~(low|high)
    for g in (low,high):
        forbidden=~g;forbidden[0]=False
        if np.any(T[np.ix_(g,forbidden)]>TOL):
            raise ValueError('fixed genetic classes must not leave except by extinction')
    return low,high,seg


def analyze_kernel(T, states, p0, horizon=HORIZON):
    """Count first entries, not repeated fixed censuses; retain extinct starts."""
    T=np.asarray(T,dtype=float);p0=np.asarray(p0,dtype=float)
    low,high,seg=masks_and_validate(T,states,p0,horizon)
    gs=(low,high,seg);n=len(states)
    p=np.zeros((horizon+1,n));p[0]=p0
    entries=np.zeros((horizon+1,2));entries[0]=[p0[low].sum(),p0[high].sum()]
    deaths=np.zeros((horizon+1,3))
    # Separate renewal recursion uses only S->S, S->L/H and L/H->L/H blocks.
    q=p0[seg].copy();ell=p0[low].copy();hh=p0[high].copy()
    alt_error=0.;rows=[]
    for t in range(horizon+1):
        if t:
            prior=p[t-1]
            entries[t]=[float(prior[seg]@T[np.ix_(seg,g)].sum(1)) for g in (low,high)]
            deaths[t]=deaths[t-1]+[float(prior[g]@T[g,0]) for g in gs]
            p[t]=prior@T
            entry_l=q@T[np.ix_(seg,low)];entry_h=q@T[np.ix_(seg,high)]
            ell=ell@T[np.ix_(low,low)]+entry_l
            hh=hh@T[np.ix_(high,high)]+entry_h
            q=q@T[np.ix_(seg,seg)]
            for got,want in ((ell,p[t,low]),(hh,p[t,high]),(q,p[t,seg])):
                if len(got): alt_error=max(alt_error,float(np.max(abs(got-want))))
        reached=entries[:t+1].sum(0)
        rows.append({'update':t,'occupied':float(p[t,1:].sum()),
                     'low_fixed_alive':float(p[t,low].sum()),
                     'high_fixed_alive':float(p[t,high].sum()),
                     'segregating_alive':float(p[t,seg].sum()),
                     'low_first_entry':float(entries[t,0]),'high_first_entry':float(entries[t,1]),
                     'ever_low_fixed':float(reached[0]),'ever_high_fixed':float(reached[1]),
                     'extinct_after_low':float(deaths[t,0]),'extinct_after_high':float(deaths[t,1]),
                     'extinct_before_fixation':float(deaths[t,2])})
    occ=p[:,1:].sum(1);reach=entries.sum(0)
    terminal=np.array([p[-1,g].sum() for g in gs])
    lifetime=float(occ[:-1].sum())  # E[min(tau_extinction,H)] = sum[t=0..H-1] P(N_t>0)
    alive=np.r_[0.,np.ones(n-1)];reward=np.zeros(n)
    for _ in range(horizon): reward=alive+T@reward
    death_time_mass=np.diff(p[:,0])
    from_extinction=float(np.arange(1,horizon+1)@death_time_mass+horizon*occ[-1])
    errors={'renewal_vs_full_forward':alt_error,
            'row_mass':float(np.max(abs(T.sum(1)-1))),
            'forward_mass':float(np.max(abs(p.sum(1)-1))),
            'extinction_partition':float(np.max(abs(deaths.sum(1)-p[:,0]))),
            'first_entry_partition':float(np.max(abs(reach-terminal[:2]-deaths[-1,:2]))),
            'lifetime_backward':abs(float(p0@reward)-lifetime),
            'lifetime_extinction_time':abs(from_extinction-lifetime),
            'six_terminal_partitions':abs(float(terminal.sum()+deaths[-1].sum())-1)}
    if max(errors.values())>1e-10: raise ArithmeticError('independent accounting disagreement')
    summary={'horizon':horizon,'restricted_mean_time_to_extinction':lifetime,
             'expected_occupied_censuses_1_to_H':float(occ[1:].sum()),
             'P_H_occupied':float(occ[-1]),'P_H_low_fixed_alive':float(terminal[0]),
             'P_H_high_fixed_alive':float(terminal[1]),'P_H_segregating_alive':float(terminal[2]),
             'P_low_fixed_ever_by_H':float(reach[0]),'P_high_fixed_ever_by_H':float(reach[1]),
             'P_extinct_after_low_fixation_by_H':float(deaths[-1,0]),
             'P_extinct_after_high_fixation_by_H':float(deaths[-1,1]),
             'P_extinct_before_fixation_by_H':float(deaths[-1,2])}
    for j,label in enumerate(('low','high')):
        summary[f'P_H_occupied_given_{label}_fixation_by_H']=float(terminal[j]/reach[j]) if reach[j]>0 else None
        summary[f'mean_{label}_fixation_update_given_fixed_by_H']=float(np.arange(horizon+1)@entries[:,j]/reach[j]) if reach[j]>0 else None
    return {'summary':summary,'timeseries':rows,'verification':{**errors,'max_error':max(errors.values())}}


def load_inputs(archive,native_archive):
    raw=Path(archive).read_bytes();nat=Path(native_archive).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=ARCHIVE_SHA or hashlib.sha256(nat).hexdigest()!=NATIVE_SHA:
        raise ValueError('immutable input ZIP hash mismatch')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        k=z.read('pr471_all_96_kernels.npz')
        if hashlib.sha256(k).hexdigest()!=KERNEL_SHA:raise ValueError('kernel hash mismatch')
        with np.load(io.BytesIO(k),allow_pickle=False) as a:
            states=a['states'].copy();keys=a['keys'].copy();Ts=a['kernels'].copy()
    expected_s=np.array([(l,h,n-l-h) for n in range(9) for l in range(n+1) for h in range(n-l+1)])
    expected_keys={f'{f}_{s}_{b}_{p}_{a}' for f,s,b,p,a in itertools.product((.25,.5,1.),SETTINGS,(6.,8.),('native','fixed_expression'),ARMS)}
    if not np.array_equal(states,expected_s) or Ts.shape!=(96,165,165) or set(keys)!=expected_keys or len(keys)!=96:
        raise ValueError('complete source matrix domain required')
    with zipfile.ZipFile(io.BytesIO(nat)) as z:
        for name,item in json.loads(z.read('manifest.json')).items():
            content=z.read(name)
            if len(content)!=item['size_bytes'] or hashlib.sha256(content).hexdigest()!=item['sha256']:
                raise ValueError('native payload hash mismatch')
        actual=json.loads(z.read('native_output.json'))
    return states,dict(zip(keys,Ts)),actual


def write_csv(path,rows):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def run(archive,native_archive,out):
    states,kernels,native=load_inputs(archive,native_archive)
    p0=np.zeros(165);p0[np.flatnonzero((states==[0,8,0]).all(1))[0]]=1
    originals={(r['mismatch_fraction'],r['setting'],r['budget']):r for r in native['results']}
    all_rows=[];series=[];paired=[];checks=[];postfix=[];endpoint_errors=[]
    for frac,setting,budget,arm in itertools.product((.25,.5,1.),SETTINGS,(6.,8.),ARMS):
        meta={'mismatch_fraction':frac,'setting':setting,'budget':budget,'visitor_arm':arm}
        a={}
        for policy in ('native','fixed_expression'):
            key=f'{frac}_{setting}_{budget}_{policy}_{arm}';T=kernels[key]
            a[policy]=analyze_kernel(T,states,p0)
            r=a[policy]['summary'];all_rows.append({**meta,'expression_policy':policy,**r})
            series.extend({**meta,'expression_policy':policy,**x} for x in a[policy]['timeseries'])
            checks.append({'key':key,**a[policy]['verification']})
            expected=originals[frac,setting,budget]['full_arms'][policy+'|'+arm]
            for val,want in ((r['P_H_occupied'],expected['P80_occupied']),
                             (r['P_H_low_fixed_alive'],expected['P80_low_allele_fixed_and_occupied']),
                             (r['P_H_low_fixed_alive']/r['P_H_occupied'],expected['P80_low_allele_fixed_given_occupied'])):
                endpoint_errors.append(abs(val-want))
        A=a['native']['summary'];B=a['fixed_expression']['summary']
        deltas={f'delta_{k}':A[k]-B[k] for k in A if k!='horizon' and A[k] is not None and B[k] is not None}
        paired.append({**meta,**deltas,'positive_endpoint_negative_lifetime':
                       bool(deltas['delta_P_H_occupied']>TOL and deltas['delta_restricted_mean_time_to_extinction']< -TOL)})
        # Standardize both entry census and remaining duration after fixation.
        # No empirical pathway or fixation-selected groups are interchanged here.
        Tn=kernels[f'{frac}_{setting}_{budget}_native_{arm}'];Tf=kernels[f'{frac}_{setting}_{budget}_fixed_expression_{arm}']
        low,high,_=masks_and_validate(Tn,states,p0,HORIZON)
        for name,g in (('low_fixed',low),('high_fixed',high)):
            vn=np.ones(g.sum());vf=vn.copy();blockn=Tn[np.ix_(g,g)];blockf=Tf[np.ix_(g,g)]
            for duration in range(1,HORIZON+1):
                vn=blockn@vn;vf=blockf@vf
                for n,x,y in zip(states[g].sum(1),vn,vf):
                    postfix.append({**meta,'fixed_class':name,'entry_census':int(n),
                                    'remaining_updates':duration,'native_survival':float(x),
                                    'fixed_expression_survival':float(y),'contrast':float(x-y)})
    if len(endpoint_errors)!=288 or max(endpoint_errors)>TOL:
        raise ArithmeticError('source kernel native endpoint disagreement')
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    write_csv(out/'pr471_fixation_lifetime_arms.csv',all_rows)
    write_csv(out/'pr471_fixation_lifetime_pairs.csv',paired)
    write_csv(out/'pr471_fixation_first_passage_timeseries.csv',series)
    write_csv(out/'pr471_standardized_postfixation_survival.csv',postfix)
    result={'schema':'pr471_retrospective_fixation_lifetime_v1','status':'ALL_96_SAVED_KERNELS_ACCOUNTED',
            'horizon':HORIZON,'kernels':96,'contexts':24,'paired_comparisons':48,
            'new_random_histories':0,'native_source_reexecuted':False,
            'source_archive_sha256':ARCHIVE_SHA,'kernel_member_sha256':KERNEL_SHA,'native_archive_sha256':NATIVE_SHA,
            'inference':'Retrospective saved-matrix diagnostics; no changed primary endpoint or causal mediation.',
            'lifetime_definition':'E[min(tau_extinction,80)]=sum[t=0..79] P(N_t>0); not uncensored lifetime.',
            'first_fixation_definition':'First census fixed for low or high allele before extinction, counted once; extinct starts retained.',
            'conditional_fixation_boundary':'P(occupied at80 | reached fixation by80) mixes entry times/censuses and is not a causal effect.',
            'standardized_postfixation_boundary':'Common fixed genotype, census1..8 and remaining1..80 updates; model expression-policy contrast, not natural-history mediation.',
            'native_endpoint_checks':288,'native_endpoint_max_error':max(endpoint_errors),
            'max_accounting_error':max(x['max_error'] for x in checks),
            'runtime':{'python':platform.python_version(),'numpy':np.__version__},
            'kernel_checks':checks,'arm_summaries':all_rows,'paired_results':paired}
    (out/'pr471_fixation_lifetime_results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('kernel_checks','arm_summaries','paired_results')},indent=2))
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--archive',type=Path,required=True);ap.add_argument('--native-archive',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();run(args.archive,args.native_archive,args.out)
