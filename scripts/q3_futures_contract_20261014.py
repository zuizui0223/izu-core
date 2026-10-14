"""Frozen Q3 contract, raw-only admission and bounded readout. No model updates."""
import hashlib
import importlib.util
import io
import json
import math
import os
from pathlib import Path
import sys
import time
import zipfile

import numpy as np

ARCHIVE_SHA = '90b9d063c564edf97f12d3a3917819486f72d4ecb8281a20ebdaf39ad7de14c6'
SOURCE_SHA = 'f0fd126f638e1c6bd130e640ce4491b3bb47aac3da1838359a902776c9a4e037'
PROTOCOL_SHA = 'e549464de272e5a792b45e61ea68f14af02ddf46ed1287a2a81249d0791f48e9'
PREFLIGHT_SHA = '165a0d39f6f226ac4ccfbfb65fef4b2189fde272ccb0c0f33d840d542ae2760b'
FIELDS = ('ids', 'alleles', 'allele_origin', 'mutation_flags', 'birth_years')
BLOCKS = ('causal_main', 'causal_confirmation')
NAMESPACE = 'izu-q3-conditional-restoration-v1-20261014'
MAX_CALLS = 1981472
MAX_DISK = 16 * 1024**3


def require(ok, why):
    if not ok:
        raise ValueError(why)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def checked_bytes(path, expected):
    raw = Path(path).read_bytes()
    require(sha(raw) == expected, f'SHA256 mismatch: {path}')
    return raw


def write_json(path, value):
    with Path(path).open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2, allow_nan=False)
        f.write('\n')


def seed_for(key, replicate):
    return int.from_bytes(hashlib.sha256(f'{NAMESPACE}\0{key}\0{replicate}'.encode()).digest()[:16], 'big')


def restore(alleles):
    a = np.asarray(alleles)
    require(a.ndim == 3 and a.shape[1:] == (3, 2) and len(a) > 0, 'occupied diploid state required')
    v = a[0, 1, 0]
    require(np.isfinite(a).all() and np.all(a[:, 1] == v) and 1/16 <= v <= 15/16, 'interior I fixation required')
    b = a.copy()
    b[:, 1] = [v-1/16, v+1/16]
    require(np.array_equal(a.mean(2), b.mean(2)), 'restoration changed expression')
    return b


def event_start(values, initial):
    run = 0
    for year, value in enumerate(values):
        run = run+1 if value is not None and np.isfinite(value) and initial-value >= .05 else 0
        if run == 20:
            return year-19
    return None


def classify(lo, hi):
    return dict(direction='positive' if lo > 0 else 'negative' if hi < 0 else 'unresolved',
                practical='positive' if lo > .01 else 'negative' if hi < -.01 else
                'operationally_equivalent' if lo >= -.01 and hi <= .01 else 'unresolved')


