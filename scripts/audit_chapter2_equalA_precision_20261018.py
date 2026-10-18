"""Read-only review of PR597's completed equal-A PILOT event records.

No native biological operators, new evolutionary paths, source retuning, or
confirmatory claims. Exact enumeration is of the empirical pigeonhole
bootstrap distribution, NOT exact confidence-interval coverage.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
from statistics import NormalDist
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'docs/audits/CHAPTER2_EQUALA_PILOT_EVENT_SOURCE_20261018.json'


def compositions(total,parts):
    if parts==1:
        yield (total,)
    else:
        for i in range(total+1):
            for rest in compositions(total-i,parts-1):
                yield (i,)+rest


def exact_pigeonhole(x):
    """Resample independent founder and visitor levels, preserving paired arms.

    Each cell's two replicate differences are averaged, not treated as two
    independent source axes. Enumerate count vectors with integer multinomial
    multiplicities. Nominal percentile intervals are exploratory at six levels.
    """
    x=np.asarray(x)
    if x.ndim!=3 or min(x.shape)<1 or max(x.shape[:2])>6 or x.dtype.kind not in 'iu':
        raise ValueError('integer score array with each independent axis <=6 required')
    nf,nv,nr=x.shape
    def axis(n):
        c=np.array(list(compositions(n,n)),dtype=np.int64)
        m=np.array([math.factorial(n)//math.prod(math.factorial(int(v)) for v in a)
                    for a in c],dtype=np.int64)
        if m.sum()!=n**n:raise AssertionError('multinomial mass')
        return c,m
    cf,mf=axis(nf);cv,mv=axis(nv)
    num=(cf@x.sum(axis=2)@cv.T).ravel()
    weights=(mf[:,None]*mv[None,:]).ravel()
    values,inv=np.unique(num,return_inverse=True)
    masses=np.zeros(len(values),dtype=np.int64)
    np.add.at(masses,inv,weights)
    total=int(masses.sum());den=nf*nv*nr
    if total!=nf**nf*nv**nv:raise AssertionError('joint weight mismatch')
    cumulative=np.cumsum(masses)
    def quantile(p):
        q=Fraction(p)
        threshold=(q.numerator*total+q.denominator-1)//q.denominator
        return float(values[np.searchsorted(cumulative,threshold)]/den)
    mean=float(np.dot(values.astype(float),masses)/total/den)
    if not math.isclose(mean,float(x.mean()),abs_tol=1e-12):
        raise AssertionError('reweighting mean differs')
    return dict(mean=mean,lower95=quantile('0.025'),upper95=quantile('0.975'),
                lower975=quantile('0.0125'),upper975=quantile('0.9875'),
                ordered_resample_weight=total,count_vector_pairs=len(weights),
                scope='Exact empirical bootstrap weights; nominal percentile coverage NOT exact; post-outcome sensitivity only.')


def variance_components(x):
    x=np.asarray(x,dtype=float)
    if x.ndim!=3 or min(x.shape)<2 or not np.isfinite(x).all():
        raise ValueError('balanced two-axis repeats required')
    nf,nv,nr=x.shape;g=x.mean();f=x.mean((1,2));v=x.mean((0,2));c=x.mean(2)
    mf=nv*nr*np.sum((f-g)**2)/(nf-1)
    mv=nf*nr*np.sum((v-g)**2)/(nv-1)
    mi=nr*np.sum((c-f[:,None]-v[None,:]+g)**2)/((nf-1)*(nv-1))
    me=np.sum((x-c[:,:,None])**2)/(nf*nv*(nr-1))
    return dict(founder=max(0.,float((mf-mi)/(nv*nr))),
                visitor=max(0.,float((mv-mi)/(nf*nr))),
                interaction=max(0.,float((mi-me)/nr)),within_cell=float(me))


def mde_proxy(var,nf,nv,nr):
    if min(nf,nv)<3 or nr<1 or any(v<0 or not math.isfinite(v) for v in var.values()):
        raise ValueError('invalid proxy inputs')
    # Source #585 convention: familywise .05 and joint .8 across two outcomes.
    z=NormalDist().inv_cdf(1-.05/4)+NormalDist().inv_cdf(.9)
    se2=var['founder']/nf+var['visitor']/nv+(var['interaction']+var['within_cell']/nr)/(nf*nv)
    return z*math.sqrt(se2)


def review(data):
    if (data.get('schema')!='chapter2_equalA_pilot_events_ci_v1'
        or data['source']['ci_run_id']!=39106340477
        or data['source']['head_sha']!='cc17c7355d27b907b71b124046990b914e4963dd'
        or data.get('all_144_paths_alive_at_80') is not True):
        raise ValueError('wrong source or unsupported extinct event summary')
    def array(key,nullable=True):
        raw=data[key]
        if len(raw)!=6 or any(len(row)!=12 for row in raw):raise ValueError('missing cells')
        if any(not ((t is None and nullable) or (type(t) is int and 1<=t<=80))
               for row in raw for t in row):raise ValueError('bad event time or zero-filled null')
        return np.array([[81 if t is None else t for t in row] for row in raw],dtype=np.int64).reshape(6,6,2)
    f=array('first_I_loss_fixed');e=array('first_I_loss_evolving');a=array('first_A_loss_evolving',False)
    fl=f<=80;el=e<=80;d=el.astype(int)-fl.astype(int);dt=e-f
    c=variance_components(d);saved=data['logged_summary']
    if (int(fl.sum())!=saved['I_losses']['fixed'] or int(el.sum())!=saved['I_losses']['evolving']):
        raise ValueError('event counts differ from logged summary')
    for name,x in (('fixed',f),('evolving',e)):
        if not math.isclose(float(x.mean()),saved['accessible_census_time_inclusive_0_80'][name],abs_tol=1e-10):
            raise ValueError('restricted access time differs from source')
    for k,v in c.items():
        if not math.isclose(v,saved['paired_I_loss_components'][k],abs_tol=1e-12):
            raise ValueError('paired variance differs from source')
    joint={'neither':int((~fl&~el).sum()),'evolving_only':int((~fl&el).sum()),
           'fixed_only':int((fl&~el).sum()),'both':int((fl&el).sum())}
    sensitivity=[]
    # Explicit assumption, NOT an estimated upper confidence limit. Keeps both
    # independent source variances nonzero despite truncated visitor estimate.
    stress=dict(founder=.05,visitor=.05,interaction=.2,within_cell=.4)
    for n in (6,12,16,24,32,48,64):
        sensitivity.append(dict(founders=n,visitors=n,repeats=2,paths=4*n*n,
          updates=320*n*n,baseline_I_loss_MDE=mde_proxy(c,n,n,2),
          assumed_stress_I_loss_MDE=mde_proxy(stress,n,n,2)))
    return dict(
      status='POST_OUTCOME_EQUALA_PILOT_SOURCE_REVIEW_NOT_CONFIRMATION',
      source_event_sha256=hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
      source_run=39106340477,counts=dict(fixed_high_I_loss=int(fl.sum()),evolving_high_I_loss=int(el.sum()),
        per_policy=72,founders=6,visitors=6,nested_repeats=2,all_alive=144),
      risk_difference=float(d.mean()),
      accessible_census_time={'fixed':float(f.mean()),'evolving':float(e.mean())},
      restricted_access_census_difference=float(dt.mean()),
      time_unit='count of accessible censuses among t=0..80 inclusive (81 slots), not exact no-return time',
      bootstrap_risk=exact_pigeonhole(d),bootstrap_access_time=exact_pigeonhole(dt),
      paired_joint_I_loss_counts=joint,
      paired_risk_variance_components=c,
      per_founder_risk_differences=d.mean((1,2)).tolist(),
      per_visitor_risk_differences=d.mean((0,2)).tolist(),
      CIF_G_strictly_before_TE={'fixed':int((f<35).sum()),'evolving':int((e<35).sum())},
      evolving_A_support_loss_by_80=int((a<=80).sum()),
      survival_endpoint_is_saturated=True,
      prospective_precision_sensitivity=sensitivity,
      adverse_scenario_is_assumption_not_estimated_bound=stress,
      formal_confirmation_authorized=False,
      gate_status='HOLD: six independent levels per axis; survival has no events; no justified SESOI/adverse variance/full joint-power decision.',
      limits=[
        'All event times transcribed from CI summaries; no independently validated genotype archive in this review.',
        'Crossed seed draws: 144 paths and 72 matched pairs are not 144/72 independent island systems.',
        'Bootstrap resamples each independent axis, retains both policies and averages nested repeats; no exact finite-sample coverage guarantee.',
        '97.5% marginal intervals are a post-outcome two-endpoint sensitivity, not a retrospectively registered test.',
        'The 42/72 vs 58/72 contrast suggests faster/larger genetic closure under this policy and model, not a confirmed universal effect.',
        'All groups survived: no rescue benefit or statistical equivalence in survival is established.',
        'No actual restored-descendant trajectories, natural islands, stochastic recovery t-star or mediation measured.',
        'No new biological simulations executed by this arithmetic audit; no old results, seeds or original protocols modified.'
      ])


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,default=SOURCE)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    if args.out.exists():p.error('refuse overwrite')
    result=review(json.loads(args.source.read_text(encoding='utf8')))
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n',encoding='utf8')
    print(json.dumps({k:result[k] for k in ('status','counts','risk_difference','bootstrap_risk','gate_status')}))
