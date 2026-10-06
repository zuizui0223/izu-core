"""Check every exported rate estimate against stored evidence, independent of plotting."""
from pathlib import Path
import csv
import hashlib
import json
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def main():
    selection = ROOT / 'outputs/figures/model3_selection_process_20261005'
    with np.load(ROOT / 'outputs/model3_isolation_selection_gradient_20261005/gradients.npz') as source:
        a = {name: source[name] for name in ['snapshots','distances','states','gradients','intervals']}
        rows = list(csv.DictReader((selection / 'plotted_values.csv').open(encoding='utf-8')))
        assert len(rows) == 2340
        seen = set()
        t = int(np.flatnonzero(a['snapshots'] == 400)[0])
        for r in rows:
            si, trait = int(r['setting_index']), int(r['trait_index'])
            di = int(np.flatnonzero(a['distances'] == float(r['distance']))[0])
            state = [float(r[x]) for x in ['matching', 'investment', 'capacity']]
            pi = int(np.flatnonzero(np.all(a['states'] == state, axis=1))[0])
            key = (si, trait, di, pi); assert key not in seen; seen.add(key)
            assert float(r['established_types_per_update']) == .24 * np.exp(-a['distances'][di])
            np.testing.assert_allclose(float(r['mean']), a['gradients'][si,di,:,t,pi,trait].mean(), rtol=0, atol=1e-14)
            np.testing.assert_array_equal([float(r['ci_low']),float(r['ci_high'])], a['intervals'][si,di,t,pi,trait])
    folder = ROOT / 'outputs/figures/model3_replenishment_evolution_20261005'
    summary = json.loads((ROOT / 'data/results/model3_replenishment_evolution_summary_20261005.json').read_text())
    rows = list(csv.DictReader((folder / 'plotted_endpoints.csv').open(encoding='utf-8')))
    assert len(rows) == 468
    seen = set()
    for r in rows:
        key = (r['setting'],r['contrast'],int(r['update']),float(r['replenishment']),r['trait'])
        assert key not in seen; seen.add(key)
        original = next(e for e in summary['endpoints'] if (e['setting'],e['contrast'],e['update'],e['replenishment']) == key[:4])
        values = original['traits'][r['trait']]
        np.testing.assert_array_equal([float(r['mean']),float(r['ci_low']),float(r['ci_high'])], [values['mean'],*values['pointwise_interval']])
        assert int(r['occupied_of512']) == original['occupied_cases']
        assert int(r['paired_of512']) == original['paired_cases']
    assets = [selection/'selection_process.pdf',folder/'all_endpoints.pdf',folder/'all_order_thresholds.pdf']
    receipt = {'status':'all_exported_estimates_match_sources','selection_means':2340,
               'evolution_estimates':468,'selection_axis':'0.24 exp(-d), successful visitor establishment per update',
               'files':[{'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in assets],
               'scope':'CSV-to-evidence agreement; primary rendered pages reviewed separately; no claim of universal biological validity.'}
    (ROOT/'data/results/model3_rate_figures_verified_20261005.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
