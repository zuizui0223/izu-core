# Source-locked first transfer: finite β/FPS and Γseed versus long-horizon Γpersist (2026-10-10)

**Status:** model-internal holdout cohort executed; new visitor histories, source-locked before this cohort's outcomes; the selected biological focal states were chosen *after* prior 384-case engineering results. This is NOT a preregistered field/ecological confirmation and NOT an evolutionary-suicide test.

## Scientific question and what was actually manipulated

The higher-level program asks when an individual reproductive advantage (source genetic contribution W = 0.5 maternal outcross F + 0.5 paternal outcross P + viable self S) predicts a population persistence benefit. This experiment tests a **narrower subquestion**: does a common **±0.05 initial population-wide investment expression/genotype shift** cause a detectable unconditional occupancy contrast at generations 20 and 80? The two original four-visitor prior-selfing discovery conditions were matching=.2, investment=.35, assurance=.35 or .65, with B48; K8 and K48, baseline and a postzygotic 50% viable-self-seed gate were crossed.

Independent environmental source generation: **64 distinct visitor RNG histories (61021001–61021064)**, seeded at time0 with the original four hand-authored visitors (optima .15/.35/.55/.75), followed by original Model3 stochastic visitor arrivals and loss, across 80 reproductive updates. One paired demographic replicate per visitor-history ID. Common master RNG streams across all phenotype contrasts; visitors from the same seed shared within each pair. No plant immigration, adult survival or mutation.

**Deliberately, every founder genotype is monomorphic, at N0=K.** Offspring remain genetically identical; no allele-frequency evolution is possible. This is an actual intervention effect of **fixed genotype/expression values on finite-population persistence**, but NOT a comparison of evolving alleles versus a genetic-trait freeze. It cannot prove evolutionary rescue, suicide, drift-induced maladaptation or allele-load effects.

## Exact source and artifacts

