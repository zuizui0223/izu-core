# Q3 → Q4 bridge: exact demographic feasibility and stop decision

**2026-10-10 — read-only reanalysis of exposed results, not a preregistration, independent trial or field inference.**  
**Source stage:** frozen original-genome #457 retrospective audit on merged `main`, independent of but contextualized by unmerged Draft #452's low-N monomorphic source pilot.  
**No new ecological visitor histories, no new plant genotype trajectories and no survival rerun.**

## 1. Question: does genetic realization necessarily become a demographic consequence?

The four-question chain is **threshold → order → realization → consequence**. Q3 records the actual inherited diploid genotype trajectory and who survives long enough to reproduce; Q4 must follow **the same population's** pollen transfer, fertile maternal offspring, density-regulated recruitment and *unconditional* persistence. The following narrow one-generation calculations only test whether Q4 could be resolved from presently exposed **aggregate source states**. They do not establish an evolution→survival causal path.

The Model 3 source demographic law for the #457 original t400 counterfactual has **adult survival=0** and **no immigrant seeds**. Let `mu` be the expected number of locally viable seeds under the original reproductive ledger, and `K` the demographic adult cap:

```text
Z ~ Poisson(mu)
N_next = min(Z,K)
E[N_next] = mu * Pr(Z<=K-2) + K * Pr(Z>=K)
Pr(N_next>0) = 1-exp(-mu)       for any K>=1 at fixed mu
```

The final identity is exact **only for this conditional one-generation zero-survival/no-immigration case**. At fixed `mu`, changing `K` can change **expected next census**, but **not immediate probability of ≥1 survivor**. Over subsequent generations `K` can still affect census, viable seed means, drift and extinction through feedback: this is precisely why a one-step calculation cannot replace an 80-update experiment.

## 2. Verified #457 source-grid readout (original 64 histories reused; 1/8 repeats)

Read-only `scripts/audit_chapter2_four_question_q3q4_feasibility.py` consumes three independently archived **main** receipts, checks the original 256-row source checksum lineage, verifies the 4×6 grid, checks resource + recipient-specific receipt = net maternal viable seed, and requires the `b=1` expected-census values to agree with the separate original K48 ceiling audit.

Its total analyzed *source-history × setting × resource multiplier* cells is **64 × 4 × 6 = 1,536**, **not 1,536 independent population histories**. All 24 setting–budget summaries are included, without picking a favourable budget.

| Observed source condition | Next-census response | One-year occupancy |
|---|---|---|
| **Original resource budget** `b=1`, K48/B48 | Mean evolved-versus-investment-restored next-N effects essentially zero (largest magnitude 0.000248 plants). | Every setting mean near 1; original source K48 is capacity saturated. |
| **`b=0.05`**, all four mating settings | 52–64/64 histories per setting have both E and clamp expected next-N between 0.1K and 0.9K. Means of E–clamp next-N: delayed **−0.0121**, prior **+0.1236**, pollen discount **+0.0880**, assurance cost **+0.0441**. | Mean E `Pr(N_next>0)` remains **≥0.995992** across settings; no E history has occupancy in [0.1,0.9]. |
| **`b=0.125`**, all four mating settings | All 64/64 histories per setting have E and clamp expected next-N between 0.1K and 0.9K. Means of E–clamp next-N: delayed **−0.0304**, prior **+0.3090**, pollen discount **+0.2201**, assurance cost **+0.1103**. | Mean E `Pr(N_next>0)` remains **≥0.999995**; no E history has occupancy in [0.1,0.9]. |
| **Entire observed 24-cell grid** | Resource response can be interior, and the mean *census* contrast differs in direction across mating settings. | Just **6/1,536** E history–setting–scale cells have intermediate [0.1,0.9] one-step occupancy, all at `b=0.025` in the assurance-cost setting. The *lowest* setting-average one-step occupancy is **0.945796**. |

The 6/1,536 quantity counts repeated evaluations of **only 64 old histories** across settings/scales. It is not an independent-sample rate or an incidence estimate for natural islands. With all four mating settings included, **three of four** have *higher* mean viable maternal seed output in the evolved-versus-investment-restored source comparison, despite less average delivered pollen. The history-level Shapley source component uncertainties are post-hoc and largely cross zero. There is no general sign-consistent harmful population output.

**Additional exact, source-wide upper bound.** The four archived original K48 near-state receipts guarantee that every evolved/restored pair's viable maternal seed intensity satisfies `mu >= 67.279434303` before budget scaling. Consequently, at a common budget multiplier `b` the paired difference in **conditional one-generation occupancy probability** is bounded without stochastic resampling:

```text
|Pr(occupied next year | E) - Pr(occupied next year | I-restored)|
 = |exp(-b*mu_E)-exp(-b*mu_C)|
 <= exp(-b*67.279434303).
```

For `b=0.125`, this bound is **0.000222646**; for `b=0.25`, **4.96e-8**; for the original `b=1`, **6.04e-30**. Thus *within the already observed original source states*, no individual original history at `b>=0.125` can generate a conditional **one-step** occupancy probability change larger than ~0.000223 via this investment-restoration comparison. This is a **deterministic mathematical upper bound**, not a bootstrap confidence interval, new ecological threshold, statistical power estimate, or bound on 80-update survival: inherited state, `mu` and demography can change after the first update.

