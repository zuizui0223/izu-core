"""Ecological endpoints with explicit extinction and independent-history denominators."""
import argparse
from collections import defaultdict
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import csv
import json

import numpy as np

from .design import compile_design,digest,canonical


def _mean(x):
    x=np.asarray(x,dtype=float); x=x[np.isfinite(x)]
    return float(x.mean()) if len(x) else None


def _cluster_ci(values, histories, *, bounded=False):
    """Fixed-size cluster bootstrap for means; bounded occupancy uses Hoeffding.

    Conditional traits use a ratio of totals after resampling histories, preserving
    missing/extinct observations. No nominal interval from one independent history.
    """
    values=np.asarray(values,dtype=float); histories=np.asarray(histories)
    ids=np.unique(histories)
    if bounded:
        means=np.array([values[histories==i].mean() for i in ids])
        if not len(means): return None
        half=np.sqrt(np.log(40)/(2*len(means)))
        return [float(max(0.,means.mean()-half)),float(min(1.,means.mean()+half))]
    eligible=[i for i in ids if np.isfinite(values[histories==i]).any()]
    if len(eligible)<2:
        return None
    sums=np.array([np.nansum(values[histories==i]) for i in ids])
    counts=np.array([np.isfinite(values[histories==i]).sum() for i in ids])
    rng=np.random.default_rng(91821)
    draws=rng.integers(0,len(ids),(1999,len(ids)))
    totals=counts[draws].sum(axis=1); ok=totals>0
    means=sums[draws].sum(axis=1)[ok]/totals[ok]
    return np.quantile(means,[.025,.975]).tolist() if len(means)>=1900 else None


def _investment_change(record,density=False):
    a=record['result']['density_traits' if density else 'trait_mean']
    return float(a[-1,1]-a[0,1])


def _survives(record):
    return bool(record['result']['population'][-1]>0)


def _defined(record):
    return not (np.any(record['result'].get('resident_control_undefined',False)) or
                np.any(record['result'].get('density_control_undefined',False)))


def paired_contrast(a,b):
    if not all(_defined(r) for r in a+b):
        return dict(status='not_evaluable',reason='resident_genotype_control_undefined',
                    undefined_cases=[r['case_id'] for r in a+b if not _defined(r)])
    def keyed(rows):
        out={}
        for r in rows:
            key=(r['history_seed'],r['demographic_seed'])
            if key in out: raise ValueError('duplicate pair key')
            out[key]=r
        return out
    aa,bb=keyed(a),keyed(b)
    if set(aa)!=set(bb):
        raise ValueError('incomplete paired support')
    pairs=[(aa[k],bb[k]) for k in sorted(aa)]
    if any(x['weight']!=y['weight'] for x,y in pairs):
        raise ValueError('factor weights differ between paired arms')
    eligible=[]; differences=[]; histories=[]; joint=0
    for x,y in pairs:
        occupied=_survives(x) and _survives(y); joint+=int(occupied)
        ok=occupied and np.isfinite(_investment_change(x)) and np.isfinite(_investment_change(y))
        differences.append(_investment_change(y)-_investment_change(x) if ok else np.nan)
        histories.append(x['history_seed'])
        if ok: eligible.append([x['case_id'],y['case_id']])
    return dict(n_pairs=len(pairs),n_joint_survivors=joint,n_trait_change_eligible=len(eligible),eligible_pairs=eligible,
        occupancy_a=_mean([_survives(x) for x,y in pairs]),occupancy_b=_mean([_survives(y) for x,y in pairs]),
        conditional_mean_b_minus_a=_mean(differences),conditional_ci=_cluster_ci(differences,histories),
        interpretation='joint-survivor-selected descriptive contrast, not unconditional mediation')


def decompose_crossed(values,weights):
    v=np.asarray(values,dtype=float)
    if v.ndim!=3 or min(v.shape)<1 or set(weights)!={'S','C'}:
        raise ValueError('expected S x C x D values and fixed S/C weights')
    w=[]
    for key,n in zip(('S','C'),v.shape[:2]):
        a=np.asarray(weights[key],float)
        if a.shape!=(n,) or not np.isfinite(a).all() or (a<=0).any() or not np.isclose(a.sum(),1):
            raise ValueError('positive normalized factor weights required')
        w.append(a)
    if not np.isfinite(v).all():
        return dict(status='not_evaluable',reason='incomplete_survivor_support',
                    n_finite=int(np.isfinite(v).sum()),n_total=int(v.size))
    sw,cw=w; m=v.mean(axis=2); grand=float(sw@m@cw)
    s=m@cw-grand; c=sw@m-grand
    interaction=m-grand-s[:,None]-c[None,:]
    terms=np.array([sw@(s*s),cw@(c*c),sw@(interaction**2)@cw])
    between=float(terms.sum())
    within=float(sw@v.var(axis=2,ddof=1)@cw) if v.shape[2]>1 else None
    if between<=1e-25:
        return dict(status='not_evaluable',reason='zero_between_cell_variation',within_cell_variance=within)
    return dict(status='descriptive_cell_means',S=float(terms[0]/between),C=float(terms[1]/between),
        I=float(terms[2]/between),between_cell_variance=between,within_cell_variance=within,
        repeats_per_cell=v.shape[2],finite_repeat_noise_in_cell_means=None if within is None else within/v.shape[2],
        interpretation='weighted empirical cell-mean shares; finite-repeat noise not removed, not latent variance components')


