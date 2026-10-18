"""Source-bound Q3 METHOD-REVIEW candidate, not registered or executable biology.

Uses all recorded pilot/control variance inputs, never selects a favorable
future seed family. No Model3 operator imported. The unchanged #585 checker
screens a conservative rectangular budget; a second exact shared-prefix
budget is reported without pretending nested draws are independent sources.
"""
from __future__ import annotations
import copy
import hashlib
import json
import math
from pathlib import Path
from statistics import NormalDist
import numpy as np
from scripts.audit_chapter2_equalA_precision_20261018 import variance_components
from scripts.validate_chapter2_future_power_20261017 import evaluate, mde_normal_proxy

ROOT=Path(__file__).resolve().parents[1]
EVENT_PATH=ROOT/'docs/audits/CHAPTER2_EQUALA_PILOT_EVENT_SOURCE_20261018.json'
RECON_PATH=ROOT/'docs/audits/CHAPTER2_BUDGET_COMPANION_STREAM_RECONCILIATION_20261018.json'
EXPECTED_BLOBS={EVENT_PATH.name:'e007ac785be7264ebb9040c9ff8bfd1a2d504279',
                RECON_PATH.name:'31ea7fc3c652909461c878c4e9e102c99df183e1'}
INPUT_NAME='docs/audits/CHAPTER2_JOINT_METHOD_REVIEW_INPUTS_20261018.json'
PLAN_NAME='docs/protocols/CHAPTER2_Q3_JOINT_METHOD_REVIEW_CANDIDATE_20261018.json'
OUT_NAME='docs/audits/CHAPTER2_JOINT_METHOD_REVIEW_GATE_20261018.json'
ENDPOINTS=('genetic_loss','survival_interaction')
COMPONENTS=('founder','visitor','interaction','within_cell')
# Deliberately transparent SENSITIVITY assumption, not estimated confidence bound.
# .65 exceeds all measured within-cell variances, including .5138889 in control104.
STRESS=dict(founder=.05,visitor=.05,interaction=.20,within_cell=.65)
MARGIN=.10


