"""All declared rate conditions, stages and event categories; no smoothed fits."""
from pathlib import Path
import hashlib
import json
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'outputs/model3_replenishment_evolution_20261005'
OUT=ROOT/'outputs/figures/model3_replenishment_evolution_20261005'


def main():
    p=ROOT/'data/results/model3_replenishment_evolution_summary_20261005.json'
    result=json.loads(p.read_text());assert result['status']=='complete_all_declared_rates'
    check=json.loads((ROOT/'data/results/model3_replenishment_readout_verified_20261005.json').read_text())
    assert check['summary_sha256']==hashlib.sha256(p.read_bytes()).hexdigest()
    OUT.mkdir(parents=True,exist_ok=True);curves=np.load(SOURCE/'evolution_curves.npz')
    settings=['assurance_cost','prior_selfing'];titles=['Delayed selfing + capacity cost','Prior selfing + no capacity cost']
    traits=['matching','investment','capacity'];colors=['#7B62A3','#D55E00','#0072B2'];plotrows=[]
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'pdf.fonttype':42,'svg.fonttype':'none'})
    with PdfPages(OUT/'all_endpoints.pdf') as pdf:
        for contrast in ['from_founders','minus_high_supply']:
            for update in [200,400,1000]:
                fig,axs=plt.subplots(2,3,figsize=(13,8),sharex=True,sharey='col')
                for si,setting in enumerate(settings):
                    rows=sorted([r for r in result['endpoints'] if r['setting']==setting and r['contrast']==contrast and r['update']==update],key=lambda r:r['replenishment'])
                    assert len(rows)==13
                    x=np.array([r['replenishment'] for r in rows])
                    for j,trait in enumerate(traits):
                        ax=axs[si,j]
                        histories=np.array([curves[f"{setting}_d{r['distance']:.2f}_{contrast}"][:,update,j] for r in rows])
                        means=np.array([r['traits'][trait]['mean'] for r in rows],dtype=float)
                        ci=np.array([r['traits'][trait]['pointwise_interval'] for r in rows],dtype=float)
                        ax.plot(x,histories,color=colors[j],alpha=.10,lw=.6)
                        ax.fill_between(x,ci[:,0],ci[:,1],color=colors[j],alpha=.20)
                        ax.plot(x,means,'o-',color=colors[j],lw=2,ms=3)
                        ax.axhline(0,color='#606060',ls='--',lw=.7)
                        ax.set(xlim=(0,.25),xlabel='Established visitor types / update',
                               title=trait.replace('capacity','Selfing capacity').capitalize())
                        if j==0:ax.set_ylabel(titles[si]+'\nTrait change')
                        ax.spines[['top','right']].set_visible(False)
                        for r,mean,interval in zip(rows,means,ci):
                            plotrows.append([setting,contrast,update,r['replenishment'],trait,mean,*interval,r['occupied_cases'],r['paired_cases']])
                fig.suptitle(f'Realized evolution across replenishment: update {update}\n'+('Change from founders' if contrast=='from_founders' else 'Paired difference from the highest-supply condition'),fontsize=15)
                fig.subplots_adjust(top=.86,bottom=.18,hspace=.4,wspace=.25)
                fig.text(.1,.07,'Thin: 64 history means (8 demographic repeats each); bold: mean; band: pointwise 95% history-bootstrap interval.\nLines connect sampled rates; no smooth model fitted. Extinct traits remain undefined. Population survival is reported in the CSV.\nCapacity 48; mutation 0.01; no island-area calibration. Settings differ jointly in selfing timing and cost.',fontsize=9)
                pdf.savefig(fig)
                if update==1000 and contrast=='from_founders':
                    fig.savefig(OUT/'replenishment_endpoints.png',dpi=180);fig.savefig(OUT/'replenishment_endpoints.svg')
                plt.close(fig)
    cats=['assurance_first','near_simultaneous','investment_first','assurance_only','investment_only','neither']
    labels=['Capacity first','Within 5 updates','Investment first','Only capacity reached','Only investment reached','Neither reached']
    palette=['#0072B2','#BBBBBB','#D55E00','#86BCD9','#F0B78B','#F0F0F0']
    with PdfPages(OUT/'all_order_thresholds.pdf') as pdf:
        for threshold in [.025,.05,.1]:
            fig,axs=plt.subplots(2,2,figsize=(12,10),sharex=True)
            for si,setting in enumerate(settings):
                for ci,contrast in enumerate(['from_founders','minus_high_supply']):
                    rows=sorted([r for r in result['temporal_order'] if r['setting']==setting and r['contrast']==contrast and r['threshold']==threshold],key=lambda r:r['replenishment'])
                    assert len(rows)==13;ax=axs[si,ci];left=np.zeros(13)
                    for cat,label,color in zip(cats,labels,palette):
                        values=np.array([r['counts'].get(cat,0) for r in rows]);ax.barh(np.arange(13),values,left=left,color=color,label=label,edgecolor='white',linewidth=.3);left+=values
                    assert np.all(left==64)
                    ax.set(yticks=np.arange(13),yticklabels=[f"{r['replenishment']:.3f}" for r in rows],xlim=(0,64),xticks=[0,16,32,48,64],xlabel='Number of visitor histories (total 64)',ylabel='Established types / update',title=titles[si]+'\n'+('Change from founders' if contrast=='from_founders' else 'Additional change relative to high supply'))
                    ax.spines[['top','right']].set_visible(False)
            fig.suptitle(f'Which declared change is reached first? Threshold {threshold}',fontsize=16)
            handles,legend=axs[0,0].get_legend_handles_labels();fig.legend(handles,legend,loc='lower center',ncol=3,bbox_to_anchor=(.5,.04),frameon=False)
            fig.subplots_adjust(top=.90,bottom=.15,hspace=.35,wspace=.30)
            fig.text(.1,.015,'Threshold held 20 updates; ties within 5. Unreached events censored at 1,000. Counts do not identify infinitesimal onset or mediation.',fontsize=9)
            pdf.savefig(fig)
            if threshold==.05:fig.savefig(OUT/'replenishment_order.png',dpi=170)
            plt.close(fig)
    with (OUT/'plotted_endpoints.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f);writer.writerow(['setting','contrast','update','replenishment','trait','mean','ci_low','ci_high','occupied_of512','paired_of512']);writer.writerows(plotrows)
    (OUT/'provenance.json').write_text(json.dumps({'summary_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'endpoint_estimates':len(plotrows),'no_simulations_run':True},indent=2)+'\n',encoding='utf-8')
    print(OUT)


if __name__=='__main__':main()
