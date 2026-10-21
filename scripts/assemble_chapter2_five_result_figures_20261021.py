"""Editorial figure assembly from existing outputs; no inference or simulation."""
from pathlib import Path
import copy
import hashlib
import json
import xml.etree.ElementTree as E
from html import escape

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'figures/chapter2_nee_five_results'
OLD=ROOT/'figures/chapter2_nee'
NS='http://www.w3.org/2000/svg'
E.register_namespace('',NS)

def source(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8'))

def text(x,y,t,size=20,color='#233447'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-family="Arial, sans-serif">{escape(t)}</text>'

def write(name,title,content,meta,height=650):
    s=f'<svg xmlns="{NS}" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img"><title>{escape(title)}</title><desc>Source-linked editorial display; evidence ranks and cohorts remain separate.</desc><metadata>{escape(json.dumps(meta))}</metadata><rect width="1200" height="{height}" fill="white"/>'+text(40,45,title,27)+content+'</svg>'
    (OUT/name).write_bytes(s.encode())

def crop(name,title,x,width):
    p=OLD/'figure_01_q1_mechanism.svg';root=E.parse(p).getroot()
    nested=E.Element(f'{{{NS}}}svg',dict(x='0',y='85',width='1200',height='580',viewBox=f'{x} 340 {width} 380',preserveAspectRatio='none',overflow='hidden'))
    for el in root:
        if el.tag.rsplit('}',1)[-1] not in ('title','desc','metadata'):
            child=copy.deepcopy(el)
            if child.text and child.text.startswith(('B ﾂｷ Fixed A','C ﾂｷ A-evolution')):child.text=child.text[4:]
            nested.append(child)
    write(name,title,E.tostring(nested,encoding='unicode')+text(40,690,'Change in I; vertical line = zero. Points and intervals retained from source Q1 figure.',17),dict(source=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),operation='crop existing admitted panel; no recalculation'),height=700)

def main():
    OUT.mkdir(exist_ok=True)
    content=text(40,90,'Which responses are predictable, and which options remain?',23)
    labels=[('Assurance A','Autonomous selfing capacity','Buffers unfilled ovules'),('Matching M','Fit to visitor optima','History-specific matching'),('Investment I','Allocation to attraction','Reproductive return versus cost')]
    for j,(head,a,b) in enumerate(labels):
        x=40+j*390
        content+=f'<rect x="{x}" y="140" width="360" height="155" rx="12" fill="{["#f8e9d7","#dceee7","#dce8f3"][j]}"/>'+text(x+18,180,head,25)+text(x+18,222,a,18)+text(x+18,258,b,18)
    for y,line in [(350,'Founding variation sets available alleles; it does not determine every trajectory.'),(400,'R1窶迭2: separate responses interact through reproductive and genetic processes.'),(450,'R3: selection direction and finite realization have different predictability.'),(500,'R4窶迭5: persistence, ancestral recovery and new-environment response differ.'),(575,'Conceptual framework; links are not estimated causal mediation.' )]:content+=text(40,y,line,21 if y<575 else 18)
    write('figure_01_framework.svg','Figure 1. From founding state to future floral options',content,dict(kind='conceptual',source='scripts/model3_island/reproduction.py'))
    crop('figure_02_independent_decline.svg','Figure 2. Investment declines with fixed assurance',45,675)
    crop('figure_03_assurance_interaction.svg','Figure 3. Assurance changes environmental investment contrasts',725,730)
    matched_path='docs/audits/CHAPTER2_MATCHED_AI_REPEATABILITY_20261019.json';pred_path='docs/audits/CHAPTER2_FOUNDER_PREDICTABILITY_20261021.json'
    d=source(matched_path);p=source(pred_path)['results'];content=text(40,95,'A  Repeated-history cohort',21)
    content+=text(40,125,'Identical far endpoints across four repeats / 128 histories',17)
    vals=[]
    for j,(setting,v) in enumerate(d['settings'].items()):
        y=155+j*90;content+=text(40,y,setting.replace('_',' '),19)
        for trait,dy,color in [('A',8,'#b3762e'),('I',34,'#386d9c')]:
            val=v['central'][trait]['far_identical_endpoint_contexts'];vals.append(dict(setting=setting,trait=trait,value=val))
            content+=f'<rect x="260" y="{y+dy-18}" width="{val*2.5}" height="20" fill="{color}" data-trait="{trait}" data-value="{val}"/>'+text(270+val*2.5,y+dy-2,f'{trait}: {val}',17)
    content+=text(650,95,'B  Separate crossed cohort: prediction skill',21)+text(650,125,'History-only; evolving A, B8 change',18)
    for j,trait in enumerate(('I','M')):
        val=100*p[f'evolving_{trait}_change']['loo_skill']['history'];y=220+j*115
        content+=text(650,y,f'{trait}: {val:.2f}%',24)+f'<rect x="650" y="{y+18}" width="{val*10}" height="28" fill="#386d9c" data-trait="{trait}" data-skill="{val}"/>'
    content+=text(650,440,'M is secondary; not a common-cohort A/I/M ranking.',17)+text(650,475,'Founder-only I skill: -0.46%; additive: -0.09%.',17)
    content+=text(40,560,'Panel A: endpoint agreement 竕 selection strength. Panel B: skill 竕 causal variance share.',19)+text(40,600,'Known-source pairing prediction; shared visitor-count schedule. Residual includes interaction and chance.',18)
    write('figure_04_predictability.svg','Figure 4. Trait-specific predictability in two separate cohorts',content,dict(sources=[matched_path,pred_path],endpoint_counts=vals,history_skills={t:p[f'evolving_{t}_change']['loo_skill']['history'] for t in ('I','M')}))
    for old,new,num in [('figure_04_access_survival.svg','figure_05_persistence_options.svg',5),('figure_06_late_transfer.svg','figure_06_transfer.svg',6)]:
        s=(OLD/old).read_text(encoding='utf-8')
        if num==5:s=s.replace('Figure 4','Figure 5')
        (OUT/new).write_bytes(s.encode())

if __name__=='__main__':main()
