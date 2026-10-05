"""All controlled selection fields; arrows are not evolutionary trajectories."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import ListedColormap

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs/model3_reciprocal_selection_20261005'
data=np.load(OUT/'fields.npz')
axis=data['axis'];xx,yy=np.meshgrid(axis,axis)
settings=['delayed_control','prior_selfing','pollen_discount','assurance_cost']
communities=['reference8','left4','right4','center4','leftdup8']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'pdf.fonttype':42,'svg.fonttype':'none'})
with PdfPages(OUT/'selection_fields.pdf') as pdf:
    for matching in [.2,.5,.8]:
        fig,axs=plt.subplots(4,5,figsize=(15,12),sharex=True,sharey=True)
        for i,setting in enumerate(settings):
            for j,community in enumerate(communities):
                ax=axs[i,j];gi,ga,*_=data[f'{setting}__{community}__x{matching}']
                regime=(gi>0).astype(int)+2*(ga>0).astype(int)
                ax.pcolormesh(xx,yy,regime,cmap=ListedColormap(['#F4D5C5','#E5DDEB','#CAE8E5','#F6ECC7']),vmin=0,vmax=3,shading='nearest',rasterized=True)
                if gi.min()<0<gi.max():ax.contour(xx,yy,gi,levels=[0],colors=['#C45127'],linewidths=1.5)
                if ga.min()<0<ga.max():ax.contour(xx,yy,ga,levels=[0],colors=['#006D8F'],linewidths=1.5,linestyles='dashed')
                skip=(slice(None,None,6),slice(None,None,6));norm=np.maximum(np.hypot(gi,ga),1e-20)
                ax.quiver(xx[skip],yy[skip],(gi/norm)[skip],(ga/norm)[skip],color='#344A53',scale=15,width=.004)
                ax.set(xlim=(0,1),ylim=(0,1),xticks=[0,.5,1],yticks=[0,.5,1])
                if i==0:ax.set_title(community)
                if j==0:ax.set_ylabel(setting+'\nSelfing capacity')
                if i==3:ax.set_xlabel('Floral investment')
        fig.suptitle(f'How reproductive state changes local selection (matching = {matching})',fontsize=17,y=.98)
        fig.subplots_adjust(left=.1,right=.98,top=.93,bottom=.13,hspace=.25,wspace=.15)
        fig.text(.1,.075,'Solid orange: investment selection = 0. Dashed blue: capacity selection = 0. Teal region: investment favoured down, capacity up.',fontsize=10)
        fig.text(.1,.045,'Arrows show normalized local selection gradients, NOT evolutionary velocity. All four existing settings and five controlled communities shown.',fontsize=9)
        fig.text(.1,.02,'Fixed monomorphic residents; no genetic covariance or evolving visitor history. Exploratory diagnostic; no observed-island frequency interpretation.',fontsize=9)
        pdf.savefig(fig)
        if matching==.5:
            fig.savefig(OUT/'selection_fields_matching05.png',dpi=160)
            fig.savefig(OUT/'selection_fields_matching05.svg')
        plt.close(fig)
print(OUT/'selection_fields.pdf')
