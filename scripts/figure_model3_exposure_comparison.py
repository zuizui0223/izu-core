"""Publication exports of verified paired endpoints; no synthetic trajectories."""
from pathlib import Path
import hashlib
import json
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def main():
    root=Path(__file__).resolve().parents[1]
    source=root/'data/results/model3_exposure_experiment_comparison_20261005.json'
    result=json.loads(source.read_text(encoding='utf-8'))
    assert result['status']=='verified_paired_experiment_comparison' and len(result['results'])==12
    out=root/'outputs/figures/model3_exposure_comparison_20261005'
    out.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'pdf.fonttype':42,'svg.fonttype':'none'})
    fig,axes=plt.subplots(3,4,figsize=(15,9),sharex=True,sharey='row')
    columns=[('assurance_cost',0.),('assurance_cost',.01),('prior_selfing',0.),('prior_selfing',.01)]
    traits=[('investment','Floral investment'),('capacity','Selfing capacity'),('matching','Matching position')]
    series=[('sustained_far_minus_near','#1E6091','o',-9),('equalized_far_minus_near','#CB6B28','s',9)]
    exported=[]
    for col,(setting,rate) in enumerate(columns):
        rows=sorted([r for r in result['results'] if r['setting']==setting and r['mutation_rate']==rate],key=lambda r:r['period'])
        assert [r['period'] for r in rows]==[200,400,1000]
        axes[0,col].set_title(('Delayed selfing; cost 0.5' if setting=='assurance_cost' else 'Prior selfing; cost 0')+f'\nMutation probability {rate:g}',fontsize=11,pad=12)
        for ri,(trait,label) in enumerate(traits):
            ax=axes[ri,col];ax.axhline(0,color='#767676',lw=.8,ls=':')
            for comparison,color,marker,offset in series:
                means=np.array([r['comparisons'][comparison][trait]['mean'] for r in rows])
                ci=np.array([r['comparisons'][comparison][trait]['interval'] for r in rows])
                assert np.all(ci[:,0]<=means) and np.all(means<=ci[:,1])
                ax.errorbar(np.array([200,400,1000])+offset,means,yerr=np.vstack([means-ci[:,0],ci[:,1]-means]),
                    fmt=marker,color=color,mfc='white' if marker=='s' else color,ms=5,capsize=3,lw=1.2)
                for row,mean,bounds in zip(rows,means,ci):
                    exported.append([setting,rate,trait,comparison,row['period'],float(mean),*bounds,row['eligible_triplets']])
            ax.spines[['top','right']].set_visible(False)
            ax.set_xticks([200,400,1000]);ax.set_xlim(125,1075)
            if col==0:ax.set_ylabel(label+'\nMore − less isolated')
            if ri==2:ax.set_xlabel('Reproductive update')
    handles=[Line2D([],[],marker='o',color='#1E6091',linestyle='none',label='Isolation maintained'),
             Line2D([],[],marker='s',color='#CB6B28',mfc='white',linestyle='none',label='Same visitor environment after update 200')]
    fig.suptitle('Does continued isolation maintain stronger floral divergence?',fontsize=18,y=.985)
    fig.legend(handles=handles,loc='upper center',bbox_to_anchor=(.5,.947),ncol=2,frameon=False)
    fig.text(.5,.018,'Points: means across 64 visitor histories; bars: descriptive 95% history-bootstrap intervals.\n'
             '8 demographic repeats per history; shared surviving triplets. Marker offsets avoid overlap. Three measured endpoints, not smoothed trajectories.\n'
             'Settings jointly vary selfing timing and cost. Updates are not calibrated years; persistence of a difference does not establish irreversibility.',
             ha='center',va='bottom',fontsize=9)
    fig.subplots_adjust(top=.84,bottom=.16,left=.085,right=.99,hspace=.25,wspace=.12)
    for ext in ['png','svg','pdf']:fig.savefig(out/f'exposure_comparison.{ext}',dpi=180)
    plt.close(fig)
    with (out/'plotted_values.csv').open('w',newline='',encoding='utf-8') as handle:
        writer=csv.writer(handle);writer.writerow(['setting','mutation','trait','comparison','period','mean','lower','upper','eligible_triplets']);writer.writerows(exported)
    assert len(exported)==72
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    (out/'provenance.json').write_text(json.dumps(dict(source=str(source),source_sha256=sha(source),
        plotted_estimates=72,files={p.name:sha(p) for p in out.iterdir() if p.name!='provenance.json'}),indent=2)+'\n',encoding='utf-8')
    print(str(out/'exposure_comparison.png'))


if __name__=='__main__':main()
