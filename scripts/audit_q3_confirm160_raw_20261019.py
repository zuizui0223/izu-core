"""Complete-only, independent arithmetic audit of local Q3 raw release assets.

Never imports a simulation/producer module, downloads data, or evolves a state.
The caller must supply the complete release, including SUMMARY160.json. Source
hashes are checked against an immutable Git commit, not the current worktree.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import zipfile

import numpy as np
from scipy.stats import t as student_t

SOURCE_COMMIT = 'f7792629b35b07e93ac9c98f8feb4d3894da85eb'
ROOT = Path(__file__).resolve().parents[1]
EPS = (0., .005, .01, .02, .05)
FIELDS = ('alleles', 'allele_origin', 'mutation_flags', 'ids', 'birth_years')
STREAMS = ('founders', 'visitor_arrivals', 'visitor_loss', 'seed_arrivals',
           'seed_settlement', 'survival', 'parents', 'segregation', 'mutation',
           'recruitment', 'visitor_settlement', 'source_genotypes', 'visitor_initial')


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(value).hexdigest()


def file_digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_json(raw):
    def pairs(items):
        out = {}
        for key, value in items:
            require(key not in out, 'duplicate JSON key')
            out[key] = value
        return out
    return json.loads(raw, object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON')))


def expected_plan(technical):
    return dict(schema='q3_native_technical_runner_v1' if technical else 'q3_production160_v1',
        mode='technical' if technical else 'confirmation',
        namespace=('q3-native-integration-technical-20261019-v1' if technical else
                   'ch2_joint160_consolidated_20261019_v2:106:planning-only'),
        founders=list(range(9100001, 9100004) if technical else range(501001, 501161)),
        visitors=list(range(9200001, 9200004) if technical else range(502001, 502161)),
        policies=['fixed', 'evolving'], budgets=[8., 4.5], fork=35, end=80,
        capacity=48, margin=.10, confirmation_authorized=not technical)


def founder_arrays(seed):
    """Independently reconstruct the declared founder only; zero transitions."""
    rng = np.random.default_rng(np.random.SeedSequence([seed, 1, 0]))
    value = .5 + rng.normal(0, .08, (48, 3, 2))
    a = 1 - np.abs(np.mod(value, 2) - 1)
    a[:, 1, :] = rng.choice([.375, .5, .625], size=(48, 2))
    rng.choice([.25, .5, .75], size=(48, 2))  # original pre-balance consumption
    first = np.tile([.25, .5, .75], 16)
    np.random.default_rng((seed + 39110) % (2**32)).shuffle(first)
    a[:, 2, 0] = first
    a[:, 2, 1] = 1 - first
    return dict(alleles=a, allele_origin=np.arange(288, dtype=np.int64).reshape(48, 3, 2),
                mutation_flags=np.zeros((48, 3, 2), bool), ids=np.arange(48, dtype=np.int64),
                birth_years=np.zeros(48, dtype=np.int64))


def verify_sources(provenance, source_root, source_commit):
    require(len(source_commit) == 40 and all(c in '0123456789abcdef' for c in source_commit),
            'full immutable source commit required')
    native = provenance['native']
    require(set(provenance) == {'native','adapter','protocol'} and
            set(native) == {'base_commit','files','python','numpy','scipy','byteorder'} and
            native['base_commit'] == 'e131da0376a615bceca8770d5d7236a30a5a36fe',
            'source provenance contract')
    expected_files = {
        'scripts/model3_island/' + name + '.py' for name in
        ('__init__', 'types', 'history', 'randomness', 'population', 'reproduction')}
    expected_files |= {'scripts/chapter2_q3_balanced_assurance_founders_20261018.py',
        'scripts/q3_joint_inference_20261019.py', 'scripts/q3_native_runner_20261019.py'}
    require(set(native['files']) == expected_files, 'source inventory mismatch')
    require(native['byteorder'] == 'little', 'unsupported source byte order')
    hashes = dict(native['files'])
    hashes['scripts/q3_production160_20261019.py'] = provenance['adapter']
    hashes['docs/protocols/CHAPTER2_CONFIRM160_EXECUTION_20261019.json'] = provenance['protocol']
    for path, sha in hashes.items():
        raw = subprocess.run(['git', 'show', source_commit + ':' + path], cwd=source_root,
                             check=True, capture_output=True).stdout
        require(digest(raw) == sha, 'source hash mismatch: ' + path)
    return hashes


def snapshot(raw, spec, contract, initial, parent=None):
    with np.load(io.BytesIO(raw), allow_pickle=False) as z:
        require(len(z.files) == 7 and set(z.files) == set(FIELDS) | {'counts', '_meta'},
                'snapshot array inventory')
        require(z['_meta'].dtype == np.uint8 and z['_meta'].ndim == 1, 'metadata shape')
        meta = load_json(z['_meta'].tobytes())
        arrays = {k: z[k] for k in z.files if k != '_meta'}
    require(set(meta) == {'task','current','master','contract_sha256','parent_payload_sha256',
                         'target_I','rng','payload_sha256'}, 'snapshot metadata inventory')
    h = hashlib.sha256(canonical({k: v for k, v in meta.items() if k != 'payload_sha256'}))
    for name in sorted(arrays):
        a = arrays[name]
        h.update(canonical([name, a.dtype.str, list(a.shape)]))
        h.update(a.tobytes())
    require(h.hexdigest() == meta['payload_sha256'], 'snapshot payload mismatch')
    plan = contract['plan']
    stage = 'prefix' if spec['stage'] == 'prefix' else 'fork'
    master = int.from_bytes(hashlib.sha256(
        f"{plan['namespace']}|{stage}|{spec['founder']}|{spec['visitor']}".encode()).digest()[:16], 'big')
    target = float(initial['alleles'][:, 1, :].mean())
    require(meta['task'] == spec and meta['current'] == spec['end'] and
            meta['contract_sha256'] == contract['contract_sha256'] and
            meta['master'] == master and meta['target_I'] == target, 'snapshot assignment mismatch')
    require(set(meta['rng']) == set(STREAMS), 'RNG registry mismatch')
    for state in meta['rng'].values():
        require(state['bit_generator'] == 'PCG64', 'RNG generator mismatch')
        probe = np.random.PCG64()
        probe.state = state  # validate representation, do not draw
    length = spec['end'] - spec['start'] + 1
    count = arrays['counts']
    require(count.dtype == np.dtype('<i8') and count.shape == (length,) and
            np.all((count >= 0) & (count <= 48)), 'invalid counts')
    for key in FIELDS:
        shape = (length, 48, 3, 2) if key in FIELDS[:3] else (length, 48)
        dtype = np.dtype('float64' if key == 'alleles' else 'bool' if key == 'mutation_flags' else 'int64')
        require(arrays[key].shape == shape and arrays[key].dtype == dtype, 'field shape/type')
    require(np.isfinite(arrays['alleles']).all(), 'nonfinite alleles')
    require(meta['parent_payload_sha256'] == (None if parent is None else parent[0]['payload_sha256']),
            'fork parent mismatch')
    ancestor = initial if parent is None else {
        k: parent[1][k][-1, :int(parent[1]['counts'][-1])] for k in FIELDS}
    require(int(count[0]) == len(ancestor['ids']), 'fork/founder count mismatch')
    for key in FIELDS:
        require(np.array_equal(arrays[key][0, :count[0]], ancestor[key]), 'fork/founder state mismatch')
    origin_values = initial['alleles'].ravel()
    upper, lower = [], []
    previous = None
    for i, size in enumerate(count):
        year = spec['start'] + i
        for key in FIELDS:
            require(not np.any(arrays[key][i, size:]), 'nonzero padded state')
        origins = arrays['allele_origin'][i, :size]
        values = arrays['alleles'][i, :size]
        require(np.all((origins >= 0) & (origins < 288)), 'origin outside founder')
        require(np.array_equal(values, origin_values[origins]), 'allele/origin mismatch')
        require(not np.any(arrays['mutation_flags'][i]), 'unexpected mutation')
        require(np.all(arrays['birth_years'][i, :size] == year) and
                np.array_equal(arrays['ids'][i, :size], np.arange(year * 48, year * 48 + size)),
                'native identity/birth mismatch')
        for loc in range(3):
            require(np.all((origins[:, loc, :] // 2) % 3 == loc), 'cross-locus origin')
            if previous is not None:
                require(set(origins[:, loc, :].ravel()) <= set(previous[:, loc, :].ravel()),
                        'new origin or nonabsorbing extinction')
        previous = origins
        upper.append(float(values[:, 1, :].max()) if size else None)
        lower.append(float(values[:, 2, :].min()) if size else None)
    return meta, arrays, upper, lower


def events(upper, target):
    loss = next((i for i, v in enumerate(upper) if v is not None and v < target - 1e-12), None)
    death = next((i for i, v in enumerate(upper) if v is None), None)
    return bool(loss is not None and (death is None or loss < death)), bool(
        death is not None and (loss is None or death < loss)), loss


def infer(g, occupancy):
    d = np.stack((g[:, :, 1] - g[:, :, 0],
        occupancy[:, :, 1, 1] - occupancy[:, :, 1, 0]
        - occupancy[:, :, 0, 1] + occupancy[:, :, 0, 0]), axis=-1).astype(float)
    nf, nv = d.shape[:2]
    means = d.mean(axis=(0, 1))
    row = d.mean(axis=1) - means
    col = d.mean(axis=0) - means
    residual = d - means - row[:, None, :] - col[None, :, :]
    var = (row**2).sum(axis=0)/nf**2 + (col**2).sum(axis=0)/nv**2 + (
        residual**2).sum(axis=(0, 1))/(nf*nv)**2
    critical = student_t.ppf(.9875, min(nf, nv)-1)
    endpoints = []
    for name, m, v in zip(('genetic_loss', 'survival_interaction'), means, var):
        lo, hi = float(m-critical*np.sqrt(v)), float(m+critical*np.sqrt(v))
        valid = bool(v > 0)
        endpoints.append(dict(name=name, estimate=float(m), variance=float(v),
            interval=[lo, hi] if valid else None,
            classification='degenerate_unresolved' if not valid else 'positive' if lo > 0 else
                           'negative' if hi < 0 else 'unresolved',
            exceeds_positive_margin=bool(valid and lo > .1),
            within_equivalence_band=bool(valid and lo >= -.1 and hi <= .1)))
    return dict(endpoints=endpoints, joint_positive=all(e['classification']=='positive' for e in endpoints),
                both_exceed_margin=all(e['exceeds_positive_margin'] for e in endpoints))


def close(actual, expected, label):
    if isinstance(expected, dict):
        require(isinstance(actual, dict) and set(actual) == set(expected), label + ' keys')
        for k, v in expected.items(): close(actual[k], v, label + '.' + k)
    elif isinstance(expected, list):
        require(isinstance(actual, list) and len(actual) == len(expected), label + ' length')
        for a, b in zip(actual, expected): close(a, b, label)
    elif isinstance(expected, float):
        require(type(actual) in (int, float) and np.isclose(actual, expected, rtol=1e-10, atol=1e-12), label)
    else:
        require(actual == expected and (type(expected) is not bool or type(actual) is bool), label)


def audit(root, *, technical=False, source_root=ROOT, source_commit=SOURCE_COMMIT):
    root = Path(root)
    shards = 1 if technical else 32
    names = {'SUMMARY160.json'} | {f'{prefix}-{i}.{ext}' for i in range(shards)
        for prefix, ext in [('raw-shard', 'zip'), ('seal', 'json'), ('hashes', 'txt')]}
    require(root.is_dir() and {p.name for p in root.iterdir()} == names and
            all(p.is_file() and not p.is_symlink() for p in root.iterdir()),
            'complete-only root inventory: missing/unexpected/nonregular asset')
    # Admit EVERY transport hash and seal before inspecting any scientific arrays.
    seals = []
    plan = expected_plan(technical)
    provenance = None
    hashes = None
    for i in range(shards):
        entries = {}
        for line in (root/f'hashes-{i}.txt').read_text().splitlines():
            sha, name = line.split()
            require(name not in entries, 'duplicate hash entry')
            entries[name] = sha
        require(set(entries) == {f'raw-shard-{i}.zip', f'seal-{i}.json'}, 'hash inventory')
        for name, sha in entries.items(): require(file_digest(root/name) == sha, 'asset checksum: '+name)
        seal = load_json((root/f'seal-{i}.json').read_bytes())
        require(set(seal) == {'contract','records','inventory','saved_states','unique_updates',
                             'complete','seal_sha256'}, 'seal schema')
        require(digest(canonical({k:v for k,v in seal.items() if k!='seal_sha256'})) ==
                seal['seal_sha256'], 'seal checksum')
        c = seal['contract']
        require(set(c) == {'plan','technical','shard','shards','provenance','contract_sha256'},
                'contract schema')
        require(digest(canonical({k:v for k,v in c.items() if k!='contract_sha256'})) ==
                c['contract_sha256'], 'contract checksum')
        require(c['plan'] == plan and type(c['technical']) is bool and c['technical'] == technical
                and type(c['shard']) is int and c['shard'] == i and c['shards'] == shards,
                'contract plan/shard mismatch')
        if provenance is None:
            provenance = c['provenance']
            hashes = verify_sources(provenance, source_root, source_commit)
            if not technical:
                runtime = provenance['native']
                require(runtime['python'].startswith('3.12.') and runtime['numpy'] == '2.2.6'
                        and runtime['scipy'] == '1.15.3', 'production runtime differs from pinned workflow')
        require(c['provenance'] == provenance, 'mixed provenance/runtime')
        seals.append(seal)
    summary = load_json((root/'SUMMARY160.json').read_bytes())
    nf, nv = len(plan['founders']), len(plan['visitors'])
    g = np.zeros((nf,nv,2), dtype=int)
    occupancy = np.zeros((nf,nv,2,2), dtype=int)
    sensitivity = np.zeros((len(EPS),nf,nv,2), dtype=int)
    counts = {}
    for shard, seal in enumerate(seals):
        cells = [(fi,vi,f,v) for fi,f in enumerate(plan['founders'])
                 for vi,v in enumerate(plan['visitors']) if (fi*nv+vi)%shards == shard]
        expected_files = {f'{f}_{v}_{p}_{s}.npz' for _,_,f,v in cells
                          for p in plan['policies'] for s in ('prefix','B8','B4p5')}
        require(set(seal['inventory']) == expected_files and seal['complete'] is True and
                seal['saved_states'] == 256*len(cells) and seal['unique_updates'] == 250*len(cells),
                'seal inventory/count mismatch')
        records = {(r['founder'],r['visitor']):r for r in seal['records']}
        require(len(records) == len(seal['records']) == len(cells) and
                set(records) == {(f,v) for _,_,f,v in cells}, 'seal crossing inventory')
        with zipfile.ZipFile(root/f'raw-shard-{shard}.zip') as z:
            inventory = {'RUN.json','ARCHIVE_MANIFEST.json'} | {'states/'+s for s in expected_files}
            require(len(z.namelist()) == len(inventory) and set(z.namelist()) == inventory,
                    'archive member inventory')
            manifest = load_json(z.read('ARCHIVE_MANIFEST.json'))
            require(set(manifest) == inventory-{'ARCHIVE_MANIFEST.json'}, 'archive manifest inventory')
            run = z.read('RUN.json')
            require(digest(run) == manifest['RUN.json'] and load_json(run) == seal['contract'],
                    'archive contract mismatch')
            for fi,vi,f,v in cells:
                initial = founder_arrays(f)
                target = float(initial['alleles'][:,1,:].mean())
                r = records[f,v]
                require(r['target_I'] == target and len(r['arms']) == 4, 'record target/arms')
                recorded = {(a['policy'],a['stage']):a for a in r['arms']}
                require(set(recorded) == {(p,s) for p in plan['policies'] for s in ('B8','B4p5')},
                        'record arm inventory')
                for pi,policy in enumerate(plan['policies']):
                    prefix = None
                    for stage,budget,start,end in [('prefix',8.,0,35),('B8',8.,35,80),('B4p5',4.5,35,80)]:
                        filename = f'{f}_{v}_{policy}_{stage}.npz'
                        raw = z.read('states/'+filename)
                        require(digest(raw) == manifest['states/'+filename] ==
                                seal['inventory'][filename]['sha256'], 'snapshot transport checksum')
                        spec = dict(founder=f,visitor=v,policy=policy,stage=stage,budget=budget,start=start,end=end)
                        data = snapshot(raw,spec,seal['contract'],initial,prefix)
                        require(data[0]['payload_sha256'] == seal['inventory'][filename]['payload'],
                                'seal payload mismatch')
                        if stage == 'prefix':
                            prefix = data
                            continue
                        upper, lower = prefix[2]+data[2][1:], prefix[3]+data[3][1:]
                        ev = [events(upper,target-eps) for eps in EPS]
                        alive = upper[-1] is not None
                        access = [bool(alive and upper[-1]>=target-eps-1e-12) for eps in EPS]
                        arm = dict(policy=policy,stage=stage,alive=alive,genetic_first=[e[0] for e in ev],
                            extinction_first=[e[1] for e in ev],first_loss=[e[2] for e in ev],
                            final_access=access,max_I=upper,min_A=lower)
                        close(recorded[policy,stage],arm,'raw/seal endpoint')
                        bi = 0 if stage=='B8' else 1
                        occupancy[fi,vi,pi,bi] = alive
                        if bi == 0:
                            g[fi,vi,pi] = ev[0][0]
                            sensitivity[:,fi,vi,pi] = [e[0] for e in ev]
                        out = counts.setdefault(policy+'_'+stage, dict(alive=0,alive_accessible=0,
                            genetic_first=0,extinction_first=0))
                        for key,val in [('alive',alive),('alive_accessible',access[0]),
                                        ('genetic_first',ev[0][0]),('extinction_first',ev[0][1])]:
                            out[key] += int(val)
    expected = dict(status='TECHNICAL' if technical else 'COMPLETE_MODEL_CONDITIONAL_CONFIRMATION',
        independent_axes=[nf,nv],crossings=nf*nv,unique_updates=250*nf*nv,files=6*nf*nv,
        saved_states=256*nf*nv,shard_seals=[s['seal_sha256'] for s in sorted(seals,
            key=lambda s:f"seal-{s['contract']['shard']}.json")],arms=counts,
        genetic_loss_inputs=g.tolist(),occupancy_inputs=occupancy.tolist(),
        epsilon_descriptive=[dict(epsilon=eps,fixed=int(sensitivity[i,:,:,0].sum()),
            evolving=int(sensitivity[i,:,:,1].sum())) for i,eps in enumerate(EPS)],
        actual_restoration_tested=False,biological_SESOI_endorsed=False)
    require(set(summary) == set(expected)|{'primary'}, 'summary inventory')
    for key,value in expected.items(): close(summary[key],value,'summary.'+key)
    independent = infer(g,occupancy)
    for key,value in independent.items(): close(summary['primary'][key],value,'inference.'+key)
    for key,value in dict(method='pigeonhole_variance_t_candidate',independent_axes=[nf,nv],
        familywise_alpha=.05,marginal_confidence=.975,df=min(nf,nv)-1,
        proposed_margin=.1,execution_authorized=False).items():
        close(summary['primary'][key],value,'inference contract.'+key)
    return dict(status='PASS_INDEPENDENT_RAW_ARITHMETIC_AUDIT',technical=technical,
        source_commit=source_commit,source_files=hashes,crossings=nf*nv,
        raw_files=6*nf*nv,saved_states=256*nf*nv,summary_sha256=file_digest(root/'SUMMARY160.json'),
        primary=independent,epsilon_descriptive=expected['epsilon_descriptive'],
        limits=['No independently implemented biological transition replay.',
                'Founder construction and arithmetic independently reimplemented; NumPy RNG is shared.',
                'Transport hashes establish consistency, not external publication authenticity.',
                'Conditional t-reference inference has no universal finite-sample coverage guarantee.',
                'No actual restoration experiment or biological SESOI endorsement.'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--technical',action='store_true')
    parser.add_argument('--source-root',type=Path,default=ROOT)
    parser.add_argument('--source-commit',default=SOURCE_COMMIT)
    args = parser.parse_args()
    require(not args.out.exists(), 'refuse output overwrite')
    result = audit(args.root,technical=args.technical,source_root=args.source_root,source_commit=args.source_commit)
    with args.out.open('xb') as handle: handle.write(canonical(result)+b'\n')
    print(json.dumps(result,sort_keys=True))