def encoded(obj):
    return (json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()


def load_inputs():
    loaded={}
    for path in (RECON_PATH,EVENT_PATH):
        raw=path.read_bytes()
        gitsha=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        if gitsha!=EXPECTED_BLOBS[path.name]:
            raise ValueError('source blob differs from reviewed GitHub commit: '+path.name)
        loaded[path.name]=json.loads(raw)
    return loaded[RECON_PATH.name],loaded[EVENT_PATH.name]


def derive_inputs(rec,events):
    if (rec.get('schema')!='chapter2_budget_companion_stream_reconciliation_v1'
        or events.get('schema')!='chapter2_equalA_pilot_events_ci_v1'
        or events.get('all_144_paths_alive_at_80') is not True
        or set(rec.get('streams',{}))!={'90','104'}):
        raise ValueError('wrong pilot source or unsupported competing deaths')
    # Complete original event array and repeated control streams are three
    # related variance checks, not three independent founder/visitor cohorts.
    def losses(key):
        raw=events[key]
        if len(raw)!=6 or any(len(row)!=12 for row in raw):
            raise ValueError('missing original cells')
        if any(t is not None and (type(t) is not int or not 1<=t<=80)
               for row in raw for t in row):
            raise ValueError('bad original event')
        return np.array([[int(t is not None) for t in row] for row in raw]).reshape(6,6,2)
    f,e=losses('first_I_loss_fixed'),losses('first_I_loss_evolving')
    if (int(f.sum()),int(e.sum()))!=(42,58):raise ValueError('original event counts')
    env=lambda d:{c:max(v[c] for v in d.values()) for c in COMPONENTS}
    gs={'original':variance_components(e-f)};ss={};point={}
    for prefix,entry in rec['streams'].items():
        if entry['seed_prefix']!=[20261018,int(prefix)]:raise ValueError('wrong seed family')
        codes=entry['terminal_status_codes']
        wanted={'fixed_B8','evolving_B8','fixed_B4.5','evolving_B4.5'}
        if set(codes)!=wanted:raise ValueError('missing policy-budget arms')
        x={}
        for name,code in codes.items():
            if len(code)!=72 or set(code)-set('012'):raise ValueError('bad status code')
            x[name]=np.array([int(c) for c in code]).reshape(6,6,2)
        if np.any(x['fixed_B8']==0) or np.any(x['evolving_B8']==0):
            raise ValueError('B8 deaths prevent substituting terminal closure for incidence')
        g=(x['evolving_B8']==1).astype(int)-(x['fixed_B8']==1).astype(int)
        s=((x['evolving_B4.5']>0).astype(int)-(x['fixed_B4.5']>0).astype(int)
           -(x['evolving_B8']>0).astype(int)+(x['fixed_B8']>0).astype(int))
        gs[prefix]=variance_components(g);ss[prefix]=variance_components(s)
        point[prefix]={'genetic_control_risk_difference':float(g.mean()),
                       'survival_interaction':float(s.mean())}
    return dict(schema='chapter2_joint_method_review_pilot_inputs_v1',
        status='PILOT_COMPONENT_ENVELOPE_FOR_METHOD_REVIEW_NOT_CONFIRMATION',
        source_commit='98a0f2de98a6572bc4789c0431f44c45f283400e',
        source_blobs=EXPECTED_BLOBS,
        source_sha256={RECON_PATH.name:hashlib.sha256(encoded(rec)).hexdigest(),
                       EVENT_PATH.name:hashlib.sha256(encoded(events)).hexdigest()},
        source_hash_encoding='SHA256 of canonical decoded JSON; git blob pins cover original bytes',
        independent_source_counts={'founders':6,'visitors':6,'historical_repeats':2},
        source_seed_families_are_nested_not_pooled=True,
        genetic_loss_component_sources=gs,survival_component_sources=ss,
        component_envelopes={'genetic_loss':env(gs),'survival_interaction':env(ss)},
        descriptive_source_point_estimates=point,
        genetic_original_point_estimate=float((e-f).mean()),
        adverse_scenario=STRESS,
        adverse_is_sensitivity_assumption_not_empirical_upper_bound=True,
        actual_new_biological_histories=0,
        caution='Envelope is conservative relative to the recorded component estimates, not a confidence envelope for population variances.')


def collapsed(var,r):
    if type(r) is not int or r<1:raise ValueError('bad nested repeats')
    return dict(founder=var['founder'],visitor=var['visitor'],
                interaction=var['interaction']+var['within_cell']/r)


def budget(nf,nv,r):
    if any(type(x) is not int or x<1 for x in (nf,nv,r)):
        raise ValueError('bad independent source counts/repeats')
    pre=nf*nv*r*2;terminal=pre*2
    return dict(founders=nf,visitors=nv,nested_repeats=r,
        historical_prefix_paths=pre,terminal_branch_paths=terminal,
        shared_prefix_updates=pre*35,future_branch_updates=terminal*45,
        unique_update_ceiling=pre*35+terminal*45,
        legacy_rectangular_update_ceiling=terminal*80,
        rectangular_ceiling_deliberately_double_counts_shared_prefix=True,
        new_pollinator_return_futures=0)


def allocation_frontier(margin):
    if not 0<margin<1:raise ValueError('invalid design margin')
    result=[]
    for r in (1,2,4):
        n=next(n for n in range(3,2049) if
               mde_normal_proxy(collapsed(STRESS,r),n,n,.05,.8,2)<=margin)
        nr=math.ceil(n/8)*8
        result.append(dict(nested_repeats=r,minimum_square_n=n,rounded_n=nr,
                           unique_updates=budget(nr,nr,r)['unique_update_ceiling'],
                           scope='Equal independent axes; fixed round-up to eight-source batches, not a globally optimized design'))
    return result


def candidate_plan(pilot,n=136):
    """No registry enrollment and no execution. Normative margins require review."""
    if type(n) is not int or n<3:raise ValueError('bad proposed axes')
    b=budget(n,n,1)
    justifications={
      'genetic_loss':('Study-specific proposed minimum effect: an absolute 0.10 change '
        'means one additional initially assigned population per ten loses the alleles '
        'needed for its own founder-mean I by census80. This is a normative resolution '
        'choice for the model question, not estimated from the favorable pilot effect '
        'and not a validated threshold for wild islands. Independent method review must endorse it.'),
      'survival_interaction':('Study-specific proposed minimum effect: a 0.10 absolute '
        'policy-by-budget interaction means one net additional survivor per ten initially '
        'assigned populations under the prespecified challenge relative to B8. This uses '
        'the same population-probability resolution as genetic loss. It is a normative '
        'model-study choice, not a field-calibrated conservation threshold; review required.')}
    frontier=allocation_frontier(MARGIN)
    return dict(schema='chapter2_future_crossed_power_contract_v1',
        status='PRE_EXECUTION_POWER_PLAN_NOT_EXECUTED',
        stage='METHOD_REVIEW_CANDIDATE_NOT_REGISTERED',
        study_id='ch2_joint_equalA_access_rescue_candidate_20261018_v1',
        pilot_study_id='ch2_equalA_and_nested_companions_20261018',
        pilot_sha256=hashlib.sha256(encoded(pilot)).hexdigest(),pilot_source_repo_path=INPUT_NAME,
        pilot_precedes_registration=True,pilot_cohort_nonoverlap_confirmed=True,
        pilot_stream_namespace='20261018:89,90,104; founder301001..301006; visitor302001..302006',
        future_stream_namespace='ch2_joint_candidate_20261018_v1:105:reserved-not-consumed',
        new_biological_runs_started=False,endpoint_rule_frozen_before_new_outcomes=True,
        finite_cost_budget_documented=True,
        founder_count=n,visitor_history_count=n,number_of_environments=2,number_of_policies=2,
        updates_per_case=80,declared_full_paths=b['terminal_branch_paths'],
        declared_total_updates=b['legacy_rectangular_update_ceiling'],
        number_of_coprimary_outcomes=2,familywise_alpha=.05,minimum_joint_directional_power=.8,
        outcomes=[dict(name=e,minimum_scientifically_meaningful_abs_effect=MARGIN,
                       sesoi_scientific_justification=justifications[e]) for e in ENDPOINTS],
        variance_uncertainty_scenarios=[
            dict(name='baseline',by_endpoint={e:collapsed(pilot['component_envelopes'][e],1) for e in ENDPOINTS}),
            dict(name='adverse',by_endpoint={e:collapsed(STRESS,1) for e in ENDPOINTS})],
        variance_assumption_caveats={
            'baseline':'Componentwise maximum across all measured appropriate sources, not independent pooling',
            'adverse':'0.05 founder, 0.05 visitor, 0.20 interaction, 0.65 within-cell: sensitivity assumption, NOT measured upper bound',
            'single_demographic_replicate':'One per new crossing saves cost; interaction and stochastic residual cannot be separated in future final sample. Pilot had two repeats to estimate them.'},
        stage_budget=b,allocation_frontier=frontier,
        prospective_seed_registry={
            'founders':list(range(401001,401001+n)),
            'visitors':list(range(402001,402001+n)),
            'master_bit_width':128,'master_rule':'SHA256(study_id|105|stage|founder_index|visitor_index), first 16 bytes as unsigned integer',
            'stages':['prefix35','fork45'],'policy_and_budget_absent_from_master_key':True,
            'same_generator_ids_not_eventwise_coupling':True,
            'biological_streams_consumed':0},
        observation_rule='Every originally assigned path counts; extinct traits undefined. Genetic loss is first living max_I < founder_mean_I before extinction, measured in B8. Survival is (E-F under B4.5)-(E-F under B8).',
        trial_scope='K48, delayed selfing, assurance cost0.5, initially equal A0.5 with segregating alleles, no mutation/migration; common history35 then B8/B4.5 for45 with no visitors',
        decision_rule='Two two-sided 97.5% marginal intervals (Bonferroni familywise .05); report both signs. Joint-positive directions need both lower bounds >0. Evidence effects exceed .10 requires BOTH lower bounds >.10, not merely significance.',
        field_generalization=False,registered=False,method_reviewer_approved=False,
        actual_operating_characteristics_validated=False,execution_authorized=False,
        requires_before_biology=['Independent review of margins and adverse variances',
            'Operating-characteristic assessment of bounded/near-boundary outcomes and two-way dependence',
            'Implement and dry-test runner/saving/analysis against the final immutable source contract',
            'Archive on authorized output surface and explicit resource/execution approval'])


def decision(g,s,margin):
    if not 0<margin<1:raise ValueError('bad margin')
    for a in (g,s):
        if len(a)!=2 or not all(math.isfinite(x) for x in a) or a[0]>a[1]:
            raise ValueError('invalid interval')
    return dict(joint_positive_direction=g[0]>0 and s[0]>0,
        both_effects_demonstrated_above_margin=g[0]>margin and s[0]>margin,
        both_inside_equivalence_band=all(-margin<a[0] and a[1]<margin for a in (g,s)),
        genetic_direction='positive' if g[0]>0 else 'negative' if g[1]<0 else 'unresolved',
        survival_direction='positive' if s[0]>0 else 'negative' if s[1]<0 else 'unresolved',
        interval_requirement='Valid prespecified simultaneous interval procedure; no exact bootstrap coverage asserted')


def conditional_gaussian_screen(plan):
    z=NormalDist().inv_cdf(1-plan['familywise_alpha']/4)
    n,v=plan['founder_count'],plan['visitor_history_count']
    adverse=plan['variance_uncertainty_scenarios'][1]['by_endpoint'];prob={}
    for out in plan['outcomes']:
        x=adverse[out['name']]
        se=math.sqrt(x['founder']/n+x['visitor']/v+x['interaction']/(n*v))
        # Correct-direction rejection, conditional on exactly known normal variance.
        prob[out['name']]=NormalDist().cdf(out['minimum_scientifically_meaningful_abs_effect']/se-z)
    return dict(normal_model_only=True,known_variance_assumed=True,
        biological_histories_generated=0,
        per_endpoint_correct_direction_probability_at_design_effect=prob,
        union_bound_joint_correct_direction_at_design_effect=max(0.,sum(prob.values())-1),
        FWER_at_global_null_union_bound=4*(1-NormalDist().cdf(z)),
        guarantees_power_for_Model3=False,
        note='Checks #585 approximation algebra only. Does not validate fitted variance, binary boundary distributions, cluster bootstrap coverage or biological operating characteristics.')


def review_candidate(plan,pilot):
    sr=plan['prospective_seed_registry'];n=plan['founder_count'];v=plan['visitor_history_count']
    if len(sr['founders'])!=n or len(set(sr['founders']))!=n or len(sr['visitors'])!=v or len(set(sr['visitors']))!=v:
        raise ValueError('incomplete prospective source axes')
    old_f=set(range(301001,301007))|set(range(291001,291007))|{181001,181002}
    old_v=set(range(302001,302007))|set(range(292001,292007))|{182001,182002}
    if set(sr['founders'])&old_f or set(sr['visitors'])&old_v:
        raise ValueError('prospective source overlap')
    if (sr['biological_streams_consumed']!=0 or plan.get('registered') is not False
        or plan.get('execution_authorized') is not False):raise ValueError('candidate cannot authorize biology')
    masters=set()
    for stage in sr['stages']:
        for f in range(n):
            for vv in range(v):
                key=f"{plan['study_id']}|105|{stage}|{f}|{vv}".encode()
                masters.add(hashlib.sha256(key).digest()[:16])
    if len(masters)!=n*v*2:raise ValueError('new source master collision')
    b=budget(n,v,1)
    if plan['stage_budget']!=b:raise ValueError('shared-prefix budget differs')
    passed=evaluate(plan,encoded(pilot))
    return dict(status='METHOD_REVIEW_SUBMISSION_READY_EXECUTION_NOT_AUTHORIZED',
        legacy_gate=passed, registered=False,method_reviewer_approved=False,
        execution_authorized=False,biological_runs_started=False,
        prospective_master_count=len(masters), prospective_master_collisions=0,
        budget=b,conditional_gaussian_check=conditional_gaussian_screen(plan),
        overall_scientific_gate='HOLD_PENDING_INDEPENDENT_METHOD_AND_OPERATING_CHARACTERISTIC_REVIEW')


def main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out-dir',type=Path,required=True)
    args=p.parse_args()
    if args.out_dir.exists():p.error('refuse overwrite')
    pilot=derive_inputs(*load_inputs());plan=candidate_plan(pilot);gate=review_candidate(plan,pilot)
    for name,obj in ((INPUT_NAME,pilot),(PLAN_NAME,plan),(OUT_NAME,gate)):
        path=args.out_dir/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(encoded(obj))
    print(json.dumps({'proxy_gate':gate['legacy_gate']['status'],
                     'scientific_gate':gate['overall_scientific_gate'],
                     'founders':plan['founder_count'],'visitors':plan['visitor_history_count'],
                     'unique_updates':gate['budget']['unique_update_ceiling']}))

if __name__=='__main__':main()
