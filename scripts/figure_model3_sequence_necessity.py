"""Assemble verified, distinct cohorts without treating timing as mediation."""
from pathlib import Path
import hashlib
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import ScalarFormatter

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    order_path = ROOT/'data/results/model3_persistent_isolation_summary_20261005.json'
    order_receipt = ROOT/'outputs/figures/model3_temporal_order_20261005/provenance.json'
    assert digest(order_path) == json.loads(order_receipt.read_text())['source_sha256']
    order = json.loads(order_path.read_text())
    folder = ROOT/'outputs/figures/model3_capacity_intervention_20261005'
    provenance = json.loads((folder/'provenance.json').read_text())
    series_path = folder/'plotted_series.npz'
    assert digest(series_path) == provenance['series_sha256']
    summary_path = ROOT/'data/results/model3_assurance_intervention_summary_20261005.json'
    assert digest(summary_path) == provenance['source_summary_sha256']
    series = np.load(series_path)
    out = ROOT/'outputs/figures/model3_sequence_necessity_20261005'
    out.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':10,
                         'pdf.fonttype':42, 'svg.fonttype':'none'})
    fig = plt.figure(figsize=(12, 14))
    gs = fig.add_gridspec(3, 2, left=.095, right=.97, bottom=.16, top=.89,
                          hspace=.78, wspace=.30, height_ratios=[1.25, 1, 1])
    settings = ['assurance_cost', 'prior_selfing']
    labels = ['Delayed selfing; capacity cost 0.5', 'Prior selfing; capacity cost 0']
    colors = {'near':'#D55E00', 'far':'#0072B2'}
    event_colors = {'assurance_first':'#0072B2', 'near_simultaneous':'#888888',
                    'investment_first':'#D55E00'}
    event_records = []
    for col, setting in enumerate(settings):
        row = next(r for r in order['temporal_order'] if r['setting']==setting
                   and r['mutation_rate']==.01 and r['threshold']==.05
                   and r['contrast']=='far_change_from_founders')
        ax = fig.add_subplot(gs[0,col])
        for e in row['events']:
            assert e['assurance_time'] is not None and e['investment_time'] is not None
            ax.scatter(e['assurance_time'],e['investment_time'],s=35,
                       c=event_colors[e['order']],alpha=.75,edgecolor='white',lw=.4)
            event_records.append(dict(setting=setting, **e))
        ax.plot([1,1000],[1,1000],ls='--',color='#555555',lw=1)
        ax.set(xscale='log',yscale='log',xlim=(1,1000),ylim=(1,1000),
               xlabel='Capacity increase: crossing update',
               ylabel='Investment decrease: crossing update',title=labels[col])
        for axis in [ax.xaxis,ax.yaxis]:
            axis.set_major_formatter(ScalarFormatter())
        ax.set_xticks([1,10,100,1000]);ax.set_yticks([1,10,100,1000])
        ax.text(.04,.95,'Above diagonal: capacity crosses earlier',
                transform=ax.transAxes,va='top',fontsize=9)
        ax.text(.53,.05,f"Capacity first: {row['counts'].get('assurance_first',0)}/64\n"
                f"Within 5 updates: {row['counts'].get('near_simultaneous',0)}/64",
                transform=ax.transAxes,fontsize=9)
        ax.spines[['top','right']].set_visible(False)
    plotted = {}
    for row,setting in enumerate(settings):
        for col,mode in enumerate(['fixed','evolving']):
            ax = fig.add_subplot(gs[row+1,col])
            for arm in ['near','far']:
                key=f'{setting}_{mode}_{arm}'
                values=series[key][:,:,1]
                assert values.shape==(64,1001)
                plotted[key]=values.copy()
                for history in values:
                    ax.plot(np.arange(1001),history,color=colors[arm],alpha=.065,lw=.6)
                ax.plot(np.arange(1001),np.nanmean(values,axis=0),color=colors[arm],
                        ls='--' if arm=='near' else '-',lw=2.5)
            ax.set(xlim=(0,1000),ylim=(0,1),xlabel='Reproductive update',
                   ylabel='Attraction investment')
            ax.set_xticks([0,200,400,600,800,1000]);ax.set_yticks([0,.25,.5,.75,1])
            ax.set_title(('Capacity fixed at 0.5' if mode=='fixed' else 'Capacity can evolve')
                         +'\n'+labels[row],fontsize=10)
            ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.12)
    fig.text(.095,.975,'Sequence and necessity are different questions',fontsize=19,weight='bold')
    fig.text(.095,.938,'A  Which trait reaches a declared change first?',fontsize=14,weight='bold')
    fig.text(.095,.919,'Main cohort: both traits vary among founders. Lower replenishment; mutation probability 0.01.',fontsize=10)
    fig.text(.095,.65,'B  Must selfing capacity evolve for investment to decline?',fontsize=14,weight='bold')
    fig.text(.095,.631,'Separate intervention: all founders have capacity 0.5; block or permit its evolution.',fontsize=10)
    handles=[Line2D([0],[0],color=colors[a],ls='--' if a=='near' else '-',lw=2.5,
                    label=l) for a,l in [('near','Higher replenishment (0.24/update)'),
                                        ('far','Lower replenishment (0.01195/update)')]]
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.54,.087),ncol=2,frameon=False,fontsize=10)
    fig.text(.095,.022,
             'A: Each point = one visitor-history mean of 8 repeats. Change 0.05 held for 20 updates; ties within 5.\n'
             'B: Thin lines = 64 history means over surviving repeats; thick lines = mean across histories. No smoothing.\n'
             'Capacity 48; both settings shown. One intervention population becomes extinct; missing traits are not zero.\n'
             'Fixed capacity does not fix realized selfing. Different cohorts cannot quantify mediation. Updates are not years.',fontsize=9)
    for ext in ['pdf','svg','png']:
        fig.savefig(out/f'sequence_necessity.{ext}',dpi=180)
    np.savez_compressed(out/'plotted_investment.npz',**plotted)
    (out/'plotted_events.json').write_text(json.dumps(event_records,indent=2)+'\n')
    receipt=dict(status='rendered_pending_visual_review',order_sha256=digest(order_path),
                 intervention_series_sha256=digest(series_path),event_points=len(event_records),
                 investment_coordinates=sum(v.size for v in plotted.values()),
                 plotted_series_sha256=digest(out/'plotted_investment.npz'),
                 scope='No new estimates. Two distinct verified cohorts assembled; timing is not causal necessity.')
    (out/'provenance.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt))


if __name__=='__main__':
    main()
