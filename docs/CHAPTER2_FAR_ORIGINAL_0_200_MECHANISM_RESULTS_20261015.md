# First 200 updates of far relative I preservation: exact original-source genetic accounting (2026-10-15)

**Status: EXECUTED/ACCOUNTED, retrospective single-repeat source reconstruction, NOT a new independent ecological test or unique selection/drift mediation.** This resolves the technical provenance question of *when the early far E−F I level forms*, without establishing a universal genetic mechanism or natural-island history.

## Source/verification

- Original freeze [run 37458098483](https://github.com/zuizui0223/izu-core/actions/runs/37458098483), first of eight original demographic repeats, seed `26111601`; 64 shared original visitor histories per mating rule, arm **far**, modes fixed and evolvable A. Independent history unit is the original visitor seed; repeat outcomes in different reproductive rules are paired on that seed, not four independent ecological systems.
- [Exact-source audit workflow 38712511100](https://github.com/zuizui0223/izu-core/actions/runs/38712511100), producer commit `7ece820357e4f3e7633944e58b2e5ccf96cd5d86`. 4/4 shard jobs + independent full readout succeeded: **512 exact original genotype trajectories, 102,400 original model updates**, 512/512 bitwise equality to each archived t200 diploid allele array, **102,400/102,400 exact annual I accounting identities**, and all four four-rule source mean signs reproduced. No new independent visitor/founder cohort.
- Full raw-array source artifacts remain on that workflow; [compact 64-history source readout artifact 11961502360](https://github.com/zuizui0223/izu-core/actions/runs/38712511100/artifacts/11961502360). The producer stores yearly complete diploid alleles, origin and mutation flags, individual IDs/birthyears, actual parentage and F/P/S ledger totals. The historical output stored only periodic genotype arrays, not independently authenticated original parentage IDs; those are *exactly reconstructed by the original code and RNG* conditional on endpoint genotype parity.
- Source protocol [here](protocols/chapter2_far_original_0_200_accounting_20261015.json); original genome t200 source [here](CHAPTER2_FAR_ASSURANCE_ORIGINAL_GENOME_PRICE_AUDIT_20261015.md); new, independently re-seeded t200→1000 conditional future [here](CHAPTER2_FAR_T200_HISTORY_SWAP_64H_RESULTS_20261015.md).

## Actual time of the early source far E−F investment divergence

All values below are **original** evolvable-A minus fixed-A I levels, averaged across 64 original visitor histories, **one** demographic repeat per history. At update0 the compared states have identical genetic initial conditions. Descriptive 95% intervals resample the 64 **visitor histories**, 4096 times, not years/plants. Near and far are both synthetic pollen-limited visitor regimes; this is **far only**.

| Rule | t10 | t20 | t50 | t100 | t150 | t200 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Delayed/no cost | +0.0030 | −0.0108 | +0.0162 | **+0.0486** | +0.0517 | **+0.0554** |
| Prior selfing | +0.0035 | +0.0115 | **+0.0373** | +0.0432 | +0.0572 | **+0.0599** |
| Pollen discount | +0.0024 | −0.0072 | +0.0163 | +0.0059 | +0.0229 | +0.0303 |
| Direct A cost | +0.0050 | +0.0000 | +0.0274 | +0.0232 | +0.0233 | +0.0272 |

**Not all apparent onset times are identified.** At t50 the prior-selfing descriptive interval is [+0.00503,+0.06885]; at t100 the delayed-control interval is [+0.00736,+0.08991]. Pollen-discount and direct-cost source intervals at t200 **include zero**, although their first-repeat mean is positive and all four original settings have positive full eight-repeat t1000 E−F intervals in a *different original analysis*. The source t200 positive/negative visitor-history counts are 33/31 delayed, 44/20 prior, 35/29 discount, 37/27 cost. This is heterogeneity, not a deterministic sign in each finite history.

## Exact annually telescoping genetic response accounting

For any occupied source state, define `I_old`, `I_next` and a conditional expected newborn-genetic Price shift `p` from source mother-father-self parent weights:

```
W_i = (F_i + P_i)/2 + S_i
p = Cov_N(I_i, W_i) / mean_N(W_i)
I_next - I_old
  = (n_survivors/N_next) * (I_survivors - I_old)
  + (n_recruits/N_next) * p
  + (n_recruits/N_next) * (I_recruited - I_old - p)
```

Every source annual identity matches its actual diploid descendant generation within 1e−12, with no immigrant seed recruitment. The three terms are labelled **adult survival sampling**, **parent-weight conditional expected genetic Price contribution**, and **realized recruited-gamete/parent sampling plus mutation residual**. Because the original model has no adult year-to-year survival, the first term is exactly zero for **all 102,400 updates**. This does **not** eliminate finite demographic/genetic sampling of new offspring.

Cumulative original `E−F` difference in the t0→200 **realized I change** (raw I units; 95% descriptive history bootstrap):

| Rule | E−F total I change | Weighted parental Price E−F | Recruited transmission residual E−F | Adult survival |
| --- | ---: | --- | --- | ---: |
| Delayed/no cost | +0.05536 | +0.01698 [−0.01504,+0.04973] | +0.03838 [−0.00204,+0.07990] | 0 |
| Prior selfing | +0.05993 | **+0.03465 [+0.00268,+0.06791]** | +0.02528 [−0.00802,+0.05950] | 0 |
| Pollen discount | +0.03035 | +0.02579 [−0.00780,+0.06219] | +0.00456 [−0.03388,+0.04218] | 0 |
| Direct A cost | +0.02722 | +0.00507 [−0.03144,+0.04101] | +0.02215 [−0.02392,+0.06827] | 0 |

The two nonzero columns **exactly add to the original t200 E−F I differences**. Both have positive point estimates in all four settings, but only the **prior-selfing parental Price column** has a descriptive 95% history interval excluding zero. Do **NOT** call these percentages of a causal treatment mediation or a unique drift/selection fraction: the Price weight is measured along treatment-dependent inherited states, and the residual mixes finite parental sampling, segregation and mutation. These components are a source-state accounting identity, not independent experimental knockouts.

### What changes in the interpretation of the “far paradox”

1. At original t0 the fixed and evolving A modes start from identical investment genotypes; the far E−F investment gap **is generated during the first 200 updates**, most visibly in the original first-repeat prior-selfing and delayed conditions. Thus a negative t400 rare-mutant A→I gradient or the t400 conditional one-step Price E−F cannot retroactively negate earlier positive accumulated I differences.
2. In the original t200→1000 archived first-repeat paths, all four **positive** far E−F levels **become smaller** by t1000. This is consistent with *attenuation of early differences*, not ongoing guaranteed positive investment-preserving selection.
3. The **new t200 matched-genotype future-policy factorial** confirms no common positive later effect when future A evolution is permitted among evolved-A origin genotypes: its 63 nondevelopment-history E−F mean is negative in all four reproductive settings, with descriptive bootstrap intervals overlapping zero. All 1,024 new conditional futures retain occupancy, so this is not attrition from extinction.
4. Source visitor-absent years in the first 200 range from **17 to 179** across source histories; no-pollen fixed-genotype investment selection remains `−2*c_I*I`, not zero. The mechanism is about accumulated inherited states and next-generation transmission, **not cessation of all selection**.
5. Two unresolved causal origins remain: why A-permission first establishes such time-dependent genomic-state and parentage differences, and whether a matched-founder/independent-visitor cohort reproduces the same relative early Price/residual pattern. The current accounting does **not** uniquely apportion drift, covariances, mutation or bounded response.

**Editorial consequence:** Q1 is a known-theory context and a source-verified model-specific interaction; this source finding constrains mechanism discussion, but does **not** upgrade the far sign into a new universal ecological law. Q2 and Q3 remain the focus of the standalone paper argument as independently bounded questions, while Q4 is a separate demographic test. Lepers (2014) already includes an individual-based stochastic comparison; see [the full-text prior-art correction](CHAPTER2_LEPERS_FULLTEXT_PRIORITY_CORRECTION_20261015.md). No active Letter conclusion, figure or source-registered threshold has been modified by this audit.