def summarize(records, cases):
    require(len(cases) == 64 and len({c['key'] for c in cases}) == 64, '64 unique slots required')
    for block, triggered in zip(BLOCKS, (31,30)):
        rows = [c for c in cases if c['block'] == block]
        require(len(rows) == 32 and sum(c['trigger'] is not None for c in rows) == triggered, 'block inventory')
    expected = {(c['key'], r) for c in cases if c['trigger'] is not None for r in range(64)}
    identities = [(r['key'], r['replicate']) for r in records]
    require(len(identities) == len(expected) and set(identities) == expected, 'missing/duplicate/foreign pair')
    survival = dict(both_alive=0, native_only=0, restored_only=0, both_extinct=0)
    for r in records:
        for arm in ('native', 'restored'):
            value, alive = r[arm+'_I'], r[arm+'_survived']
            require(type(alive) is bool and alive == (value is not None), 'survival/mean mismatch')
            require(value is None or (np.isfinite(value) and 0 <= value <= 1), 'invalid terminal mean')
        a,b = r['native_survived'],r['restored_survived']
        survival['both_alive' if a and b else 'native_only' if a else 'restored_only' if b else 'both_extinct'] += 1
        if a and b:
            require(abs(r['native_I']-r['restored_I']) <= 1/16+1e-14, 'contrast outside frozen support')
    result = dict(pairs=len(records), slots=64, policy_zero_slots=3, survival=survival,
                  target='fixed_state_coupling_specific_paired_survivor_conditional',
                  original_primary='unresolved_unchanged', means=None)
    by_key={c['key']:c['block'] for c in cases}
    result['survival_by_block']={block:{label:sum(by_key[r['key']]==block and r['native_survived']==a and r['restored_survived']==b for r in records)
        for label,a,b in [('both_alive',True,True),('native_only',True,False),('restored_only',False,True),('both_extinct',False,False)]} for block in BLOCKS}
    if survival['both_alive'] != len(records):
        result.update(decision='not_evaluable', reason='terminal_extinction', directional_replication='not_evaluable')
        return result
    case_mean = {c['key']: 0.0 for c in cases}
    for r in records:
        case_mean[r['key']] += (r['native_I']-r['restored_I'])/64
    means = {}
    for block in ('all64', *BLOCKS):
        rows = cases if block == 'all64' else [c for c in cases if c['block'] == block]
        n, t = len(rows), sum(c['trigger'] is not None for c in rows)
        mean = math.fsum(case_mean[c['key']] for c in rows)/n
        b = (1/16)*math.sqrt(2*t*math.log(120)/(64*n*n))
        means[block] = dict(estimate=mean, half_width=b, interval=[mean-b,mean+b], **classify(mean-b,mean+b))
    directions = [means[b]['direction'] for b in BLOCKS]
    replicated = directions[0] if len(set(directions))==1 and directions[0]!='unresolved' else 'opposed' if set(directions)=={'positive','negative'} else 'unresolved'
    result.update(decision='evaluated_conditional', means=means, directional_replication=replicated,
                  all_averages_operationally_equivalent=all(m['practical']=='operationally_equivalent' for m in means.values()))
    return result


class Budget:
    """Single-coordinator, durable conservative reservation BEFORE any native calls."""
    def __init__(self, path, max_calls=MAX_CALLS):
        self.path = Path(path)
        if self.path.exists():
            raise FileExistsError(self.path)
        self.calls, self.max_calls, self.reservations = 0, max_calls, []
        write_json(self.path, dict(reserved_calls=0, max_calls=max_calls, reservations=[]))

    def reserve(self, calls, label):
        require(type(calls) is int and calls >= 0 and self.calls+calls <= self.max_calls, 'native call cap')
        require(label not in {r['label'] for r in self.reservations}, 'duplicate reservation')
        self.calls += calls
        self.reservations.append(dict(label=label, calls=calls))
        temp = self.path.with_suffix('.tmp')
        with temp.open('w', encoding='utf-8') as f:
            json.dump(dict(reserved_calls=self.calls, max_calls=self.max_calls, reservations=self.reservations), f)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp, self.path)


def arrays(raw):
    with np.load(io.BytesIO(raw), allow_pickle=False) as f:
        return {k:f[k].copy() for k in f.files}


def load_native(source):
    """A private package name avoids accidentally importing the checkout kernel."""
    package = Path(source)/'scripts/model3_island'
    name = 'q3_frozen_native'
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, package/'__init__.py', submodule_search_locations=[str(package)])
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    modules = [__import__(name+'.'+n, fromlist=[n]) for n in ('types','population','reproduction','randomness')]
    require(all(Path(m.__file__).resolve().is_relative_to(Path(source).resolve()) for m in modules), 'native import escaped frozen source')
    return modules


