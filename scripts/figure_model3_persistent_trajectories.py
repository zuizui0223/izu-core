"""Actual sustained-isolation time series, with between-history variation."""
from pathlib import Path
import hashlib
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def main():
    root=Path(__file__).resolve().parents[1]
    source=root/'outputs/model3_persistent_isolation_20261005/temporal_order_curves.npz'
    summary=root/'data/results/model3_persistent_isolation_summary_20261005.json'
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    record=json.loads(summary.read_text(encoding='utf-8'))
    assert record['status']=='completed_summary' and record['curve_sha256']==sha(source)
    out=root/'outputs/figures/model3_persistent_trajectories_20261005';out.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'pdf.fonttype':42,'svg.fonttype':'none'})
    fig,axes=plt.subplots(3,4,figsize=(15,9),sharex=True,sharey='row')
    columns=[('assurance_cost',0.),('assurance_cost',.01),('prior_selfing',0.),('prior_selfing',.01)]
    plotted={};x=np.arange(1001)
    with np.load(source) as z:
        for col,(setting,rate) in enumerate(columns):
            axes[0,col].set_title(('Delayed selfing; cost 0.5' if setting=='assurance_cost' else 'Prior selfing; cost 0')+f'\nMutation probability {rate:g}',fontsize=11,pad=12)
            for ri,(trait,label) in enumerate([(1,'Floral investment'),(2,'Selfing capacity'),(0,'Matching position')]):
                ax=axes[ri,col];ax.axhline(0,color='#888888',lw=.7,ls=':')
                for arm,color,style in [('near','#CB6B28','--'),('far','#1E6091','-')]:
                    key=f'{setting}_u{rate}_{arm}_change_from_founders'
                    values=z[key][:,:,trait]
                    assert values.shape==(64,1001) and np.all(values[:,0]==0) and np.isfinite(values).all()
                    mean=values.mean(axis=0);lower,upper=np.quantile(values,[.1,.9],axis=0)
                    ax.fill_between(x,lower,upper,color=color,alpha=.13,linewidth=0)
                    ax.plot(x,mean,color=color,ls=style,lw=1.8)
                    plotted[key+f'_trait{trait}']=np.vstack([mean,lower,upper])
                ax.spines[['top','right']].set_visible(False);ax.set_xlim(0,1000);ax.set_xticks([0,500,1000])
                if col==0:ax.set_ylabel(label+'\nChange from founders')
                if ri==2:ax.set_xlabel('Reproductive update')
    fig.suptitle('Floral evolution while isolation persists',fontsize=19,y=.985)
    fig.legend(handles=[Line2D([],[],color='#CB6B28',ls='--',label='Less isolated'),Line2D([],[],color='#1E6091',label='More isolated')],
               loc='upper center',bbox_to_anchor=(.5,.948),ncol=2,frameon=False)
    fig.text(.5,.025,'Lines: mean of 64 visitor-history means; shading: 10th–90th percentiles across histories, NOT confidence intervals.\n'
        'Each history averages 8 demographic repeats among surviving populations. All 1,001 saved states are shown; no smoothing.\n'
        'Isolation remains different for all 1,000 updates. Selfing timing and cost vary jointly; updates are not calibrated years.',ha='center',fontsize=9)
    fig.subplots_adjust(top=.84,bottom=.16,left=.085,right=.99,hspace=.22,wspace=.12)
    for ext in ['png','svg','pdf']:fig.savefig(out/f'persistent_trajectories.{ext}',dpi=180)
    plt.close(fig)
    np.savez_compressed(out/'plotted_series.npz',**plotted)
    (out/'provenance.json').write_text(json.dumps(dict(source_sha256=sha(source),summary_sha256=sha(summary),
        series=len(plotted),points_per_series=1001,bands='between-history 10th–90th percentiles, not confidence intervals',
        files={p.name:sha(p) for p in out.iterdir() if p.name!='provenance.json'}),indent=2)+'\n',encoding='utf-8')
    print(str(out/'persistent_trajectories.png'))


if __name__=='__main__':main()
