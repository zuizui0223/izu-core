"""Source-backed supporting figure; distinct experiments remain separate."""
from pathlib import Path
import csv
import hashlib
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/figures/model3_genetic_realization_20261005'
OUT.mkdir(parents=True, exist_ok=True)
sources = [ROOT/'data/results/model3_ch2_bridge_summary_20260927/summary.json',
           ROOT/'data/results/model3_mutation_memory_20261004.json',
           ROOT/'data/results/model3_mutation_variability_20261005.json']
bridge = json.loads(sources[0].read_text())['campaigns']['main']['pairs']
mutation = json.loads(sources[1].read_text())['abm']
variability=json.loads(sources[2].read_text())
assert variability['source_summary_sha256']==hashlib.sha256(sources[1].read_bytes()).hexdigest()
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':10,
                     'pdf.fonttype':42, 'svg.fonttype':'none',
                     'axes.spines.top':False, 'axes.spines.right':False})
fig, ax = plt.subplots(1, 3, figsize=(15.5, 6), gridspec_kw={'width_ratios':[1.35,1,1]})
rows=[]
conditions=['natural','richness_matched','visitor_pool','large_plants']
labels=['Natural histories\n48 plants','Visitor counts\nmatched','8 histories\npooled','Natural histories\n192 plants']
for j,(model,color,label) in enumerate([('individual','#008C95','Finite ABM'),('density','#8046A0','Deterministic density')]):
    for i,key in enumerate(conditions):
        v=bridge[key][model]; x=i+(j-.5)*.16; lo,hi=v['mean_ci']; mean=v['mean']
        ax[0].errorbar(x,mean,yerr=[[mean-lo],[hi-mean]],fmt='o',color=color,capsize=3,
                       label=label if i==0 else None)
        rows.append(dict(panel='A',condition=key,model=model,capacity='',mutation='',past='',
                         value=mean,lower=lo,upper=hi,measure='far_minus_near_investment_change'))
ax[0].axhline(0,color='#777777',lw=.8)
ax[0].set(xticks=range(4),xticklabels=labels,ylabel='Isolation effect on investment change\n(more isolated − less isolated)')
ax[0].set_title('A  Finite realization depends on ecology',loc='left',fontweight='bold',pad=15)
ax[0].legend(frameon=False,loc='lower left')
groups=[(48,0),(48,.01),(192,0),(192,.01)]
for j,(past,color,label) in enumerate([('present','#0072B2','Visitors present during initial history'),('absent','#D55E00','Visitors absent during initial history')]):
    for i,(capacity,rate) in enumerate(groups):
        records=[v for v in mutation if v['capacity']==capacity and v['mutation_rate']==rate and v['common_environment_periods']==800]
        assert len(records)==1
        v=records[0]; x=i+(j-.5)*.14
        for panel,field,measure in [(1,'mean_allele_counts','mean_allele_count'),(2,'last100_mean_change','last100_investment_change')]:
            value=v[field][j]
            detail=next(r for r in variability['rows'] if r['capacity']==capacity and r['mutation_rate']==rate
                        and r['past']==past and r['measure']==('allele_count' if panel==1 else 'last100_change'))
            assert abs(detail['mean']-value)<1e-13
            lo,hi=detail['descriptive_bootstrap_95']
            ax[panel].scatter(x+np.linspace(-.025,.025,8),detail['repeats'],s=14,
                              color=color,alpha=.4,zorder=2)
            ax[panel].errorbar(x,value,yerr=[[max(0,value-lo)],[max(0,hi-value)]],fmt='o',
                               color=color,capsize=3,label=label if i==0 else None,zorder=3)
            rows.append(dict(panel=chr(65+panel),condition='one_locus_history_diagnostic',model='individual',capacity=capacity,mutation=rate,past=past,value=value,lower=lo,upper=hi,measure=measure))
for panel,title,ylabel in [(1,'B  Mutation retains genetic variation','Mean number of alleles'),(2,'C  Evolution can continue','Mean investment change\nover the final 100 updates')]:
    ax[panel].set(xticks=range(4),xticklabels=['48\n0','48\n0.01','192\n0','192\n0.01'],xlabel='Plant capacity (top) / mutation rate (bottom)',ylabel=ylabel)
    ax[panel].set_title(title,loc='left',fontweight='bold',pad=15)
    if panel==1:ax[panel].set_ylim(bottom=0)
    else:ax[panel].axhline(0,color='#777777',lw=.8)
fig.legend(*ax[1].get_legend_handles_labels(),loc='lower center',bbox_to_anchor=(.66,.15),ncol=1,frameon=False,fontsize=9)
fig.subplots_adjust(left=.07,right=.98,top=.83,bottom=.37,wspace=.43)
fig.text(.07,.965,'Selection, realized change and genetic supply are different parts of the process',fontsize=15,fontweight='bold')
fig.text(.07,.065,'A: 200 updates; selfing capacity fixed at 0.5; no mutation; 128 visitor histories, 8 demographic repeats. Points and 95% history-bootstrap intervals.\nB–C: separate one-locus diagnostic; 200 different-history + 800 common-environment updates. Small dots: all 8 repeats; large points: means; descriptive 95% repeat-bootstrap intervals.\nAll populations occupied. B–C intervals condition on the two fixed visitor histories; a zero-width interval does not imply population-level certainty.',fontsize=8.5)
fig.text(.07,.02,'Density is not the exact ABM expectation; differences do not isolate drift. B–C do not validate the full three-trait mutation/PDE comparison.',fontsize=9,color='#555555')
for ext in ['pdf','svg','png']:
    fig.savefig(OUT/f'genetic_realization.{ext}',dpi=200)
with (OUT/'plotted_values.csv').open('w',newline='',encoding='utf-8') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
(OUT/'provenance.json').write_text(json.dumps({'sources':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'rows':len(rows),'scope':'existing result visualization; no re-estimation or new simulation'},indent=2))
print(OUT)