def admit(archive, source_input, repo, out):
    """Verify complete archived identities and original state inventory, no updates."""
    repo, out = Path(repo), Path(out)
    preflight = json.loads(checked_bytes(repo/'data/designs/restoration_futures_preflight_20261014.json', PREFLIGHT_SHA))
    checked_bytes(repo/'docs/CHAPTER2_RESTORATION_CONDITIONAL_FUTURES_20261014.md', PROTOCOL_SHA)
    source = out/'frozen_source'
    source.mkdir()
    original = out/'original'
    original.mkdir()
    with zipfile.ZipFile(io.BytesIO(checked_bytes(archive, ARCHIVE_SHA))) as z, zipfile.ZipFile(io.BytesIO(checked_bytes(source_input, SOURCE_SHA))) as sz:
        require(len(z.namelist())==len(set(z.namelist())), 'duplicate archive member')
        source_manifest_raw = sz.read('work/EL_next_20261007/extension_source_manifest.json')
        manifest = json.loads(source_manifest_raw)
        for name, digest in preflight['frozen_source_sha256'].items():
            raw = z.read(name)
            require(sha(raw)==digest, 'frozen source member hash')
            rel = name.removeprefix('FROZEN_SOURCE/')
            require(not Path(rel).is_absolute() and '..' not in Path(rel).parts, 'source path traversal')
            path = source/rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        for name,digest in manifest['files'].items():
            require(sha((source/name).read_bytes())==digest, 'original source manifest mismatch')
        campaign = json.loads(sz.read('work/EL_order_boundary_20261007/natural_campaign_design.json'))
        write_json(out/'campaign.json', campaign)
        old_seeds, new_seeds = set(), set()
        for case in preflight['cases']:
            key = case['key']
            raw = z.read('ORIGINAL64/'+key+'.npz')
            require(sha(raw)==case['original_npz_sha256'], 'original NPZ hash')
            receipt = json.loads(z.read('ORIGINAL64/'+key+'.json'))
            a = arrays(raw)
            meta = json.loads(str(a['metadata']))
            require(receipt['sha256']==sha(raw) and receipt['status']=='complete_verified' and not receipt['technical'], 'original receipt')
            require(meta['identity']==receipt['identity'], 'original identity disagreement')
            identity = meta['identity']
            require(identity['source']['source_manifest']==sha(source_manifest_raw), 'manifest identity')
            for group in (identity['source']['local'], identity['producer']):
                for name,digest in group.items():
                    require(sha(sz.read('work/EL_order_boundary_20261007/'+name))==digest, 'original producer/context identity')
            require(meta['task']['key']==key and meta['task']['block']==case['block'], 'case task identity')
            cfg = meta['config']
            require(cfg['capacity']==48 and cfg['survival']==0 and cfg['years']==200 and cfg['seed_arrival']['supply']==0 and meta['mutation_mask']==[False,False,True], 'native config drift')
            old_seeds.add(meta['seed'])
            trigger = None
            require(len(a['offsets'])==202 and len(a['parent_offsets'])==201, 'original time inventory')
            for t in range(201):
                lo, hi = a['offsets'][t:t+2]
                v = a['alleles'][lo:hi,1]
                if v.size and (v==v.flat[0]).all():
                    trigger = t
                    break
            require(trigger==case['trigger'], 'first trigger mismatch')
            require(case['remaining_updates']==(0 if trigger is None else 200-trigger), 'remaining duration')
            require(len(case['pair_seeds'])==(0 if trigger is None else 64), 'seed inventory')
            for r, seed in enumerate(case['pair_seeds']):
                expected = seed_for(key,r)
                require(int(seed)==expected and expected not in new_seeds, 'fresh master seed mismatch')
                new_seeds.add(expected)
            (original/(key+'.npz')).write_bytes(raw)
        require(len(new_seeds)==3904 and not old_seeds.intersection(new_seeds), 'new seed admission')
    require(len(preflight['cases'])==64 and sum(c['remaining_updates'] for c in preflight['cases'])==7740, 'complete inventory')
    native = load_native(source)
    types, pop, repro, randomness = native
    component_ids = list(randomness.STREAM_IDS.values())
    require(len(component_ids)==len(set(component_ids)), 'duplicate component stream identity')
    write_json(out/'ADMISSION.json', dict(status='RAW_SOURCE_STATE_INVENTORY_ADMITTED', archive_sha256=ARCHIVE_SHA,
               source_input_sha256=SOURCE_SHA, source_manifest_sha256=sha(source_manifest_raw),
               source_members=len(preflight['frozen_source_sha256']), cases=64, fresh_pairs=3904,
               stream_ids=randomness.STREAM_IDS, numpy=np.__version__, python=sys.version,
               production_updates=990720, no_biology_during_admission=True))
    return preflight