def transport_score(training,heldout,training_weights,heldout_weights):
    if canonical(training_weights)!=canonical(heldout_weights):
        raise ValueError('cannot transport a ranking across different declared factor weights')
    a=np.asarray(training,float); b=np.asarray(heldout,float)
    if a.ndim!=3 or b.shape[:2]!=a.shape[:2]:
        raise ValueError('factor support differs')
    da=decompose_crossed(a,training_weights); db=decompose_crossed(b,heldout_weights)
    if da['status']!='descriptive_cell_means' or db['status']!='descriptive_cell_means':
        return dict(status='not_evaluable',reason='unsupported_crossed_endpoint',training=da,heldout=db)
    cw=np.asarray(training_weights['C']); sw=np.asarray(training_weights['S'])
    prediction=a.mean(axis=2)@cw; observed=b.mean(axis=2)@cw
    error=prediction-observed
    ranks=lambda d:sorted(('S','C','I'),key=lambda k:-d[k])
    return dict(status='evaluated',mae=float(sw@np.abs(error)),bias=float(sw@error),
        prediction=prediction.tolist(),observed=observed.tolist(),training_ranking=ranks(da),heldout_ranking=ranks(db),
        same_ranking=ranks(da)==ranks(db),training=da,heldout=db,
        interpretation='start-state marginal prediction under the declared held-out history distribution')


def effective_exposure(service,weights,correlation,*,stationary=True):
    def invalid(reason): return dict(status='not_evaluable',reason=reason,k_eff=None)
    x=np.asarray(service,float); w=np.asarray(weights,float); r=np.asarray(correlation,float)
    if not stationary: return invalid('nonstationary_history')
    if x.ndim!=1 or len(x)<3: return invalid('insufficient_observations')
    n=len(x)
    if not np.isfinite(x).all() or np.var(x)<=1e-20: return invalid('zero_or_invalid_service_variance')
    if w.shape!=(n,) or not np.isfinite(w).all() or (w<0).any() or w.sum()<=0: return invalid('invalid_reproductive_weights')
    if r.shape!=(n,n) or not np.isfinite(r).all() or not np.allclose(r,r.T,atol=1e-10) or not np.allclose(np.diag(r),1,atol=1e-10):
        return invalid('invalid_correlation')
    if np.linalg.eigvalsh(r).min()<-1e-9: return invalid('non_positive_semidefinite_correlation')
    w=w/w.sum(); denominator=float(w@r@w)
    if denominator<=1e-14: return invalid('nonpositive_correlation_denominator')
    return dict(status='evaluated',k_eff=1/denominator,n_observations=n,
        interpretation='weighted effective exposure diagnostic; not historical pooling k or island count')


def crossed_campaign(records):
    grouped=defaultdict(list)
    for r in records:
        if r['family']=='transport': grouped[(r['cohort'],r['pair_group'])].append(r)
    tensors={}; partitions=[]
    for key,rows in sorted(grouped.items()):
        if not all(_defined(r) for r in rows):
            raise ValueError('undefined controls cannot enter a crossed decomposition')
        starts=sorted({r['start_id'] for r in rows}); histories=sorted({r['history_seed'] for r in rows})
        demos=sorted({r['demographic_seed'] for r in rows})
        shape=(len(starts),len(histories),len(demos))
        occupancy=np.full(shape,np.nan); investment=np.full(shape,np.nan)
        seen=set(); sw={}
        for r in rows:
            idx=(starts.index(r['start_id']),histories.index(r['history_seed']),demos.index(r['demographic_seed']))
            if idx in seen: raise ValueError('duplicate crossed cell')
            seen.add(idx); occupancy[idx]=_survives(r); investment[idx]=_investment_change(r)
            if r['start_id'] in sw and sw[r['start_id']]!=r['weight']:
                raise ValueError('starting-state weights differ across histories')
            sw[r['start_id']]=r['weight']
        weights={'S':(np.array([sw[s] for s in starts])/sum(sw.values())).tolist(),
                 'C':(np.ones(len(histories))/len(histories)).tolist()}
        tensors[key]=(starts,weights,occupancy,investment)
        partitions.append(dict(cohort=key[0],regime=key[1],starts=starts,histories=histories,
            demographic_repeats=demos,occupancy=decompose_crossed(occupancy,weights),
            investment=decompose_crossed(investment,weights)))
    transfers=[]
    for key,a in tensors.items():
        if key[0]!='production': continue
        for other,b in tensors.items():
            if other[0]!='heldout': continue
            if a[0]!=b[0]: raise ValueError('held-out starting-state support differs')
            transfers.append(dict(training_regime=key[1],heldout_regime=other[1],
                occupancy=transport_score(a[2],b[2],a[1],b[1]),
                investment=transport_score(a[3],b[3],a[1],b[1])))
    return partitions,transfers


