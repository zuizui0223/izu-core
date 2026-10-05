"""Source-linked complete rate tables and bounded interpretation; no simulation."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def main():
    source = ROOT / 'data/results/model3_replenishment_evolution_summary_20261005.json'
    s = json.loads(source.read_text())
    receipt = json.loads((ROOT / 'data/results/model3_replenishment_readout_verified_20261005.json').read_text())
    assert receipt['summary_sha256'] == hashlib.sha256(source.read_bytes()).hexdigest()
    assert s['verified_cases'] == 13312
    text = ['# Realized evolution across continuous visitor replenishment', '',
        '## Design and interpretation', '',
        'This exploratory extension varies successful visitor establishment per reproductive update across 13 rates (lambda = 0.24 exp(-d)). The coordinate d is not calibrated geographic distance. Plant capacity remains 48; this does not represent island area. A common external visitor source supplies independent populations, with no stepping-stone network or plant immigration. Reproduction, inheritance, disappearance, source pool and founders remain unchanged.', '',
        'Each of two joint reproductive settings has 64 visitor histories and eight demographic repeats per rate. Mutation probability is 0.01, mutation SD 0.05, and the horizon is 1,000 uncalibrated reproductive updates. The 11 intermediate rates add 11,264 cases to 2,048 reused endpoint cases. Endpoints and earlier local-selection results were known when the extension was declared; its design and readout were recorded before inspecting intermediate-rate outcomes. This is not a restart of the stopped high-resolution deterministic/PDE comparison.', '',
        '## Findings', '',
        'In the delayed-selfing, capacity-cost setting, sampled mean investment decline at update 1,000 increases as replenishment falls. Capacity already increases at the highest rate: replenishment limitation intensifies a response rather than initiating all selfing-capacity evolution. The prior-selfing, zero-capacity-cost setting shows large founder-relative changes even at high supply and a much smaller additional gradient. The settings differ jointly in timing and cost; their contrast does not isolate either factor.', '',
        'Founder-relative order and order of additional divergence answer different questions. At the lowest rate and the primary 0.05 sustained-change threshold, capacity precedes investment in 51/64 delayed histories and 38/64 prior histories; the others are within five updates. For the delayed setting, the additional divergence relative to high replenishment reaches the investment threshold first in 32/64 histories, capacity first in 10, within five updates in 20, and investment alone in two. Thus capacity-first evolution is not evidence that the earliest additional effect of replenishment limitation is capacity change. Threshold timing is neither infinitesimal onset nor causal mediation.', '',
        'No fitted transition point, natural distance threshold, universal chronological order or robustness across all other parameters is claimed. The fixed-capacity intervention and finite/deterministic comparisons remain separate cohorts. The three declared change thresholds and both contrasts are retained.', '',
        '## Complete endpoint and primary-order tables', '',
        'All values below are at update 1,000. Intervals are pointwise descriptive 95% bootstrap intervals over 64 histories (5,000 resamples), not simultaneous bands or natural-population prevalence. Investment is signed change, so negative means reduced investment. Capacity is autonomous-selfing ability, not realized selfing rate. Counts include censored categories.', '']
    cats = ['assurance_first', 'near_simultaneous', 'investment_first', 'assurance_only', 'investment_only', 'neither']
    for setting in ['assurance_cost', 'prior_selfing']:
        for contrast in ['from_founders', 'minus_high_supply']:
            text += [f'### {setting}: {contrast}', '',
                '| Establishment rate | Investment change [95% interval] | Capacity change [95% interval] | Occupied / 512 | Paired / 512 | C first / tie / I first / C only / I only / neither |',
                '|---|---|---|---|---|---|']
            rows = sorted((r for r in s['endpoints'] if r['setting'] == setting and r['contrast'] == contrast and r['update'] == 1000), key=lambda r: -r['replenishment'])
            assert len(rows) == 13
            for row in rows:
                event = next(e for e in s['temporal_order'] if e['setting'] == setting and e['contrast'] == contrast and e['distance'] == row['distance'] and e['threshold'] == .05)
                values = []
                for trait in ['investment', 'capacity']:
                    v = row['traits'][trait]; lo, hi = v['pointwise_interval']
                    values.append(f"{v['mean']:+.5f} [{lo:+.5f}, {hi:+.5f}]")
                counts = [event['counts'].get(c, 0) for c in cats]
                assert sum(counts) == 64
                text.append(f"| {row['replenishment']:.6f} | {values[0]} | {values[1]} | {row['occupied_cases']} | {row['paired_cases']} | {' / '.join(map(str, counts))} |")
            text.append('')
    text += ['## Evidence and complete companion results', '',
        '- Summary: `data/results/model3_replenishment_evolution_summary_20261005.json` (all three traits, updates 200/400/1,000, contrasts, thresholds and event records).',
        '- Raw verification: `data/results/model3_replenishment_raw_curves_verified_20261005.json`: 13,312 cases and 9,993,984 reconstructed trait coordinates, exact agreement.',
        '- Readout verification: `data/results/model3_replenishment_readout_verified_20261005.json`: 9,984 crossing records and 156 endpoint rows, exact agreement.',
        '- Figures: `outputs/figures/model3_replenishment_evolution_20261005/all_endpoints.pdf` (six pages), `all_order_thresholds.pdf` (three pages), and `plotted_endpoints.csv` (468 estimates).',
        '- Arrays: `outputs/model3_replenishment_evolution_20261005/evolution_curves.npz`.',
        f"- Summary SHA256: `{hashlib.sha256(source.read_bytes()).hexdigest()}`.",
        f"- Array SHA256: `{s['array_sha256']}`.", '',
        'These checks establish data-to-readout consistency, not independent replication of the biological simulator. All declared endpoint conditions have 512 occupied populations; survival between endpoints is available in the array archive. No extinct phenotype is imputed.', '']
    target = ROOT / 'docs/MODEL3_REPLENISHMENT_EVOLUTION_RESULTS_20261005.md'
    target.write_text('\n'.join(text), encoding='utf-8')
    print(target)


if __name__ == '__main__':
    main()
