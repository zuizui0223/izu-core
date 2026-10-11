# Independent new-source and new-future visitor histories: assurance genotype origin and finite persistence

**2026-10-10 — Fresh model-internal cohort, completely executed and archived. The stringent source-locked primary did NOT pass. Not a field-island or cross-model confirmation.**

## Key question

Prior PR #452 synthetic source-to-future experiments implicated selected-history reproductive-assurance genotypes in greater persistence than matching/investment genotypes under a fixed original Model3 prior-selfing stress. But those experiments reused previous selected and neutral donor genomic histories, and the first newly seeded future-only transfer had an effect of +30.67 percentage points at K8 under a strict 50-history donor conditional comparison, whose preregistered distribution-free Hoeffding 95% interval included zero.

**New test:** Generate **192 entirely new original donor visitor histories** rather than reusing the outcome-exposed 64 histories, then generate **192 independently seeded post-t20 future visitor-transition histories** conditional on each new source's actual visitor composition at t20. Require the selected-original and neutral-parentage donor sources to BOTH be alive at t20 before a paired whole-locus genotype mosaic can be formed, with all source extinctions transparently retained as donor ineligibility. New source and new future seed ranges were set independently of the earlier cohorts before this study's outcomes.

## Original source/genetic definitions

The model remains original canonical Model3 with three diploid trait loci: matching, floral investment and reproductive assurance. Original source genotypes start from the **same frozen eight-founder allele state across all 192 histories** (for source matching); different ecological and demographic RNG histories vary independently. Prior selfing, ovule budget 8, fixed pollen recipient denominator B48, no immigration, no mutation, no adult survival, and postzygotic viable-self halving are the imposed source intervention.

At t0..t19, two matched donor populations differ only in offspring genomic parentage: original fitness-weighted selected parentage versus a synthetic within-self/outcross-channel neutral parentage. The neutral operator retains actual source viable seed output and channel birth counts, not the physically complete paternal/maternal ovule allocations. **It retains finite segregation/drift and is NOT a genotype freeze.** The eligibility gate is BOTH of those donor populations surviving t20; conditional-genomic-source effects are not effects on original extinction probability from t0.

At eligible t20 sources, two nested samples of eight **whole diploid individuals** from each donor's existing genotype state are crossed with the four artificial genomic compositions: all neutral, assurance locus only selected-origin, matching+investment loci only selected-origin, all three loci selected-origin. Both allele copies and genealogy/origins/flags of each transferred locus are preserved. Artificial mosaics can create cross-source, cross-locus genomic combinations that need not be possible naturally. Starting recipient N0=8 and pollen B=48 are identical; future K8/K48 differ solely in capacity regulation. The future original genotype-dependent parentage operator is the same in all mosaic cells. Every whole-genome draw within a source history receives the SAME new future visitor innovations and paired demographic RNG streams for K/trait module comparison.

This is **192 new original source history × 2 nested genotype draws × 4 mosaic arms × 2 target K**, conditional on both donor states existing, not a fixed number of complete paths regardless of earlier source extinction.

## Pre-outcome scientific lock and execution