def summarize(records,design):
    groups=defaultdict(list)
    if len({r['case_id'] for r in records})!=len(records): raise ValueError('duplicate result case')
    for r in records: groups[(r['cohort'],r['cell_id'])].append(r)
    cells=[]
    for (cohort,cell_id),rows in sorted(groups.items()):
        histories=[r['history_seed'] for r in rows]
        base=dict(cohort=cohort,cell_id=cell_id,family=rows[0]['family'],n_total=len(rows),n_histories=len(set(histories)))
        if not all(_defined(r) for r in rows):
            cells.append(dict(**base,kind='trajectory',status='not_evaluable',
                reason='resident_genotype_control_undefined',n_undefined=sum(not _defined(r) for r in rows)))
            continue
        if 'outcross_gradient' in rows[0]['result']:
            cross=[_mean(r['result']['outcross_gradient']) for r in rows]
            total=[_mean(r['result']['total_gradient']) for r in rows]
            cells.append(dict(**base,kind='assay',outcross_gradient=_mean(cross),total_gradient=_mean(total),
                outcross_gradient_ci=_cluster_ci(cross,histories),total_gradient_ci=_cluster_ci(total,histories)))
            continue
        occupied=np.array([_survives(r) for r in rows]); n=int(occupied.sum())
        changes=np.array([_investment_change(r) if ok else np.nan for r,ok in zip(rows,occupied)])
        density_change=np.array([_investment_change(r,True) for r in rows])
        errors=changes-density_change
        baseline=[bool(r['result']['population'][0]>0) for r in rows]
        ancestry=[r['result']['founder_ancestry'][-1] if ok else np.nan for r,ok in zip(rows,baseline)]
        persistence=[bool(np.all(np.asarray(r['result']['founder_ancestry'])>0)) if ok else np.nan
                     for r,ok in zip(rows,baseline)]
        generation=[]; realized_selfing=[]
        for r in rows:
            a=r['result']['demographic']; keys=r['result']['demographic_keys'].tolist()
            total=a[:,keys.index('parent_contributions')].sum()
            generation.append(float(a[:,keys.index('parent_age_sum')].sum()/total) if total else np.nan)
            recruits=a[:,keys.index('resident_recruits')].sum()
            realized_selfing.append(float(a[:,keys.index('resident_selfed_recruits')].sum()/recruits)
                if recruits and 'resident_selfed_recruits' in keys else np.nan)
        ci=_cluster_ci(changes,histories)
        target=design.get('numerical_tolerances',{}).get('trait')
        cells.append(dict(**base,kind='trajectory',n_survivors=n,occupancy=float(occupied.mean()),
            n_trait_change_eligible=int(np.isfinite(changes).sum()),n_initial_lineage_baselines=sum(baseline),
            occupancy_ci=_cluster_ci(occupied,histories,bounded=True),
            mean_investment_change=_mean(changes),investment_change_ci=ci,
            conditional_precision_met=None if target is None or ci is None else (ci[1]-ci[0])/2<=target,
            individual_density_bias=_mean(errors),individual_density_mae=_mean(np.abs(errors)),
            bias_ci=_cluster_ci(errors,histories),
            sign_disagreement=_mean(np.where(np.isfinite(changes)&np.isfinite(density_change),
                np.sign(changes)!=np.sign(density_change),np.nan)),
            mean_density_change=_mean(density_change),mean_founder_ancestry=_mean(ancestry),
            founder_lineage_persistence=_mean(persistence),
            mean_realized_selfing_fraction=_mean(realized_selfing),
            realized_selfing_scope='retained viable resident recruits, excluding immigrants',
            first_extinction_count=sum(int(r['result']['extinction_year'])>=0 for r in rows),
            recolonization_count=sum(int(r['result']['recolonizations']) for r in rows),
            mean_generation_interval=_mean(generation),
            terminal_investment_variance=_mean([r['result']['trait_variance'][-1,1] for r in rows]),
            terminal_investment_heterozygosity=_mean([r['result']['heterozygosity'][-1,1] for r in rows])))
    pairs=[]
    for (cohort,a),(cohort_b,b) in combinations(groups,2):
        ra,rb=groups[(cohort,a)],groups[(cohort_b,b)]
        if (cohort!=cohort_b or ra[0]['pair_group']!=rb[0]['pair_group'] or
                ra[0]['start_id']!=rb[0]['start_id'] or 'population' not in ra[0]['result'] or 'population' not in rb[0]['result']):
            continue
        pairs.append(dict(cohort=cohort,a=a,b=b,**paired_contrast(ra,rb)))
    crossed,transport=crossed_campaign(records)
    return dict(cells=cells,paired_contrasts=pairs,crossed=crossed,transport=transport,
        uncertainty='occupancy: 95% independent-history Hoeffding bounds; conditional means: 1999 cluster bootstrap resamples',
        claim_boundary='model-conditional contrasts; extinct traits remain undefined; ancestry is not causal resident-only adaptation')


