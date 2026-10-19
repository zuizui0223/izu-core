"""Independent read-only factorial audit: no native reproduction/producer imports."""
import argparse, hashlib, json, random
from pathlib import Path

PROTO=Path('docs/protocols/CHAPTER2_BASELINE_POLLEN_LIMIT_2X2_FROZEN_20261019.json')
SHA='87af92484af9988181b4f3bed6760d39325de70cca8c0b4e1cec19c47b8c9849'
LEVELS=('strong_baseline_limitation','weak_baseline_limitation')
STARTS=(.3,.5)
FOUNDERS=tuple(range(810101,810113))
REPS=(1,2,3,4)
ARMS=('control','decline')

def mean(v):return sum(v)/len(v) if v else None
def key(r):return (r['baseline'],r['start_A'],r['founder_seed'],r['demography_repeat'],r['arm'])

def quantile_ci_by_founder(xs,seed,n=10000):
 rng=random.Random(seed);k=len(xs)
 if not k:return None
 estimates=sorted(sum(xs[rng.randrange(k)] for _ in range(k))/k for _ in range(n))
 return [estimates[int(.025*n)],estimates[int(.975*n)-1]]

def check(rows,summary):
 expected={(level,a,f,r,arm) for level in LEVELS for a in STARTS
           for f in FOUNDERS for r in REPS for arm in ARMS}
 if len(rows)!=384 or len(set(map(key,rows)))!=384 or set(map(key,rows))!=expected:
  raise ValueError('incomplete or duplicate full allocation')
 ix={key(x):x for x in rows}
 for k,x in ix.items():
  level,a,f,r,arm=k
  y=ix[level,a,f,r,'decline' if arm=='control' else 'control']
  z=ix[(LEVELS[1] if level==LEVELS[0] else LEVELS[0]),a,f,r,arm]
  if (x['source_contract_sha256']!=SHA or x['updates']!=80 or
      x['prefix_updates']!=30 or x['prefix_state_hash']!=y['prefix_state_hash'] or
      x['initial_state_hash']!=y['initial_state_hash'] or
      x['initial_state_hash']!=z['initial_state_hash'] or
      x['t_prefix']!=y['t_prefix'] or
      x['t_end']['n']!=x['n_terminal'] or
      x['alive_at_end']!=(x['n_terminal']>0) or
      x['q_first']!=y['q_first'] or x['q_pre_last']!=y['q_pre_last']):
   raise ValueError('source/prefix/initial/occupancy mismatch')
  if x['t0']['n']!=48:raise ValueError('wrong founder count')
  for stage in ('t0','t_prefix','t_end'):
   t=x[stage]
   if not isinstance(t['n'],int) or not 0<=t['n']<=48:raise ValueError('invalid census')
   for attr in ('A','I','M','max_I','min_A'):
    v=t[attr]
    if (t['n']==0 and v is not None) or (t['n']>0 and
        (not isinstance(v,(int,float)) or not 0<=v<=1)):
     raise ValueError('invalid extinct or living trait')
  for q in ('q_first','q_pre_last','q_future_first','q_future_last'):
   v=x[q]
   if v is not None and (not isinstance(v,(int,float)) or not 0<=v<=1):
    raise ValueError('invalid pollen-service fraction')
 if summary['source_contract_sha256']!=SHA or summary['counts']['rows']!=384:
  raise ValueError('producer summary identity/count mismatch')
 summaries=[]
 interactions=[]
 for a in STARTS:
  for level in LEVELS:
   ctrl=[ix[level,a,f,r,'control'] for f in FOUNDERS for r in REPS]
   drop=[ix[level,a,f,r,'decline'] for f in FOUNDERS for r in REPS]
   keep=[(s,t) for s,t in zip(ctrl,drop) if s['t_prefix']['n'] and s['t_end']['n'] and t['t_end']['n']]
   prior=[s for s in ctrl if s['t_prefix']['n']]
   deltas=lambda trait:mean([t['t_end'][trait]-s['t_end'][trait] for s,t in keep])
   pre=lambda trait:mean([s['t_prefix'][trait]-s['t0'][trait] for s in prior])
   row=dict(start_A=a,baseline=level,allocated_pairs=48,both_survived=len(keep),
            terminal_survival_count_control=sum(s['alive_at_end'] for s in ctrl),
            terminal_survival_count_decline=sum(s['alive_at_end'] for s in drop),
            pre_decline_A_change_mean=pre('A'),pre_decline_I_change_mean=pre('I'),
            terminal_decline_minus_control_A=deltas('A'),
            terminal_decline_minus_control_I=deltas('I'))
   old=[s for s in summary['summary'] if s['start_A']==a and s['baseline']==level]
   if len(old)!=1:raise ValueError('producer summary stratum missing')
   for name,v in row.items():
    w=old[0][name]
    if (v is None)!=(w is None) or (v is not None and
        (abs(v-w)>1e-12 if isinstance(v,float) else v!=w)):
     raise ValueError('independent producer summary mismatch: '+name)
   row.update(A_end_control=mean([s['t_end']['A'] for s in ctrl if s['alive_at_end']]),
              A_end_decline=mean([s['t_end']['A'] for s in drop if s['alive_at_end']]),
              I_end_control=mean([s['t_end']['I'] for s in ctrl if s['alive_at_end']]),
              I_end_decline=mean([s['t_end']['I'] for s in drop if s['alive_at_end']]),
              initial_q=mean([s['q_first'] for s in ctrl if s['q_first'] is not None]),
              pre_end_q=mean([s['q_pre_last'] for s in ctrl if s['q_pre_last'] is not None]),
              post_q_control=mean([s['q_future_first'] for s in ctrl if s['q_future_first'] is not None]),
              post_q_decline=mean([s['q_future_first'] for s in drop if s['q_future_first'] is not None]))
   summaries.append(row)
  per_founder_A=[];per_founder_I=[]
  for f in FOUNDERS:
   vals={}
   for level in LEVELS:
    pairs=[(ix[level,a,f,r,'control'],ix[level,a,f,r,'decline']) for r in REPS]
    vals[level]={trait:mean([y['t_end'][trait]-x['t_end'][trait] for x,y in pairs
        if x['t_end']['n'] and y['t_end']['n']]) for trait in ('A','I')}
   if all(vals[lev]['A'] is not None for lev in LEVELS):
    per_founder_A.append(vals[LEVELS[1]]['A']-vals[LEVELS[0]]['A'])
    per_founder_I.append(vals[LEVELS[1]]['I']-vals[LEVELS[0]]['I'])
  interactions.append(dict(start_A=a,
   interaction_A=mean(per_founder_A),interaction_I=mean(per_founder_I),
   n_founders=len(per_founder_A),bootstrap_95_A=quantile_ci_by_founder(per_founder_A,20261019+int(a*100)),
   bootstrap_95_I=quantile_ci_by_founder(per_founder_I,20261119+int(a*100)),
   positive_founder_interactions_A=sum(v>0 for v in per_founder_A),
   interpretation='descriptive founder-bootstrap; not a registered confirmatory hypothesis test'))
 return dict(status='EXPLORATORY_RAW_ENDPOINT_AUDIT_PASS',
   source_contract_sha256=SHA,raw_rows=384,paired_arms=192,founders=12,
   summaries=summaries,interactions=interactions,
   limitations=['Same native operators not independently reimplemented',
    'No observed stochastic visitor histories, no natural island data',
    'Founder-cluster bootstrap conditional on the frozen 12 founders and model setting',
    'Genetic trait responses conditional on occupancy; all-start occupancy reported'])

def main():
 p=argparse.ArgumentParser()
 p.add_argument('--strong',required=True);p.add_argument('--weak',required=True)
 p.add_argument('--summary',required=True);p.add_argument('--out',required=True)
 args=p.parse_args()
 if Path(args.out).exists():raise ValueError('do not overwrite audit')
 if hashlib.sha256(PROTO.read_bytes()).hexdigest()!=SHA:raise ValueError('protocol mismatch')
 s=json.loads(Path(args.strong).read_text())
 w=json.loads(Path(args.weak).read_text())
 if s.get('level')!=LEVELS[0] or w.get('level')!=LEVELS[1]:
  raise ValueError('wrong source shards')
 if s.get('source_contract_sha256')!=SHA or w.get('source_contract_sha256')!=SHA:
  raise ValueError('wrong source contract')
 summary=json.loads(Path(args.summary).read_text())
 d=check(s['rows']+w['rows'],summary)
 Path(args.out).write_text(json.dumps(d,indent=2,sort_keys=True,allow_nan=False)+'\n')
 print(d['status'])

if __name__=='__main__':main()
