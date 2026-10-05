# Realized evolution across continuous visitor replenishment

## Design and interpretation

This exploratory extension varies successful visitor establishment per reproductive update across 13 rates (lambda = 0.24 exp(-d)). The coordinate d is not calibrated geographic distance. Plant capacity remains 48; this does not represent island area. A common external visitor source supplies independent populations, with no stepping-stone network or plant immigration. Reproduction, inheritance, disappearance, source pool and founders remain unchanged.

Each of two joint reproductive settings has 64 visitor histories and eight demographic repeats per rate. Mutation probability is 0.01, mutation SD 0.05, and the horizon is 1,000 uncalibrated reproductive updates. The 11 intermediate rates add 11,264 cases to 2,048 reused endpoint cases. Endpoints and earlier local-selection results were known when the extension was declared; its design and readout were recorded before inspecting intermediate-rate outcomes. This is not a restart of the stopped high-resolution deterministic/PDE comparison.

## Findings

In the delayed-selfing, capacity-cost setting, sampled mean investment decline at update 1,000 increases as replenishment falls. Capacity already increases at the highest rate: replenishment limitation intensifies a response rather than initiating all selfing-capacity evolution. The prior-selfing, zero-capacity-cost setting shows large founder-relative changes even at high supply and a much smaller additional gradient. The settings differ jointly in timing and cost; their contrast does not isolate either factor.

Founder-relative order and order of additional divergence answer different questions. At the lowest rate and the primary 0.05 sustained-change threshold, capacity precedes investment in 51/64 delayed histories and 38/64 prior histories; the others are within five updates. For the delayed setting, the additional divergence relative to high replenishment reaches the investment threshold first in 32/64 histories, capacity first in 10, within five updates in 20, and investment alone in two. Thus capacity-first evolution is not evidence that the earliest additional effect of replenishment limitation is capacity change. Threshold timing is neither infinitesimal onset nor causal mediation.

No fitted transition point, natural distance threshold, universal chronological order or robustness across all other parameters is claimed. The fixed-capacity intervention and finite/deterministic comparisons remain separate cohorts. The three declared change thresholds and both contrasts are retained.

## Complete endpoint and primary-order tables

All values below are at update 1,000. Intervals are pointwise descriptive 95% bootstrap intervals over 64 histories (5,000 resamples), not simultaneous bands or natural-population prevalence. Investment is signed change, so negative means reduced investment. Capacity is autonomous-selfing ability, not realized selfing rate. Counts include censored categories.

### assurance_cost: from_founders

| Establishment rate | Investment change [95% interval] | Capacity change [95% interval] | Occupied / 512 | Paired / 512 | C first / tie / I first / C only / I only / neither |
|---|---|---|---|---|---|
| 0.240000 | -0.01579 [-0.03502, +0.00289] | +0.33472 [+0.32414, +0.34502] | 512 | 512 | 22 / 4 / 0 / 38 / 0 / 0 |
| 0.186912 | -0.11019 [-0.12830, -0.09215] | +0.37639 [+0.36832, +0.38449] | 512 | 512 | 47 / 6 / 0 / 11 / 0 / 0 |
| 0.145567 | -0.14591 [-0.16565, -0.12634] | +0.39393 [+0.38608, +0.40144] | 512 | 512 | 51 / 8 / 0 / 5 / 0 / 0 |
| 0.113368 | -0.20791 [-0.22562, -0.18935] | +0.40983 [+0.40352, +0.41577] | 512 | 512 | 55 / 8 / 0 / 1 / 0 / 0 |
| 0.088291 | -0.24034 [-0.25636, -0.22433] | +0.42058 [+0.41484, +0.42597] | 512 | 512 | 54 / 10 / 0 / 0 / 0 / 0 |
| 0.068761 | -0.26300 [-0.27916, -0.24745] | +0.42072 [+0.41554, +0.42608] | 512 | 512 | 54 / 10 / 0 / 0 / 0 / 0 |
| 0.053551 | -0.27484 [-0.29084, -0.25807] | +0.42799 [+0.42236, +0.43330] | 512 | 512 | 52 / 11 / 0 / 1 / 0 / 0 |
| 0.041706 | -0.29067 [-0.30353, -0.27814] | +0.43042 [+0.42493, +0.43579] | 512 | 512 | 52 / 12 / 0 / 0 / 0 / 0 |
| 0.032480 | -0.29907 [-0.31255, -0.28601] | +0.42981 [+0.42486, +0.43441] | 512 | 512 | 52 / 12 / 0 / 0 / 0 / 0 |
| 0.025296 | -0.30872 [-0.32101, -0.29686] | +0.43261 [+0.42780, +0.43722] | 512 | 512 | 52 / 12 / 0 / 0 / 0 / 0 |
| 0.019700 | -0.30944 [-0.32131, -0.29750] | +0.43092 [+0.42597, +0.43561] | 512 | 512 | 52 / 12 / 0 / 0 / 0 / 0 |
| 0.015343 | -0.32076 [-0.33141, -0.31020] | +0.43359 [+0.42930, +0.43777] | 512 | 512 | 52 / 12 / 0 / 0 / 0 / 0 |
| 0.011949 | -0.32909 [-0.33949, -0.31882] | +0.43503 [+0.43024, +0.43959] | 512 | 512 | 51 / 13 / 0 / 0 / 0 / 0 |