def load_records(design,results,*,mode='production',require_complete=True):
    from .run import verify_snapshot
    results=Path(results); expected=[c for c in compile_design(design) if (c['cohort']=='pilot')==(mode=='pilot')]
    verify_snapshot(results,design)
    saved=json.loads((results/'manifest.json').read_text())
    identity={'manifest_hash':digest(design),'mode':mode}
    if saved['identity']!=identity or canonical(saved['design'])!=canonical(design):
        raise ValueError('result manifest mismatch')
    rows=[]; missing=[]
    for case in expected:
        folder=results/case['case_id']; path=folder/'receipt.json'; arrays=folder/'arrays.npz'
        if not path.exists(): missing.append(case['case_id']); continue
        receipt=json.loads(path.read_text())
        if (receipt.get('status')!='complete' or receipt.get('case_hash')!=digest(case)
                or any(receipt.get(k)!=v for k,v in identity.items())
                or not arrays.exists() or sha256(arrays.read_bytes()).hexdigest()!=receipt.get('arrays_sha256')):
            raise ValueError('invalid result receipt')
        if canonical(json.loads((folder/'input.json').read_text()))!=canonical(case):
            raise ValueError('case input mismatch')
        # The full state audit streams one case at a time. Reporting retains only
        # yearly endpoints, never every individual/genotype state in RAM at once.
        excluded={'state_offsets','state_alleles','state_allele_origin','state_mutation_flags',
                  'state_ids','state_birth_years','final_genotypes','final_allele_origin','final_ids',
                  'final_birth_years','final_mutation_flags','final_density_counts','initial_genotypes',
                  'density_checkpoints','density_counts','density_checkpoint_years','density_counts_shape',
                  'density_counts_sha256','parentage','parentage_offsets','parentage_keys'}
        with np.load(arrays,allow_pickle=False) as data:
            result={k:data[k].copy() for k in data.files if k not in excluded}
        cell=case['cell']
        rows.append(dict(case_id=case['case_id'],cell_id=cell['id'],cohort=case['cohort'],
            history_seed=case['history_seed'],demographic_seed=case['demographic_seed'],
            family=case['family'],pair_group=cell['pair_group'],start_id=cell['start_id'],weight=cell['weight'],result=result))
    if missing and require_complete: raise ValueError(f'{len(missing)} cases missing; campaign incomplete')
    return rows


def main():
    p=argparse.ArgumentParser(); p.add_argument('--design',required=True); p.add_argument('--results',required=True)
    p.add_argument('--output',required=True); p.add_argument('--mode',choices=['pilot','production'],default='production')
    a=p.parse_args(); design=json.loads(Path(a.design).read_text(encoding='utf-8'))
    rows=load_records(design,a.results,mode=a.mode); report=summarize(rows,design)
    output=Path(a.output); output.mkdir(parents=True,exist_ok=True)
    (output/'summary.json').write_bytes(canonical(report))
    fields=sorted(set().union(*(r.keys() for r in report['cells'])))
    with (output/'cells.csv').open('w',newline='',encoding='utf-8') as handle:
        writer=csv.DictWriter(handle,fieldnames=fields); writer.writeheader(); writer.writerows(report['cells'])
    from .plot import plot_records
    plot_records(rows,report,output)
    print(json.dumps({'cases':len(rows),'cells':len(report['cells']),'output':str(output)}))


if __name__=='__main__': main()
