"""Exploratory *restored visitor replenishment* futures from authenticated old states.

NOT a confirmatory study, a new species model, or a ratchet/lifeboat verdict.
Does not modify archived biology or its signed observations.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import math
from statistics import NormalDist
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts import q3_futures_contract_20261014 as archive_contract

FIELDS = ('ids', 'alleles', 'allele_origin', 'mutation_flags', 'birth_years')
NAMESPACE = 'izu-recovery-checkpoint-exploration-20261018-v1'
CHECKPOINTS = (0, 25, 50, 100, 150, 200)


def seed_for(key: str, year: int, repeat: int, kind: str) -> int:
    """Separate restoration visitor and demographic draw namespaces."""
    if not isinstance(key, str) or not key or year < 0 or repeat < 0 or kind not in ('visitors', 'population'):
        raise ValueError('invalid fresh-stream namespace key')
    message = f'{NAMESPACE}\0{key}\0{year}\0{repeat}\0{kind}'.encode()
    value = int.from_bytes(hashlib.sha256(message).digest()[:8], 'big')
    return value % (2**31 - 2) + 1 if kind == 'visitors' else value


def extract_occupied_state(arrays: dict, time: int, types):
    offsets = np.asarray(arrays['offsets'])
    if (time < 0 or time + 1 >= len(offsets) or offsets.ndim != 1
            or not np.issubdtype(offsets.dtype, np.integer)
            or offsets[0] != 0 or (np.diff(offsets) < 0).any()
            or int(offsets[-1]) != len(arrays['alleles'])):
        raise ValueError('invalid original census offsets')
    lo, hi = map(int, offsets[time:time+2])
    state = types.PlantState(**{field:arrays[field][lo:hi].copy() for field in FIELDS})
    return state


def investment_support(alleles: np.ndarray, target: float, *, mutation_I: bool,
                       seed_immigration: bool) -> dict:
    """Genotype upper-bound theorem, NOT a sufficiency/recovery probability test."""
    a = np.asarray(alleles)
    if not (np.isfinite(target) and 0 <= target <= 1 and a.ndim == 3 and a.shape[1:] == (3,2)
            and np.isfinite(a).all()):
        raise ValueError('malformed source population or target')
    if len(a) == 0:
        return dict(occupied=False, high_allele_max=None, closed=None,
                    reason='extinction_is_not_genetic_fixation')
    highest = float(a[:, 1, :].max())
    if mutation_I or seed_immigration:
        return dict(occupied=True, high_allele_max=highest, closed=None,
                    reason='upper_support_theorem_not_applicable')
    return dict(occupied=True, high_allele_max=highest,
                closed=bool(highest < target),
                reason='strict_upper_allele_exclusion' if highest < target else 'support_necessary_not_sufficient')


def wilson(k: int, n: int, z: float=1.959963984540054) -> tuple[float,float] | None:
    if type(k) is not int or type(n) is not int or n < 0 or not (0 <= k <= n):
        raise ValueError('invalid Bernoulli counts')
    if n == 0: return None
    p = k/n
    denom = 1 + z*z/n
    mid = (p + z*z/(2*n))/denom
    span = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/denom
    return max(0., mid-span), min(1.,mid+span)


def threshold_window(rows: list[dict], cutoff: float=.2) -> int | None:
    """First point whose *all subsequent* Wilson upper bounds fall below cutoff.

    No extrapolation between discrete checkpoints; undefined/n=0 => not identified.
    """
    if not 0 < cutoff < 1 or not rows: return None
    rows=sorted(rows,key=lambda x:x['t'])
    for i, row in enumerate(rows):
        tail = rows[i:]
        if all(r.get('conditional_interval') is not None and
               r['conditional_interval'][1] < cutoff for r in tail):
            return row['t']
    return None


def first_sustained_recovery(trace: list[float | None], target: float, consecutive: int) -> bool:
    if consecutive < 1: raise ValueError('invalid duration')
    run = 0
    for v in trace:
        run = run + 1 if v is not None and np.isfinite(v) and v >= target else 0
        if run >= consecutive: return True
    return False


def native_future(state, history, cfg, population, reproduction, randomness,
                  *, seed: int, start: int, target: float, horizon: int, sustained: int):
    if len(history.visitors) != horizon or len(history.seed_candidates) != horizon:
        raise ValueError('visitor path length changed')
    if cfg.seed_arrival.supply != 0 or cfg.survival != 0:
        raise ValueError('original no-immigration annual context required')
    streams={name:randomness.stream(seed,name,0) for name in randomness.STREAM_IDS}
    st=state
    empty=population.subset(state,np.empty(0,dtype=int))
    path=[]
    count_path=[]
    outcross_path=[]
    high_bound=[]
    for dt in range(horizon+1):
        n=len(st.ids)
        value=float(st.alleles[:,1,:].mean()) if n else None
        path.append(value)
        count_path.append(n)
        high_bound.append(float(st.alleles[:,1,:].max()) if n else None)
        if dt==horizon:break
        ledger=reproduction.reproduce(st,history.visitors[dt],cfg)
        outcross_path.append(float(ledger.outcross.sum()))
        if len(history.seed_candidates[dt].ids):
            raise ValueError('seed immigrants violate upper-allele theorem')
        st,_=population.advance(st,ledger,empty,cfg,streams,year=start+dt,
                                mutation_traits=(False,False,True))
        if len(st.ids) and high_bound[-1] is not None and st.alleles[:,1,:].max()>high_bound[-1]+1e-12:
            raise AssertionError('I allele support increased with no mutation/immigration')
    # Survival at both ends is a separate required part of the unconditional outcome.
    occupied_terminal=count_path[-1]>0
    success=bool(occupied_terminal and first_sustained_recovery(path[1:],target,sustained))
    return dict(success=success,occupied_terminal=occupied_terminal,
                terminal_I=path[-1],terminal_n=count_path[-1],
                restored_outcross_sum=float(sum(outcross_path)),
                path_I=path, path_n=count_path,
                high_I_allele_max=high_bound)


def native_gradient(state, visitors, config, selection) -> dict:
    """MONOMORPHIC-RESIDENT local approximation, not actual finite-path causation."""
    if len(state.ids)==0: return dict(gradient=None, sign='extinct')
    resident=state.alleles.mean(axis=(0,2)).copy()
    if config.assurance_mode=='fixed': resident[2]=config.fixed_assurance
    try:
        g=float(np.asarray(selection.investment_invasion_terms(resident,visitors,config)['gradient']))
    except (ArithmeticError,FloatingPointError,ValueError):
        return dict(gradient=None,sign='undefined')
    return dict(gradient=g,sign='positive' if g>1e-9 else 'negative' if g< -1e-9 else 'near_zero')


def classify_failure(*, was_occupied: bool, genetic_closed: bool | None,
                     local_gradient_sign: str, success: bool) -> str:
    """Overlapping mechanisms remain explicit; no forced two-cause attribution."""
    if not was_occupied: return 'extinct_before_restoration'
    if success: return 'restored_successfully'
    if genetic_closed is True:
        return 'genetically_inaccessible_target' if local_gradient_sign=='positive' else 'genetic_and_other_or_selection'
    if local_gradient_sign == 'negative': return 'nonpositive_local_selection_proxy'
    return 'unresolved_finite_time_or_polymorphic_selection'


def load_cases(archive: Path, source_input: Path, out: Path):
    """Use existing source-hash and original-NPZ admission, not a new ad-hoc parser."""
    out.mkdir(parents=True,exist_ok=False)
    record=archive_contract.admit(archive,source_input,Path(__file__).resolve().parents[1],out)
    return record


def run(archive: Path, source_input: Path, out: Path, *, repeats: int, horizon: int,
        checkpoint_times: tuple[int,...], samples_per_block: int, cutoff: float,
        sustained: int):
    if not (1 <= repeats <= 64 and 1 <= horizon <= 200 and 1 <= sustained <= horizon
            and 1 <= samples_per_block <= 32 and 0 < cutoff < 1
            and checkpoint_times and len(set(checkpoint_times))==len(checkpoint_times)
            and all(0<=t<=200 for t in checkpoint_times)):
        raise ValueError('invalid bounded EXPLORATORY design')
    cohort=load_cases(archive,source_input,out)
    types,pop,reproduction,randomness=archive_contract.load_native(out/'frozen_source')
    history_mod=importlib.import_module(types.__package__+'.history')
    selection_mod=importlib.import_module(types.__package__+'.selection')
    campaign=json.loads((out/'campaign.json').read_text())
    selected=[]
    for block in ('causal_main','causal_confirmation'):
        selected += sorted((c for c in cohort['cases'] if c['block']==block),key=lambda x:x['key'])[:samples_per_block]
    data=[]
    # Exploratory pointwise curves with within-case Bonferroni uncertainty bands.
    z_adjusted=NormalDist().inv_cdf(1-0.05/(2*len(checkpoint_times)))
    from collections import defaultdict
    counts=defaultdict(int)
    for c in selected:
        a=archive_contract.arrays(archive_contract.checked_bytes(out/'original'/(c['key']+'.npz'),c['original_npz_sha256']))
        meta=json.loads(str(a['metadata']))
        cfg=types.Config.from_dict(meta['config'])
        if not (cfg.seed_arrival.supply == 0 and cfg.survival == 0 and cfg.capacity==48
                and cfg.visitor_arrival.kernel == 'exponential'
                and cfg.assurance_mode=='evolving' and cfg.years==200
                and meta['task']['supply']==.125 and meta['task']['composition']=='matched'
                and len(a['offsets'])==201+1):
            raise ValueError('archived context does not match bounded study')
        optimum=campaign['compositions'][meta['task']['composition']]
        visitor0=types.VisitorState(np.arange(len(optimum),dtype=np.int64),np.asarray(optimum),
                                   np.full(len(optimum),cfg.visitor_breadth),np.ones(len(optimum)))
        # Change ONLY exogenous visitor replenishment. Reproductive kernel remains archived.
        new_arrival=replace(cfg.visitor_arrival,distance=0.0,
                             supply=max(0.3,cfg.visitor_arrival.supply))
        if new_arrival.supply*math.exp(-new_arrival.distance/new_arrival.scale) <= \
           cfg.visitor_arrival.supply*math.exp(-cfg.visitor_arrival.distance/cfg.visitor_arrival.scale):
            raise ValueError('restoration does not increase expected arrival pressure')
        future_cfg=replace(cfg,visitor_arrival=new_arrival,island_history='separation',
                           initial_visitors=len(visitor0.ids),years=horizon)
        target=float(extract_occupied_state(a,0,types).alleles[:,1,:].mean())
        # Exact source-only first high-I closure time (all original censuses).
        source_closure=None
        for source_t in range(201):
            original=extract_occupied_state(a,source_t,types)
            s0=investment_support(original.alleles,target,mutation_I=False,seed_immigration=False)
            if s0['closed']:
                source_closure=source_t
                break
        for t in checkpoint_times:
            state=extract_occupied_state(a,t,types)
            support=investment_support(state.alleles,target,mutation_I=False,seed_immigration=False)
            historical_I=float(state.alleles[:,1,:].mean()) if len(state.ids) else None
            grad=native_gradient(state,visitor0,future_cfg,selection_mod)
            declined=historical_I is not None and historical_I <= target-.05
            successors=[]
            if len(state.ids):
                for rep in range(repeats):
                    v_seed=seed_for(c['key'],t,rep,'visitors')
                    d_seed=seed_for(c['key'],t,rep,'population')
                    # make_history creates a new exogenous *near* future with original visitors inherited.
                    visitors=history_mod.make_history(future_cfg,seed=v_seed,inherited_visitors=visitor0)
                    successes=native_future(state,visitors,future_cfg,pop,reproduction,randomness,
                                seed=d_seed,start=t,target=target,horizon=horizon,sustained=sustained)
                    successors.append(dict(replicate=rep,visitor_seed=v_seed,demographic_seed=d_seed,
                                           **successes))
            # Fixed-state, conditional results. Disallow selected paths as independent founders.
            n_success=sum(x['success'] for x in successors)
            interval=wilson(n_success,len(successors),z=z_adjusted)
            for x in successors:
                x['failure_class']=classify_failure(was_occupied=bool(len(state.ids)),
                          genetic_closed=support['closed'],local_gradient_sign=grad['sign'],success=x['success'])
                counts[x['failure_class']]+=1
            data.append(dict(key=c['key'],block=c['block'],t=t,original_status='SOURCE_CONDITIONAL_EXPLORATORY',
                             initial_I=target,current_I=historical_I,historical_decline=declined,
                             first_source_high_I_closure=source_closure,
                             occupied=bool(len(state.ids)),I_support=support,local_gradient_proxy=grad,
                             target_attainments=n_success,futures=len(successors),
                             conditional_p=n_success/len(successors) if successors and declined else None,
                             conditional_interval=interval if declined else None,
                             descriptive_maintenance_p=n_success/len(successors) if successors and not declined else None,
                             successors=successors))
    window={}
    for case in selected:
        rows=[r for r in data if r['key']==case['key']]
        window[case['key']]=threshold_window(rows,cutoff=cutoff)
    outjson=dict(status='EXPLORATORY_SOURCE_CONDITIONAL_NOT_PREREGISTERED',
                 claim_limit='No independent founder effect, Q3 A-policy contrast, full-population success, confirmed irreversible t*, or naturally dated pollinator extirpation.',
                 namespace=NAMESPACE,case_count=len(selected),checkpoint_times=list(checkpoint_times),
                 new_biological_futures=sum(r['futures'] for r in data),
                 source_scope='Two previously defined A-evolving founder blocks; no paired A-fixed history, no permanent visitor-extirpation date.',
                 threshold_definition='Exploratory first eligible checkpoint with all LATER measured Bonferroni-adjusted Wilson upper limits below cutoff; no between-point or permanent inference.',
                 threshold_cutoff=cutoff,sustained=sustained,horizon=horizon,repeats=repeats,
                 interval_scope='Within each fixed source history, 95% Bonferroni-adjusted Wilson for grid checkpoints, fresh nested future streams; not across source histories.',
                 reason_counts=dict(counts),candidate_grid_t_star=window,case_rows=data)
    target=out/'RECOVERY_PROBE_READOUT.json'
    with target.open('x',encoding='utf8') as f:
        json.dump(outjson,f,indent=2,allow_nan=False)
        f.write('\n')
    return {k:v for k,v in outjson.items() if k!='case_rows'}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--archive',type=Path,required=True)
    p.add_argument('--source-input',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--repeats',type=int,default=8)
    p.add_argument('--horizon',type=int,default=40)
    p.add_argument('--sustained',type=int,default=10)
    p.add_argument('--samples-per-block',type=int,default=2)
    p.add_argument('--checkpoint-times',type=int,nargs='+',default=list(CHECKPOINTS))
    p.add_argument('--cutoff',type=float,default=.2)
    args=p.parse_args()
    print(json.dumps(run(args.archive,args.source_input,args.out,repeats=args.repeats,horizon=args.horizon,
      checkpoint_times=tuple(args.checkpoint_times),samples_per_block=args.samples_per_block,
      cutoff=args.cutoff,sustained=args.sustained),indent=2))


if __name__=='__main__': main()