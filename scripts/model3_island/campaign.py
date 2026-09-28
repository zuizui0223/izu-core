"""Prospective ecological contrasts; constants are declared before production.

Rates are dimensionless model regimes, not estimates for named islands. The pilot
changes only horizon/cohort size and checks execution, not which effects to keep.
"""
import argparse
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path

from .types import Config,ArrivalConfig,EVENT_ORDER
from .design import source_hashes,validate_design,canonical


AXIS5=[0.,.25,.5,.75,1.]
AXIS7=[0.,.25,.4,.5,.6,.75,1.]
AXIS11=[0.,.125,.25,.325,.4,.45,.5,.55,.6,.75,1.]


def build_design(*,pilot=False):
    seed=ArrivalConfig(0.,1.,1.,'exponential',.5,0.)
    visitor=ArrivalConfig(.3,1.,1.,'exponential',.8,.05)
    config=Config(1,EVENT_ORDER,'reproductive_year',48,200,0.,8.,20.,.5,1.,.5,0.,.025,
        'fixed',.5,'delayed',0.,0.,.4,'count_scaled',4.,1.,1.,seed,visitor,
        'founding',4,.2,1.,(.5,.5,.5),.15)
    d=dict(schema_version=1,frozen=not pilot,model='discrete_genotype_density',base_config=asdict(config),
        storage={'density_counts':'checkpoints_and_replay_digest','checkpoint_every':100},
        units={'time':'reproductive_year','distance':'dispersal_scale','traits':'unit_interval'},
        parameter_ranges={'trait':[0.,1.],'distance':[0.,3.],'survival':[0.,.9],
            'mutation_probability':[0.,.001],'capacity':[48,768],'time':[1,2000]},
        mechanism_flags={'self_exclusion':True,'fixed_inbreeding_depression':True,'evolving_load':False},
        cohorts={'pilot':[71001,71002],'production':list(range(72001,72129)),
                 'heldout':list(range(73001,73129))},demographic_seeds=[17,29],founder_seed=74001,
        numerical_tolerances={'trait':.01,'occupancy':.02},
        effect_thresholds={'investment':.05,'occupancy':.10,'heterozygosity':.10},horizons=[200,400,2000],
        precision={'proportion_half_width':.125,'confidence':.95,'max_histories':128,
            'conditional_rule':'fixed_R_report_interval_and_eligible_n','rare_event_rule':'report_upper_bound'},
        resource_limits={'runtime_seconds':43200.,'memory_mb':3072.,'output_mb':8192.,'min_free_mb':4096.},source_hashes=source_hashes(),
        claim_exclusions=['PDE','Q1_fit','drift_only','continuous_trait_convergence','purging',
            'named_island_calibration','natural_direct_indirect_effect','evolutionary_optimum'],families=[])

    def segment(years,count=4,optimum=.5,pool=0):
        return dict(years=years,pool=pool,count=count,optimum=optimum,sd=.12)

    def history(years=200):
        return {'kind':'segments','segments':[segment(years)]}

    def add(family,question,cell_id,*,patch=None,recipe=None,count=48,start=.5,
            grid=None,projection='continuous',immigration='source',group=None,sd=.15,cohorts=None):
        if not any(f['name']==family for f in d['families']):
            d['families'].append(dict(name=family,question=question,cells=[]))
        f=next(f for f in d['families'] if f['name']==family)
        f['cells'].append(dict(id=cell_id,kind='assay' if family=='assays' else 'trajectory',
            config_patch=patch or {},grid_axes=grid or [AXIS7,AXIS7,[.5]],
            founders=dict(count=count,draw_count=min(count,48),means=[.5,start,.5],sd=sd,birth_year=0),
            history=recipe or history(),cohorts=cohorts or ['production'],weight=1.,
            start_id=f'investment_{start}',pair_group=group or family,
            projection_mode=projection,immigration_mode=immigration,counterfactual=None))

    # Fixed-state assays: census and genotypes identical in every intervention.
    for activity in (.05,.4):
        for optimum in (.5,.9):
            for assurance in (0.,.5):
                for cost in (0.,.5):
                    name=f'assay_a{activity}_m{optimum}_s{assurance}_c{cost}'.replace('.','p')
                    add('assays','Does attraction lose outcross return at fixed assurance and fixed cost?',name,
                        patch={'activity':activity,'fixed_assurance':assurance,'investment_cost':cost},
                        recipe={'kind':'segments','segments':[segment(200,optimum=optimum)]})

    schedules={
        'uninterrupted':[segment(200)],
        'early_gap':[segment(40,count=0,pool=1),segment(160)],
        'late_gap':[segment(40),segment(40,count=0,pool=1),segment(120)],
        'early_mismatch':[segment(40,optimum=.9,pool=2),segment(160)],
        'late_mismatch':[segment(40),segment(40,optimum=.9,pool=2),segment(120)]}
    for name,segments in schedules.items():
        add('chronology','Matched visitor identities/exposure, order reversed, common final 120-year recovery',
            'order_'+name,recipe={'kind':'segments','segments':segments})

    for pd in (0.,1.,3.):
        for vd in (0.,1.,3.):
            add('connectivity','Separate seed and visitor reach probabilities across repeated islands',
                f'connectivity_p{int(pd)}_v{int(vd)}',recipe={'kind':'assembly'},
                patch={'seed_arrival':{'supply':.3,'distance':pd},'visitor_arrival':{'distance':vd}})

    for label,kind,n,nv in [('founding_empty','founding',0,0),('separation_inherited','separation',48,4),
                          ('founding_matched','founding',48,4),('separation_matched','separation',48,4)]:
        add('initialization','Founding/separation bundles and identical-present-state label control',label,
            count=n,recipe={'kind':'assembly'},patch={'island_history':kind,'initial_visitors':nv,
            'seed_arrival':{'supply':.3}})

    for label,patch in [
        ('fixed_disabled',{'fixed_assurance':0.}),('fixed_half',{}),('fixed_high',{'fixed_assurance':.9}),
        ('evolving_delayed',{'assurance_mode':'evolving'}),
        ('evolving_discount',{'assurance_mode':'evolving','pollen_discount':1.}),
        ('evolving_prior',{'assurance_mode':'evolving','assurance_timing':'prior'}),
        ('evolving_cost',{'assurance_mode':'evolving','assurance_cost':.5})]:
        add('assurance','Fixed versus inherited assurance feedback; discount and timing sensitivities',
            'assurance_'+label,patch=patch,recipe={'kind':'segments','segments':schedules['early_gap']},
            grid=[AXIS5]*3)

    for label,mu,supply,mode in [('visitor_only',0.,0.,'source'),('source_immigrants',0.,.3,'source'),
        ('resident_immigrants',0.,.3,'resident_matched'),('mutation_low',.0001,0.,'source'),
        ('mutation_high',.001,0.,'source')]:
        add('recovery','Visitor restoration versus demographic/genetic input; mutation present throughout',
            'recovery_'+label,patch={'mutation_rate':mu,'seed_arrival':{'supply':supply}},
            recipe={'kind':'segments','segments':schedules['early_gap'],'seed_window':[80,200]},immigration=mode)
    for mu in (0.,.0001):
        add('recovery','Longer response/recovery with declared mutation, not accelerated natural history',
            f'recovery_long_mu{mu}'.replace('.','p'),patch={'years':2000,'mutation_rate':mu},
            recipe={'kind':'segments','segments':[segment(400,count=0,pool=1),segment(1600)]},group='long_recovery')

    for capacity in (48,192,768):
        for convention in ('per_capita','fixed_total'):
            supply=.3*(capacity/48 if convention=='per_capita' else 1)
            add('scaling','Large-capacity at fixed density/migration versus island-area with fixed total input',
                f'scale_{convention}_{capacity}',patch={'capacity':capacity,'seed_arrival':{'supply':supply}},
                count=capacity,group='scale_'+convention)
    for n,axis in [(5,AXIS5),(7,AXIS7),(11,AXIS11)]:
        for projection in ('grid','continuous'):
            add('scaling','Numerical refinement is separate from finite-population effects',
                f'grid_{n}_{projection}',grid=[axis,axis,[.5]],projection=projection,
                patch={'mutation_rate':.0001},group='grid_fixed')
    for label,axes in [('coarse',[AXIS5]*3),('fine',[AXIS7,AXIS7,AXIS5])]:
        add('scaling','Refinement of the inherited-assurance comparison',f'grid_evolving_{label}',
            grid=axes,patch={'assurance_mode':'evolving'},group='grid_evolving')

    for s,label in [(0.,'annual'),(.75,'perennial4'),(.9,'perennial10')]:
        for convention in (['annual'] if s==0 else ['annual','lifetime']):
            factor=1-s if convention=='lifetime' else 1.
            add('life_history','Adult longevity with annual versus lifetime reproductive budgets',
                f'life_{label}_{convention}',patch={'years':400,'survival':s,
                    'ovule_budget':8*factor,'pollen_budget':20*factor},
                recipe={'kind':'segments','segments':[segment(80,count=0,pool=1),segment(320)]})

    for distance in (0.,3.):
        for start in (.3,.5,.7):
            add('transport','Starting state crossed with visitor histories and demographic repeats; held-out regimes',
                f'transport_d{int(distance)}_s{int(start*10)}',start=start,
                recipe={'kind':'assembly'},patch={'visitor_arrival':{'distance':distance}},
                cohorts=['production','heldout'],group=f'transport_d{int(distance)}')
    # Recovery means response relative to an otherwise identical uninterrupted
    # environment, including the same mutation regime and seed arrival window.
    recovery=next(f for f in d['families'] if f['name']=='recovery')
    for treatment in list(recovery['cells']):
        control=deepcopy(treatment)
        control['id']=treatment['id']+'_uninterrupted'
        years=treatment['config_patch'].get('years',config.years)
        control['history']['segments']=[segment(years)]
        treatment['counterfactual']=control['id']
        recovery['cells'].append(control)
    if pilot:
        d['horizons']=[6]; d['demographic_seeds']=[17]; d['resource_limits']['runtime_seconds']=1800.
        for family in d['families']:
            # All declared arms are exercised; no effect-based screening.
            for cell in family['cells']:
                cell['cohorts']=['pilot']; cell['config_patch']['years']=6
                recipe=cell['history']
                if recipe['kind']=='segments':
                    segments=recipe['segments']; n=len(segments)
                    for i,seg in enumerate(segments): seg['years']=1 if i<n-1 else 6-(n-1)
                if 'seed_window' in recipe: recipe['seed_window']=[3,6]
    validate_design(d)
    return d


def main():
    p=argparse.ArgumentParser(); p.add_argument('--pilot',action='store_true'); p.add_argument('--output',required=True)
    a=p.parse_args(); path=Path(a.output); path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists(): raise ValueError('do not overwrite an existing prospective manifest')
    path.write_bytes(canonical(build_design(pilot=a.pilot)))


if __name__=='__main__': main()