### assurance_cost: minus_high_supply

| Establishment rate | Investment change [95% interval] | Capacity change [95% interval] | Occupied / 512 | Paired / 512 | C first / tie / I first / C only / I only / neither |
|---|---|---|---|---|---|
| 0.240000 | +0.00000 [+0.00000, +0.00000] | +0.00000 [+0.00000, +0.00000] | 512 | 512 | 0 / 0 / 0 / 0 / 0 / 64 |
| 0.186912 | -0.09440 [-0.11054, -0.07801] | +0.04168 [+0.03084, +0.05238] | 512 | 512 | 16 / 6 / 24 / 3 / 10 / 5 |
| 0.145567 | -0.13012 [-0.14790, -0.11261] | +0.05921 [+0.04964, +0.06885] | 512 | 512 | 14 / 8 / 30 / 1 / 9 / 2 |
| 0.113368 | -0.19212 [-0.20805, -0.17536] | +0.07511 [+0.06459, +0.08594] | 512 | 512 | 12 / 17 / 29 / 0 / 6 / 0 |
| 0.088291 | -0.22455 [-0.24321, -0.20535] | +0.08586 [+0.07584, +0.09584] | 512 | 512 | 16 / 14 / 31 / 0 / 3 / 0 |
| 0.068761 | -0.24722 [-0.26446, -0.22976] | +0.08600 [+0.07471, +0.09765] | 512 | 512 | 17 / 14 / 32 / 0 / 1 / 0 |
| 0.053551 | -0.25905 [-0.27697, -0.24057] | +0.09327 [+0.08259, +0.10395] | 512 | 512 | 16 / 13 / 32 / 0 / 3 / 0 |
| 0.041706 | -0.27488 [-0.29247, -0.25706] | +0.09570 [+0.08461, +0.10674] | 512 | 512 | 12 / 14 / 34 / 0 / 4 / 0 |
| 0.032480 | -0.28328 [-0.30175, -0.26517] | +0.09509 [+0.08372, +0.10599] | 512 | 512 | 14 / 17 / 30 / 0 / 3 / 0 |
| 0.025296 | -0.29293 [-0.31123, -0.27493] | +0.09790 [+0.08690, +0.10890] | 512 | 512 | 10 / 19 / 32 / 0 / 3 / 0 |
| 0.019700 | -0.29365 [-0.31464, -0.27276] | +0.09620 [+0.08528, +0.10743] | 512 | 512 | 10 / 20 / 32 / 0 / 2 / 0 |
| 0.015343 | -0.30497 [-0.32410, -0.28599] | +0.09888 [+0.08795, +0.10970] | 512 | 512 | 10 / 20 / 31 / 0 / 3 / 0 |
| 0.011949 | -0.31331 [-0.33164, -0.29577] | +0.10032 [+0.08962, +0.11091] | 512 | 512 | 10 / 20 / 32 / 0 / 2 / 0 |

### prior_selfing: from_founders

| Establishment rate | Investment change [95% interval] | Capacity change [95% interval] | Occupied / 512 | Paired / 512 | C first / tie / I first / C only / I only / neither |
|---|---|---|---|---|---|
| 0.240000 | -0.31558 [-0.32541, -0.30535] | +0.49277 [+0.49149, +0.49400] | 512 | 512 | 42 / 22 / 0 / 0 / 0 / 0 |
| 0.186912 | -0.32418 [-0.33468, -0.31420] | +0.49452 [+0.49326, +0.49573] | 512 | 512 | 43 / 21 / 0 / 0 / 0 / 0 |
| 0.145567 | -0.33361 [-0.34368, -0.32386] | +0.49374 [+0.49239, +0.49502] | 512 | 512 | 42 / 22 / 0 / 0 / 0 / 0 |
| 0.113368 | -0.32400 [-0.33307, -0.31480] | +0.49458 [+0.49340, +0.49568] | 512 | 512 | 41 / 23 / 0 / 0 / 0 / 0 |
| 0.088291 | -0.33340 [-0.34174, -0.32525] | +0.49530 [+0.49428, +0.49628] | 512 | 512 | 41 / 23 / 0 / 0 / 0 / 0 |
| 0.068761 | -0.33306 [-0.34133, -0.32517] | +0.49518 [+0.49403, +0.49629] | 512 | 512 | 39 / 25 / 0 / 0 / 0 / 0 |
| 0.053551 | -0.34277 [-0.35035, -0.33534] | +0.49574 [+0.49442, +0.49701] | 512 | 512 | 40 / 24 / 0 / 0 / 0 / 0 |
| 0.041706 | -0.33639 [-0.34436, -0.32817] | +0.49498 [+0.49353, +0.49629] | 512 | 512 | 38 / 26 / 0 / 0 / 0 / 0 |
| 0.032480 | -0.33592 [-0.34349, -0.32838] | +0.49497 [+0.49401, +0.49593] | 512 | 512 | 38 / 26 / 0 / 0 / 0 / 0 |
| 0.025296 | -0.33514 [-0.34371, -0.32693] | +0.49494 [+0.49385, +0.49599] | 512 | 512 | 38 / 26 / 0 / 0 / 0 / 0 |
| 0.019700 | -0.33488 [-0.34289, -0.32678] | +0.49510 [+0.49372, +0.49643] | 512 | 512 | 38 / 26 / 0 / 0 / 0 / 0 |
| 0.015343 | -0.33954 [-0.34843, -0.33070] | +0.49520 [+0.49411, +0.49620] | 512 | 512 | 38 / 26 / 0 / 0 / 0 / 0 |
| 0.011949 | -0.33567 [-0.34549, -0.32585] | +0.49460 [+0.49340, +0.49579] | 512 | 512 | 38 / 26 / 0 / 0 / 0 / 0 |

