"""Render audited, complete campaign summaries without re-estimation or selection."""
from pathlib import Path
import json
from hashlib import sha256
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/results/model3_island_v2_summary'
s=json.loads((OUT/'summary.json').read_text())
audit=json.loads((ROOT/'data/results/model3_island_v2_audit.json').read_text())
assert audit['status']=='passed' and audit['cases_checked']==19968 and audit['replayed']==80
c={r['cell_id']:r for r in s['cells'] if r['cohort']=='production'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'svg.fonttype':'none'})
fig,axs=plt.subplots(4,2,figsize=(13,18));fig.subplots_adjust(left=.20,right=.97,top=.95,bottom=.07,hspace=.65,wspace=.75)
teal='#007C91';orange='#D55E00'
def forest(ax,ids,labels,title):
 for i,k in enumerate(ids):
  r=c[k];m=r.get('mean_investment_change');ci=r.get('investment_change_ci')
  if m is not None:
   ax.errorbar(m,i,xerr=[[m-ci[0]],[ci[1]-m]],fmt='o',color=teal,capsize=3)
   if r.get('mean_density_change') is not None:ax.plot(r['mean_density_change'],i,'s',mfc='none',mec=orange)
  else:ax.text(.02,i,'Extinct: 0/256',transform=ax.get_yaxis_transform(),va='center')
 ax.axvline(0,color='.6',lw=.8);ax.set_yticks(range(len(ids)),labels);ax.invert_yaxis();ax.set_title(title,loc='left',fontweight='bold',fontsize=11);ax.set_xlabel('Change in floral investment (0–1 scale)')
forest(axs[0,0],['order_uninterrupted','order_early_gap','order_late_gap','order_early_mismatch','order_late_mismatch'],['Uninterrupted','Early absence','Late absence','Early mismatch','Late mismatch'],'A  Timing leaves different outcomes')
forest(axs[0,1],['assurance_fixed_disabled','assurance_fixed_half','assurance_fixed_high','assurance_evolving_delayed','assurance_evolving_prior','assurance_evolving_discount','assurance_evolving_cost'],['Fixed 0','Fixed 0.5','Fixed 0.9','Evolving: delayed','Evolving: prior','Pollen discount','Assurance cost'],'B  Assurance during early absence')
ax=axs[1,0]
m=np.array([[c[f'connectivity_p{p}_v{v}']['mean_investment_change'] for v in [0,1,3]] for p in [0,1,3]])
im=ax.imshow(m,cmap='RdBu_r',vmin=-.15,vmax=.15)
for i in range(3):
 for j in range(3):ax.text(j,i,f'{m[i,j]:+.3f}',ha='center',va='center')
ax.set_xticks(range(3),[0,1,3]);ax.set_yticks(range(3),[0,1,3]);ax.set_xlabel('Visitor distance / dispersal scale');ax.set_ylabel('Seed distance / dispersal scale');ax.set_title('C  Separate seed and visitor connectivity',loc='left',fontweight='bold',fontsize=11);fig.colorbar(im,ax=ax,shrink=.7,label='Investment change')
ax=axs[1,1]
ids=['recovery_visitor_only','recovery_source_immigrants','recovery_resident_immigrants','recovery_mutation_low','recovery_mutation_high','recovery_long_mu0p0','recovery_long_mu0p0001']
for i,k in enumerate(ids):
 p=next(p for p in s['paired_contrasts'] if {p['a'],p['b']}=={k,k+'_uninterrupted'})
 sign=1 if p['b']==k else -1;v=sign*p['conditional_mean_b_minus_a'];ci=sorted(sign*x for x in p['conditional_ci'])
 ax.errorbar(v,i,xerr=[[v-ci[0]],[ci[1]-v]],fmt='o',color=teal,capsize=3)
