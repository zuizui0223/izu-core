"""Source-backed scientific figure exports; no optimum or PDE labels."""
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

COLORS={'individual':'#007C91','density':'#D55E00'}


def plot_records(records,summary,output):
    output=Path(output); output.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
                         'axes.spines.right':False,'pdf.fonttype':42,'svg.fonttype':'none'})
    groups=defaultdict(list)
    for r in records:
        if 'population' in r['result']: groups[(r['cohort'],r['cell_id'])].append(r)
    cells={(c['cohort'],c['cell_id']):c for c in summary['cells']}
    written=[]
    for key,rows in groups.items():
        fig,axes=plt.subplots(1,3,figsize=(12,3.7),layout='constrained')
        years=np.arange(len(rows[0]['result']['population']))
        for r in rows:
            axes[0].plot(years,r['result']['trait_mean'][:,1],color=COLORS['individual'],alpha=.15,lw=.65)
        matrix=np.stack([r['result']['trait_mean'][:,1] for r in rows])
        count=np.isfinite(matrix).sum(axis=0)
        mean=np.divide(np.nansum(matrix,axis=0),count,out=np.full(len(years),np.nan),where=count>0)
        axes[0].plot(years,mean,color=COLORS['individual'],lw=2,label='Individual: survivor mean')
        density=np.stack([r['result']['density_traits'][:,1] for r in rows])
        dcount=np.isfinite(density).sum(axis=0)
        dmean=np.divide(np.nansum(density,axis=0),dcount,out=np.full(len(years),np.nan),where=dcount>0)
        axes[0].plot(years,dmean,color=COLORS['density'],ls='--',lw=2,label='Conditional density')
        axes[0].set(xlabel='Reproductive year',ylabel='Floral investment (0–1)',ylim=(0,1))
        axes[0].legend(fontsize=8,frameon=False)
        occupancy=np.stack([r['result']['population']>0 for r in rows]).mean(axis=0)
        axes[1].plot(years,occupancy,color=COLORS['individual'],lw=2)
        axes[1].set(xlabel='Reproductive year',ylabel='Occupied replicates / all replicates',ylim=(-.02,1.02))
        c=cells[key]; bound=c['occupancy_ci']
        axes[1].errorbar(years[-1],occupancy[-1],yerr=[[occupancy[-1]-bound[0]],[bound[1]-occupancy[-1]]],
                         color=COLORS['individual'],capsize=4,fmt='o')
        changes=np.array([r['result']['trait_mean'][-1,1]-r['result']['trait_mean'][0,1] for r in rows])
        dchanges=np.array([r['result']['density_traits'][-1,1]-r['result']['density_traits'][0,1] for r in rows])
        axes[2].scatter(dchanges,changes,s=14,alpha=.65,color=COLORS['individual'],edgecolors='none')
        axes[2].plot([-1,1],[-1,1],ls=':',color='.4',lw=1)
        finite=np.r_[changes[np.isfinite(changes)],dchanges[np.isfinite(dchanges)]]
        lim=max(.05,float(np.max(np.abs(finite)))+ .02) if len(finite) else .05
        axes[2].set(xlim=(-lim,lim),ylim=(-lim,lim),xlabel='Density: change in investment',ylabel='Individual: change in investment')
        axes[2].set_aspect('equal',adjustable='box'); axes[2].axhline(0,color='.85',lw=.6); axes[2].axvline(0,color='.85',lw=.6)
        fig.suptitle(f"{key[1]} | {key[0]} | {c['n_histories']} independent histories, {c['n_survivors']}/{c['n_total']} occupied at endpoint",fontsize=11)
        fig.supxlabel('Thin lines: individual replicates. Endpoint occupancy bar: 95% history-level Hoeffding bound. Extinct traits omitted, not zero.',fontsize=8)
        stem=output/f'{key[0]}-{key[1]}'
        for extension in ('svg','pdf','png'):
            path=stem.with_suffix('.'+extension); fig.savefig(path,dpi=180); written.append(str(path))
        plt.close(fig)
    return written