### prior_selfing: minus_high_supply

| Establishment rate | Investment change [95% interval] | Capacity change [95% interval] | Occupied / 512 | Paired / 512 | C first / tie / I first / C only / I only / neither |
|---|---|---|---|---|---|
| 0.240000 | +0.00000 [+0.00000, +0.00000] | +0.00000 [+0.00000, +0.00000] | 512 | 512 | 0 / 0 / 0 / 0 / 0 / 64 |
| 0.186912 | -0.00861 [-0.01910, +0.00133] | +0.00175 [+0.00021, +0.00326] | 512 | 512 | 4 / 0 / 5 / 4 / 18 / 33 |
| 0.145567 | -0.01804 [-0.02871, -0.00745] | +0.00097 [-0.00054, +0.00252] | 512 | 512 | 3 / 0 / 5 / 1 / 22 / 33 |
| 0.113368 | -0.00842 [-0.01923, +0.00186] | +0.00181 [+0.00033, +0.00330] | 512 | 512 | 2 / 0 / 5 / 8 / 21 / 28 |
| 0.088291 | -0.01782 [-0.02735, -0.00907] | +0.00253 [+0.00110, +0.00398] | 512 | 512 | 6 / 2 / 5 / 3 / 24 / 24 |
| 0.068761 | -0.01748 [-0.02830, -0.00752] | +0.00241 [+0.00094, +0.00389] | 512 | 512 | 5 / 3 / 5 / 1 / 27 / 23 |
| 0.053551 | -0.02719 [-0.03780, -0.01685] | +0.00297 [+0.00146, +0.00446] | 512 | 512 | 8 / 3 / 6 / 1 / 26 / 20 |
| 0.041706 | -0.02081 [-0.03217, -0.01001] | +0.00221 [+0.00072, +0.00360] | 512 | 512 | 4 / 3 / 5 / 4 / 26 / 22 |
| 0.032480 | -0.02034 [-0.03119, -0.01047] | +0.00220 [+0.00083, +0.00360] | 512 | 512 | 6 / 2 / 4 / 5 / 26 / 21 |
| 0.025296 | -0.01956 [-0.03048, -0.00915] | +0.00217 [+0.00077, +0.00352] | 512 | 512 | 6 / 2 / 4 / 6 / 25 / 21 |
| 0.019700 | -0.01930 [-0.02964, -0.00895] | +0.00233 [+0.00083, +0.00379] | 512 | 512 | 5 / 2 / 3 / 6 / 27 / 21 |
| 0.015343 | -0.02397 [-0.03534, -0.01325] | +0.00243 [+0.00109, +0.00379] | 512 | 512 | 7 / 3 / 3 / 5 / 30 / 16 |
| 0.011949 | -0.02009 [-0.03061, -0.00970] | +0.00183 [+0.00048, +0.00318] | 512 | 512 | 7 / 3 / 3 / 4 / 31 / 16 |

## Evidence and complete companion results

- Summary: `data/results/model3_replenishment_evolution_summary_20261005.json` (all three traits, updates 200/400/1,000, contrasts, thresholds and event records).
- Raw verification: `data/results/model3_replenishment_raw_curves_verified_20261005.json`: 13,312 cases and 9,993,984 reconstructed trait coordinates, exact agreement.
- Readout verification: `data/results/model3_replenishment_readout_verified_20261005.json`: 9,984 crossing records and 156 endpoint rows, exact agreement.
- Figures: `outputs/figures/model3_replenishment_evolution_20261005/all_endpoints.pdf` (six pages), `all_order_thresholds.pdf` (three pages), and `plotted_endpoints.csv` (468 estimates).
- Arrays: `outputs/model3_replenishment_evolution_20261005/evolution_curves.npz`.
- Summary SHA256: `2570bbdd4c4d202e0982eb3afddade40bd6d8ab11551e3b20b49532feea85cea`.
- Array SHA256: `3c217335b57831a60b4257410acfa82a9e32ef1f8190da63300790eabd63ac31`.

These checks establish data-to-readout consistency, not independent replication of the biological simulator. All declared endpoint conditions have 512 occupied populations; survival between endpoints is available in the array archive. No extinct phenotype is imputed.
