# Q4 exact demographic-only null: why an island population can decline without genetic change

**2026-10-10. Analysis class: exact finite-state Markov propagation in a restricted, clonal Model 3; source-selected exploratory model, NOT natural-island data or a new confirmation of evolved underinvestment.**

## Central link to the four-question study

The central scientific order is **threshold → order → realization → consequence**. A Q1 local fitness gradient, a Q2 assigned-expression order or an observed Q3 allele trajectory must not automatically be equated with Q4 persistence. The merged #460 one-step analysis found that viable seed effects and 80-year occupancy cannot be interchanged. This study makes the next mathematical step: **calculate exact 80-reproductive-update occupancy from the original birth/seed-pollen operator with NO genetic evolution**.

This is an explicit **counterfactual null model**. If it can already generate low and high survival regimes under the same ecological resource settings, Q4 must quantify *additional* effects of inherited selection, not merely point to terminal extinction under low resources.

## Original biology retained, state deliberately restricted

- Reproductive ledger: **unchanged** `scripts/chapter2_kb_reproduction.py::reproduce_kb` (the published controlled B-versus-K original kernel, not a new survival equation).
- Local Model 3 plant genotype: all adults at every time have identical diploid alleles for `(matching,investment,assurance)=(0.20,0.35,0.35)`; no mutations, no adult survival, no plant immigration.
- Visitor environment: **fixed** four source functional types, optima `[.15,.35,.55,.75]`, breadth 0.18, effectiveness 1; fixed count-scaled source activity. This is the pre-exposed **static_matched4** configuration from unmerged exploratory #452, NOT an externally sampled island pollinator assemblage.
- Pollen background `B=48` is held fixed separately from demographic capacity `K ∈ {8,48}`.
- Original six configuration cells: initial `N0=8`, `K∈{8,48}`, ovule budget `∈{4.5,6,8}`. These are previously exposed pilot values, **not** post hoc searches for a new favourable condition.
- Due to genetically identical adults and zero mutation, inheritance under the canonical `inherit` operator leaves these identical phenotypes unchanged, whatever parental lottery occurs. Conditional reproduction is therefore a function only of current census `N` (plus the *fixed* visitor and resource condition).

For each positive current census `n`, the unmodified reproduction operator gives an expected viable offspring intensity `μ(n)` including outcross and viable selfed seeds. The original demographic operator with zero survival and immigration gives:

```text
N[t+1] = min(Poisson(mu(N[t])), K)
T[n,k] = PoissonPMF(k; mu(n)),              k < K
T[n,K] = PoissonSF(K-1; mu(n))
T[0,0] = 1
p[t+1] = p[t] @ T; p[0] = point_mass(N0=8)
P(occupied at t) = sum_{n=1}^K p[t,n]
```

This is **exact for this no-variation/no-visitor-turnover submodel**: it integrates every Poisson realization analytically, instead of drawing arbitrary 16 or 64 sample trajectories. It is **not** an exact population-size closure for the segregating-genotype experiment, where changing alleles and visitor composition change `μ(n)`.

The source-ledger check gives `μ(N=8,K=8,B=48,budget=6)=8.994424151...`, agreeing with the prior unmerged #452 `8.99442` source diagnostic. Under `K=8`, its next-census expectation is 7.2680427; under `K=48` it is 8.9944242. One-step occupancy at the same viable seed intensity is identical for the two K arms.

## Exact results (all six original configurations, no sampling confidence intervals)

| K | Ovule budget | P(occupied at 20 updates) | P(occupied at 80 updates) | Reading |
|---:|---:|---:|---:|---|
| 8 | 4.5 | 0.017939 | 0.00000000394 | Demographic near-certain extinction |
| 8 | 6 | 0.496902 | **0.030243** | Intermediate initially, very low at 80 |
| 8 | 8 | 0.978905 | **0.902748** | High persistence |
| 48 | 4.5 | 0.052378 | **0.015275** | Low persistence |
| 48 | 6 | 0.840048 | **0.828719** | High persistence even with unchanged genotype |
| 48 | 8 | 0.998187 | **0.998185** | Near-ceiling persistence |

