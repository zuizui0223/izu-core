"""Source-checked history trajectories; no smoothing or synthetic curves."""
import argparse
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scripts.summarize_model3_full_mutation import read_case


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    a=p.parse_args();source=Path(a.source);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    summary=json.loads((source/'summary_core_64_8.json').read_text())
    assert summary['n_cases']==4096
    histories={}
    for setting in ['assurance_cost','prior_selfing']:
        for rate in [0.,.01]:
            values=[]
            for h in range(76001,76065):
                differences=[]
                for r in range(7101,7109):
                    near,far=[read_case(source,f'core_{setting}_u{rate}_h{h}_r{r}_{arm}') for arm in ['near','far']]
                    occupied=(near[:,0]>0)&(far[:,0]>0)
                    differences.append(np.where(occupied[:,None],far[:,1:4]-near[:,1:4],np.nan))
                values.append(np.nanmean(differences,axis=0))
            histories[f'{setting}_{rate}']=np.array(values)
    np.savez_compressed(out/'history_mean_trajectories.npz',**histories)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'pdf.fonttype':42,'svg.fonttype':'none'})
    fig,axes=plt.subplots(2,2,figsize=(12,8),sharex=True,sharey='col')
    colors={0.:'#B65A22',.01:'#1673A4'}
    for row,setting in enumerate(['assurance_cost','prior_selfing']):
        for column,(trait,ix) in enumerate([('Floral investment',1),('Reproductive assurance',2)]):
            ax=axes[row,column]
            ax.axvspan(0,200,color='#EFEFEF',zorder=0)
            ax.axvline(200,color='#777777',lw=.9)
            ax.axhline(0,color='#555555',lw=.8)
            for rate in [0.,.01]:
                v=histories[f'{setting}_{rate}'][:,:,ix]
                # Every time point is drawn; thin lines are history means.
                ax.plot(np.arange(1001),v.T,color=colors[rate],lw=.35,alpha=.09)
                mean=np.nanmean(v,axis=0)
                ax.plot(mean,color=colors[rate],lw=2,ls='--' if rate==0 else '-')
                for t in [200,1000]:
                    record=next(r for r in summary['rows'] if r['setting']==setting and r['mutation_rate']==rate and r['period']==t)
                    item=record['traits'][['access','investment','assurance'][ix]]
                    assert np.isclose(mean[t],item['mean_gap'],atol=1e-12)
                    low,high=item['interval']
                    ax.errorbar(t,mean[t],yerr=[[mean[t]-low],[high-mean[t]]],color=colors[rate],fmt='o',ms=3,capsize=3,lw=1.2)
            ax.spines[['top','right']].set_visible(False)
            ax.set_xlim(0,1030);ax.set_xticks([0,200,400,600,800,1000])
            ax.set_title(('Delayed selfing; assurance cost 0.5' if row==0 else 'Prior selfing; assurance cost 0')+'\n'+trait,loc='left',fontsize=12)
            ax.set_ylabel('Far-history minus near-history')
            if row==1:ax.set_xlabel('Reproductive period (not calibrated years)')
    fig.suptitle('Floral differences after visitor environments become identical',fontsize=17,x=.08,ha='left')
    legend=[Line2D([0],[0],color=colors[r],lw=2,ls='--' if r==0 else '-',label='No mutation' if r==0 else 'Mutation probability 0.01') for r in [0.,.01]]
    fig.legend(handles=legend,loc='upper right',bbox_to_anchor=(.96,.935),frameon=False,ncol=2)
    fig.text(.08,.915,'Shaded: different immigration distances | After period 200: identical visitor histories',fontsize=10)
    fig.text(.08,.035,'Thin lines: 64 history means (8 paired repeats each). Thick lines: mean across histories; no smoothing.\nBars: descriptive 95% history-bootstrap intervals at periods 200 and 1,000. Traits condition on paired survival.\nCapacity 48; all three traits evolve. The two rows differ in both selfing timing and assurance cost.',fontsize=9)
    fig.subplots_adjust(left=.09,right=.97,bottom=.16,top=.82,wspace=.23,hspace=.34)
    for ext in ['png','pdf','svg']:fig.savefig(out/f'history_memory.{ext}',dpi=180)
    plt.close(fig)
    print('Verified plotted endpoint means against the final summary; saved PNG, PDF, SVG and history arrays.')


if __name__=='__main__':main()
