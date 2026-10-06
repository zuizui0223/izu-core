"""Paired threshold times and the full declared threshold sensitivity."""
from pathlib import Path
import json,hashlib,csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter


def main():
    root=Path(__file__).resolve().parents[1]
    source=root/'data/results/model3_persistent_isolation_summary_20261005.json'
    data=json.loads(source.read_text())
    out=root/'outputs/figures/model3_temporal_order_20261005';out.mkdir(parents=True,exist_ok=True)
    rows=[r for r in data['temporal_order'] if r['contrast']=='far_change_from_founders']
    assert len(rows)==12
    with (out/'all_far_threshold_events.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['setting','mutation_rate','threshold','history_seed','investment_time','assurance_time','order'])
        w.writeheader()
        for r in rows:
            for e in r['events']:w.writerow({k:r[k] for k in ['setting','mutation_rate','threshold']}|e)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'pdf.fonttype':42,'svg.fonttype':'none'})
    colors={'assurance_first':'#0072B2','near_simultaneous':'#999999','investment_first':'#D55E00'}
    fig,axes=plt.subplots(2,2,figsize=(11,10),gridspec_kw={'height_ratios':[1.5,1]})
    for col,setting in enumerate(['assurance_cost','prior_selfing']):
        selected=[r for r in rows if r['setting']==setting and r['mutation_rate']==.01]
        primary=next(r for r in selected if r['threshold']==.05)
        ax=axes[0,col]
        for e in primary['events']:
            assert e['assurance_time'] is not None and e['investment_time'] is not None
            ax.scatter(e['assurance_time'],e['investment_time'],s=45,c=colors[e['order']],edgecolors='white',linewidths=.4,alpha=.75)
        ax.plot([1,1000],[1,1000],color='#555555',ls='--',lw=1)
        ax.set_xscale('log');ax.set_yscale('log');ax.set_xlim(1,1000);ax.set_ylim(1,1000)
        ax.set_xticks([1,10,100,1000]);ax.set_yticks([1,10,100,1000])
        ax.xaxis.set_major_formatter(ScalarFormatter());ax.yaxis.set_major_formatter(ScalarFormatter())
        ax.set_xlabel('Selfing-capacity crossing (update)');ax.set_ylabel('Investment-decline crossing (update)')
        ax.text(.04,.93,'Above diagonal: capacity crosses earlier',transform=ax.transAxes,fontsize=9)
        ax.set_title(['Delayed selfing | capacity cost 0.5','Prior selfing | capacity cost 0'][col],fontsize=12)
        ax.spines[['top','right']].set_visible(False)
        bx=axes[1,col]
        for i,threshold in enumerate([.025,.05,.1]):
            row=next(r for r in selected if r['threshold']==threshold);left=0
            assert sum(row['counts'].values())==64
            for order in ['assurance_first','near_simultaneous','investment_first']:
                n=row['counts'].get(order,0)
                if n:
                    bx.barh(i,n,left=left,color=colors[order],height=.6)
                    bx.text(left+n/2,i,str(n),ha='center',va='center',color='white',fontweight='bold')
                left+=n
            assert left==64
        bx.set_yticks([0,1,2],['0.025','0.05','0.10']);bx.invert_yaxis()
        bx.set_ylabel('Change threshold');bx.set_xlabel('Visitor histories (64 total)')
        bx.set_xlim(0,64);bx.set_xticks([0,16,32,48,64]);bx.spines[['top','right']].set_visible(False)
    fig.suptitle('Which changes first within an isolated population?',fontsize=17,y=.985)
    fig.text(.5,.943,'Each point pairs two crossing times from the SAME visitor history; primary threshold = 0.05',ha='center',fontsize=10)
    handles=[plt.Rectangle((0,0),1,1,color=colors[k]) for k in colors]
    fig.legend(handles,['Capacity first','Within 5 updates','Investment first'],loc='lower center',bbox_to_anchor=(.5,.095),ncol=3,frameon=False)
    fig.subplots_adjust(top=.875,bottom=.22,left=.12,right=.975,hspace=.42,wspace=.40)
    fig.text(.10,.025,'More-isolated treatment; mutation probability 0.01; both traits have founder variation.\n'
        'Crossing = change from founders maintained for 20 updates; not the first infinitesimal change.\n'
        'One history averages 8 demographic repeats. All 64 histories reach both thresholds shown.\n'
        'Updates are not calibrated years. Ordering does not establish causation. Zero-mutation cases are retained in CSV.',fontsize=9)
    for ext in ['png','pdf','svg']:fig.savefig(out/f'temporal_order.{ext}',dpi=180)
    receipt=dict(status='rendered',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        exported_events=sum(len(r['events']) for r in rows),primary_points=128,
        csv_sha256=hashlib.sha256((out/'all_far_threshold_events.csv').read_bytes()).hexdigest())
    (out/'provenance.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt))


if __name__=='__main__':main()