ax.set_yticks(range(7),['Visitors restored','+ Source seeds','+ Resident-like seeds','Mutation 0.0001','Mutation 0.001','2,000 y: no mutation','2,000 y: mutation']);ax.invert_yaxis();ax.axvline(0,color='.6',lw=.8);ax.set_xlabel('Investment change: gap minus matched control');ax.set_title('D  Restoration retains a history deficit',loc='left',fontweight='bold',fontsize=11)
ax=axs[2,0]
for prefix,style,label in [('scale_fixed_total','o-','Fixed seed supply'),('scale_per_capita','s--','Per-capita seed supply')]:
 vals=[c[f'{prefix}_{n}'] for n in [48,192,768]]
 ax.plot([48,192,768],[r['mean_investment_change'] for r in vals],style,label=label,color=teal if style=='o-' else '#9467bd')
 for n,r in zip([48,192,768],vals):
  m=r['mean_investment_change'];ci=r['investment_change_ci'];ax.errorbar(n,m,yerr=[[m-ci[0]],[ci[1]-m]],color='.5',capsize=3)
 ax.plot([48,192,768],[r['mean_density_change'] for r in vals],':',color=orange)
ax.set_xscale('log',base=4);ax.set_xticks([48,192,768],[48,192,768]);ax.set_xlabel('Population capacity');ax.set_ylabel('Investment change');ax.set_title('E  Larger populations approach density means',loc='left',fontweight='bold',fontsize=11);ax.legend(fontsize=8,frameon=False)
forest(axs[2,1],['life_annual_annual','life_perennial4_annual','life_perennial10_annual','life_perennial4_lifetime','life_perennial10_lifetime'],['Annual','4-year: annual budget','10-year: annual budget','4-year: lifetime budget','10-year: lifetime budget'],'F  Longevity and reproductive budget')
ax=axs[3,0]
for i,r in enumerate(s['crossed']):
 b=0
 for key,color in [('S','#009E73'),('C','#0072B2'),('I','#CC79A7')]:
  v=r['investment'][key];ax.barh(i,v,left=b,color=color,label=key if i==0 else None);b+=v
ax.set_yticks(range(4),[r['cohort']+' / '+r['regime'].replace('transport_','') for r in s['crossed']]);ax.set_xlabel('Empirical cell-mean variance share');ax.set_xlim(0,1);ax.set_title('G  Descriptive S/C/I shares',loc='left',fontweight='bold',fontsize=11);ax.legend(ncol=3,frameon=False,fontsize=9,loc='lower center',bbox_to_anchor=(.5,1.10))
ax=axs[3,1]
for r in s['transport']:
 q=r['investment'];a=r['training_regime'].replace('transport_','');b=r['heldout_regime'].replace('transport_','')
 ax.scatter(q['prediction'],q['observed'],label=a+' → '+b,s=35)
ax.plot([-.2,.2],[-.2,.2],':',color='.5');ax.set(xlabel='Predicted mean change (training)',ylabel='Observed mean change (held out)',xlim=(-.2,.2),ylim=(-.2,.2));ax.set_title('H  Stable ranks do not guarantee transfer',loc='left',fontweight='bold',fontsize=11);ax.legend(fontsize=8,frameon=False)
fig.suptitle('Visitor history, assurance and connectivity shape floral investment',fontsize=17,fontweight='bold')
fig.text(.03,.015,'Model-conditional results; quantitative grid convergence is not established. 128 independent histories × 2 demographic repeats per arm.\nTeal points: individual means, bars: 95% history-cluster intervals. Open orange squares / dotted lines: density means (not PDE).\nTraits conditional on survival and defined initial states; numerical-gate and full denominator tables accompany this figure.',fontsize=10)
for ext in ['png','svg','pdf']:fig.savefig(OUT/f'ecological_comparisons.{ext}',dpi=200)
plt.close(fig)
(OUT/'ecological_comparisons_source.json').write_text(json.dumps({'summary_sha256':sha256((OUT/'summary.json').read_bytes()).hexdigest(),'script':'scripts/plot_model3_island_ecology.py','audit':audit,'scope':'Existing complete summaries; no new estimation'},indent=2))
