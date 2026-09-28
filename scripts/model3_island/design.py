"""Prospective, explicit-cell experiment manifests; no outcome-based arm selection."""
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
import json
import math
import re

import numpy as np

from .types import Config
from .density import make_grid

ROOT=Path(__file__).resolve().parents[2]
FAMILIES={'assays','chronology','connectivity','initialization','assurance',
          'recovery','scaling','life_history','transport'}
REQUIRED={'schema_version','frozen','model','base_config','units','parameter_ranges',
          'mechanism_flags','cohorts','demographic_seeds','founder_seed','numerical_tolerances',
          'effect_thresholds','horizons','precision','resource_limits','source_hashes',
          'claim_exclusions','families','storage'}
CELL_FIELDS={'id','kind','config_patch','grid_axes','founders','history','cohorts',
             'weight','start_id','pair_group','projection_mode','immigration_mode','counterfactual'}


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()


def digest(value):
    return sha256(canonical(value)).hexdigest()


def source_hashes():
    files=sorted((ROOT/'scripts/model3_island').glob('*.py'))
    return {p.relative_to(ROOT).as_posix():sha256(p.read_bytes()).hexdigest() for p in files}


def merge_config(base, patch):
    result=deepcopy(base)
    for k,v in patch.items():
        if k not in result:
            raise ValueError(f'unknown configuration field: {k}')
        result[k]=merge_config(result[k],v) if isinstance(v,dict) else v
    return result


def _integer(x,lower=0):
    return isinstance(x,int) and not isinstance(x,bool) and x>=lower


def _positive(x):
    return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x) and x>0


def _validate_history(recipe, config):
    if 'seed_window' in recipe:
        w=recipe['seed_window']
        if not isinstance(w,list) or len(w)!=2 or not all(_integer(x) for x in w) or not 0<=w[0]<=w[1]<=config.years:
            raise ValueError('invalid seed arrival window')
    fields=set(recipe)-{'seed_window'}
    if recipe.get('kind')=='assembly':
        if fields!={'kind'}:
            raise ValueError('unknown assembly settings')
        return
    if recipe.get('kind')!='segments' or fields!={'kind','segments'}:
        raise ValueError('unknown history recipe')
    total=0; pools={}
    for s in recipe['segments']:
        if set(s)!={'years','pool','count','optimum','sd'}:
            raise ValueError('segment fields must be explicit')
        if not _integer(s['years'],1) or not _integer(s['pool']) or not _integer(s['count']):
            raise ValueError('invalid segment counts')
        if not 0<=s['optimum']<=1 or not math.isfinite(s['sd']) or s['sd']<0:
            raise ValueError('invalid segment trait distribution')
        if s['count'] and config.background_resources==0:
            raise ValueError('controlled visitors need background resources')
        signature=(s['count'],s['optimum'],s['sd'])
        if s['pool'] in pools and pools[s['pool']]!=signature:
            raise ValueError('pool ID changes visitor composition')
        pools[s['pool']]=signature
        total+=s['years']
    if total!=config.years:
        raise ValueError('segment years must cover the entire horizon')


