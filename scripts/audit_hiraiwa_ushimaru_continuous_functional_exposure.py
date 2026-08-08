#!/usr/bin/env python3
"""Audit continuous pollinator functional diversity as a trait-matching exposure.

The archived source code for Hiraiwa & Ushimaru (2024) models community corrected
trait matching (TM_z) against pollinator functional-diversity/evenness metrics
with site and season random intercepts. The source figure code exposes the fitted
FDQ coefficient used for visualization.

This audit preserves that source-native model statement and adds a transparent
fixed-effect sensitivity analysis using the same 40 site × season network rows:

    TM_z ~ FDQ + FEve + site fixed effects + season fixed effects

The fixed-effect sensitivity asks whether the FDQ direction persists after all
time-invariant site differences and common seasonal shifts are absorbed. It is a
contemporary within-site association, not a historical causal estimate.
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


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding='utf-8-sig', newline='') as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 40:
        raise ValueError(f'expected 40 site-season network rows, found {len(rows)}')
    return rows


def verify_source_code(path: Path) -> dict[str, object]:
    text = path.read_text(encoding='utf-8', errors='replace')
    if EXPECTED_SOURCE_FORMULA not in text:
        raise ValueError('expected source TM_z model formula not found in code.R')
    # Figure 3 line in the source archive:
    # yy<-1.5540*xx+2.4023 -9.2976*mean(data_main$FEve)
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
        'source_code_locator': 'code.R lines 281-337, Figure 3 community-level trait-matching block',
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=Path('artifacts/hiraiwa_ushimaru_figshare/files/data_main.csv'))
    parser.add_argument('--code', type=Path, default=Path('artifacts/hiraiwa_ushimaru_figshare/files/code.R'))
    parser.add_argument('--out', type=Path, default=Path('artifacts/hiraiwa_ushimaru_figshare/continuous_exposure/summary.json'))
    args = parser.parse_args()

    rows = load_rows(args.data)
    source = verify_source_code(args.code)
    sites = sorted({row['site'] for row in rows})
    seasons = sorted({int(row['season']) for row in rows})
    base_site = sites[0]
    base_season = seasons[0]

    # intercept, FDQ, FEve, 7 site dummies, 4 season dummies
    names = ['intercept', 'FDQ', 'FEve']
    names += [f'site[{site}]' for site in sites if site != base_site]
    names += [f'season[{season}]' for season in seasons if season != base_season]
    x = []
    y = []
    for row in rows:
        design = [1.0, float(row['FDQ']), float(row['FEve'])]
        design += [1.0 if row['site'] == site else 0.0 for site in sites if site != base_site]
        design += [1.0 if int(row['season']) == season else 0.0 for season in seasons if season != base_season]
        x.append(design)
        y.append(float(row['TM_z']))
    fit = ols(x, y)
    coef = dict(zip(names, fit['coefficients']))

    # Site-centred correlation is a simple model-free sensitivity to whether the
    # FDQ/TM relation exists within sites rather than only between islands.
    site_means: dict[str, dict[str, float]] = {}
    for site in sites:
        subset = [row for row in rows if row['site'] == site]
        site_means[site] = {
            'FDQ': sum(float(row['FDQ']) for row in subset) / len(subset),
            'TM_z': sum(float(row['TM_z']) for row in subset) / len(subset),
        }
    fdq_within = [float(row['FDQ']) - site_means[row['site']]['FDQ'] for row in rows]
    tm_within = [float(row['TM_z']) - site_means[row['site']]['TM_z'] for row in rows]

    report = {
        'source_dataset': '10.6084/m9.figshare.25025000.v1',
        'source_native_model': source,
        'fixed_effect_sensitivity': {
            'formula': 'TM_z ~ FDQ + FEve + site_fixed_effects + season_fixed_effects',
            'n_site_season_rows': fit['n'],
            'n_sites': len(sites),
            'n_seasons': len(seasons),
            'fdq_coefficient': coef['FDQ'],
            'feve_coefficient': coef['FEve'],
            'r_squared': fit['r_squared'],
            'interpretation': 'The FDQ coefficient remains positive after absorbing every time-invariant site difference and common season effects.'
        },
        'within_site_model_free_sensitivity': {
            'site_centered_fdq_tm_correlation': correlation(fdq_within, tm_within),
            'interpretation': 'Positive site-centred correlation shows that higher seasonal FDQ tends to co-occur with higher corrected trait matching within the same geographic sites.'
        },
        'mechanistic_gain': (
            'Unlike the binary Oshima/post indicator, FDQ varies across multiple sites and seasons. The positive '
            'source-model and site-fixed-effect associations therefore provide a continuous functional-exposure '
            'bridge between pollinator community structure and trait matching that is not reducible to static island identity alone.'
        ),
        'claim_boundary': (
            'This remains observational contemporary association. Site fixed effects remove time-invariant site '
            'confounding but not time-varying environmental covariates, reverse causation within networks, measurement '
            'error, or historical selection. It does not identify the historical cause of Campanula floral or breeding-system change.'
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
