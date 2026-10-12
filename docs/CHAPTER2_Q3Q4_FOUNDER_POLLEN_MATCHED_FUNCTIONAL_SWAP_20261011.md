# Q3→Q4 functional mismatch: founder-total-pollen matched negative control (2026-10-11)

**Evidence rank:** post-discovery exact counterfactual in ONE synthetic Model 3. Not observed island visitation, independently preregistered ecological replication, or a causal decomposition of naturally evolving plant-pollinator networks.

## Why this control is required

The parent source comparison (PR #468) keeps four visitor functional types but shifts their floral-optimum traits from `matched4` to `shifted4`. The apparent effect of a different visitor community might reflect (1) **less pollen actually reaching flowers**, (2) redistribution of seed parentage, or (3) other features of changing genotype and census. Without a delivery-matched control, these cannot be separated.

The present experiment matches the **INITIAL N=8 founder total delivered pollen only**, using a **fixed** scalar on effectiveness of the ORIGINAL `matched4` functional assemblage:

```text
reference_scale(λ) = delivered_pollen(shifted4, effectiveness=1 at N=8)
                   / delivered_pollen(matched4, effectiveness=1 at N=8)

Comparator A: shifted four functional optima, effectiveness=1
Comparator B: original four functional optima, effectiveness=reference_scale(λ)
```

Both references have **exactly four visitor types** with breadth0.18, constant optima within the experiment, original Model 3 K8/B48, four 2026-10-06 mating rules and resource budgets 6/8, identical initial eight investment-heterozygous founders (0.20/0.50, expression0.35), zero adult survival, no immigration or mutation. There is no post-hoc scalar tuning to the 80-generation survival outcome or to subsequent individual genotype composition.

The scalar is fixed for all population-genetic states and all eighty generations. Once genotypes and census vary, **total pollen delivered need not remain exactly equal**. Thus the exercise tests a matched-*founder* counterfactual rather than longitudinal natural mediation or an equal-pollen-at-every-state experiment.

## Founder matched source values

| Fraction λ of historical functional replacement | Matched four-visitor effectiveness multiplier | Founder total delivered pollen in BOTH comparators |
|---:|---:|---:|
| .25 | 0.66461077 | 0.31685427 |
| .50 | 0.08204444 | 0.03911482 |
| .75 | approx. 0.001458 | 0.00069540 |
| 1.00 | 0.00000370042 | 0.00000176418 |

The parent #468 unscaled reference has `delivered=0.47675164` at λ0. The shifted visitor optima retain four types even at λ1; they are not zero visitors. Both delivery-matched founder groups also have the same expected total viable maternal seeds and first generation Mendelian genotype transmission at each setting, not just the same total delivered pollen.

## Independent source operator probe, resource budget 6 (delayed selfing)

These are exact 80-update occupancy probabilities from an independently written implementation of the original K8/B48 model mathematics, retained **as diagnostic targets for GitHub native-kernel CI**, not promoted as independent ecological validation.

| Functional replacement λ | P80 with shifted functional optima | P80 with original optima but founder-delivery matched | Residual shifted-minus-matched P80 |
|---:|---:|---:|---:|
| 0.25 | 0.0136038153 | 0.0136128276 | **−0.0000090123** |
| 0.50 | 0.0058605520 | 0.0058753833 | **−0.0000148313** |
| 1.00 | 0.0052822863 | 0.0052822872 | **−0.0000000009** |

Comparison uses native genotype-dependent floral investment expression in both pollen-visitor contexts. Both visitor contexts are capable of providing the same **initial** total pollen receipt, and the long-run source population occupancy differences are small in the selected budget6 fixture. The separate **native-minus-fixed-investment expression** treatment contrast differs between shifted and pollen-matched reference contexts by −0.0000066220 (λ.25), −0.0000088342 (λ.50), and −0.0000000006 (λ1).

**Important non-universality:** At budget8, λ.25 delayed-selfing the shifted-minus-matched native P80 difference is **+0.00019886** (opposite direction). Do not assert exact equality, mediation fraction or strict zero composition effect. All four original mating settings and both budgets are retained in the runner's **32 pairs** (4 functional replacement fractions ×4 mating systems ×2 budgets).

## Ecological interpretation and distinction from PR #452

Earlier Draft #452 evaluated **36 fixed-state** delivery-equalized reproductive ledgers and found that the large group viable-seed contrast of functional replacement mostly disappeared after matching total pollen delivery. This follow-up asks whether a similar phenomenon is visible after **80 generations** of segregating inheritance and demographic stochasticity. The restricted synthetic results align qualitatively, but they are **not independent confirmation** or a new field system.

At this source parameterization, the dominant observable consequence of mismatched floral/visitor functional traits appears to operate through reduced pollen delivery. A small residual can persist from different trajectories of pollen routing, genotype composition and density after the first update; **this calculation cannot uniquely assign it to paternal assortment, maternal allocation or a direct functional-trait ecological filter**, because delivery is equalized only in the founders.

## Q1 → Q4 inference boundary

- **Q1 閾値:** functional-trait matching changes total pollen service and can affect full paternal-inclusive genetic returns; a single aggregate pollen match does not identify each focal gradient.
- **Q2 順序:** no evolutionary mutation-access order or temporal introduction of pollinator functions is manipulated.
- **Q3 実現:** Mendelian genotype transmission proceeds after original matched founders; all genotype categories are determined by inherited class rather than numeric allele equality (correcting the error in PR #466).
- **Q4 帰結:** group seed intensity, genotype sorting and 80-year unconditional occupancy are distinct quantities. The founder-total-pollen match is a **negative control** for a putative large direct survival effect of visitor optimum identity beyond pollen quantity.

To transport the finding to islands, externally grounded flower/visitor functional traits and **observed pollen deposition, mating outcomes and recruitment** would be needed, together with visitor identity and time-varying abundance. The current source contains none of those natural observations. Neither PR #411 nor #442 independent confirmatory source decision is changed.

## Reproducibility

- `scripts/audit_chapter2_q3q4_founder_delivery_matched_20261011.py`: exact original `reproduce_kb` 165-state genetic recruitment and frozen effectiveness scalar.
- `tests/test_chapter2_q3q4_founder_delivery_matched_20261011.py`: all 32 source pairs, four visitor types both arms, equal initial delivered pollen, equal initial viable seed intensity and parentage, stochasticity, several original 80-year numeric targets, and evidence-rank guards.
- Direct predecessor: PR #468 functional matching with original `matched4/shifted4`; no new histories, traits, model families or field data.