All quantities are **exact probabilities in this deliberately frozen clonal/static-visitor model**, not observed frequency in six independent populations. They were independently checked by algebraic source-reproduction reimplementation and are pinned to the native-ledger regression tests in this PR. Source parameters are conditional artificial model settings, not measured natural units.

## Scientific interpretation

**Q4 demographic diversity does not require Q3 allele change.** Even with identical plant genotypes throughout and four visitors that never turn over, fixed resource and K yield strong differences in 80-year survival. At the original budget6, **K8: 3.0% versus K48: 82.9%** H80 occupancy, entirely from density-dependent recruitment, Poisson stochasticity, and the demographic ceiling. The *starting* eight-plant reproductive intensity is identical at B48; later differences arise because populations follow different census distributions. This **does not** prove that genetic evolution never affects occupancy; it establishes that the baseline demographic contrast must be subtracted or controlled before calling any evolving model difference an evolutionary consequence.

The exact non-genetic outcomes are qualitatively compatible with the **static-visitor engineering pilot in unmerged #452**: K8 budget6 is near the floor and K48 budget6 has frequent survival even there. But #452's actual 16-history experiments had **standing investment genetic variation** and Mendelian segregation, so the two treatments are different biological populations. The present results are **not independent replication, effect estimation, or quantitative validation of those observed 16-history proportions**.

There is a second important distinction: the single-year cap-independent event `P(next N>0 | current mu)` does not imply `K` is irrelevant to 80-generation survival, because `K` changes the census-state distribution feeding into the next year's reproduction. The exact Markov propagation demonstrates this delayed population-level K pathway without genetic evolution.

## Mechanism admission criteria for a future Q3→Q4 causal experiment

1. State the estimand as the incremental effect of a clearly defined **genetic** or **expression** intervention over an appropriate matched demographic-only baseline. A mean-expression-centering treatment is not an allele-mutation freeze or a genotype intervention.
2. In the same histories and matched genome founders, report `N(t)`, `mu(t)`, local full `F/P/S` genetic return, allele mean/variance, visitor state, stochastic recruitment and first extinction. Preselect no survivors.
3. Report whether the local Q1 `β<0 / Γ_seed>0` conflict persists as `N` moves: the already exposed monomorphic #452 source conflict was restricted to `N=6–9`, and K48 can move beyond it.
4. If the original model cannot maintain the conflict in an informative survival envelope while also producing inherited mean investment change, conclude **NO-GO under original Model 3**, not evolutionary suicide. A different demographic or visitor mechanism must be declared as a genuinely new model first.

## Implementation and evidence rank

- `scripts/audit_chapter2_exact_clonal_demographic_null.py`: finite `(K+1)×(K+1)` transition and deterministic 80-step probability propagation using native `reproduce_kb`.
- `tests/test_chapter2_exact_clonal_demographic_null.py`: source `N8` viability identity, clone genotype transmission, row stochasticity, absorbing extinction, 6 condition/80-step regression and no-new-history guards.
- CI executes deterministic operator tests only, **not** any new stochastic biological campaign or independent-history test.
- Source fixture reference: [Draft #452](https://github.com/zuizui0223/izu-core/pull/452), especially `docs/CHAPTER2_INVESTMENT_COMMONS_PERSISTENCE_FEASIBILITY_20261010.md`. Its claims and uncertainties remain unmerged, exploratory.
- Main evidence spine: merged [PR #459](https://github.com/zuizui0223/izu-core/pull/459); one-step bound: merged [PR #460](https://github.com/zuizui0223/izu-core/pull/460).
- One active manuscript remains unchanged, and NO current Ecology Letters editorial claim is upgraded by this exact null.
