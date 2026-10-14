import hashlib
import importlib
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from test_q3_triangle_contract_20261014 import cases, records


@pytest.mark.parametrize('fail_shard', [None, 6])
def test_publication_streams_one_shard_and_never_publishes_partial_campaign(tmp_path, monkeypatch, fail_shard):
    m = importlib.import_module('publish_q3_triangle_campaign_20261014')
    cs = cases();rr = records(cs)
    uploaded, commands = {}, []
    def cli(args):
        commands.append(args)
        if args[:2] == ['run', 'download']:
            folder = Path(args[args.index('--dir')+1]);assert not list(folder.iterdir())
            shard = int(args[args.index('--name')+1].split('-')[-2])
            raw = f'archive-{shard}'.encode();name = f'Q3_TRIANGLE_SHARD_{shard:02d}.zip'
            (folder/name).write_bytes(raw)
            (folder/f'SHARD_{shard:02d}_RECEIPT.json').write_text(json.dumps(dict(shard=shard,
                run_id='123', execution_sha256='d'*64, archive_sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))))
        elif args[:2] == ['release', 'upload']:
            p = Path(args[3]);uploaded[p.name] = p.read_bytes()
        elif args[:2] == ['release', 'download']:
            name = args[args.index('--pattern')+1]
            folder = Path(args[args.index('--dir')+1]);assert not list(folder.iterdir())
            (folder/name).write_bytes(uploaded[name])
        elif args[:2] == ['release', 'view']:
            return json.dumps(dict(assets=[dict(name=n, size=len(b)) for n,b in uploaded.items()]))
        elif args[0] == 'api':
            return json.dumps(dict(object=dict(sha='b'*40)))
        return ''
    def verify(path, plan, execution_sha, run_id, guard):
        shard = int(path.stem[-2:])
        if shard == fail_shard:
            raise ValueError('injected incomplete raw shard')
        return dict(shard=shard, run_id='123', execution_sha256='d'*64, triplets=488, trajectories=1464,
                    production_updates=185760, replay_updates=185760, fixture_updates=4 if shard == 0 else 0,
                    reserved_native_updates=371524 if shard == 0 else 371520), [r for r in rr if shard*8 <= r['replicate'] < (shard+1)*8]
    monkeypatch.setattr(m, 'verify_shard', verify)
    if fail_shard is None:
        result = m.publish_campaign(tmp_path, dict(cases=cs), 'd'*64, dict(run_id='123', head='b'*40), cli, lambda:None)
        assert result['native_updates'] == 6687364
        assert len(uploaded) == 21
        manifest = json.loads(uploaded['CAMPAIGN_MANIFEST.json'])
        assert manifest['cumulative_accounting']['native_updates'] == 6687368
        assert manifest['prior_technical_hold']['run_id'] == 38528315875
        assert commands[-1][:2] == ['release', 'edit'] and '--draft=false' in commands[-1]
    else:
        with pytest.raises(ValueError, match='incomplete raw'):
            m.publish_campaign(tmp_path, dict(cases=cs), 'd'*64, dict(run_id='123', head='b'*40), cli, lambda:None)
        assert not any(c[:2] == ['release', 'edit'] for c in commands)
