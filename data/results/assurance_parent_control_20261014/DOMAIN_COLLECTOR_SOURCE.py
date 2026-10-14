"""V2 exact-domain admission of completed immutable V1 birth replay receipts."""
from pathlib import Path
import hashlib,json
READER='860680aa7ba248b43dad6e4e984f3af52fc23438014ca8b13246b72bbc167906'
COMMIT='90d586f8f54ed660ed1634f0a1119951c0700309'


def admit_domain(run,receipts):
    if run['source_commit']!=COMMIT or run['cases']!=4096 or run['updates']!=819200:
        raise ValueError('producer full cohort identity differs')
    expected={(b,i,o,t) for b in ('main','confirmation') for i in range(512)
              for o in ('A_access_first','I_access_first') for t in (1.05,1.5)}
    seen=set();shards=set();updates=0
    for row in run['records']:
        shard=row['shard'];r=receipts[shard]
        if type(shard) is not int or shard not in range(16) or shard in shards or r['shard']!=shard:
            raise ValueError('actual independently read shard differs or duplicates')
        shards.add(shard)
        if (r['status']!='CONTROLLED256_INDEPENDENT_WEIGHT_AND_BIRTH_REPLAY'
            or r['cases']!=256 or r['updates']!=51200 or len(r['records'])!=256
            or r['execution_commit']!=COMMIT or r['source_archive_sha256']!=row['sha256']
            or r['independent_reader_normalized_sha256']!=READER
            or r['new_control_producer_imported'] is not False or r['new_sampler_imported'] is not False):
            raise ValueError('frozen independent reader/shard receipt differs')
        updates+=r['updates']
        for record in r['records']:
            t=record['task'];key=(t['block'],t['replicate'],t['origin'],t['target'])
            if (key not in expected or key in seen or t['replicate']%16!=shard
                or t['policy']!='A_mean_equal_A_shadow_parents'):
                raise ValueError('independently authenticated complete task domain differs')
            seen.add(key)
    if seen!=expected or shards!=set(range(16)) or updates!=819200:
        raise ValueError('complete unique4096 independent domain required')
    return dict(cases=len(seen),updates=updates,shards=len(shards),
        frozen_reader_sha256=READER,
        task_domain_sha256=hashlib.sha256(json.dumps(sorted(seen)).encode()).hexdigest())


def main():
    W=Path(__file__).resolve().parents[1];root=W/'work/assurance_parent_control_independent_20261014'
    run=json.loads((W/'work/assurance_parent_control_execution_20261014/RUN_COMPLETION.json').read_bytes())
    provisional=root/'ALL4096_INDEPENDENT_ADMISSION.json';raw=provisional.read_bytes();v1=json.loads(raw)
    receipts={}
    for row in v1['records']:
        body=(root/row['receipt']).read_bytes()
        if hashlib.sha256(body).hexdigest()!=row['sha256']:
            raise ValueError('original independent receipt bytes changed')
        if row['shard'] in receipts:raise ValueError('duplicate externally labelled receipt')
        receipts[row['shard']]=json.loads(body)
    value=admit_domain(run,receipts)
    value.update(status='ALL4096_PUBLIC_CONTROLLED_FUTURES_INDEPENDENTLY_REPLAYED_DOMAIN_VERIFIED',
        source_commit=COMMIT,provisional_counts_only_receipt_sha256=hashlib.sha256(raw).hexdigest(),
        v2_collector_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        max_allele_replay_error=max(r['max_allele_replay_error'] for r in receipts.values()),
        records=v1['records'],new_control_producer_imported=False,new_sampler_imported=False,
        correction='V1 full native-operator birth replays are retained. V2 adds actual shard labels, frozen reader identity and exact unique all4096 domain; no new biological history or repeated birth replay.')
    with (root/'ALL4096_INDEPENDENT_ADMISSION_V2.json').open('x',encoding='utf-8') as f:json.dump(value,f,indent=2);f.write('\n')
    print(json.dumps({k:v for k,v in value.items() if k!='records'},indent=2))


if __name__=='__main__':main()
