"""Verified full-resolution history means, not interpolated endpoint sketches."""
from pathlib import Path
import hashlib,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def main():
    root=Path(__file__).resolve().parents[1]
    raw=root/'outputs/model3_assurance_intervention_20261005'
    out=root/'outputs/figures/model3_capacity_intervention_20261005'
    out.mkdir(parents=True,exist_ok=True)
    summarypath=root/'data/results/model3_assurance_intervention_summary_20261005.json'
    verify=json.loads((root/'data/results/model3_assurance_intervention_verified_20261005.json').read_text())
    assert hashlib.sha256(summarypath.read_bytes()).hexdigest()==verify['summary_sha256']
    series={};hashes={}
    for setting in ['assurance_cost','prior_selfing']:
        for mode in ['fixed','evolving']:
            for arm in ['near','far']:
                histories=[]
                for seed in range(76001,76065):
                    traces=[]
                    for rep in range(7101,7109):
                        p=raw/f'{setting}_u0.01_h{seed}_r{rep}_{arm}_{mode}.npz'
                        digest=hashlib.sha256(p.read_bytes()).hexdigest()
                        assert digest==json.loads(p.with_suffix('.json').read_text())['sha256']
                        hashes[p.name]=digest
                        with np.load(p) as z:
                            trace=z['trace'].copy()
                        assert trace.shape==(1001,10)
                        traces.append(np.where(trace[:,0,None]>0,trace[:,1:4],np.nan))
                    histories.append(np.nanmean(traces,axis=0))
                series[f'{setting}_{mode}_{arm}']=np.array(histories)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'pdf.fonttype':42,'svg.fonttype':'none'})
    fig,axes=plt.subplots(2,3,figsize=(14.5,8.5),sharex=True,sharey=True)
    colors={'near':'#D55E00','far':'#0072B2'};styles={'near':'--','far':'-'}
    for row,setting in enumerate(['assurance_cost','prior_selfing']):
        for col,(mode,index) in enumerate([('fixed',1),('evolving',1),('evolving',2)]):
            ax=axes[row,col]
            for arm in ['near','far']:
                values=series[f'{setting}_{mode}_{arm}'][:,:,index]
                for history in values:ax.plot(np.arange(1001),history,color=colors[arm],alpha=.065,lw=.6)
                ax.plot(np.arange(1001),np.nanmean(values,axis=0),color=colors[arm],ls=styles[arm],lw=2.5)
            ax.set_xlim(0,1000);ax.set_ylim(0,1)
            ax.set_xticks([0,200,400,600,800,1000]);ax.set_yticks([0,.25,.5,.75,1])
            ax.spines[['top','right']].set_visible(False)
            ax.grid(axis='y',alpha=.12)
            if row==1:ax.set_xlabel('Reproductive update')
            ax.set_ylabel('Selfing capacity' if col==2 else 'Attraction investment')
            ax.set_title(['Capacity held at 0.5','Capacity allowed to evolve','Resulting capacity evolution'][col],fontsize=12,pad=12)
        axes[row,0].text(0,1.21,['Delayed selfing | capacity cost = 0.5','Prior selfing | capacity cost = 0'][row],
            transform=axes[row,0].transAxes,fontweight='bold',fontsize=12)
    fig.suptitle('Attraction investment declines even when selfing capacity cannot evolve',fontsize=17,y=.99)
    handles=[Line2D([0],[0],color=colors[a],ls=styles[a],lw=2.5,label=label) for a,label in [('near','Less isolated'),('far','More isolated')]]
    fig.legend(handles=handles,loc='upper center',bbox_to_anchor=(.5,.953),ncol=2,frameon=False)
    fig.subplots_adjust(left=.075,right=.98,bottom=.22,top=.82,hspace=.58,wspace=.27)
    fig.text(.075,.055,'Thin lines: 64 visitor-history means, each over up to 8 surviving populations. Thick lines: mean across histories.\n'
        'Same 48 founders; mutation probability 0.01; isolation maintained for 1,000 updates (not calibrated years). No smoothing.\n'
        'Fixed capacity does not fix the realized selfing fraction. One delayed/evolving/less-isolated population becomes extinct.',fontsize=10)
    for ext in ['png','pdf','svg']:fig.savefig(out/f'capacity_intervention.{ext}',dpi=180)
    np.savez_compressed(out/'plotted_series.npz',**series)
    provenance=dict(source_summary_sha256=verify['summary_sha256'],raw_cases=len(hashes),raw_hashes=hashes,
        series_sha256=hashlib.sha256((out/'plotted_series.npz').read_bytes()).hexdigest(),
        meaning='64 history means per series, each over living demographic repeats; thick curve is equal-weight history mean. Positive mutation only; zero-mutation negative controls retained in full summary.')
    (out/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'raw_cases':len(hashes),'output':str(out/'capacity_intervention.pdf')}))


if __name__=='__main__':main()
