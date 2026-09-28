"""Prespecified paired-history summaries; no outcome-driven selection or stopping."""
import numpy as np
from scripts.audit_model3_ch2_bridge import classify_histories
from scripts.model3_island.summarize import decompose_crossed

THRESHOLDS=(0.,.01,.05)


def paired_mean(values):
    x=np.asarray(values,float)
    if x.ndim!=3 or min(x.shape)<1:raise ValueError('expected starts x histories x demographic repeats')
    valid=np.isfinite(x);n=int(valid.sum());sums=np.where(valid,x,0).sum(axis=(0,2));counts=valid.sum(axis=(0,2))
    m=float(sums.sum()/n) if n else None
    ci=None
    if (counts>0).sum()>=2:
        draw=np.random.default_rng(927032).integers(0,x.shape[1],(1999,x.shape[1]))
        den=counts[draw].sum(axis=1);keep=den>0
        if keep.sum()>=1900:ci=np.quantile(sums[draw].sum(axis=1)[keep]/den[keep],[.025,.975]).tolist()
    return {'mean':m,'mean_ci':ci,'n_pairs':int(x.size),'n_eligible_pairs':n,'n_histories':x.shape[1],
            'n_histories_with_eligible_pairs':int((counts>0).sum()),
            'conditional_mean_half_width_met':None if ci is None else (ci[1]-ci[0])/2<=.025,
            'scope':'joint-survivor conditional mean; cluster resampling whole independent histories, not demographics'}


def effect_report(near,far):
    near=np.asarray(near,float);far=np.asarray(far,float)
    if near.shape!=far.shape:raise ValueError('paired support differs')
    delta=far-near
    report=paired_mean(delta)
    report['mean_by_start']=[paired_mean(delta[i:i+1]) for i in range(len(delta))]
    report['classification']=[classify_histories(delta,e) for e in THRESHOLDS]
    report['repeat_label_disagreement']=report['classification'][0]['repeat_disagreements']
    report['split_half_disagreement']=[]
    cut=delta.shape[2]//2
    if cut:
        for e in THRESHOLDS:
            a=classify_histories(delta[:,:,:cut],e)['labels'];b=classify_histories(delta[:,:,cut:],e)['labels']
            report['split_half_disagreement'].append({'epsilon':e,'count':sum(x!=y for x,y in zip(a,b)),
                'eligible_both':sum(x!='undefined' and y!='undefined' for x,y in zip(a,b)),
                'mixed_in_both':sum(x==y=='mixed' for x,y in zip(a,b))})
    report['decomposition']=decompose_crossed(delta,{'S':[1/len(delta)]*len(delta),'C':[1/delta.shape[1]]*delta.shape[1]})
    return report


def compare_effects(reference,intervention):
    a=np.asarray(reference,float);b=np.asarray(intervention,float)
    if a.shape!=b.shape:raise ValueError('paired intervention support differs')
    differences=[]
    for e in THRESHOLDS:
        aa=classify_histories(a,e)['labels'];bb=classify_histories(b,e)['labels']
        keep=np.array([x!='undefined' and y!='undefined' for x,y in zip(aa,bb)])
        v=np.array([int(y=='mixed')-int(x=='mixed') for x,y in zip(aa,bb)],float)
        v[~keep]=np.nan;r=paired_mean(v[None,:,None])
        differences.append({'epsilon':e,'mean_difference':r['mean'],'ci':r['mean_ci'],
            'n_eligible_histories':int(keep.sum()),'scope':'paired difference of descriptive mixed labels; finite-repeat uncertainty remains'})
    return {'mean_difference':paired_mean(b-a),'mixed_fraction_differences':differences}

def bounded_history_mean(values,low,high):
    """Conservative unconditional bounds, including all-zero/all-one samples."""
    x=np.asarray(values,float)
    if x.ndim!=3 or not np.isfinite(x).all() or np.any(x<low) or np.any(x>high) or high<=low:
        raise ValueError('complete bounded history observations required')
    m=float(x.mean());half=(high-low)*np.sqrt(np.log(40)/(2*x.shape[1]))
    return {'mean':m,'mean_ci':[max(low,m-half),min(high,m+half)],'n_histories':x.shape[1],
        'n_observations':int(x.size),'interval':'95% independent-history Hoeffding bound',
        'unconditional':True}
