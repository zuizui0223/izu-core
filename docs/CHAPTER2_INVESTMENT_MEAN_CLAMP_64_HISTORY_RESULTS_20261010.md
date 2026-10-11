# Chapter 2: matched-t20 investment-mean expression clamp — source-verified 64-history experiment

**2026-10-10; complete model-internal engineering result, NOT empirical island validation or a general genetic evolutionary-suicide result.**

## Scientific question

Does the **dynamically changing population-mean floral-investment phenotype** affect population persistence after the same original finite-genetic population has survived 20 updates? Unlike arbitrary genotype resampling, the source genetic state, entire diploid three-locus genotype support, Mendelian inheritance operator and demographic RNG states are left intact.

Model intervention:
- At years 0–19, both conditions use exactly the **same original unmodified canonical Model3**.
- From year20 onward, the native arm expresses each current diploid genotype in reproduction. The counterfactual arm changes only **parental expressed investment values** by one common additive shift `t20_source_mean_investment - current_genetic_mean_investment`, retaining each parent's relative investment deviations, absolute allele differences and original genetic state for inheritance. If current group mean equals t20 target, the original source state is returned unmodified.
- For every paired visitor-history source, both arms share **identical full genomic state at t20, all original RNG stream states and the year20 reproductive ledger/offspring state at t21**. The tests and complete runner fail if those fingerprints disagree.
- This is a *mean-expression feedback knockout*, **not** a complete genetic-drift knockout or true genotype-frequency freeze. The genotype-to-phenotype mapping is counterfactually altered; therefore a nonzero effect is not uniquely attributable to historical drift.

## Engineering support failure and pre-outcome protocol revision

