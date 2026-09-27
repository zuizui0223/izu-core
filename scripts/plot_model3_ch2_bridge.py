"""Publication exports from the complete, audited bridge summary only."""
import argparse
import csv
from hashlib import sha256
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scripts.report_model3_ch2_bridge import PAIRS

LABELS=('Natural histories','Richness matched','Eight visitor histories pooled','Larger plant population')
COLORS={'individual':'#007F86','density':'#C05B32'}


def load_verified(root):
    root=Path(root)
    provenance=json.loads((root/'provenance.json').read_text())
    for name,h in provenance['artifacts'].items():
        if sha256((root/name).read_bytes()).hexdigest()!=h:
            raise ValueError('audited artifact checksum differs: '+name)
    report=json.loads((root/'summary.json').read_text())
    if report['status']!='complete_audited_summary':raise ValueError('complete audit required')
    with np.load(root/'derived_tensors.npz',allow_pickle=False) as z:
        tensors={k:z[k] for k in z.files}
    return report,tensors


def history_points(delta):
    """A plotted point uses every demographic replicate; no survivor-only shortcut."""
    x=np.asarray(delta,float)
    if x.ndim!=3:raise ValueError('starts x histories x repeats required')
    return x.mean(axis=2)


def render(report,tensors,out,*,layout_only=False):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,
        'axes.spines.right':False,'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none'})
    main=report['campaigns']['main'];rows=[];files=[]
    def save(fig,name,caption):
        fig.text(.06,.035,caption,ha='left',va='bottom',fontsize=9,linespacing=1.5)
        if layout_only:fig.text(.5,.98,'SYNTHETIC LAYOUT CHECK — NOT RESEARCH RESULTS',ha='center',va='top',color='#B22222',weight='bold',fontsize=13)
        for ext in ('png','pdf','svg'):
            p=out/(name+'.'+ext);fig.savefig(p,dpi=220,facecolor='white');files.append(p)
        plt.close(fig)
    for mode in ('individual','density'):
        fig,axes=plt.subplots(2,2,figsize=(12,10),sharex=True,sharey=True)
        fig.subplots_adjust(left=.10,right=.98,bottom=.19,top=.90,hspace=.26,wspace=.18)
        fig.suptitle('Isolation effects across starting populations — '+('individual model' if mode=='individual' else 'deterministic density model'),y=.945,fontsize=16)
        for pi,((pair,near,far),ax) in enumerate(zip(PAIRS,axes.flat)):
            delta=tensors['main__'+far+'__'+mode]-tensors['main__'+near+'__'+mode]
            points=history_points(delta);r=main['pairs'][pair][mode]
            jitter=np.random.default_rng(270927).uniform(-.15,.15,points.shape[1])
            for s in range(len(points)):
                valid=np.isfinite(points[s]);v=points[s,valid]
                if len(v)>1 and np.ptp(v)>0:
                    body=ax.violinplot([v],positions=[s],widths=.60,showextrema=False)['bodies'][0]
                    body.set_facecolor(COLORS[mode]);body.set_edgecolor('none');body.set_alpha(.13)
                ax.scatter(s+jitter[valid],v,s=11,color=COLORS[mode],alpha=.42,linewidths=0)
                m=r['mean_by_start'][s];ci=m['mean_ci']
                if m['mean'] is not None:
                    ax.scatter(s,m['mean'],s=48,marker='D',color='#172A34',zorder=5)
                    if ci is not None:ax.vlines(s,*ci,color='#172A34',linewidth=2.2,zorder=4)
                ax.text(s,-1.00,f'{valid.sum()}/{points.shape[1]} histories',ha='center',fontsize=8)
                for h,value in enumerate(points[s]):rows.append({'panel':pair,'model':mode,'start_index':s,'history_index':h,'effect':None if not np.isfinite(value) else float(value)})
            ax.set_title(chr(65+pi)+'. '+LABELS[pi],loc='left',fontsize=12,weight='bold')
            ax.axhline(0,color='#5B6570',linestyle='--',linewidth=.8);ax.set_ylim(-1.07,1.07)
            ax.set_xticks(range(3),['0.3','0.5','0.7']);ax.grid(axis='y',alpha=.12)
        for ax in axes[:,0]:ax.set_ylabel('Isolated − less isolated\nchange in floral investment')
        for ax in axes[1]:ax.set_xlabel('Nominal initial investment')
        save(fig,'isolation_distributions_'+mode,
            'Each dot: one visitor history, averaged over all demographic repeats; incomplete histories are omitted and counted.\n'
            'Diamonds: joint-survivor conditional means; bars: 95% history-bootstrap intervals. Violin widths show relative density.\n'
            'Positive / negative values mean greater / smaller investment change under isolation. Identical scales in all panels.')
    fig,axes=plt.subplots(1,3,figsize=(15,6),sharey=True)
    fig.subplots_adjust(left=.14,right=.99,bottom=.30,top=.83,wspace=.12)
    fig.suptitle('How often does the isolation effect change sign across starting populations?',fontsize=16,y=.94)
    for ei,(epsilon,ax) in enumerate(zip((0,.01,.05),axes)):
        for mi,mode in enumerate(('individual','density')):
            for pi,(pair,_,_) in enumerate(PAIRS):
                r=main['pairs'][pair][mode]['classification'][ei];y=pi+(mi-.5)*.22;p=r['mixed_fraction'];ci=r['mixed_fraction_hoeffding_95']
                if p is not None:
                    ax.hlines(y,*ci,color=COLORS[mode],linewidth=1.5)
                    ax.scatter(p,y,color=COLORS[mode],marker='o' if mi==0 else 's',s=33,label=mode if pi==0 else None)
                ax.text(1.04,y,f"{r['counts']['mixed']}/{r['n_eligible']}",va='center',fontsize=8)
        ax.set_title(f'Sign threshold: ±{epsilon:g}',fontsize=12);ax.set_xlim(-.03,1.26);ax.set_xticks([0,.25,.5,.75,1]);ax.set_xlabel('Mixed-sign fraction');ax.grid(axis='x',alpha=.15)
    axes[0].set_yticks(range(4),['Natural','Richness matched','Visitor pool','Larger plants']);axes[0].invert_yaxis();axes[0].legend(loc='upper left',bbox_to_anchor=(0,-.18),ncol=2,frameon=False)
    save(fig,'mixed_sign_fractions','Mixed means at least one starting population above +threshold and another below −threshold.\n'
        'Labels use repeat means; they are not noise-free branching probabilities. Numbers: mixed / eligible histories.\n'
        'Bars: 95% independent-history Hoeffding bounds; undefined histories are excluded from this denominator.')
    fig,axes=plt.subplots(1,2,figsize=(12,7))
    fig.subplots_adjust(left=.19,right=.97,bottom=.24,top=.88,wspace=.40)
    occupancy=[]
    for pair,near,far in PAIRS:
        occupancy.append(main['pairs'][pair]['occupancy_effect'])
    for i,r in enumerate(occupancy):
        axes[0].hlines(i,*r['mean_ci'],color=COLORS['individual']);axes[0].scatter(r['mean'],i,color=COLORS['individual'])
    axes[0].set_yticks(range(4),['Natural','Richness matched','Visitor pool','Larger plants']);axes[0].invert_yaxis();axes[0].axvline(0,color='grey',lw=.7)
    axes[0].set_xlim(-1.05,1.05);axes[0].set_title('A. Persistence effect');axes[0].set_xlabel('Isolated − less isolated occupancy')
    matrix=np.full((8,3),np.nan);labels=[]
    for pi,(pair,_,_) in enumerate(PAIRS):
        for mi,mode in enumerate(('individual','density')):
            d=main['pairs'][pair][mode]['decomposition'];i=pi*2+mi;labels.append(['Natural','Matched','Pooled','Larger'][pi]+' / '+['individual','density'][mi])
            if d['status']=='descriptive_cell_means':matrix[i]=[d[k] for k in ('S','C','I')]
    axes[1].imshow(np.ma.masked_invalid(matrix),cmap='Blues',vmin=0,vmax=1,aspect='auto')
    for (i,j),v in np.ndenumerate(matrix):axes[1].text(j,i,'N/E' if not np.isfinite(v) else f'{v:.0%}',ha='center',va='center',color='white' if v>.55 else '#172A34',fontsize=9)
    axes[1].set_xticks(range(3),['S','C','I']);axes[1].set_yticks(range(8),labels,fontsize=9);axes[1].set_title('B. Descriptive variation shares')
    save(fig,'occupancy_and_decomposition','A: all populations included; 95% independent-history Hoeffding bounds. Extinction is not zero trait change.\n'
        'B: S = initial state; C = visitor history; I = their non-additive combination. N/E = not evaluable.\n'
        'Shares describe repeat-averaged cells; finite-repeat noise is not removed. Within-cell noise is reported in the summary.')
    with (out/'plotted_history_points.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    files.append(out/'plotted_history_points.csv')
    return files


def main():
    p=argparse.ArgumentParser();p.add_argument('--input',default='data/results/model3_ch2_bridge_summary_20260927');p.add_argument('--output',default='figures/model3_ch2_bridge_20260927');a=p.parse_args()
    report,tensors=load_verified(a.input);out=Path(a.output)
    if (out/'figure_provenance.json').exists():raise ValueError('preserve existing figures; choose a new output directory')
    files=render(report,tensors,out)
    provenance={'audited_input':str(a.input),'summary_sha256':sha256((Path(a.input)/'summary.json').read_bytes()).hexdigest(),'plot_source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'files':{p.name:sha256(p.read_bytes()).hexdigest() for p in files},'visual_review':'pending'}
    (out/'figure_provenance.json').write_text(json.dumps(provenance,indent=2),encoding='utf-8')


if __name__=='__main__':main()
