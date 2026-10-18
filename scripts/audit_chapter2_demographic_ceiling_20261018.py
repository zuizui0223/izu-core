"""Source-derived survival ceiling for the frozen PR597 equal-A pilot.

No new Model3 history, descendant replay, optimizer, or random draw. The
finite-state Poisson calculation integrates probabilities, not trajectories.
The comparison theorem assumes delayed selfing, no adult carryover/immigration,
fixed A=.5, B=8, delta=c_I=c_A=.5, and inherited I in [.375,.625].
The resource-window calculation proposes a distinct demographic companion;
it never changes the frozen pilot or authorizes a confirmatory experiment.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.stats import poisson

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'docs/audits/CHAPTER2_EQUALA_PILOT_EVENT_SOURCE_20261018.json'
SOURCE_HEAD='cc17c7355d27b907b71b124046990b914e4963dd'
SOURCE_DESIGN_SHA='442e1340928406f26043d51cab6de30808b7707f4ff68df27af6f1b6f16812f5'
NATIVE_BLOBS={
    'scripts/model3_island/population.py':'20e90f249f63e9f37e8801d19d9b75cade2fe193',
    'scripts/model3_island/reproduction.py':'95314698a3296b6f13b8c053c36f2df0b7b744ca',
    'docs/protocols/CHAPTER2_Q3_EQUALA_CROSSED_VARIANCE_PILOT_FROZEN_20261018.json':
        'ac99b70766103b2cb8b7cc45b23185229d6a21c8',
}


def birth_rate(budget: float, investment: float, assurance: float, *, q: float=0.) -> float:
    """Native delayed-selfing expected viable seed output per current adult.

    Full-service q is a fixed-state effective fertilization fraction. Costs
    and selfed-offspring viability are the source .5 values, not new fitted
    estimates. This is not a population growth eigenvalue for evolving traits.
    """
    if (any(not isinstance(x,(int,float)) or isinstance(x,bool) or not math.isfinite(x)
            for x in (budget,investment,assurance,q)) or budget<0
            or not 0<=investment<=1 or not 0<=assurance<=1 or not 0<=q<=1):
        raise ValueError('invalid finite reproductive input')
    ovules=budget*math.exp(-.5*investment**2-.5*assurance**2)
    return ovules*(q+.5*assurance*(1-q))


def transition(rate: float, capacity: int) -> np.ndarray:
    """Z'=min(K,Poisson(rate*Z)). State zero is absorbing."""
    if (type(capacity) is not int or not 1<=capacity<=256
            or not math.isfinite(rate) or not 0<=rate<=100):
        raise ValueError('invalid finite Poisson comparison chain')
    p=np.empty((capacity+1,capacity+1))
    # Stable upper tail avoids subtracting tiny mass from one when n is small.
    for n in range(capacity+1):
        p[n,:capacity]=poisson.pmf(np.arange(capacity),n*rate)
        p[n,capacity]=poisson.sf(capacity-1,n*rate)
    if np.any(p<0) or np.max(np.abs(p.sum(1)-1))>1e-12:
        raise ArithmeticError('transition probabilities failed conservation')
    return p


def extinction_probability(rate: float, capacity: int, steps: int, *, initial: int|None=None) -> float:
    """Deterministic finite-time absorption; retain tiny probabilities directly."""
    if type(steps) is not int or not 0<=steps<=10000:
        raise ValueError('invalid comparison horizon')
    n0=capacity if initial is None else initial
    if type(n0) is not int or not 0<=n0<=capacity:
        raise ValueError('invalid initial population')
    p=transition(rate,capacity)
    mass=np.zeros(capacity+1); mass[n0]=1.
    for _ in range(steps): mass=mass@p
    if abs(mass.sum()-1)>2e-10 or mass[0]<0 or mass[0]>1+2e-10:
        raise ArithmeticError('propagated probability mass failed')
    # Only a possible upper roundoff (~1e-14) is limited, not tiny extinction.
    return min(1.,float(mass[0]))


def replacement_interval(i_min: float,i_max: float,a_low: float,a_high: float) -> tuple[float,float]:
    """Budget window: low-A r<1 AND high-A r>1 for every I in support.

    These are fixed diagnostic trait values, NOT inferred states of both arms.
    """
    if not 0<=i_min<=i_max<=1 or not 0<a_low<a_high<=1:
        raise ValueError('invalid trait support or assurance contrast')
    low=math.exp(.5*i_max**2+.5*a_high**2)/(.5*a_high)
    high=math.exp(.5*i_min**2+.5*a_low**2)/(.5*a_low)
    if low>=high: raise ValueError('no separated replacement interval')
    return low,high


