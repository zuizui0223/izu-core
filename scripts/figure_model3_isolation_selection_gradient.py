"""All states and snapshots; central-state emphasis fixed independently of signs."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs/model3_isolation_selection_gradient_20261005'
d=np.load(OUT/'gradients.npz');x=d['distances'];p=int(np.flatnonzero(np.all(d['states']==[.5,.5,.5],axis=1))[0])
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'pdf.fonttype':42,'svg.fonttype':'none'})
with PdfPages(OUT/'isolation_selection.pdf') as pdf:
    for ti,t in enumerate(d['snapshots']):
        fig,axs=plt.subplots(2,2,figsize=(11,8),sharex=True)
        for si,setting in enumerate(['Delayed selfing + capacity cost','Prior selfing + no capacity cost']):
            for k,title in enumerate(['Selection on floral investment','Selection on selfing capacity']):
                ax=axs[si,k];m=d['means'][si,:,ti,:,k];ci=d['intervals'][si,:,ti,p,k,:]
                ax.plot(x,m,color='#BCD5D8',lw=.6)
                ax.fill_between(x,ci[:,0],ci[:,1],color='#008C95',alpha=.17)
                ax.plot(x,m[:,p],'-o',color='#00747B',lw=2,ms=3)
                ax.axhline(0,color='#333333',ls='--',lw=1)
                ax.set(title=title if si==0 else '',ylabel=setting+'\nLocal log-fitness gradient',xlabel='Arrival distance (model units)',xlim=(0,3))
                ax.spines[['top','right']].set_visible(False)
        fig.suptitle(f'Where does selection change sign? Fixed plants, visitor snapshot {t}',fontsize=16)
        fig.subplots_adjust(top=.89,bottom=.24,hspace=.4,wspace=.32)
        fig.text(.12,.055,'Thin lines: all 45 resident states, each averaged over 64 histories. Bold: matching = investment = capacity = 0.5.\nBand: pointwise 95% history-bootstrap interval for the central state. Lines join sampled distances; no fitted threshold.\nPositive: increase favoured. Negative: decrease favoured. These gradients are not realized evolutionary rates.',fontsize=10)
        pdf.savefig(fig)
        if t==400:fig.savefig(OUT/'isolation_selection_t400.png',dpi=170)
        plt.close(fig)
print(OUT/'isolation_selection.pdf')
