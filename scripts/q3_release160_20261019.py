"""Compile and audit ONE source-bound 160x160 review candidate.

No biological imports, RNG sampling, experiment execution, approval generation,
or change to the earlier 136-candidate, technical-only drivers, or #585 gate.
The assignment file is a planning manifest, not a population or result archive.
"""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
from statistics import NormalDist

ROOT=Path(__file__).resolve().parents[1]
BASE='d31ae2f3fa981f2bb523357cd434a1a66ef0c818'
OC='docs/audits/CHAPTER2_JOINT_OC_COMPACT_20261019.json'
SOURCE_BLOBS={
 'scripts/model3_island/__init__.py':'b385daf32fb3d1a2435ef97fce62f47c8f56e81f',
 'scripts/model3_island/types.py':'0bc427b3261e7baf1651648ee879b368f9bf935b',
 'scripts/model3_island/history.py':'0c58aee6f73ae133d96d8da4dd6678886ff3061c',
 'scripts/model3_island/randomness.py':'46f1ee55899e729cdd09d9dbb9332694ef1e2071',
 'scripts/model3_island/population.py':'20e90f249f63e9f37e8801d19d9b75cade2fe193',
 'scripts/model3_island/reproduction.py':'95314698a3296b6f13b8c053c36f2df0b7b744ca',
 'scripts/chapter2_q3_balanced_assurance_founders_20261018.py':'5e1c82afd2369c6117f847be8d7f3715814cc102',
 'scripts/q3_joint_inference_20261019.py':'61f10f1bb680310068136ea1b481f0c466c0f314',
 'scripts/q3_native_runner_20261019.py':'9c8ba3297df8c5a7655e0c5d1590af84de6858bd',
 'scripts/q3_partitioned_runner_20261019.py':'4daf07b6147210c14026a77270c98eb0212ce502',
 OC:'794f4915b8b08f80674dfa0db11ede1db655449e',
}