def diagnose(data: dict) -> dict:
    if (data.get('schema')!='chapter2_equalA_pilot_events_ci_v1'
        or data['source']['head_sha']!=SOURCE_HEAD
        or data['source']['design_sha256']!=SOURCE_DESIGN_SHA
        or data['design']['no_mutation_all_three_loci'] is not True
        or data['design']['no_seed_immigration'] is not True
        or data['design']['assurance_timing']!='delayed'
        or data['design']['assurance_cost']!=.5
        or data['design']['updates']!=80
        or data['design']['initial_expressed_A_all_adults']!=.5):
        raise ValueError('not the admitted closed-source equal-A pilot')
    rate=birth_rate(8,.625,.5)
    bound=extinction_probability(rate,48,80)
    lo,hi=replacement_interval(.375,.625,.5,.75)
    diagnostic=[]
    for budget in (8.,4.5):
        for assurance in (.5,.75):
            for investment in (.375,.625):
                r=birth_rate(budget,investment,assurance)
                e=extinction_probability(r,48,45)
                diagnostic.append(dict(budget=budget,assurance=assurance,investment=investment,
                    fixed_trait_per_capita_seed_rate=r,extinction_by_45=e,
                    survival_by_45=1-e,not_evolved_arm_effect_estimate=True))
    return dict(
        schema='chapter2_source_demographic_ceiling_diagnostic_v1',
        status='SOURCE_DERIVED_COMPARISON_BOUND_NOT_NEW_BIOLOGICAL_EVIDENCE',
        source=dict(head=SOURCE_HEAD,native_git_blobs=NATIVE_BLOBS,
            event_source_canonical_sha256=hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            parameter_source='base_config ovule_budget=8,investment_cost=depression=.5; frozen pilot assurance_cost=.5,capacity=48,adult_survival=0; I support [.375,.625]'),
        source_counts=dict(living_at_t80=144 if data['all_144_paths_alive_at_80'] else None,
            fixed_high_I_loss=data['logged_summary']['I_losses']['fixed'],
            evolving_high_I_loss=data['logged_summary']['I_losses']['evolving']),
        new_biological_histories=0,new_descendant_restoration_paths=0,
        fixed_arm_ceiling=dict(minimum_viable_seeds_per_adult=rate,
            minimum_mean_recruits_at_n48=48*rate,
            single_step_zero_recruits_probability_at_n48=math.exp(-48*rate),
            upper_probability_extinction_by_t80=bound,
            maximum_possible_positive_survival_policy_effect=bound,
            probability_type='analytic stochastic-comparison bound evaluated numerically, NOT fitted from zero deaths'),
        post_pilot_resource_proposal=dict(
            status='PROPOSED_MECHANISTIC_COMPANION_NOT_REGISTERED_OR_EXECUTED',
            lower_budget_strict=lo,upper_budget_strict=hi,illustrative_budget=4.5,
            budget_as_fraction_of_original=.5625,
            property='r(A=.5)<1<r(A=.75) for all allowed I; states are diagnostic contrasts, not arm means',
            scaling_identity='at fixed genomes and visitors, multiplying ovule_budget by s multiplies the complete viable-parentage matrix by s; conditional parental probabilities are unchanged',
            warning='s scales absolute recruitment, not just A; population changes can indirectly change later selection; no inference that evolving A will always reach .75'),
        fixed_trait_45_update_reference_chains=diagnostic,
        gate_decision='DO_NOT_POWER_A_POSITIVE_SURVIVAL_RESCUE_EFFECT_WITH_THE_B8_FIXED_A_COMPARATOR',
        future_confirmation_authorized=False,
        restrictions=[
            'Upper bound applies to the FIXED-A arm under specified source parameters; no corresponding uniform survival guarantee for an arbitrary evolving-A population.',
            'I allele support must remain <=.625, expression must be the diploid mean, delayed selfing applies, and there is no adult carryover or seed immigration.',
            'Proof uses a monotone Poisson coupling over all population sizes. Single-step exp(-lambda) alone is not a finite-horizon extinction bound.',
            'With finite K and stochastic reproduction eventual extinction remains possible; supercritical per-capita reproduction is not permanent persistence.',
            'B4.5 curves are exactly integrated fixed-trait comparison chains; they are not new empirical outcomes or evolved-policy effect estimates.',
            'The post-pilot resource window is a proposal for a separate prospective companion, not retroactive alteration of the registered history or approval under #585.',
            'No guarantee of trait recovery follows from survival; no survival difference establishes genetic mediation.',
        ])


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,default=SOURCE)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    if args.out.exists(): p.error('refuse overwrite')
    result=diagnose(json.loads(args.source.read_text(encoding='utf8')))
    args.out.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open('x',encoding='utf8') as f:
        json.dump(result,f,indent=2,sort_keys=True,allow_nan=False); f.write('\n')
    print(json.dumps({k:result[k] for k in ('status','fixed_arm_ceiling','post_pilot_resource_proposal','gate_decision')},indent=2))
