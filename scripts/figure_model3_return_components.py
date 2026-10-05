"""Paired visitor-history contribution slopes from verified fixed-plant assays."""
from pathlib import Path
import json,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    root=Path(__file__).resolve().parents[1]
    path=root/'data/results/model3_return_components_20261005.json'
    summary=json.loads(path.read_text(encoding='utf-8'))
    source=root/'outputs/model3_fixedplant_returns_20261005/individual_arrays.npz'
    assert hashlib.sha256(source.read_bytes()).hexdigest()==summary['source_arrays_sha256']
    out=root/'outputs/figures/model3_return_components_20261005';out.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'pdf.fonttype':42,'svg.fonttype':'none'})
    fig,axes=plt.subplots(2,3,figsize=(12,8),sharey=True)
    with np.load(source) as arrays:
        for i,setting in enumerate(['assurance_cost','prior_selfing']):
            vals=[]
            for arm in ['near','far']:
                a=np.array([arrays[f'{setting}_h{h}_{arm}_t400'][:2].mean(axis=1) for h in range(76001,76065)])
                vals.append(np.column_stack([a[:,1],a[:,0]-a[:,1],a[:,0]]))
            for j,(label,component) in enumerate(zip(['Outcross contribution','Viable selfed contribution','Total contribution'],['outcross_contribution','viable_selfed_contribution','total_contribution'])):
                ax=axes[i,j]
                for h in range(64):ax.plot([0,1],[vals[0][h,j],vals[1][h,j]],color='#008c95',alpha=.18,lw=.65)
                means=[v[:,j].mean() for v in vals]
                row=next(r for r in summary['rows'] if r['setting']==setting and r['period']==400 and r['component']==component)
                assert np.allclose(means,[row['near'],row['far']],rtol=0,atol=1e-12)
                ax.plot([0,1],means,'o-',color='#172f3e',lw=3,ms=6)
                ax.axhline(0,color='#888888',ls='--',lw=.8)
                ax.set_xticks([0,1],['High supply\n0.24 / update','Low supply\n0.01195 / update']);ax.set_xlim(-.25,1.25)
                ax.set_title(label)
                ax.text(.04,.96,f"Mean: {means[0]:+.3f} → {means[1]:+.3f}",transform=ax.transAxes,va='top',fontsize=10)
                ax.spines[['top','right']].set_visible(False)
            axes[i,0].set_ylabel(('Delayed selfing + capacity cost' if i==0 else 'Prior selfing + no capacity cost')+'\nContribution slope per investment unit')
    fig.suptitle('Visitor limitation changes the reproductive return to attraction',fontsize=16,y=.98)
    fig.text(.08,.035,'Thin lines: 64 paired visitor-history means (48 fixed plants each). Thick line: mean across histories.\nVisitor snapshot 400; capacity fixed at 0.5. Components include allocation costs. These are local slopes, not evolutionary trajectories.',fontsize=10)
    fig.tight_layout(rect=[0,.10,1,.94])
    for ext in ['pdf','svg','png']:fig.savefig(out/f'return_components.{ext}',dpi=180)
    (out/'verification.json').write_text(json.dumps({'means_checked':12,'source_sha256':summary['source_arrays_sha256'],'snapshot':400,'histories':64,'plants_per_history':48},indent=2),encoding='utf-8')


if __name__=='__main__':main()
