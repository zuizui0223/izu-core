"""Read-only signed accounting of admitted restored I trajectories; no simulation."""
from pathlib import Path
import argparse,hashlib,json
import numpy as np

READOUT_SHA='4bbd159276d47f2c5a7d4e87d3f4fe1b4a642574f38203e6aeff327dabd06a97'
def sha(b):return hashlib.sha256(b).hexdigest()

def components(source,mothers,fathers,children,expected_response):
    source=np.asarray(source,dtype=float);mothers=np.asarray(mothers,dtype=float)
    fathers=np.asarray(fathers,dtype=float);children=np.asarray(children,dtype=float)
    if (source.ndim!=1 or not len(source) or mothers.ndim!=1 or not len(mothers)
        or mothers.shape!=fathers.shape or children.shape!=(len(mothers),2)
        or not np.isfinite(expected_response)
        or any(not np.isfinite(x).all() or (x<0).any() or (x>1).any() for x in (source,mothers,fathers,children))):
        raise ValueError('occupied finite source and offspring investment records required')
    resident=float(source.mean());selected=float(((mothers+fathers)/2).mean());final=float(children.mean())
    result=dict(selection=float(expected_response),parent_sampling=selected-resident-expected_response,
        transmission=final-selected,observed_change=final-resident)
    error=abs(sum(result[k] for k in ('selection','parent_sampling','transmission'))-result['observed_change'])
    if error>1e-12:raise ValueError('signed investment closure failed')
    result['closure_error']=error
    return result

def audit(raw_dir):
    raw_dir=Path(raw_dir);b=(raw_dir/'READOUT.json').read_bytes()
    if sha(b)!=READOUT_SHA:raise ValueError('original admitted producer readout identity')
    report=json.loads(b);out=[]
    for record in report['cases']:
        p=raw_dir/(record['key']+'.npz');b=p.read_bytes()
        if sha(b)!=record['raw_sha256']:raise ValueError('restored raw case drift')
        with np.load(p,allow_pickle=False) as f:a={k:f[k].copy() for k in f.files}
        r=json.loads(str(a['metadata'].item()));task=r['task'];tr=r['trigger']
        if task['key']!=record['key'] or r['original_I']!=record['original_I'] or r['restored_I']!=record['restored_I']:
            raise ValueError('case/primary identity')
        rec=dict(key=task['key'],block=task['block'],trigger=tr,raw_sha256=sha(b))
        rows=[]
        if tr is not None:
            for t in range(len(r['rows'])-1):
                lo,hi=a['offsets'][t:t+2];nl,nh=a['offsets'][t+1:t+3];pl,ph=a['parent_offsets'][t:t+2]
                ids=a['ids'][lo:hi];traits=a['alleles'][lo:hi,1,:].mean(axis=1)
                nxt=a['alleles'][nl:nh,1,:];edge=a['parentage'][pl:ph]
                if not len(ids) or not len(nxt) or not np.array_equal(edge[:,0],a['ids'][nl:nh]):
                    raise ValueError('occupied descendant parentage inventory')
                index={int(x):i for i,x in enumerate(ids)}
                mothers=np.array([index[int(x)] for x in edge[:,1]]);fathers=np.array([index[int(x)] for x in edge[:,2]])
                if (a['mutation_flags'][nl:nh,1,:].any()
                    or not np.any(nxt[:,0,None]==a['alleles'][lo:hi,1,:][mothers],axis=1).all()
                    or not np.any(nxt[:,1,None]==a['alleles'][lo:hi,1,:][fathers],axis=1).all()):
                    raise ValueError('investment parental transmission or no-I-mutation law differs')
                row=components(traits,traits[mothers],traits[fathers],nxt,r['rows'][t]['expected_response'][1])
                row['year']=r['rows'][t]['year'];rows.append(row)
        totals={k:sum(x[k] for x in rows) for k in ('selection','parent_sampling','transmission','observed_change')}
        if abs(totals['observed_change']-(r['restored_I']-r['original_I']))>1e-12:
            raise ValueError('complete terminal path closure')
        rec.update(**totals,updates=len(rows),annual=rows);out.append(rec)
    if len(out)!=64 or len({r['key'] for r in out})!=64:raise ValueError('all64 unique histories')
    blocks={}
    for block in ('causal_main','causal_confirmation'):
        rows=[r for r in out if r['block']==block]
        if len(rows)!=32:raise ValueError('two fixed32-history blocks')
        blocks[block]={k:sum(r[k] for r in rows)/32 for k in ('selection','parent_sampling','transmission','observed_change')}
    return dict(status='RETROSPECTIVE_ALL64_RESTORED_GENOME_PARENTAGE_ACCOUNTING',histories=64,
        updates=sum(r['updates'] for r in out),producer_readout_sha256=READOUT_SHA,blocks=blocks,rows=out,
        scope='Signed within-path accounting; no new significance family, unique causal fractions or ABM-density mediation',new_histories=0)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--raw-dir',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();d=audit(args.raw_dir);d['auditor_sha256']=sha(Path(__file__).read_bytes())
    with args.out.open('x',encoding='utf-8') as f:json.dump(d,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({k:v for k,v in d.items() if k!='rows'}))

if __name__=='__main__':main()