**Decision for this source grid:** `NO_GO_FOR_CURRENT_SOURCE_GRID_AS_Q3_TO_Q4_LONGITUDINAL_CONFIRMATION`. This is a *retrospective technical feasibility finding*, not a failed independently registered survival trial and not evidence that true longer-term genetic effects are zero.

## 3. A second density trap: seed supply > N does not ensure expected replacement at capacity

The still-unmerged #452 original monomorphic source fixture reports `N=8`, `B=48`, resource budget 6, total `mu≈8.99442` viable seed intensity. The same exact capped-Poisson operator gives:

| Source moment (same viable seed mean) | Value |
|---|---:|
| Uncapped seed intensity `mu` | 8.99442 |
| `E[min(Poisson(mu),8)]` | **7.26804** |
| `E[min(Poisson(mu),48)]` | **8.99442** |
| `Pr(N_next>0)` for either cap | **0.999876** |

The two capacities do **not** keep the same subsequent trajectories; the equality concerns **conditional immediate occupancy at the same source `mu`**. At capacity K8, stochastic missed reproductive slots cannot be carried forward from a year of abundant seed production, so expected next-N can be below 8 even if expected seeds exceed 8.

In the distinct **unmerged** #452 384-path, 16-history-per-cell 80-update feasibility pilot, only **1 of 12** tested environment × K × resource cases had both policies' endpoint occupancy between 0.15 and 0.85: dynamic visitors/K48/budget6 (native 12/16, founder-centred 13/16). At K8 the pilot was predominantly floor or ceiling; at K48 the monomorphic local focal investment gradient switches towards positive as density grows beyond N≈10. Those facts limit the original conflict-to-persistence argument but **do not exhaust other possible biological models or environmental conditions**. The #452 receipts remain on its Draft branch; this new main-based exact audit *does not treat them as an independent replication or CI-validated input*.

## 4. What this means for the four research questions

| Stage | What present results support | What the present results do not identify |
|---|---|---|
| **Q1 閾値** | Conditional focal-vs-group reproductive return sign conflict in original source context; pollen-mediated benefits to other mothers. | A stable natural ecological tipping point or a universal public-good conflict. |
| **Q2 順序** | Assigned expression ordering can be tested independently; pooled original near–far order test was practically equivalent. | A general effect of naturally occurring mutation/allelic change order. |
| **Q3 実現** | Diploid inheritance, parental lottery, loss of variation and drift mean local selection need not be realized in any finite history. | The fraction of the source gradient actually realized as sustained genetic investment decline **under a prospectively independent treatment**. |
| **Q4 帰結** | K/census and ovule-resource buffering alter expected recruitment; a separately registered small demographic K moderator exists (#442). | That evolving floral-investment reduction *causes* a decline in net viable seed, unconditional recruitment or 80-update survival. |

## 5. Next one-task scientific gate (no premature compute launch)

**Do not run 80-update confirmatory simulations in a source-selected budget.** First specify and independently justify a demographic operating envelope in which (a) the negative *full paternal-inclusive* individual investment return, (b) a positive group viable-seed effect after nonfocal pollen accounting, (c) sustained inherited downward investment, and (d) nonsaturated, *unconditional* demographic survival information can all coexist **through the same histories**.

If original Model 3 density feedback makes (a) disappear before (d) becomes informative, record an honest **NO-GO under the original model**, rather than silently changing founder number, resource level, visitor assemblage or the selection definition. An alternative demographic mechanism would be a **new, explicitly declared biological model**, requiring its own rationale and null controls.

A subsequent independent study must specify the primary `E[occupancy80(native evolved history)]−E[occupancy80(matched history with the *defined* investment-evolution intervention)]`, same founding diploid genotype and visitor RNG, paired cluster-level inference, unchanged paternal/maternal/selfing ledger, complete genetic trajectories including extinct populations, measured recruitment/mortality, and non-selection of post-treatment survivors. The genomic/evolution intervention itself is **not yet identified**: forcing allele values, suppressing mutation, and expression-recentering answer different causal questions. The current audit is **not** an actual prospective design or authorization to run one.

## Source/verification trail

- Merged #459 evidence spine: `docs/CHAPTER2_FOUR_QUESTION_POST411_EVIDENCE_SPINE_20261010.md`.
- Merged #457 receipts: `data/results/chapter2_original_evolved_budget_capacity_gate_receipt_20261010.json`, `data/results/chapter2_original_evolved_resource_receipt_shapley_receipt_20261010.json`, `data/results/chapter2_original_evolved_K48_ceiling_receipt_20261010.json`.
- Unmerged #452 [population-state / survival pilot](https://github.com/zuizui0223/izu-core/blob/analysis/chapter2-evolution-persistence-synthesis-20261010/docs/CHAPTER2_INVESTMENT_COMMONS_PERSISTENCE_FEASIBILITY_20261010.md) and [one-page scientific adjudication](https://github.com/zuizui0223/izu-core/blob/analysis/chapter2-evolution-persistence-synthesis-20261010/docs/CHAPTER2_PR452_ONE_PAGE_SCIENTIFIC_DECISION_20261010.md).
- This PR changes only an optional read-only audit, a focused test, and this decision note. The canonical Model 3 code, active manuscript, current bundle PR #458 and all original cohort outputs remain unchanged.