def canonical(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()


def sha(x):return hashlib.sha256(x).hexdigest()


def candidate():
    """The prior 136-source registry is retained. These are distinct proposed IDs."""
    n=160*160
    return dict(
      schema='q3_joint160_consolidated_review_candidate_v2',
      status='PROPOSED_NOT_REGISTERED_OR_EXECUTABLE',date='2026-10-19',
      study_id='ch2_joint160_consolidated_20261019_v2',parent_paper_PR=590,work_PR=597,
      sources=dict(base_commit=BASE,old136_plan_git_blob='1491a6523eb2b13d0e8a42508990c7e80c869819',
        old136_plan_path='docs/protocols/CHAPTER2_Q3_JOINT_METHOD_REVIEW_CANDIDATE_20261018.json',
        original_136_candidate_unchanged=True,required_git_blobs=dict(SOURCE_BLOBS)),
      axes=dict(founders=160,visitors=160,demographic_repeats=1),
      design=dict(capacity=48,policies=['fixed','evolving'],budgets=[8.0,4.5],
        fork=35,end=80,initial_expressed_A_every_adult=.5,
        A_carrier_pairs=[[.25,.75],[.5,.5],[.75,.25]],adults_per_A_pair=16,
        assurance_timing='delayed',assurance_cost=.5,depression=.5,
        I_alleles=[.375,.5,.625],mutation=False,immigration=False,adult_survival=0.,
        visitor_updates={'0..4':6,'5..34':1,'35..79':0},
        genetic_target='own realized founder mean I; first living max allele < target-1e-12',
        extinction='first empty census; traits undefined; extinction competes with closure',
        post_return_evolution_paths=0),
      decision=dict(endpoint_order=['genetic_loss','survival_interaction'],
        genetic_loss='CIF_G(evolving,B8)-CIF_G(fixed,B8) including shared-prefix events',
        survival_interaction='(E-F at B4.5)-(E-F at B8), all allocated populations retained',
        method='q3_joint_inference_20261019:pigeonhole variance+t',
        confidence_per_endpoint=.975,familywise_alpha=.05,df=159,margin=.10,
        margin_kind='normative resolution proposal; NOT approved field threshold',
        joint_positive='both interval lower bounds >0',
        both_over_margin='both lower bounds >.10; NOT the .80 power target',
        non_significant_is_equivalent=False,degenerate_variance='unresolved',
        group_G_negative_S_positive='survival benefit with less closure, NOT joint positive'),
      seed_registry=dict(namespace='ch2_joint160_consolidated_20261019_v2:106:planning-only',
        founders=list(range(501001,501161)),visitors=list(range(502001,502161)),
        masters='SHA256(namespace|stage|founder_seed|visitor_seed) first 16 bytes big endian',
        stages=['prefix','fork'],policy_budget_not_in_master=True,
        eventwise_rng_coupling_guaranteed=False,biological_rng_calls=0,
        preceding_candidate_and_pilot_sources_excluded=True),
      partition=dict(shards=32,assignment='(founder_index*160+visitor_index)%32',
        whole_crossing_keeps_both_policies_and_budgets=True,crossings_per_shard=800,
        worker_model='local processes only; host count and worker concurrency not selected'),
      budget=dict(crossings=n,prefix_tasks=2*n,future_tasks=4*n,
        prefix_updates=70*n,future_updates=180*n,unique_updates=250*n,
        rectangular_upper_updates=320*n,saved_state_slots=256*n),
      storage=dict(raw_arrays_per_copy=n*256*(48*118+8),
        raw_arrays_two_copies=2*n*256*(48*118+8),
        proposed_capacity_reserve_bytes=100_000_000_000,
        reserve_kind='operational planning headroom, NOT predicted compressed size',
        archive_location=None,quota_reserved=False,retention_approved=False,
        uncompressed_arrays_exclude_metadata_and_filesystem_overhead=True),
      claim_scope=dict(genetic_access_is_necessary_not_realized_recovery=True,
        both_endpoints_are_different_environment_contrasts=True,
        full_locus_genetic_mediation_not_identified=True,
        stochastic_recovery_time_not_measured=True,wild_island_generalization=False),
      approvals=dict(independent_method_review=None,margin_endorsement=None,
                     final_registration=None,resource_and_archive_approval=None,
                     production_runner_integration=None),
      registered=False,execution_authorized=False)


def validate(p):
    if not isinstance(p,dict) or p!=candidate():
        raise ValueError('candidate changes, approval claims or design drift require a distinct reviewed version')
    return True


def snapshot_sources(root=ROOT):
    out={}
    for name,expected in SOURCE_BLOBS.items():
        raw=(Path(root)/name).read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        if blob!=expected:raise ValueError('pinned source mismatch: '+name)
        out[name]=dict(git_blob=blob,sha256=sha(raw),bytes=len(raw))
    return out


def load_oc():
    raw=(ROOT/OC).read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    if blob!=SOURCE_BLOBS[OC]:raise ValueError('OC source mismatch')
    d=json.loads(raw)
    if (d['independent_axes']!=[160,160] or d['retained_statistical_experiments']!=60000
        or d['execution_authorized'] is not False
        or d['minimum_joint_power_MC_lower']<.8 or d['maximum_null_FWER_MC_upper']>.05):
        raise ValueError('OC evidence is not the reviewed 160-axis calibration')
    return d


def assignments(p):
    validate(p)
    reg=p['seed_registry']
    for fi,f in enumerate(reg['founders']):
        for vi,v in enumerate(reg['visitors']):
            cell=fi*160+vi
            masters={stage:hashlib.sha256(f"{reg['namespace']}|{stage}|{f}|{v}".encode()).digest()[:16].hex()
                     for stage in reg['stages']}
            yield dict(cell=cell,shard=cell%32,founder_seed=f,visitor_seed=v,
                       masters=masters,policies=p['design']['policies'],
                       budgets=p['design']['budgets'],expected_task_files=6)


def audit(p,*,storage_parent=ROOT,available_bytes=None):
    validate(p);sources=snapshot_sources();oc=load_oc()
    parent=Path(storage_parent).resolve(strict=True)
    if not parent.is_dir():raise ValueError('storage probe must be an existing directory')
    free=shutil.disk_usage(parent).free if available_bytes is None else available_bytes
    if type(free) is not int or free<0:raise ValueError('nonnegative byte capacity required')
    minimum=p['storage']['raw_arrays_two_copies']; reserve=p['storage']['proposed_capacity_reserve_bytes']
    resource=dict(parent=str(parent),free_bytes=free,uncompressed_two_copy_baseline_bytes=minimum,
                  proposed_reserve_bytes=reserve,admitted=free>=reserve,
                  raw_shortfall_bytes=max(0,minimum-free),reserve_shortfall_bytes=max(0,reserve-free),
                  is_reserved_quota=False,persistence_established=False,
                  uncompressed_baseline_not_a_compressed_size_lower_bound=True,
                  observation='live filesystem' if available_bytes is None else 'injected test capacity')
    unresolved=['independent_method_and_margin_review_missing',
                'production_runner_binding_missing',
                'archive_location_and_retention_not_approved',
                'final_registration_and_execution_approval_missing']
    if not resource['admitted']:unresolved.append('insufficient_planning_capacity')
    # An unchanged legacy normal proxy is reproduced as arithmetic, not as a
    # call to #585 or an approval of the proposed margins or source variances.
    c=NormalDist().inv_cdf(1-.05/4)+NormalDist().inv_cdf(.9)
    vc={'genetic_loss':[.02833333333333334,.03333333333333333,.5794444444444444],
        'survival_interaction':[0.,.002222222222222224,.08388888888888889]}
    proxy={k:c*math.sqrt(f/160+v/160+e/(160*160)) for k,(f,v,e) in vc.items()}
    adverse=c*math.sqrt(.05/160+.05/160+.85/(160*160))
    return dict(status='HOLD_NOT_EXECUTABLE',candidate_sha256=sha(canonical(p)),
        source_validation='PASS',pinned_sources=sources,
        calibration=dict(statistical_trials=60000,scenario_conditional=True,
          joint_detection_MC_lower=oc['minimum_joint_power_MC_lower'],
          null_error_MC_upper=oc['maximum_null_FWER_MC_upper'],
          Model3_specific_power_validated=False),
        recomputed_normal_proxy=dict(baseline=proxy,adverse_both=adverse,
          is_independent_585_approval=False,variance_envelope_is_assumption=True),
        resource=resource,unresolved=unresolved,registered=False,
        execution_authorized=False,new_biological_updates=0,
        technical_runner_still_exact_3x3=True,
        decision='Consolidated method/deployment candidate; no source cohorts generated')


def emit(out):
    p=candidate();validate(p);sources=snapshot_sources()
    out=Path(out)
    if out.exists():raise FileExistsError('refuse overwrite of planning outputs')
    out.mkdir(parents=True,exist_ok=False)
    (out/'CANDIDATE_160.json').write_text(json.dumps(p,sort_keys=True,indent=2)+'\n')
    h=hashlib.sha256();seen=set();shards=[0]*32;n=0
    with (out/'ASSIGNMENTS.jsonl.gz').open('xb') as raw:
        with gzip.GzipFile(filename='',fileobj=raw,mode='wb',mtime=0) as z:
            for r in assignments(p):
                line=canonical(r)+b'\n';h.update(line);z.write(line)
                for key in r['masters'].values():
                    if key in seen:raise ValueError('master key collision')
                    seen.add(key)
                shards[r['shard']]+=1;n+=1
    if n!=25600 or shards!=[800]*32 or len(seen)!=51200:
        raise ValueError('incomplete allocation')
    result=dict(status='COMPLETE_PLANNING_MANIFEST_NOT_EXECUTION',planned_crossings=n,
      proposed_task_files=6*n,stage_master_keys=len(seen),assignment_digest=h.hexdigest(),
      compressed_assignment_sha256=sha((out/'ASSIGNMENTS.jsonl.gz').read_bytes()),
      candidate_sha256=sha(canonical(p)),shard_crossing_counts=shards,
      biological_rng_calls=0,biological_updates=0,execution_authorized=False,
      registered=False,source_hashes=sources,producer_sha256=sha(Path(__file__).read_bytes()))
    (out/'COMPLETE.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    return result


def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--out',required=True,type=Path)
    a.add_argument('--storage-parent',type=Path,default=ROOT)
    args=a.parse_args()
    report=audit(candidate(),storage_parent=args.storage_parent)
    receipt=emit(args.out)
    (args.out/'READINESS.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps(dict(status=report['status'],crossings=receipt['planned_crossings'],
                         unresolved=report['unresolved'],execution_authorized=False)))

if __name__=='__main__':main()