def validate_design(document):
    d=document
    if not isinstance(d,dict) or set(d)!=REQUIRED:
        raise ValueError('manifest must contain exactly the required scientific fields')
    canonical(d)  # Reject nonfinite numbers before coercion.
    if (set(d['storage'])!={'density_counts','checkpoint_every'}
            or d['storage']['density_counts']!='checkpoints_and_replay_digest'
            or not _integer(d['storage']['checkpoint_every'],1)):
        raise ValueError('invalid storage/replay contract')
    if d['schema_version']!=1 or not isinstance(d['frozen'],bool) or d['model']!='discrete_genotype_density':
        raise ValueError('unsupported schema or model label')
    if d['units']!={'time':'reproductive_year','distance':'dispersal_scale','traits':'unit_interval'}:
        raise ValueError('uncalibrated physical units are not supported')
    if not d['parameter_ranges'] or not d['mechanism_flags'] or not d['claim_exclusions']:
        raise ValueError('ranges, mechanisms and claim exclusions cannot be empty')
    for bounds in d['parameter_ranges'].values():
        if not isinstance(bounds,list) or len(bounds)!=2 or not bounds[0]<=bounds[1]:
            raise ValueError('invalid parameter range')
    if d['mechanism_flags']!={'self_exclusion':True,'fixed_inbreeding_depression':True,'evolving_load':False}:
        raise ValueError('mechanism flags must match this implemented operator')
    if not {'PDE','Q1_fit','drift_only','continuous_trait_convergence'}<=set(d['claim_exclusions']):
        raise ValueError('required claim boundaries missing')
    Config.from_dict(d['base_config'])
    if set(d['cohorts'])!={'pilot','production','heldout'}:
        raise ValueError('three disjoint cohorts required')
    seeds=[]
    for cohort in d['cohorts'].values():
        if not isinstance(cohort,list) or not cohort or not all(_integer(s) and s<2**31-1 for s in cohort):
            raise ValueError('invalid history seeds')
        seeds+=cohort
    if len(set(seeds))!=len(seeds):
        raise ValueError('history cohorts overlap or repeat')
    ds=d['demographic_seeds']
    if not ds or not all(_integer(x) for x in ds) or len(set(ds))!=len(ds) or not _integer(d['founder_seed']):
        raise ValueError('invalid independent demographic or founder seeds')
    for name in ('numerical_tolerances','effect_thresholds'):
        if not d[name] or not all(_positive(x) for x in d[name].values()):
            raise ValueError(f'invalid {name}')
    if not d['horizons'] or not all(_integer(x,1) for x in d['horizons']):
        raise ValueError('invalid horizons')
    p=d['precision']
    if set(p)!={'proportion_half_width','confidence','max_histories','conditional_rule','rare_event_rule'}:
        raise ValueError('precision rules incomplete')
    h=p['proportion_half_width']
    if not _positive(h) or h>1 or p['confidence']!=.95 or not _integer(p['max_histories'],1):
        raise ValueError('invalid precision target')
    required=math.ceil(1.96**2/(4*h*h))
    if any(not required<=len(d['cohorts'][k])<=p['max_histories'] for k in ('production','heldout')):
        raise ValueError('independent histories do not meet conservative precision planning')
    if p['conditional_rule']!='fixed_R_report_interval_and_eligible_n' or p['rare_event_rule']!='report_upper_bound':
        raise ValueError('only fixed sample size, no outcome-based stopping, supported')
    limits=d['resource_limits']
    if set(limits)!={'runtime_seconds','memory_mb','output_mb','min_free_mb'} or not all(_positive(x) for x in limits.values()):
        raise ValueError('invalid resource limits')
    if not d['source_hashes'] or any(not re.fullmatch(r'[0-9a-f]{64}',v) for v in d['source_hashes'].values()):
        raise ValueError('invalid source hashes')
    for path in d['source_hashes']:
        if not (ROOT/path).resolve().is_relative_to(ROOT) or Path(path).is_absolute():
            raise ValueError('source paths must stay inside the repository')
    names=[]; cell_ids=[]
    for family in d['families']:
        if set(family)!={'name','question','cells'} or family['name'] not in FAMILIES or not family['question'] or not family['cells']:
            raise ValueError('invalid experiment family')
        names.append(family['name'])
        for cell in family['cells']:
            if set(cell)!=CELL_FIELDS or not re.fullmatch(r'[a-z0-9_-]+',cell['id']):
                raise ValueError('cell fields or ID invalid')
            cell_ids.append(cell['id'])
            if cell['projection_mode'] not in ('grid','continuous') or cell['immigration_mode'] not in ('source','resident_matched'):
                raise ValueError('unknown numerical or immigration mode')
            if cell['kind'] not in ('trajectory','assay') or not _positive(cell['weight']) or not cell['start_id'] or not cell['pair_group']:
                raise ValueError('invalid cell type, estimand labels or weight')
            if not cell['cohorts'] or len(set(cell['cohorts']))!=len(cell['cohorts']) or not set(cell['cohorts'])<=set(d['cohorts']):
                raise ValueError('invalid cell cohort')
            config=Config.from_dict(merge_config(d['base_config'],cell['config_patch']))
            if config.years not in d['horizons']:
                raise ValueError('cell horizon not prospectively declared')
            for arrival in (config.seed_arrival,config.visitor_arrival):
                bounds=d['parameter_ranges'].get('distance')
                if bounds is None or not bounds[0]<=arrival.distance<=bounds[1]:
                    raise ValueError('distance outside declared support')
            axes=cell['grid_axes']
            if len(axes)!=3 or any(not len(a) for a in axes):
                raise ValueError('three nonempty allele axes required')
            classes=math.prod(len(a)*(len(a)+1)//2 for a in axes)
            # Visitor-factorized density operator: no genotype-pair dense matrix.
            gametes=math.prod(len(a) for a in axes)
            working_bytes=64*(classes*gametes+gametes**2+config.capacity**2)+8*(config.years+1)*classes
            if working_bytes>limits['memory_mb']*1024**2:
                raise ValueError('grid or capacity exceeds declared memory budget')
            make_grid(axes)
            if config.mutation_rate and config.mutation_sd:
                for k,axis in enumerate(axes):
                    if (k<2 or config.assurance_mode=='evolving') and (axis[0]!=0 or axis[-1]!=1):
                        raise ValueError('mutating grid does not span the unit interval')
            founder=cell['founders']
            if set(founder)-{'draw_count'}!={'count','means','sd','birth_year'} or not _integer(founder['count']) or founder['count']>config.capacity:
                raise ValueError('invalid founding census')
            draws=founder.get('draw_count',founder['count'])
            if not _integer(draws) or (founder['count'] and (not draws or founder['count']%draws)) or (not founder['count'] and draws):
                raise ValueError('underlying founder draw cannot match the declared census')
            if len(founder['means'])!=3 or not all(0<=x<=1 for x in founder['means']) or founder['sd']<0 or not isinstance(founder['birth_year'],int) or founder['birth_year']>0:
                raise ValueError('invalid founding trait state')
            _validate_history(cell['history'],config)
    if len(set(names))!=len(names) or len(set(cell_ids))!=len(cell_ids):
        raise ValueError('repeated family or cell IDs')
    for family in d['families']:
        for cell in family['cells']:
            if cell['counterfactual'] is not None and (cell['counterfactual'] not in cell_ids or cell['counterfactual']==cell['id']):
                raise ValueError('invalid counterfactual link')
    if d['frozen'] and set(names)!=FAMILIES:
        raise ValueError('frozen production must include every declared experiment family')


def compile_design(document):
    validate_design(document)
    cases=[]
    for family in document['families']:
        for cell in family['cells']:
            for cohort in cell['cohorts']:
                for history_seed in document['cohorts'][cohort]:
                    # An assay has no demographic stochasticity; do not duplicate it.
                    for demographic_seed in (document['demographic_seeds'] if cell['kind']=='trajectory' else [0]):
                        case=dict(cell=deepcopy(cell),family=family['name'],cohort=cohort,
                            history_seed=history_seed,demographic_seed=demographic_seed,
                            config=merge_config(document['base_config'],cell['config_patch']))
                        case['case_id']=f"{cell['id']}-{cohort}-h{history_seed}-d{demographic_seed}"
                        cases.append(case)
    return cases