- Source contract was committed before exposure: `data/design/chapter2_assurance_independent_source_future_192_20261010.json`, SHA256 **`a17889a48c1fc86a7ec5f5a93e9989f1561134707ddc9249a781b01712c196c8`**.
- Source histories **61028001–61028192**, future conditional visitor innovations **61029001–61029192**. Neither range overlaps with earlier #452 post-t20 donor/environment test cohorts.
- Code `scripts/audit_chapter2_assurance_independent_source_future_192.py`, source-only no-exposure tests `tests/test_chapter2_assurance_independent_source_future_192.py`. Executed source SHA **`dd2376c73fcbb7df5d491d08c9584fd50fffc40e`**.
- [Actions CI #38019242017](https://github.com/zuizui0223/izu-core/actions/runs/38019242017): focused preregistered-source smoke, full original source/future calculation and original archive upload all **PASS**. Source archive [artifact #11657238247](https://github.com/zuizui0223/izu-core/actions/runs/38019242017/artifacts/11657238247), raw original JSON SHA256 **`ccc9f483a0099469e673752bd12faad8282d2641e88684b0e17c436a4c5c754b`**, ZIP SHA256 **`2528027e7029144ffbc568d1cdaee22023aea75c461265708565760e636578ed`**.
- Machine-verified compact receipt and exact source interpretation: `data/results/chapter2_assurance_independent_source_future_192_receipt_20261010.json`.
- No source model biological files were modified, no source/hypothesis/ROPE were changed after reading the newly generated outcomes, and the previously exposed 50-history genotypes did not enter this new donor experiment.

## Results: a smaller but reproducible directional genotype-source effect

All **192** originally enrolled environmental source histories were simulated. **168/192** had both selected and neutral t20 donor genotypes available; **24/192** were correctly marked not eligible for a paired t20 mosaic. Two whole-diploid resamples per source yielded **336 nested genomic source samples** per experimental arm, and **2,688 post-t20 future trajectories** across eight treatment arms (four genomic module states × K8/K48).

**End-of-study occupied / 336 nested genomic samples** (not /336 independent visitor histories):

| Genotype composition at t20 | K=8 | K=48 |
|---|---:|---:|
| All loci neutral-origin | 146/336 | 284/336 |
| **Only assurance locus selected-origin** | **211/336** | **314/336** |
| Only matching + investment loci selected-origin | 145/336 | 290/336 |
| All three loci selected-origin | 222/336 | 317/336 |

**Primary (selected assurance-only minus neutral-all at K8):** +65/336 = **+0.1934524**, i.e. **+19.35 percentage points**.

- 2,999-resample bootstrap over **168 eligible donor-history clusters**, each pre-averaged over the two nested whole-genotype draws: 95% percentile CI **[+0.11012,+0.27976]**.
- Independently precommitted, two-sided **Hoeffding 95%** worst-case distribution-free CI for bounded per-donor history paired effects in [−1,1]: **[−0.01611,+0.40301]**; halfwidth **0.20956**.
- The **precommitted strict decision rule requires both lower interval bounds > +0.05** (5 percentage points). The Hoeffding bound fails; **PRIMARY = INCONCLUSIVE**, not confirmed genetic assurance rescue.
- The previous **old-source but new-future** study reported +0.30667 for the same type of K8 contrast from 50 outcome-exposed donor histories. Completely fresh source histories report a smaller +0.19345, i.e. the previous point estimate does **not** reproduce exactly, even though the sign remains positive. This is precisely why independent source histories are essential.

At K48 the assurance-only contrast was **314/336 vs 284/336 = +0.08929**, cluster-bootstrap95 [+0.04167,+0.14286], Hoeffding95 [−0.12027,+0.29885], also **INCONCLUSIVE** under the same stringent rule. The two other-loci-only contrasts were **−0.00298 at K8** and **+0.01786 at K48**; full three-locus donor-source contrasts **+0.22619 at K8** and **+0.09821 at K48**. All original secondary intervals and nested sample/source provenance are preserved in the raw archive.

The two-order descriptive partition of the entire genome-source effect assigns at K8 assurance +0.21131 and the other loci +0.01488; at K48 assurance +0.08482 and the other loci +0.01339. These values reconstruct the genome-source contrast by arithmetic identity. They are **not naturally identifiable percent shares of extinction prevented by evolving assurance**.

## Mechanistic reading, without inflated claims

**Useful replicated model-internal observation:** An independently generated ecological source and future visitor cohort, though run within the same biological model with the same founder genomes, shows that a selected-origin assurance diploid locus in an artificial genomic mosaic is associated with higher finite-horizon survival than a neutral-origin assurance locus in the stressed scenario. In contrast, selected-origin matching and floral-investment loci alone have little effect under these particular settings.

**What is NOT confirmed:** the preregistered effect >5pp according to *both* the cluster bootstrap and the distribution-free interval; evidence of a universally advantageous locus in other settings; independent ecological mechanisms; field Izu island extinction avoidance; genetic load/purging; or evolutionary suicide. The original donors are conditionally selected for survival at t20, and genotypes are artificial cross-source mosaics, so even this new cohort cannot identify complete selected-reproductive-trait-mediated survival from t0. The 192 samples represent independent Model3 visitor/demographic RNG histories, **not independent naturally observed island ecosystems**.

**Publication gate:** Keep #411 independently confirmed floral-evolution main result separate, #451 bounded assigned-order demographic paper separate, #420 finite genetics exploration separate, and #452 as the mechanistic proof-of-concept. For a high-impact general evolutionary claim, additional biologically distinct mathematical kernels and empirical genotype/mating/offspring survival evidence are required; simply expanding the same Model3 RNG histories cannot establish generality.

## Next decision

Stop outcome-motivated repeated resampling of this *same* assurance/budget/K corner for confirmatory inference. The new fresh-source independent model cohort has tested the frozen hypothesis and yielded a **strictly inconclusive**, sign-consistent effect. Further within-model sensitivity analyses should be clearly marked exploratory, and independent model structures or field-population measurements are the scientifically meaningful next bridge. **Do not infer or announce a confirmed evolutionary rescue/suicide verdict.**
