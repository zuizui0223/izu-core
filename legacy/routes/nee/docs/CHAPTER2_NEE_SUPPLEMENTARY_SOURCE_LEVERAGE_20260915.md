# Supplementary source-leverage and redundancy diagnostics

This supplement reports diagnostics that are deliberately stricter than the frozen primary routing rule. The primary six-source natural-regime plane and its prespecified largest-source leave-out rule are unchanged. These diagnostics quantify where source-specific leverage remains and document a prospectively frozen attempt to reduce that leverage without opening candidate coordinates prematurely.

## Supplementary Table 1 | Leave-one-study-out source leverage

| Excluded source study | Systems remaining | D1 q90/q10 | phi q90-q10 | Interior occupancy | Absolute Spearman(log D1, phi) | All frozen dispersion criteria pass? |
|---|---:|---:|---:|---:|---:|:---:|
| Hawaii (Aslan et al. 2019) | 41 | 6.661 | 0.352 | 0.268 | 0.343 | yes |
| Martinique (Cyrille 2025) | 32 | 2.883 | 0.352 | 0.188 | 0.358 | no |
| England STEP / Great Britain | 39 | 6.199 | 0.162 | 0.231 | 0.193 | no |
| Tenerife (Lara-Romero et al. 2019) | 38 | 5.927 | 0.319 | 0.237 | 0.245 | yes |
| Mallorca (Lázaro et al. 2022) | 23 | 5.494 | 0.352 | 0.261 | 0.454 | yes |
| Cabrera (Serra-Marin et al. 2025) | 37 | 6.199 | 0.337 | 0.270 | 0.326 | yes |

The full six-source plane contains 42 systems. Source-balanced D1 q90/q10 = 4.521, phi span = 0.352, interior occupancy = 0.262, and absolute Spearman = 0.325.

Two exclusions are load-bearing under the stricter all-source diagnostic using the original source-native schedules. Removing England STEP reduces synchrony dispersion below the frozen numerical floor (phi span = 0.162). Removing Martinique reduces joint-interior occupancy below the frozen numerical floor (0.188), although breadth dispersion remains >2. These diagnostics were calculated after the primary route decision and do not redefine that decision.

## Supplementary Table 1b | Equal-depth six-bin synchrony sensitivity

A later code review identified a sampling-depth concern: across the 42 admitted systems, full-data `phi` correlated negatively with time-bin count (`rho_s=-0.273`; for `rho_eq`, `rho_s=-0.372`). Before executing the sensitivity, all systems were frozen to repeated rarefaction to six distinct source-native bins, with 1,000 requested iterations and the original partner identities, source weights and NEE dispersion thresholds retained. Of 1,000 iterations, 999 were valid.

| Sensitivity quantity | Result |
|---|---:|
| All-source phi-only dispersion criteria pass | 90.8% |
| England-excluded all four dispersion criteria pass | 89.1% |
| England-excluded phi-span criterion pass | 93.3% |
| Six-bin phi-span median | 0.470 |
| Six-bin phi-span 95% interval | 0.284–0.774 |
| Joint-coordinate all-source criteria pass | 61.1% |

England itself remained highly synchronous after rarefaction: Carlisle median `phi=0.446` (full 0.450), Livingstone_far 0.680 (full 0.635), and Livingstone_house 0.475 (full 0.414). Thus England's high values are not explained by having only eight source-native rounds. At the same time, the failure of the original England-deletion span is not robust to equal temporal depth: other sources move upward when reduced to six bins, so the apparent uniqueness of the England high-synchrony edge is partly a sampling-depth property. Because this small-T perturbation itself shifts `phi`, the rarefied plane is retained strictly as a sensitivity analysis and does not replace the full-data primary coordinates.

## Supplementary Table 2 | Prospectively frozen source-redundancy challenge

| Rank | Candidate | Disposition before coordinate extraction | D1 or phi opened? |
|---:|---|---|:---:|
| 1 | Petanidou Aegean / Cyclades | structural fail complete outcome independent sampling frame not reconstructible | no |
| 2 | Sicily Bombus | structural fail raw dates do not reconstruct published rounds | no |
| 3 | Mahe restoration networks | transport blocked primary standardized visitfreq unrecovered | no |
| 4 | Giannutri daily networks | fail reopened challenge outcome independent time bin rule | no |

The redundancy challenge was frozen before reopened coordinate extraction. Candidate order, admission rules, coordinate definitions, source balancing and dispersion thresholds were fixed in advance. All four candidates closed before D1 or phi extraction, so no candidate values were available for selection. The challenge therefore did not remove the England dependence and was closed without expanding the source universe further.

## Scale bridge: natural D1 is not synthetic k

Synthetic k is the nominal number of exchangeable model components, and synthetic k_eff is the variance-equivalent effective independence implied by k and correlation. Natural Hill D1 is instead the effective diversity of pooled, effort-standardized partner interaction shares. No numerical D1-to-k or D1-to-k_eff mapping is estimated or used, and no natural analogue of the synthetic k≈4 crossover is claimed. The theory-to-data connection is structural only: partner breadth and temporal synchrony are measured separately because a single second-moment compression need not preserve nonlinear response-relevant information.

## Interpretation boundary

These diagnostics support a deliberately narrow inference. The full-data natural plane demonstrates a broad, empirically occupied two-dimensional context space under the frozen measurement contract. Under the original schedules, that coverage is source-complementary rather than leave-any-source-out invariant; under equal six-bin depth, England-excluded synchrony coverage is usually restored, showing that source leverage and temporal sampling depth are partially confounded. Great Britain retains the pre-existing EuPPollNet island-study classification; it is not reclassified from its effect on the route. Failed or unavailable candidate sources are data-eligibility outcomes, not biological negatives.