The original v1 contract (`data/design/chapter2_investment_mean_clamp_new_visitor_20261010.json`), 64 source visitor seeds 61022001–61022064, failed the required biology gate in [Actions #38015657188](https://github.com/zuizui0223/izu-core/actions/runs/38015657188) after dedicated unit tests passed: unrestricted founder investment variation (source SD=0.10) made the required additive phenotype shift exceed [0,1] along one simulated path. **No source clipping or selective trajectory deletion was allowed; no complete v1 result exists.** This is a real intervention-domain failure, not an adverse extinction endpoint.

v2, before generating its *new* cohort outcomes, made a **documented feasibility correction**: reduce founder source SD from 0.10 to 0.05, preserving standing three-locus genetic variation while enforcing a pre-run guaranteed allele-support envelope. If all inherited raw investment allele values are in the original interval [lo,hi], then any additive recentering to a target mean and current mean within that support lies between `2lo−hi` and `2hi−lo`. For the fixed founder master used here (61022981), initial investment lo≈0.243641 and hi≈0.402556, so **[2lo−hi,2hi−lo]≈[0.084727,0.561470]**, entirely within the biological [0,1] domain for all future generations under zero mutation. Source `genotype_founders` checks these bounds before simulation.

The v2 redesign uses a **different, previously unused visitor cohort, 61023001–61023064**; v1's partial run is not an independent confirmation or another 64 systems. v2 is a **revised model-internal experiment after source feasibility inspection**, not an unmodified prospective preregistration.

## Exact source, execution and outcome

- Executed source commit `b072c3d8a43a286dd143b6350dfecd9a87d5791c`, [Actions CI #38015887563](https://github.com/zuizui0223/izu-core/actions/runs/38015887563). Focused source/genomic parity tests, full outcome runner and archive upload **PASS**.
- [Full original source artifact #11656606311](https://github.com/zuizui0223/izu-core/actions/runs/38015887563/artifacts/11656606311), raw JSON SHA256 `27e3ae69036515b9375bfa08e02f3d15c8911e0198d182fc22c9511f4607cc4f`; original ZIP SHA256 `0e038e9b498b0282d513efc02a60a526aed8308a2dd6b31366a5f9f3632cd6bf`.
- Full runner: `scripts/audit_chapter2_investment_mean_expression_clamp.py`; tests: `tests/test_chapter2_investment_mean_expression_clamp.py`; compact result/limits `data/results/chapter2_investment_mean_clamp_v2_64_history_receipt_20261010.json`.
- **Packaging warning:** the GitHub Actions ZIP accidentally also included the **old v1 design file** under `data/design/chapter2_investment_mean_clamp_new_visitor_20261010.json`. That file **does not govern** the executed simulation. The original output's recorded source design SHA256 is **`982de58f9d58412e3d7ba295995f4934941a75bf17c249a9b224965cb16d54dc`**, corresponding to the actual committed **v2** design `data/design/chapter2_investment_mean_clamp_new_visitor_v2_20261010.json` (Git blob SHA `ac45632d447e0aa2947108f5e240dab2da208b2b`). Always use v2 for replay.

All conditions: independent simulator visitor RNG history ID n=64 (one model generating mechanism); founder N0=8 for both K8/K48, B48 pollen normalization, prior selfing, ovule budget6, two founder assurance-source settings (.35/.65), baseline or half viable-self gate, frozen starting diploid standing variation SD0.05, source mutation0, survival0, no plant seed immigration. **Each of the 64 × 2K × 2 assurance × 2 gates = 512 prehistory states** feeds exactly two post20 futures, yielding 1,024 trajectories.

## Results: unconditional occupation at generation80

Counts are paths alive out of 64 **including extinct prehistory paths as zero in both arms**.

| K | Founder assurance | Gate | Alive at t20 | Native alive at t80 | Mean-clamped alive at t80 | Paired Δ native−clamped |
|---|---:|---|---:|---:|---:|---:|
| 8 | .35 | baseline | 38 | 20 | 18 | +2/64 |
| 8 | .35 | half-self | 0 | 0 | 0 | 0 |
| 8 | .65 | baseline | 64 | 64 | 64 | 0 |
| 8 | .65 | half-self | 15 | 1 | 1 | 0 |
| 48 | .35 | baseline | 54 | 51 | 50 | +1/64 |
| 48 | .35 | half-self | 0 | 0 | 0 | 0 |
| 48 | .65 | baseline | 64 | 64 | 64 | 0 |
| 48 | .65 | half-self | 28 | 20 | 20 | 0 |

**All eight comparisons were inconclusive**, assessed by the precommitted conservative paired exact Bonferroni/Clopper–Pearson confidence intervals and ±0.05 absolute-survival ROPE. For example, K8 founder-assurance .35 baseline gives Δ=+0.03125 with 95% conservative interval **[−0.06355,+0.12099]**; K48 same founder-assurance baseline gives Δ=+0.015625, **[−0.06598,+0.09561]**. No conclusion of equivalence can be made from all-identical outcome pairs; their exact uncertainty interval is approximately [−0.06618,+0.06618], wider than the target ROPE.

The restriction to 64 stochastic visitor draws **cannot establish a universal absence of investment-mean-feedback effects**. Extinction floors and full-occupancy ceilings are common. In both-survivor pairs only, the *observed endpoint inherited genetic-mean deviation from the t20 target* was also small in some cells: K8 assurance .35 baseline mean absolute deviation ≈0.0010, K48 assurance .35 baseline ≈0.0142, and K48 assurance .65 baseline ≈0.0222. These are **survivor-conditioned post-outcome descriptions**, not causal mediator estimates or independent evidence of a smaller genetic effect.

## Why this matters for the β × Γ hypothesis

The older 384-cell immediate reproductive model demonstrated some **beta-negative/Gamma_seed-positive** floral-investment states, with their signs still present under the original K48 analytical rare-mutant approximation. The separately source-locked 64-visitor Gamma_persist initial-trait manipulation, however, had no resolved H80 direction, and its H20 benefit in one stressed K48 cell largely disappeared descriptively in later occupancy floors. This t20 experiment adds a more specific null/inconclusive mechanism check: **disrupting the evolving mean of expressed investment alone did not produce a resolved 80-update occupancy difference in the fixed new-history cohort**, despite preserving DNA segregation and the identical initial branching state.

These negative results are not a refutation of the broader scientific question: the evolutionary-suicide direction remains unobserved and untested as a full genetically evolving-versus-frozen counterfactual; a phenotype-mean clamp and a genetic selection knockout have different interventions. A test of the separate natural genetic contribution still needs adequate standing genetic diversity, a source-locked large enough independent ecological ensemble (and preferably independent model structures or field data), a genetically meaningful effect scale, event-history design and a valid comparator. No late post-outcome budget choice should be promoted as preregistration.

**Disposition:** retain #411 as main finite floral-evolution result, #451 as a distinct expression-order capacity companion, #420 as finite genetic operator audit and #452 as source-verified mechanistic bridge with both supportive local reproductive-sign discordances and bounded/non-identifying population-persistence tests. Keep #452 Draft.
