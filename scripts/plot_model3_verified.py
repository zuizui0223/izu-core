"""Static, source-backed figures for the verified prospective model3 campaigns."""
from pathlib import Path
import hashlib
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'figures/model3_verified_20260925'
SOURCES={}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
                     'axes.spines.right':False,'svg.fonttype':'none','pdf.fonttype':42})


def read(folder,name):
    path=ROOT/'data/results'/folder/name
    SOURCES[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
    return pd.read_csv(path)


def save(fig,name):
    for extension in ('png','pdf','svg'):
        path=OUT/f'{name}.{extension}'
        fig.savefig(path,dpi=220,bbox_inches='tight')
        if extension=='svg':
            path.write_bytes(('\n'.join(line.rstrip() for line in path.read_text(encoding='utf8').splitlines())+'\n').encode())
    plt.close(fig)


def main():
    for folder in ('model3_evolution_20260925','model3_assurance_robustness_20260925','model3_grid_comparison_20260925'):
        receipt=ROOT/'data/results'/folder/'verification.json'
        check=json.loads(receipt.read_text())
        assert check['status']=='verified' and check['replayed_cases']==check['artifacts']>0
        SOURCES[str(receipt.relative_to(ROOT))]=hashlib.sha256(receipt.read_bytes()).hexdigest()
    OUT.mkdir(parents=True,exist_ok=True)
    base=read('model3_evolution_summary_20260925','endpoints.csv')
    assurance=read('model3_assurance_summary_20260925','condition_summary.csv')
    ledger=read('model3_assurance_summary_20260925','endpoints.csv')
    grid=read('model3_grid_summary_20260925','endpoints.csv')
    envs=[('mainland','Mainland','#0072B2'),('activity_only','Lower activity','#56B4E9'),
          ('community_only','Island community','#E69F00'),('both','Both island changes','#D55E00')]
    fig,axes=plt.subplots(2,2,figsize=(10,7),sharex=True,sharey=True,layout='constrained')
    for row,s in enumerate((0.,.75)):
        for col,start in enumerate((.3,.7)):
            ax=axes[row,col]
            for env,label,color in envs:
                cell=base[(base.campaign=='primary')&(base.year==100)&(base.selfing==.5)&
                    (base.control=='selected')&(base.environment==env)&(base.survival==s)&(base.start==start)]
                values=np.sort(cell.investment_change.dropna())
                ax.step(values,np.arange(1,len(values)+1)/len(cell),where='post',label=label,color=color,lw=1.8)
            ax.axvspan(-.02,.02,color='.93',zorder=-1)
            ax.axvline(0,color='.4',lw=.7,ls=':')
            ax.set_title(f'{"Annual" if s==0 else "Perennial"}; initial access {start}')
            ax.set_xlim(-.12,.12); ax.set_ylim(0,1)
            ax.set_xlabel('Change in inherited investment'); ax.set_ylabel('Cumulative fraction of 256 runs')
    axes[0,0].legend(fontsize=8,loc='upper left')
    fig.suptitle('A mean shift does not imply one response in every population\n100 reproductive years; selfing 0.5, depression 0.5; all shown cells survive',fontsize=12)
    save(fig,'01_investment_distributions')

    fig,axes=plt.subplots(2,2,figsize=(9,6.5),layout='constrained')
    for row,s in enumerate((0.,.75)):
        for col,start in enumerate((.3,.7)):
            ax=axes[row,col]
            cell=assurance[(assurance.campaign=='assurance')&(assurance.year==400)&
                (assurance.control=='selected')&(assurance.environment=='both')&
                (assurance.survival==s)&(assurance.start==start)]
            matrix=cell.pivot(index='selfing',columns='depression',values='survivors').reindex(index=[.1,.5],columns=[0.,.5,.9]).to_numpy()
            im=ax.imshow(matrix/256,vmin=0,vmax=1,cmap='Blues',aspect='auto')
            for i in range(2):
                for j in range(3):
                    ax.text(j,i,f'{matrix[i,j]:.0f}/256',ha='center',va='center',color='white' if matrix[i,j]>128 else 'black')
            ax.set_xticks(range(3),['0','0.5','0.9']); ax.set_yticks(range(2),['0.1','0.5'])
            ax.set_xlabel('Inbreeding depression'); ax.set_ylabel('Delayed selfing fraction')
            ax.set_title(f'{"Annual" if s==0 else "Perennial"}; initial access {start}')
    fig.colorbar(im,ax=axes.ravel().tolist(),label='Fraction surviving',shrink=.7)
    fig.suptitle('Assurance can fail when selfing is weak or depression is strong\nFull-island scenario, 400 reproductive years; stationary-environment stress test',fontsize=12)
    save(fig,'02_assurance_persistence')

    fig,axes=plt.subplots(2,2,figsize=(9,8),sharex=True,sharey=True,layout='constrained')
    for row,s in enumerate((0.,.75)):
        for col,capacity in enumerate((48,192)):
            ax=axes[row,col]
            for start,marker,color in ((.3,'o','#0072B2'),(.7,'^','#D55E00')):
                cell=grid[(grid.points==3)&(grid.year==100)&(grid.environment=='both')&
                    (grid.control=='selected')&(grid.survival==s)&(grid.capacity==capacity)&(grid.start==start)]
                ax.scatter(cell.density_investment-cell.initial_investment,
                    cell.investment-cell.initial_investment,s=17,alpha=.55,marker=marker,color=color,label=f'Start {start}; n={len(cell)}')
            ax.plot([-.12,.12],[-.12,.12],ls='--',color='.5',lw=1)
            ax.axhline(0,color='.8',lw=.7); ax.axvline(0,color='.8',lw=.7)
            ax.set_xlim(-.12,.12); ax.set_ylim(-.12,.12); ax.set_aspect('equal')
            ax.set_title(f'{"Annual" if s==0 else "Perennial"}; capacity {capacity}')
            ax.set_xlabel('Density model: investment change'); ax.set_ylabel('Individual model: investment change')
            ax.legend(fontsize=8)
    fig.suptitle('Matched histories produce different finite-population outcomes\n100 years; selfing 0.5, depression 0.5; 3-node grid; all plotted pairs positive',fontsize=12)
    save(fig,'03_individual_density_pairs')

    fig,axes=plt.subplots(2,2,figsize=(11,8),sharex=True,layout='constrained')
    labels=['Outcross offspring','Viable selfed offspring','Inbreeding loss','Unfertilized ovules']
    colors=['#0072B2','#009E73','#CC79A7','#dddddd']
    for row,s in enumerate((0.,.75)):
        for col,start in enumerate((.3,.7)):
            ax=axes[row,col]; names=[]; parts=[]
            for env,name in [('mainland','Mainland'),('both','Island')]:
                for depression in (0.,.5,.9):
                    cell=ledger[(ledger.campaign=='assurance')&(ledger.year==100)&(ledger.control=='selected')&
                        (ledger.selfing==.5)&(ledger.survival==s)&(ledger.start==start)&
                        (ledger.environment==env)&(ledger.depression==depression)]
                    total=cell.cumulative_ovules.sum()
                    out=cell.cumulative_outcross.sum(); viable=cell.cumulative_selfed.sum()
                    loss=cell.cumulative_inbreeding_loss.sum(); raw=cell.cumulative_selfed_raw.sum()
                    values=np.array([out,viable,loss,total-out-raw])/total
                    assert np.all(values>=-1e-12) and np.isclose(values.sum(),1)
                    parts.append(values); names.append(f'{name}, depression {depression:g}')
            parts=np.array(parts); left=np.zeros(6)
            for j,(label,color) in enumerate(zip(labels,colors)):
                ax.barh(range(6),parts[:,j],left=left,color=color,label=label)
                left+=parts[:,j]
            ax.set_yticks(range(6),names,fontsize=8); ax.invert_yaxis(); ax.set_xlim(0,1)
            ax.set_xlabel('Fraction of all ovules produced'); ax.set_title(f'{"Annual" if s==0 else "Perennial"}; start {start}')
    axes[0,0].legend(fontsize=8,loc='lower left',bbox_to_anchor=(0,1.13),ncol=2)
    fig.suptitle('Pollen delivery, selfing and depression make separate contributions\nSelfing 0.5; 256 runs per bar; pooled ovules through year 100 or extinction',fontsize=12)
    save(fig,'04_reproductive_accounting')

    fig,axes=plt.subplots(1,2,figsize=(11,4.5),layout='constrained')
    campaign=ROOT/'data/results/model3_evolution_20260925'
    manifest=json.loads((campaign/'manifest.json').read_text())
    for artifact in manifest['artifacts']:
        path=campaign/artifact['path']
        with np.load(path,allow_pickle=False) as data:
            case=json.loads(str(data['case_json'][0]))
            if not (case['campaign']=='primary' and case['control']=='selected' and
                    case['selfing']==.5 and case['survival']==0 and case['start']==.3 and
                    case['environment'] in ('mainland','both')):
                continue
            visits=data['visitor_count']
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest==artifact['sha256']
        SOURCES[str(path.relative_to(ROOT))]=digest
        color='#0072B2' if case['environment']=='mainland' else '#D55E00'
        label='Mainland' if case['environment']=='mainland' else 'Island assembly'
        years=np.arange(1,401)
        axes[0].plot(years,visits.mean(axis=0),color=color,label=label)
        low,high=np.quantile(visits,[.05,.95],axis=0)
        axes[0].fill_between(years,low,high,color=color,alpha=.12)
    axes[0].set(xlabel='Reproductive year',ylabel='Visitor functional types',title='Assembly retains a long initial transient')
    axes[0].legend(fontsize=8)
    for survival,color in [(0.,'#0072B2'),(.75,'#D55E00')]:
        for start,style in [(.3,'-'),(.7,'--')]:
            cell=base[(base.campaign=='primary')&(base.environment=='both')&
                (base.control=='selected')&(base.selfing==.5)&(base.survival==survival)&(base.start==start)]
            assert (cell.population>0).all()
            fraction=cell.groupby('year').investment_alleles.apply(lambda x:(x==1).mean())
            axes[1].plot(fraction.index,fraction.values,color=color,ls=style,marker='o',
                label=f'{"Annual" if survival==0 else "Perennial"}, start {start}')
    axes[1].set(xlabel='Reproductive year',ylabel='Fraction with one investment allele',ylim=(0,1),
                title='Lost standing variation is not replenished')
    axes[1].legend(fontsize=8)
    fig.suptitle('Time changes both the visitor community and inherited variation\n256 histories; left: mean and 5–95% history range; right: all shown populations survive',fontsize=12)
    save(fig,'05_time_and_variation')
    (OUT/'provenance.json').write_text(json.dumps(dict(inputs=SOURCES,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2),encoding='utf8')
    print(OUT)


if __name__=='__main__':
    main()
