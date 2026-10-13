"""Short Model 3 *technical* native-birth test; not the 1,536-history pilot.

Exactly 2 founders x 3 original visitor contexts x 2 A widths x 2 hidden-I
homolog states x 2 DISTINCT technical RNG streams, for 3 updates each.

All original biological modules and original t0 founder arrays must pass their
Git-blob/hash gates before any reproduction/advance call. No scientific
first-passage or event result may be inferred from these fixtures.
"""
from __future__ import annotations

import argparse
import base64
import copy
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

from scripts.audit_chapter2_clock_factorial_feasibility_20261013 import (
    A_HALF_WIDTHS, I_HOMOLOG_SCALE, FOUNDER_BLOCKS, transform,
)

FIXTURE_PATH = Path('data/design/chapter2_clock_original_t0_typed_fixture_20261013.json')
FIXTURE_GIT_BLOB = '4b529cce12bc44e06d43a22b10c325a52bbd967b'
FROZEN_SOURCE_GIT_BLOBS = {
    'types.py': '0bc427b3261e7baf1651648ee879b368f9bf935b',
    'reproduction.py': '95314698a3296b6f13b8c053c36f2df0b7b744ca',
    'population.py': '20e90f249f63e9f37e8801d19d9b75cade2fe193',
    'randomness.py': '46f1ee55899e729cdd09d9dbb9332694ef1e2071',
    'history.py': '0c58aee6f73ae133d96d8da4dd6678886ff3061c',
}
T0_EXPECTED_SOURCE_LEDGER = Path('data/results/chapter2_clock_t0_reproduction_equivalence_20261013.json')
SOURCE_LEDGER_GIT_BLOB = 'e1d4e58a8dde547a94b687d6f89d2843c8bfff0c'
CONTEXTS = {
    0: (0.0, 'empty', ()),
    3: (0.125, 'matched', (.5, .5, .5, .5)),
    4: (0.125, 'separated', (.3, .3, .7, .7)),
}
TECHNICAL_SALT = 'chapter2-clock-factorial-technical-3step-v1-20261013'
TECHNICAL_REPEATS = (0, 1)
TECHNICAL_UPDATES = 3
FIELDS = ('ids', 'alleles', 'allele_origin', 'mutation_flags', 'birth_years')
MUTATION_MASK = (False, False, True)
LEDGER_FIELDS = ('outcross', 'self_raw', 'self_viable', 'ovules', 'exported',
                 'delivered', 'lost', 'maternal', 'paternal')


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git_blob(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def load_original_source():
    from scripts.model3_island import types, reproduction, population, randomness, history
    mods = dict(types=types, reproduction=reproduction, population=population,
                randomness=randomness, history=history)
    for name, expected in FROZEN_SOURCE_GIT_BLOBS.items():
        module = mods[name[:-3]]
        if git_blob(Path(module.__file__)) != expected:
            raise ValueError('Original model source Git blob mismatch: ' + name)
    return mods


def source_fixture(path: Path = FIXTURE_PATH) -> dict:
    if git_blob(path) != FIXTURE_GIT_BLOB:
        raise ValueError('original t0 typed fixture Git blob drift')
    f = json.loads(path.read_bytes())
    if (f['schema'] != 'clock_original_t0_typed_fixture_20261013_v1'
            or f['new_biological_histories'] != 0
            or set(f['original_founders']) != set(FOUNDER_BLOCKS)
            or set(f['original_provider_sha256']) != {'0', '3', '4'}):
        raise ValueError('source original t0 inventory changed')
    return f


def ledger_reference(path: Path = T0_EXPECTED_SOURCE_LEDGER) -> dict:
    if git_blob(path) != SOURCE_LEDGER_GIT_BLOB:
        raise ValueError('old t0 reproduction ledger receipt drift')
    v = json.loads(path.read_bytes())
    if v['status'] != 'SIX_ORIGINAL_SOURCE_STATES_TWENTY_FOUR_GENOTYPE_CONTRAST_LEDGERS_EXACT' or len(v['records']) != 24:
        raise ValueError('bad old t0 ledger reference')
    return {(x['block'], x['original_context']):x['source_original_ledger_sha256'] for x in v['records']}


def decode_array(payload: dict) -> np.ndarray:
    raw = base64.b64decode(payload['data_b64'], validate=True)
    if sha(raw) != payload['sha256']:
        raise ValueError('source founder field array changed')
    dtype = np.dtype(payload['dtype'])
    shape = tuple(payload['shape'])
    if dtype.hasobject or np.prod(shape, dtype=int)*dtype.itemsize != len(raw):
        raise ValueError('source founder field dtype/shape mismatch')
    arr = np.frombuffer(raw, dtype=dtype).reshape(shape).copy()
    if not np.isfinite(arr).all():
        raise ValueError('source founder field nonfinite')
    return arr


def initial_state(fixture: dict, block: str, width: float, scale: float, modules: dict):
    types = modules['types']
    founding = fixture['original_founders'][block]['source_state_arrays']
    arrays = {k:decode_array(founding[k]) for k in FIELDS}
    state = types.PlantState(**arrays)
    if len(state.ids) != 48 or not np.all(state.birth_years == 0):
        raise ValueError('wrong original t0 typed founder state')
    adjusted, record = transform(state.alleles, width, scale)
    mutated = replace(state, alleles=adjusted)
    if not np.array_equal(mutated.alleles.mean(axis=2), state.alleles.mean(axis=2)):
        raise ValueError('initial expressed biological phenotype changed')
    return mutated,record


def visitor_and_config(fixture: dict, block: str, context: int, modules: dict):
    types = modules['types']
    if context not in CONTEXTS:
        raise ValueError('unregistered original visitor context')
    source = fixture['original_founders'][block]['contexts'][str(context)]
    cfg = types.Config.from_dict(source['config'])
    supply, composition, optima = CONTEXTS[context]
    if (cfg.capacity, cfg.years, cfg.mutation_rate, cfg.mutation_sd,
        cfg.survival, cfg.assurance_mode, cfg.investment_cost,
        cfg.assurance_cost, cfg.depression, cfg.seed_arrival.supply) != (
        48, 200, .01, .05, 0, 'evolving', .5, .5, .5, 0):
        raise ValueError('source biological parameters not admitted')
    if abs(cfg.activity - .4*supply)>1e-15:
        raise ValueError('original source environment activity changed')
    visitor = types.VisitorState(
        ids=np.arange(len(optima),dtype=np.int64),optima=np.array(optima,dtype=float),
        breadths=np.full(len(optima),cfg.visitor_breadth,dtype=float),
        effectiveness=np.full(len(optima),cfg.visitor_effectiveness,dtype=float),
    )
    if len(visitor.ids) != (0 if composition == 'empty' else 4):
        raise ValueError('original visitor count changed')
    return cfg,visitor,np.asarray(source['original_returns_t0'],dtype=float)


def technical_seed(block: str, repeat: int) -> int:
    if block not in FOUNDER_BLOCKS or repeat not in TECHNICAL_REPEATS:
        raise ValueError('not a technical replication cell')
    payload=f'{TECHNICAL_SALT}\0{block}\0{repeat}'.encode()
    return int.from_bytes(hashlib.sha256(payload).digest()[:16],byteorder='big')


def streams(block: str, repeat: int, modules: dict):
    rng = modules['randomness']
    return {name:rng.stream(technical_seed(block,repeat),name,0)
            for name in rng.STREAM_IDS}


def state_hash(state) -> str:
    digest=hashlib.sha256()
    for k in FIELDS:
        a=getattr(state,k)
        digest.update(k.encode()+b'\0'+str(a.dtype).encode()+b'\0')
        digest.update(np.asarray(a.shape,dtype=np.int64).tobytes())
        digest.update(a.tobytes(order='C'))
    return digest.hexdigest()


def ledger_hash(ledger) -> str:
    digest=hashlib.sha256()
    for key in LEDGER_FIELDS:
        x=np.asarray(getattr(ledger,key),dtype=np.float64)
        digest.update(key.encode()+b'\0')
        digest.update(np.asarray(x.shape,dtype=np.int64).tobytes())
        digest.update(x.tobytes(order='C'))
    return digest.hexdigest()


def compare_child_genetics(source,child,source_info,modules,cfg,seg_rng,mut_rng,year):
    """Independent birth-only replay from *recorded parents* and shadowed RNGs."""
    pop=modules['population']
    parentage = np.asarray(source_info['parentage'])
    if parentage.shape != (len(child.ids),3):
        raise ValueError('wrong parentage/child dimensions')
    if not np.array_equal(parentage[:,0],child.ids):
        raise ValueError('parentage child IDs mismatch')
    table={int(v):i for i,v in enumerate(source.ids)}
    try:
        mi=np.array([table[int(x)] for x in parentage[:,1]],dtype=int)
        fi=np.array([table[int(x)] for x in parentage[:,2]],dtype=int)
    except KeyError as exc:
        raise ValueError('parentage points to unregistered source') from exc
    transmitted=pop.inherit(source,mi,fi,replace(cfg,mutation_rate=0),
        segregation_rng=copy.deepcopy(seg_rng),mutation_rng=copy.deepcopy(mut_rng),
        year=year+1,mutation_traits=MUTATION_MASK)
    replayed=pop.inherit(source,mi,fi,cfg,
        segregation_rng=copy.deepcopy(seg_rng),mutation_rng=copy.deepcopy(mut_rng),
        year=year+1,mutation_traits=MUTATION_MASK)
    for f in FIELDS:
        if not np.array_equal(getattr(replayed,f),getattr(child,f)):
            raise ValueError('original native birth replay mismatch: '+f)
    if not np.array_equal(transmitted.alleles[:,:2],child.alleles[:,:2]):
        raise ValueError('I/M changed with mutation disabled')
    if not np.array_equal(transmitted.allele_origin,child.allele_origin):
        raise ValueError('original parental allele-origin replay mismatch')
    if (transmitted.mutation_flags & ~child.mutation_flags).any():
        raise ValueError('previously inherited source mutation flags were erased')
    if not np.all(child.birth_years == year+1):
        raise ValueError('source birth-years incorrect')
    if source_info['immigrant_recruits'] or source_info['survivors']:
        raise ValueError('original no-immigration/zero-survival contract violated')
    if source_info['resident_recruits'] != len(child.ids):
        raise ValueError('native resident recruit/census identity changed')
    return int(np.count_nonzero(transmitted.alleles[:,2,:]!=child.alleles[:,2,:]))


def technical_case(fixture,refs,modules,block,context,width,scale,repeat)->dict:
    pop=modules['population'];repro=modules['reproduction']
    state,_=initial_state(fixture,block,width,scale,modules)
    cfg,visitor,archived_t0=visitor_and_config(fixture,block,context,modules)
    empty=pop.subset(state,np.empty(0,dtype=int))
    rng=streams(block,repeat,modules)
    start=state_hash(state)
    updates=[]
    for t in range(TECHNICAL_UPDATES):
        ledger=repro.reproduce(state,visitor,cfg)
        if t == 0:
            actual=np.array([np.asarray(getattr(ledger,k)).sum() for k in
                ('maternal','paternal','self_raw','self_viable','ovules','exported','delivered','outcross')],dtype=float)
            if not np.allclose(actual,archived_t0,rtol=0,atol=1e-12):
                raise ValueError('archived original t0 phenotype reproductive totals mismatch')
            if ledger_hash(ledger)!=refs[(block,context)]:
                raise ValueError('adjusted original genetic state altered t0 reproductive ledger')
        source_n=len(state.ids)
        shadow_segregation=copy.deepcopy(rng['segregation'])
        shadow_mutation=copy.deepcopy(rng['mutation'])
        nxt,info=pop.advance(state,ledger,empty,cfg,rng,year=t,mutation_traits=MUTATION_MASK)
        count=compare_child_genetics(state,nxt,info,modules,cfg,shadow_segregation,shadow_mutation,t)
        if len(nxt.ids)>cfg.capacity or info['resident_selfed_recruits']+info['resident_outcross_recruits']!=len(nxt.ids):
            raise ValueError('native demography/parentage conservation mismatch')
        expected_total=float(ledger.outcross.sum()+ledger.self_viable.sum())
        if not np.isclose(float(ledger.maternal.sum()),expected_total,rtol=0,atol=1e-12):
            raise ValueError('native maternal seed ledger conservation failure')
        if not np.isclose(float(ledger.paternal.sum()),expected_total,rtol=0,atol=1e-12):
            raise ValueError('native biparental seed ledger conservation failure')
        updates.append({'update':t,'source_n':source_n,'next_n':len(nxt.ids),
                        'birth_only_replay_exact':True,'birth_A_mutated_homologs':count,
                        'original_parent_pairs_valid':True,'source_state_sha256':state_hash(state),
                        'next_state_sha256':state_hash(nxt),'ledger_sha256':ledger_hash(ledger),
                        'parentage_sha256':sha(info['parentage'].tobytes())})
        state=nxt
    return {'block':block,'context':context,'A_width':width,'I_homolog_scale':scale,
            'technical_repeat':repeat,'seed_master':str(technical_seed(block,repeat)),
            'initial_state_sha256':start,'rows':updates,'last_state_sha256':state_hash(state)}


def audit(fixture_path:Path=FIXTURE_PATH)->dict:
    modules=load_original_source()
    f=source_fixture(fixture_path)
    refs=ledger_reference()
    if set(refs) != {(b,c) for b in FOUNDER_BLOCKS for c in CONTEXTS}:
        raise ValueError('original six t0 reference contexts missing')
    # This is a technical source test; all contexts and arms reuse the same
    # cryptographically distinct technical stream for their (founder,repeat).
    results=[]
    for block in FOUNDER_BLOCKS:
        for repeat in TECHNICAL_REPEATS:
            for context in CONTEXTS:
                for width in A_HALF_WIDTHS:
                    for scale in I_HOMOLOG_SCALE:
                        one=technical_case(f,refs,modules,block,context,width,scale,repeat)
                        again=technical_case(f,refs,modules,block,context,width,scale,repeat)
                        if one != again:
                            raise ValueError('native technical stream rerun not bytewise repeatable')
                        results.append(one)
    if len(results)!=48 or sum(len(x['rows']) for x in results)!=144:
        raise ValueError('incomplete original native technical fixtures')
    counts={'native_replay_checks':144,'technical_cases':48,'technical_updates':144,
            'new_pilot_cases':0,'mutation_locus':'A_only','no_immigration':True,
            'all_founders_contexts_treatments_admitted':True}
    return {'schema':'chapter2_clock_native_3step_technical_v1',
            'status':'ORIGINAL_SOURCE_48_TECHNICAL_FIXTURES_REPLAYED_NOT_BIOLOGICAL_COHORT',
            'original_biological_commit':'328548612e93469fcc8663f24548530a57399b9a',
            'original_source_blob_map':FROZEN_SOURCE_GIT_BLOBS,
            'original_t0_fixture_git_blob':FIXTURE_GIT_BLOB,
            'original_t0_reproduction_ledger_git_blob':SOURCE_LEDGER_GIT_BLOB,
            'technical_salt':TECHNICAL_SALT,'technical_repeats_per_founder':len(TECHNICAL_REPEATS),
            'numpy_runtime':np.__version__,**counts,'cases':results,
            'limits':['3-updates each: not the predeclared 200-update, 1,536-path pilot.',
                      'Replay uses the same original source inheritance function on separately shadowed RNGs; independent algebraic and parental-allele checks are supplementary, not a separate model-family replication.',
                      'This tests technical genetics/demography input viability, not any six-event evolutionary order, clock predictive power, effect size or significance.',
                      'Stored original t0 founder arrays and immutable source SHA inputs; no natural evolutionary data or independent ecosystems.']}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--fixture',type=Path,default=FIXTURE_PATH)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    if args.out.exists():
        raise ValueError('Refuse overwriting technical run result')
    result=audit(args.fixture)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open('x',encoding='utf-8',newline='\n') as f:
        json.dump(result,f,indent=2,allow_nan=False,ensure_ascii=False)
        f.write('\n')
    print(json.dumps({k:result[k] for k in ('status','technical_cases','technical_updates','new_pilot_cases')},sort_keys=True),flush=True)


if __name__=='__main__':main()
