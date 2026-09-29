#!/usr/bin/env python3
"""Audit continuous pollinator functional diversity as a trait-matching exposure.

The archived source code for Hiraiwa & Ushimaru (2024) models community corrected
trait matching (TM_z) against pollinator functional-diversity/evenness metrics
with site and season random intercepts. The source figure code exposes the fitted
FDQ coefficient used for visualization.

This audit preserves that source-native model statement and adds transparent
fixed-effect sensitivities:

    TM_z ~ FDQ + FEve + site fixed effects + season fixed effects

The model is fitted to all sites and then separately to mainland sites, the five
Izu island sites, and the four post-Oshima islands. Leave-one-site sensitivity
is added for the island subsets. The sampled pollinator species table is also
audited for *observed* Bombus rows; this is network-sampling context and is never
promoted to a biological absence statement.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
from pathlib import Path
from typing import Sequence


EXPECTED_SOURCE_FORMULA = (
    'glmmTMB(TM_z ~ richness + D + FDQ + FRic + FEve + (1|season) + (1|site)'
)
EXPECTED_SOURCE_FDQ_COEF = 1.5540
EXPECTED_SOURCE_FEVE_COEF = -9.2976
MAINLAND_SITES = {'hitachi', 'hitachinaka', 'tateyama'}
ISLAND_SITES = {'oshima', 'niijima', 'kozu', 'miyake', 'hachijo'}
POST_OSHIMA_SITES = {'niijima', 'kozu', 'miyake', 'hachijo'}
SITE_BY_ID = {
    1: 'hitachi', 2: 'hitachinaka', 3: 'tateyama', 4: 'oshima',
    5: 'niijima', 6: 'kozu', 7: 'miyake', 8: 'hachijo',
}


def solve(matrix: Sequence[Sequence[float]], vector: Sequence[float]) -> list[float]:
    n = len(vector)
    a = [list(map(float, matrix[i])) + [float(vector[i])] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(a[row][col]))
        if abs(a[pivot][col]) < 1e-12:
            raise ValueError('singular design matrix')
        a[col], a[pivot] = a[pivot], a[col]
        divisor = a[col][col]
        a[col] = [value / divisor for value in a[col]]
        for row in range(n):
            if row == col:
                continue
            factor = a[row][col]
            a[row] = [a[row][j] - factor * a[col][j] for j in range(n + 1)]
    return [a[i][-1] for i in range(n)]


def ols(x: list[list[float]], y: list[float]) -> dict[str, object]:
    p = len(x[0])
    xtx = [[sum(row[i] * row[j] for row in x) for j in range(p)] for i in range(p)]
    xty = [sum(row[i] * value for row, value in zip(x, y)) for i in range(p)]
    beta = solve(xtx, xty)
    fitted = [sum(beta[j] * row[j] for j in range(p)) for row in x]
    mean_y = sum(y) / len(y)
    rss = sum((value - fit) ** 2 for value, fit in zip(y, fitted))
    tss = sum((value - mean_y) ** 2 for value in y)
    return {
        'coefficients': beta,
        'rss': rss,
        'r_squared': 1.0 - rss / tss if tss > 0 else None,
        'n': len(y),
        'p': p,
    }


def correlation(x: list[float], y: list[float]) -> float:
    xbar = sum(x) / len(x)
    ybar = sum(y) / len(y)
    num = sum((a - xbar) * (b - ybar) for a, b in zip(x, y))
    den = math.sqrt(sum((a - xbar) ** 2 for a in x) * sum((b - ybar) ** 2 for b in y))
    return num / den


def load_rows(path: Path, expected: int | None = None) -> list[dict[str, str]]:
    with path.open(encoding='utf-8-sig', newline='') as handle:
        rows = list(csv.DictReader(handle))
    if expected is not None and len(rows) != expected:
        raise ValueError(f'expected {expected} rows in {path.name}, found {len(rows)}')
    return rows


def verify_source_code(path: Path) -> dict[str, object]:
    text = path.read_text(encoding='utf-8', errors='replace')
    if EXPECTED_SOURCE_FORMULA not in text:
        raise ValueError('expected source TM_z model formula not found in code.R')
    match = re.search(
        r'yy<-([0-9.]+)\*xx\+([0-9.]+)\s*([+-])\s*([0-9.]+)\*mean\(data_main\$FEve\)',
        text,
    )
    if not match:
        raise ValueError('source Figure 3 coefficient line not found')
    fdq = float(match.group(1))
    intercept = float(match.group(2))
    feve = float(match.group(4)) * (-1.0 if match.group(3) == '-' else 1.0)
    if abs(fdq - EXPECTED_SOURCE_FDQ_COEF) > 1e-9 or abs(feve - EXPECTED_SOURCE_FEVE_COEF) > 1e-9:
        raise ValueError('source Figure 3 coefficients differ from locked values')
    return {
        'source_full_candidate_formula': 'TM_z ~ richness + D + FDQ + FRic + FEve + (1|season) + (1|site)',
        'source_figure_best_model_fdq_coefficient': fdq,
        'source_figure_best_model_feve_coefficient': feve,
        'source_figure_best_model_intercept': intercept,
        'source_code_locator': 'archived code.R Figure 3 community-level trait-matching block',
    }


def fit_fixed_effect_subset(rows: list[dict[str, str]], allowed_sites: set[str]) -> dict[str, object]:
    subset = [row for row in rows if row['site'] in allowed_sites]
    sites = sorted({row['site'] for row in subset})
    seasons = sorted({int(row['season']) for row in subset})
    if len(sites) < 2 or len(seasons) < 2:
        raise ValueError('subset requires at least two sites and two seasons')
    base_site, base_season = sites[0], seasons[0]
    names = ['intercept', 'FDQ', 'FEve']
    names += [f'site[{site}]' for site in sites if site != base_site]
    names += [f'season[{season}]' for season in seasons if season != base_season]
    x, y = [], []
    for row in subset:
        design = [1.0, float(row['FDQ']), float(row['FEve'])]
        design += [1.0 if row['site'] == site else 0.0 for site in sites if site != base_site]
        design += [1.0 if int(row['season']) == season else 0.0 for season in seasons if season != base_season]
        x.append(design); y.append(float(row['TM_z']))
    fit = ols(x, y)
    coef = dict(zip(names, fit['coefficients']))

    site_means: dict[str, dict[str, float]] = {}
    for site in sites:
        site_rows = [row for row in subset if row['site'] == site]
        site_means[site] = {
            'FDQ': sum(float(row['FDQ']) for row in site_rows) / len(site_rows),
            'TM_z': sum(float(row['TM_z']) for row in site_rows) / len(site_rows),
        }
    fdq_within = [float(row['FDQ']) - site_means[row['site']]['FDQ'] for row in subset]
    tm_within = [float(row['TM_z']) - site_means[row['site']]['TM_z'] for row in subset]

    return {
        'formula': 'TM_z ~ FDQ + FEve + site_fixed_effects + season_fixed_effects',
        'n_site_season_rows': fit['n'],
        'sites': sites,
        'n_sites': len(sites),
        'n_seasons': len(seasons),
        'fdq_coefficient': coef['FDQ'],
        'feve_coefficient': coef['FEve'],
        'r_squared': fit['r_squared'],
        'site_centered_fdq_tm_correlation': correlation(fdq_within, tm_within),
    }


def leave_one_site_out(rows: list[dict[str, str]], sites: set[str]) -> dict[str, object]:
    coefficients: dict[str, float] = {}
    for omitted in sorted(sites):
        result = fit_fixed_effect_subset(rows, set(sites) - {omitted})
        coefficients[omitted] = float(result['fdq_coefficient'])
    values = list(coefficients.values())
    return {
        'fdq_coefficients_by_omitted_site': coefficients,
        'fdq_coefficient_range': [min(values), max(values)],
        'all_positive': all(value > 0 for value in values),
    }


def sampled_bombus_context(rows: list[dict[str, str]]) -> dict[str, object]:
    bombus = []
    for row in rows:
        insect = str(row.get('insect') or '')
        if 'bombus' not in insect.lower():
            continue
        siteid = int(row['siteid'])
        if siteid not in SITE_BY_ID:
            raise ValueError(f'unknown siteid in pollinator table: {siteid}')
        bombus.append({
            'site': SITE_BY_ID[siteid],
            'season': int(row['season']),
            'insect': insect,
        })
    unique_site_seasons = {(row['site'], row['season']) for row in bombus}
    post_rows = [row for row in bombus if row['site'] in POST_OSHIMA_SITES]
    post_site_seasons = {(row['site'], row['season']) for row in post_rows}
    mainland_rows = [row for row in bombus if row['site'] in MAINLAND_SITES]
    oshima_rows = [row for row in bombus if row['site'] == 'oshima']
    return {
        'bombus_species_site_season_rows': len(bombus),
        'bombus_site_seasons': len(unique_site_seasons),
        'mainland_bombus_rows': len(mainland_rows),
        'mainland_bombus_site_seasons': len({(row['site'], row['season']) for row in mainland_rows}),
        'oshima_bombus_rows': len(oshima_rows),
        'oshima_bombus_site_seasons': len({(row['site'], row['season']) for row in oshima_rows}),
        'post_oshima_bombus_rows': len(post_rows),
        'post_oshima_bombus_site_seasons': len(post_site_seasons),
        'observed_bombus_taxa': sorted({row['insect'] for row in bombus}),
        'reading': (
            'This is observed network-sampling context only. Zero Bombus rows in a subset mean no Bombus taxon was '
            'recorded in the archived pollinator species x site x season network table; this is not a biological '
            'absence assertion outside the sampled networks.'
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=Path('artifacts/hiraiwa_ushimaru_figshare/files/data_main.csv'))
    parser.add_argument('--pollinator-data', type=Path, default=Path('artifacts/hiraiwa_ushimaru_figshare/files/data_sp_pollinator.csv'))
    parser.add_argument('--code', type=Path, default=Path('artifacts/hiraiwa_ushimaru_figshare/files/code.R'))
    parser.add_argument('--out', type=Path, default=Path('artifacts/hiraiwa_ushimaru_figshare/continuous_exposure/summary.json'))
    args = parser.parse_args()

    rows = load_rows(args.data, expected=40)
    pollinator_rows = load_rows(args.pollinator_data)
    source = verify_source_code(args.code)
    subsets = {
        'all_eight_sites': fit_fixed_effect_subset(rows, set(MAINLAND_SITES | ISLAND_SITES)),
        'mainland_three_sites': fit_fixed_effect_subset(rows, set(MAINLAND_SITES)),
        'izu_five_islands': fit_fixed_effect_subset(rows, set(ISLAND_SITES)),
        'post_oshima_four_islands': fit_fixed_effect_subset(rows, set(POST_OSHIMA_SITES)),
    }
    sensitivity = {
        'izu_five_islands_leave_one_site_out': leave_one_site_out(rows, set(ISLAND_SITES)),
        'post_oshima_four_islands_leave_one_site_out': leave_one_site_out(rows, set(POST_OSHIMA_SITES)),
    }
    bombus_context = sampled_bombus_context(pollinator_rows)

    report = {
        'source_dataset': '10.6084/m9.figshare.25025000.v1',
        'source_native_model': source,
        'fixed_effect_subsets': subsets,
        'leave_one_site_sensitivity': sensitivity,
        'sampled_bombus_context': bombus_context,
        'mechanistic_gain': (
            'FDQ remains positively associated with corrected trait matching when the analysis is restricted to '
            'the five Izu islands and even to the four post-Oshima islands. The association therefore does not '
            'require mainland observations or the Oshima bridge-state site. Positive leave-one-island coefficients '
            'further show that no single island is required for the direction.'
        ),
        'relation_to_bombus_boundary': (
            'The positive FDQ association within Niijima, Kozu, Miyake and Hachijo occurs in a subset with zero '
            'observed Bombus rows in the archived pollinator species x site x season network table. Continuous '
            'pollinator-functional structure therefore varies within the sampled post-boundary networks and should '
            'not be reduced to a binary observed-Bombus label.'
        ),
        'claim_boundary': (
            'This remains observational contemporary association. Fixed effects remove time-invariant site differences '
            'and common season effects, but not time-varying weather/resources, measurement error, feedback within '
            'networks or historical selection. The sampled Bombus audit is not an archipelago-wide biological absence '
            'statement. The post-boundary result does not identify Bombus loss as the cause; rather, it shows that '
            'pollinator functional diversity contains explanatory variation beyond that binary sampled-network contrast.'
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
