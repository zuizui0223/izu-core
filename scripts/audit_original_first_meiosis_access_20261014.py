"""Read-only original 2,304-history gene-level first-meiosis/access audit.

Consumes exactly nine source-received ecological shard ZIPs, checks each
manifest/case SHA256 and independently reconstructs the pre-existing registered
six-category responses from original 201-census raw diploid genomes. No model
is imported or simulated; no clock predictor is fit; F1 is post-t0 information.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from collections import Counter,defaultdict
from pathlib import Path
import re
import zipfile
import numpy as np

CASE=re.compile(r'^(main|confirmation)_c([0-8])_r(\d+)\.npz$')
CLASS_LABELS=('assurance_first','investment_first','near_simultaneous',
              'assurance_only','investment_only','neither')
ORIGINAL_SOURCE_MANIFEST_SHA='4b23f2106d798215c2e466191ac88e6922ef209c909825b9205b75647898afff'
ORIGINAL_PRODUCER_SHA='cd9779c89c643c9daf4a9c9001ce14dcf5d3cf95300d98f50c4ba3a4d1998fae'
ORIGINAL_PROVIDER_ZIP_SHA={
  0:'5b850eaad6104f572f56df2a37da00fbc8473503a827703c82f6870a87e9a881',
  1:'bc675e9eb231ec7f6ac4cb7c26a762cd55d75ad8fff51eae0aa8e28568172280',
  2:'3673b1b07ed2742669f1ba43494ba814d7968cb200c6832c62a5a1c1640fe554',
  3:'676e84ff0729ba88dcd91cb161efeb2dc63f10b6679458695c5d2909c017e9c2',
  4:'900d3d22a36fa59241a933b8efc4b2fb8f320e4b25637e592640f31c529314fe',
  5:'b45f10aae6ec8fa437179285eb50cb3b98a35e3cc3e8610f6e8d36358daeb6e8',
  6:'03d9dcc3b7b993fcba9486bb543e01b8dcd75e40bbb0d5684c6cf72292105a42',
  7:'7a304cab06107d3a48d18bd033f07c046dad5c4ecb95eb2a1a4916ebd9d51876',
  8:'35a6c2da91bb02d50806a919777e21a2c855ab55b5fccc95f917a7af7d77bf62',
}


def sha256(b:bytes)->str:return hashlib.sha256(b).hexdigest()


def source_case_name(task):
    return f"{task['block']}_c{task['context']}_r{task['replicate']}.npz"


def events(means,pop):
    if means.shape!=(201,3) or pop.shape!=(201,) or pop[0]!=48:
        raise ValueError('Original source census dimensions differ')
    occupied=pop>0
    if np.any(occupied[1:] & ~occupied[:-1]):
        raise ValueError('Original population reappeared without seed arrival')
    if not np.isfinite(means[occupied]).all() or not np.isnan(means[~occupied]).all():
        raise ValueError('Original extinct traits must remain missing')
    onset=[]; transient=[]
    for col,sign in ((2,1),(1,-1)):
        x=occupied & (sign*(means[:,col]-means[0,col])>=.05)
        transient.append(int(np.flatnonzero(x)[0]) if x.any() else None)
        sustained=np.flatnonzero(np.convolve(x.astype(int),np.ones(20,dtype=int),mode='valid')==20)
        onset.append(int(sustained[0]) if len(sustained) else None)
    a,i=onset
    if a is None: label='neither' if i is None else 'investment_only'
    elif i is None:label='assurance_only'
    elif abs(a-i)<=5:label='near_simultaneous'
    else:label='assurance_first' if a<i else 'investment_first'
    return {'A':a,'I':i,'category':label},transient


def analyze(archive_paths:list[Path]):
    if len(archive_paths)!=9 or len({p.resolve() for p in archive_paths})!=9:
        raise ValueError('Exactly nine distinct original ecological provider archives required')
    archives=[];cells=defaultdict(list);rows=[];seen=set();clusters=defaultdict(set);seen_shards=set()
    for path in archive_paths:
        named=re.fullmatch(r'ecological-original-shard-([0-8])\.zip',path.name)
        if named is None or int(named[1]) in seen_shards:
            raise ValueError('Original source shard numbering incomplete or duplicated')
        shard_id=int(named[1]);seen_shards.add(shard_id)
        digest=hashlib.sha256()
        with path.open('rb') as h:
            for block in iter(lambda:h.read(1<<20),b''):digest.update(block)
        if digest.hexdigest()!=ORIGINAL_PROVIDER_ZIP_SHA[shard_id]:
            raise ValueError('Original provider ZIP full byte hash does not match frozen source')
        with zipfile.ZipFile(path) as z:
            manifest=json.loads(z.read('_COMPLETION.json'))
            if manifest.get('status')!='COMPLETE_FROZEN_ECOLOGICAL_SHARD' or manifest['cases']!=256:
                raise ValueError('Source original provider not independently admitted')
            registered={source_case_name(x['task']):x for x in manifest['records']}
            names=[k for k in z.namelist() if k.endswith('.npz')]
            if len(names)!=256 or len(set(names))!=256 or set(registered)!=set(names):
                raise ValueError('Source case inventory incomplete or extra')
            metadata_identity=manifest['identity']
            if (metadata_identity.get('technical') or metadata_identity.get('producer_sha256')!=ORIGINAL_PRODUCER_SHA
                or metadata_identity.get('source_manifest_sha256')!=ORIGINAL_SOURCE_MANIFEST_SHA
                or metadata_identity.get('numpy')!='2.2.6'):
                raise ValueError('Original source identity or numerical runtime changed')
            for filename in sorted(names):
                match=CASE.fullmatch(filename)
                if match is None:raise ValueError('Malformed original case name')
                block,context,replicate=match.groups();context=int(context);replicate=int(replicate)
                key=(block,context,replicate)
                if key in seen:raise ValueError('Duplicate original biological case across source ZIPs')
                seen.add(key);clusters[(block,replicate)].add(context)
                raw=z.read(filename)
                if sha256(raw)!=registered[filename]['sha256']:
                    raise ValueError('Original case NPZ SHA256 differs from producer receipt')
                with np.load(io.BytesIO(raw),allow_pickle=False) as src:
                    required={'alleles','offsets','population','means','metadata','parentage'}
                    if not required.issubset(src.files):raise ValueError('Incomplete raw original genetic and parentage data')
                    offs=src['offsets'];alleles=src['alleles'];pop=src['population'];means=src['means']
                    if len(offs)!=202 or offs[0]!=0 or offs[-1]!=len(alleles) or not np.array_equal(np.diff(offs),pop):
                        raise ValueError('Original raw age offsets/census mismatch')
                    a0=alleles[offs[0]:offs[1],2,:].mean(axis=1)
                    a1=alleles[offs[1]:offs[2],2,:].mean(axis=1)
                    f1_A_mutated=src['mutation_flags'][offs[1]:offs[2],2,:].any(axis=1)
                    unmutated_a1=a1[~f1_A_mutated]
                    if len(a0)!=48:raise ValueError('Original typed founder count invalid')
                    f0var=float(np.var(a0));f1var=float(np.var(a1)) if len(a1) else None
                    access=(bool(a1.max()>=a0.mean()+.05-1e-12) if len(a1) else False)
                    outcome,transient=events(means,pop)
                if outcome!=registered[filename]['events']['0.05']:
                    raise ValueError(f'Independent original six-category onset differs from frozen source: {filename}')
                row={
                    'case':filename.removesuffix('.npz'),
                    'founder':block,'original_context':context,'replicate':replicate,
                    'N_first_offspring':int(pop[1]),
                    'A_t0_expressed_variance':f0var,
                    'A_t1_expressed_variance':f1var,
                    'A_t1_any_individual_above_0p05':access,
                    'A_F1_A_mutated_offspring':int(np.count_nonzero(f1_A_mutated)),
                    'A_F1_has_unmutated_individual_above0p05':bool(len(unmutated_a1) and unmutated_a1.max()>=a0.mean()+.05-1e-12),
                    'A_transient_first':transient[0], 'I_transient_first':transient[1],
                    'A_sustained_first':outcome['A'],'I_sustained_first':outcome['I'],
                    'category':outcome['category'],
                    'A_f1_mean_change':float(means[1,2]-means[0,2]),
                }
                rows.append(row);cells[(block,context)].append(row)
            archives.append({'original_provider':path.name,'sha256':digest.hexdigest(),
                             'cases':len(names),'original_producer_sha256':metadata_identity['producer_sha256']})
    if seen_shards!=set(ORIGINAL_PROVIDER_ZIP_SHA) or len(rows)!=2304 or len(cells)!=18 or len(clusters)!=256 or any(len(v)!=9 for v in clusters.values()):
        raise ValueError('Full registered old cohort and 256 paired visitor-history streams required')
    cats=Counter(r['category'] for r in rows)
    benchmark=dict(zip(CLASS_LABELS,(335,435,358,895,10,271)))
    if any(cats.get(k,0)!=v for k,v in benchmark.items()):
        raise ValueError('Original existing published 2,304-outcome source readout mismatches')
    numbers=lambda xs:{'n':len(xs),'mean':float(np.mean(xs)),'median':float(np.median(xs)),
                         'min':float(np.min(xs)),'max':float(np.max(xs))}
    out={
      'schema':'chapter2_original_first_meiosis_access_2304_source_replay_v1',
      'status':'COMPLETE_ORIGINAL_2304_GENOTYPE_AND_EVENT_SHA_ADMITTED_EXPLORATORY',
      'source':{'frozen_original_biological_model_commit':'328548612e93469fcc8663f24548530a57399b9a',
                'original_provider_zips':archives,'verified_original_case_npzs':2304,
                'paired_history_clusters':256,'genetic_t0_profiles':18},
      'all_six_original_outcomes':dict(cats),
      'all_start_genetic_access':{
         'A_t0_phenotype_variance_zero':sum(r['A_t0_expressed_variance']==0 for r in rows),
         'A_F1_expressed_variance_positive':sum(r['A_t1_expressed_variance'] is not None and r['A_t1_expressed_variance']>0 for r in rows),
         'A_F1_population_has_genotype_at_least_founder_plus0p05':sum(r['A_t1_any_individual_above_0p05'] for r in rows),
         'A_F1_population_has_unmutated_genotype_at_least_founder_plus0p05':sum(r['A_F1_has_unmutated_individual_above0p05'] for r in rows),
         'A_F1_zero_A_mutated_offspring_cases':sum(r['A_F1_A_mutated_offspring']==0 for r in rows),
         'A_F1_new_mutated_offspring_distribution':numbers([r['A_F1_A_mutated_offspring'] for r in rows]),
         'A_F1_expressed_variance_distribution':numbers([r['A_t1_expressed_variance'] for r in rows if r['A_t1_expressed_variance'] is not None]),
         'A_after_F1_sustained_threshold_observed':sum(r['A_sustained_first'] is not None for r in rows),
         'A_transient_threshold_anytime':sum(r['A_transient_first'] is not None for r in rows),
         'A_transient_without_20_consecutive_censuses':sum(r['A_transient_first'] is not None and r['A_sustained_first'] is None for r in rows),
         'I_transient_threshold_anytime':sum(r['I_transient_first'] is not None for r in rows),
         'I_transient_without_20_consecutive_censuses':sum(r['I_transient_first'] is not None and r['I_sustained_first'] is None for r in rows),
         'A_sustained_onset_distribution':numbers([r['A_sustained_first'] for r in rows if r['A_sustained_first'] is not None]),
         'I_sustained_onset_distribution':numbers([r['I_sustained_first'] for r in rows if r['I_sustained_first'] is not None]),
         'A_first_transient_to_sustained_delay':numbers([r['A_sustained_first']-r['A_transient_first'] for r in rows if r['A_sustained_first'] is not None]),
         'I_first_transient_to_sustained_delay':numbers([r['I_sustained_first']-r['I_transient_first'] for r in rows if r['I_sustained_first'] is not None]),
      },
      'per_founder_context':[
        {'founder':b,'context':c,'n':len(v),'A_F1_variance_mean':float(np.mean([x['A_t1_expressed_variance'] for x in v])),
         'A_F1_variance_min':float(np.min([x['A_t1_expressed_variance'] for x in v])),
         'A_t1_genotype_at_least_plus0p05':sum(x['A_t1_any_individual_above_0p05'] for x in v),
         'A_transient_no_stable':sum(x['A_transient_first'] is not None and x['A_sustained_first'] is None for x in v),
         'categories':dict(Counter(x['category'] for x in v))}
        for (b,c),v in sorted(cells.items())
      ],
      'limitations':[
       'F1 segregation is an observed post-t0 mediator; it cannot be used as a t0-only prospective predictor without an explicit prospective segregation model.',
       'A positive F1 within-population variance or one high-genotype individual does not imply persistent population-mean response, fixed selected alleles or first passage.',
       'Original 2304 contexts share only 18 founder-by-visitors t0 biological states and 256 paired stochastic streams; no unpaired ecological replicate count is claimed.',
       'This is a diagnostic of the already exposed retrospective source cohort, not new independent stochastic histories or the unrun prospective 1536 pilot.',
       'The pilot deliberately changes A structural threshold support and I hidden homolog segregation. These effects are not isolated natural-island causal claims.',
      ],
      'new_biological_histories_generated':0,
      'new_Q1Q2_clock_confirmed':False,
    }
    return out,rows


def main():
 p=argparse.ArgumentParser();p.add_argument('--archives',nargs=9,type=Path,required=True)
 p.add_argument('--out',type=Path,required=True)
 p.add_argument('--case-csv',type=Path)
 args=p.parse_args()
 if args.out.exists() or (args.case_csv is not None and args.case_csv.exists()):
     raise FileExistsError('Existing original source review output must never be overwritten')
 report,rows=analyze(args.archives)
 args.out.parent.mkdir(parents=True,exist_ok=True)
 with args.out.open('x',encoding='utf-8') as f:json.dump(report,f,indent=2,ensure_ascii=False);f.write('\n')
 if args.case_csv is not None:
     import csv
     args.case_csv.parent.mkdir(parents=True,exist_ok=True)
     with args.case_csv.open('x',encoding='utf-8',newline='') as f:
         writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
 print(json.dumps({'status':report['status'],'access':report['all_start_genetic_access']},indent=2))

if __name__=='__main__':main()