- Full design was committed **before this cohort's outcomes**: `data/design/chapter2_gamma_persist_new_visitor_holdout_20261010.json`.
- Executed source SHA `e1695545c4dc8c65d85f7112a826708f66f0ecb5`, [GitHub Actions #38014927982](https://github.com/zuizui0223/izu-core/actions/runs/38014927982), **source-only smoke tests, full 1024-trajectory cohort and raw archive upload successful**. Whole-repository pytest is a separate, longer check.
- [Raw 64-history/1024-trajectory archive #11655099875](https://github.com/zuizui0223/izu-core/actions/runs/38014927982/artifacts/11655099875), 466,977 bytes of source JSON. SHA256 of raw JSON `a96540fa9c6e96ba3f1e9c15d9dcc0690707742316911f730a425ec76c5275c7`, ZIP SHA256 `2e250b401fedf77a4cfb9a7f669aa3d168824e0f8aa6fb30b743e5931b43bf1a`.
- Immutable compact original treatment and paired discordance counts: `data/results/chapter2_gamma_persist_64_history_holdout_receipt_20261010.json`.
- Dedicated runner `scripts/audit_chapter2_gamma_persist_new_histories.py`, source-only tests `tests/test_chapter2_gamma_persist_new_histories.py`.

## H=80: full outcome-unselected comparison

Counts show independently generated visitor-history outcomes (occupied out of 64). Δ is `P(occupied | +0.05 investment) − P(occupied | −0.05 investment)`. The source numerical beta and Gamma_seed correspond to the **time0 four-visitor state**, not to an averaged derivative over all later ecological visitor trajectories.

| K | assurance | gate | occupied + | occupied − | Δ |
|---|---:|---|---:|---:|---:|
| 8 | .35 | baseline | 1/64 | 2/64 | −.015625 |
| 8 | .35 | half viable self | 0/64 | 0/64 | 0 |
| 8 | .65 | baseline | 64/64 | 64/64 | 0 |
| 8 | .65 | half viable self | 0/64 | 0/64 | 0 |
| 48 | .35 | baseline | 62/64 | 63/64 | −.015625 |
| 48 | .35 | half viable self | 2/64 | 1/64 | +.015625 |
| 48 | .65 | baseline | 64/64 | 64/64 | 0 |
| 48 | .65 | half viable self | 40/64 | 43/64 | −.046875 |

There is **no robust supported long-horizon directional Γpersist in these eight source cells**. Several cells reach an empirical floor (0/64) or ceiling (64/64); this is loss of power/identifiability, not exact zero underlying treatment effect. K was manipulated jointly with founder N0=K, so the K contrast is not pure demographic capacity.

## H=20: one transient-looking contrast, but do not overclaim time interaction

At K48, assurance=.35 and half viable-self gate, **32/64 (+ investment)** versus **10/64 (− investment)** remain occupied at H20: Δ=+22/64=+0.34375. Under the same fixed cells at H80, only **2/64 versus 1/64** persist (Δ=+1/64). Thus the *observed* positive short-horizon persistence contrast does **not yield a reliably identifiable long-horizon benefit** within 64 visitor histories. This is compatible with the delayed consequences of cumulative demographic losses and exhaustion of initially favorable histories, but does not uniquely identify genetic or demographic mediation. It is not a formal test of temporal contrast significance.

## Important uncertainty correction: ordinary bootstrap degeneracy

The *originally committed* design used 1999 paired visitor-history bootstrap intervals and a ±0.05 practical-equivalence band. When every observed outcome pair agrees (including 0/64-versus-0/64 or 64/64-versus-64/64), percentile bootstrap returns **[0,0]**, which can falsely suggest equivalence with high certainty despite only 64 independent histories. **The original preregistered calculation remains in the raw archive, but such degeneracy is not itself sufficient to claim practical equivalence.**

A **clearly labeled post-outcome sensitivity** therefore computes 95% conservative intervals for the paired probability difference using marginal exact Clopper-Pearson intervals for each mutually exclusive discordance probability `Pr(+ only)` and `Pr(− only)`, each with Bonferroni-adjusted error and interval arithmetic. In the 0/64 discordance case the conservative interval has half-width about **0.0662**, larger than the predeclared 0.05 equivalence region.

- At **H80: all eight cells are inconclusive** under this conservative rule, **zero positive, zero negative, zero demonstrated practical equivalence**.
- At **H20: one source-model positive occupancy contrast survives the conservative interval** (K48, assurance=.35, half-self), while seven other cells remain inconclusive. This inference is within one model generating ecological histories, not independent ecology.
- Analysis code: `scripts/audit_chapter2_gamma_persist_exact_pair_sensitivity.py`; tests: `tests/test_chapter2_gamma_persist_exact_pair_sensitivity.py`. This is a declared post-outcome robustness sensitivity, not a substituted preregistered analysis.

## Effect of this result on the article thesis

**Supported, narrowly:** beta and Gamma_seed signs alone do not identify a useful long-horizon persistence gradient even when those source quantities are well resolved. In this holdout, early positive persistence response can coexist with near-extinction at the 80-update horizon. Together with previous synthetic finite-population K8/K48 pathwise bottlenecks, this motivates treating demographic time-horizon and floors/ceilings as an explicit additional axis.

**Not supported:** a general boundary between individual selection and long-term group persistence, evolutionary suicide, genetic drift as a causal mediator, selfing genetic-load crisis, or absence of persistence effect in other environments. For the central evolutionary question, the indispensable separate test remains **standing genetic variation and an evolution-enabled versus carefully defined genetic-expression-frozen comparison**, with independent ecological-history source and equal founder census N0. A post-hoc redraw of individual genotypes is not a no-drift clamp. The current experiment never varies allele frequencies.

**Decision:** preserve all null and inconclusive cells, preserve original preregistered bootstrap record and the conservative post-outcome correction, keep PR #452 Draft, do not retroactively promote this as a completed evolutionary-suicide primary.
