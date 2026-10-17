# Chapter 2 — code review, ecological inference and paper synthesis (2026-10-17)

**Reviewed baseline:** main commit 3a5443a2c5360b6f3b894809ded58aa004584ec2. This is a source-oriented code and scientific-claim review, not a new biological run, an independent stochastic replay, a historical reconstruction of Izu Island evolution, or a journal submission. Original pinned model code, raw data, registered endpoints, figures and the 2026-10-10 manuscript have not been modified.

## Deliverables

- [Full revised paper](CHAPTER2_MANUSCRIPT_RECONCILED_20261017.md): a complete versioned Ecology Letters-style manuscript. The title and 142-word abstract now foreground the central question, and revised section, conclusion and caption wording separates original 4/4 Q1 results from fresh-founder 3/4 transport. References, figures, source claims and the original manuscript text have otherwise been preserved. Re-rendering and word-count verification are still required for this edition.
- [Read-only numerical auditor](../scripts/audit_chapter2_paper_arithmetic_20261017.py): independently recomputes summary arithmetic from six Git-blob-pinned original receipts, including multiple registered null and scope guards. Does **not** invent or run new model results.
- [Adversarial regression tests](../tests/test_chapter2_paper_arithmetic_20261017.py): fail on modified data source blobs, an invalid Q1 difference-in-differences, mismatched Q2 six-class counts, post-hoc promotion of inconclusive Q2 results, missing Q3 cells, altered pooled Q4 results or removed manuscript scope statements.

## 1. Code review: key findings

| Priority | Original location | Source review | Action or interpretation |
|---|---|---|---|
| HIGH — fixed-A semantics | scripts/model3_island/reproduction.py lines 16–17, 39–45; population.py lines 40–46 | In fixed mode, expressed assurance capacity is 0.5 and realized selfing is **still possible**. Mutation of the assurance locus is blocked. | Interpret as disabling **assurance evolution**, never as disallowing self-fertilization itself or deleting the A locus |
| HIGH — older fixed-A gradient inconsistency | scripts/model3_island/selection.py lines 15–17 vs reproduction.py lines 16–17 | The older local-invasion gradient takes a resident's latent A allele mean even in fixed-expression mode. This can differ from the actual expressed A=0.5 when latent genotype differs. | Do not silently patch SHA-pinned historical calculations. Source-compatible, expression-aware new diagnostic is proposed in [PR #571](https://github.com/zuizui0223/izu-core/pull/571), still under review. No claim its original archive verification is complete |
| HIGH — density not exact finite expectation | scripts/model3_island/density.py and reproduction.py line 37 | The deterministic genotype-class density includes different-plant outcrossing within a genotype class; the finite model excludes within-plant donor=recipient transfer. Density is a conditional closure rather than the mathematical expected value of the finite ABM. | The observed 3/32 and 2/32 disagreement cannot be partitioned into a pure genetic drift share or declared a software arithmetic failure |
| MEDIUM — parentage orientation | reproduction.py lines 34–43 and population.py lines 63–87 | Donor rows / recipient columns appear consistent; sampling returns father, mother in their correct array order; selfed offspring are on a separate diagonal channel. | No reversed-parent indexing defect was found in the reviewed functions. This inspection is **not** an independent complete raw-genome replay |
| MEDIUM — K affects pollen as well as occupancy | reproduction.py line 35; configuration capacity | The canonical pollen recipient denominator contains population capacity K, confounding a simple K contrast with pollen-mediated reproduction. | The distinct fixed-B48 K8-versus-K48 demographic control isolates its own bounded moderator, not a universal island-size mechanism |
| MEDIUM — two crossed Q2 axes | scripts/audit_chapter2_q2_crossed_precision_20261017.py | Eight independent founder labels and eight independent visitor histories cross to produce 64 cells, only one finite path per cell. The interaction and pathwise noise cannot be separately identified. | Use source-registered crossed bootstrap, not 64 independently sampled islands; retrospective normal planning proxies are not prospective confirmed power |
| MEDIUM — reproducibility meaning | main GitHub Actions source-status at review baseline | Python 3.10/3.11/3.12 CI and scientific gate passed on main. Most original biological producer workflows were intentionally skipped. | Passing CI protects repository contracts; it does not mean 8,448 original Q1, 2,304 original Q3 or 4,096 Q4 futures were independently rerun today |

All biological operators remain unchanged in this PR. A versioned diagnostic fix to the selection source is a **separate review decision**, not something silently folded into frozen results.

## 2. Original-receipt arithmetic independently recalculated

| Question | Derived from frozen original receipts | Inference ceiling |
|---|---|---|
| Q1 original four settings | Evolving far-minus-near minus fixed far-minus-near equals stored interaction in **4/4**, to numerical floating-point error smaller than 6e-17: +0.160539, +0.220016, +0.191501, +0.100749. The original 64 independent visitor histories have eight nested demographic repeats | Original preregistered rule PASSED. In the distinct new 8-founder-by-8-visitor campaign, compression was supported in **3/4** settings; the direct A-cost estimate +0.04427 has 95% interval [−0.04407,+0.13084]. General 4/4 independent-founder transport was **not confirmed** |
| Q2 chronology | At sustained founder-relative 0.05 response, delayed selfing with assurance cost gave 51 assurance-first and 13 near-simultaneous out of 64 visitor histories. Prior selfing showed 30/64 assurance-first | Precedence is mating-rule and threshold dependent. The original fixed-A evolutionary intervention and 51-history sequence were different cohorts, not an observed within-history causal mediation |
| Q2 registered new 384 paths | From the original six categories in the far arm: [(14−1)−(6−0)]/64 = **+0.109375** (order score); original investment-event counts give (20−8)/64 = **+0.187500**. Registered adjusted intervals are [−0.125,+0.34375] and [−0.0625,+0.421875]. Matched paths partition into 39 none, 17 gained with dense, 5 lost with dense, and 3 both | Both co-primary intervals contain zero. Preserve **both_inconclusive**. Increasing carrier count is not individually monotone. The unreachable-control 0/64 is engineered by I-allele support with no I mutation/immigration, not an independent new ecological discovery |
| Q3 genetic access | Eighteen original source cells of 128 = 2,304. Pre-single-allele-fixation support loss: 703; at fixation: 535; first observed exclusions: 1,238. A separate signed source receipt contains 315 first-loss transitions with favourable preceding expected frequency response but zero retained low-I copies | Allele support can shrink under finite Mendelian transmission when the I locus has **no mutation or immigration**. The 315/1,238 is a conditional description of already selected loss transitions, **not** a natural extinction or drift hazard |
| Q3 density vs ABM | In two low-replenishment contexts, deterministic conditional density predicted A-first but finite diploid model produced only 3/32 and 2/32 A-first histories; all 64 populations remained occupied through update 200 | A genuine model-prediction mismatch, not a uniquely identified drift, genotype-loss mediation or field island effect |
| Q4 stress test | The arithmetic average across four recorded setting interactions 0.15234375, 0.05078125, 0.09765625 and 0.1328125 equals registered **+0.1083984375** (10.84 percentage points); 95% interval [0.0654296875,0.1513671875] | Supported only in independently frozen 32-visitor-history simulated stress context, with 4,096 postshock trajectories. Prior-selfing-specific interval includes zero; assurance evolution continued during stress, and K/fecundity/pollen changed together |

Audit status: **source arithmetic consistency**, not a fresh model run or a complete raw archive reproduction. Original source SHA assertions prevent quiet replacement of historical inputs, while explicit synthetic-test mode is marked separately.

## 3. Main ecological question and publication stance

**English title:** Temporal precedence is not evolutionary necessity: genetic constraints on floral evolution under pollinator limitation.

**Central question:** If reproductive assurance A crosses an adaptive response threshold before floral investment I declines, is evolving A necessary for that decline? Separately, when is a predicted decrease genetically reachable and capable of being realized by an inherited finite population?

The informative ecological finding is **not** merely that pollinator scarcity can lead to selfing and less floral investment. It is that the direction favored by reproductive returns, an observed order of inherited responses, the genetic accessibility of the next step, and persistence of the population are **not interchangeable observations**. This is a specific intervention-based counterexample under finite-diploid Model 3, not an assertion that all natural island plant evolution is non-sequential.

**Suggested four-figure narrative (retain existing figure source identities):**

1. Figure 1 — mechanistic pollen-mediated female/male gains and floral allocation costs in fixed plants.
2. Figure 2 — primary A-evolvable versus A-fixed factorial. State both 4/4 original success and 3/4 fresh-founder transport; do not call 78–90% arm attribution a causal mediation percentage.
3. Figure 3 — conditional deterministic/genetic realization conflict (3/32 and 2/32), with Q2 sequence and Q3 access as **separate cohorts** in text. Never assign the independent 703/2,304 losses as the proven mediator of the density-vs-ABM gap.
4. Figure 4 — distinct fixed-pollen-background capacity experiment; retain its small prospectively registered +0.007746 interaction and unpooled side cohorts. Discuss the separate +10.84-point stress interaction explicitly with its own original experiment reference rather than treating the two as one occupancy estimand.

**Nulls are part of the paper.** The prospective Q2 carrier-frequency intervention remained inconclusive; fixed A still permitted selfing; prior-selfing threshold chronology did not show the same majority; and a separately registered demographic assigned-order test did not identify evolutionary sequence as a natural extinction-rescue route.

### Priority versus antecedents

The relevant literature already covers joint attraction/selfing allocation (Sakai 1995; DOI https://doi.org/10.1111/j.1558-5646.1995.tb02287.x), stochastic individual-based selfing–pollinator modelling (Lepers, Dufay & Billiard 2014; DOI https://doi.org/10.1111/evo.12533), experimental pollinator-removal selfing evolution (Bodbyl Roels & Kelly 2011; DOI https://doi.org/10.1111/j.1558-5646.2011.01326.x) and genome-wide variation loss with evolved selfing (Busch et al. 2022; DOI https://doi.org/10.1111/evo.14572). Do **not** claim to have invented selfing syndrome theory, stochastic plant modelling, allele erosion or a universal succession of floral trait changes. The bounded novelty candidate is the specific coupling of independently inherited diploid A and I loci, fixed-evolvability counterfactuals, preregistered threshold order, and source-reconciled allele-access accounting.

### Limits for wild islands

Visitor-replenishment labels are synthetic, not observed distances to a mainland or actual islands. Chapter 1 gives a motivating empirical question; it does not identify historical ecological cause. Natural selection versus colonization filtering, climate, island history, local pollinator effectiveness and genealogical structure require separate field/population-genetic evidence.

## 4. Versioning and readiness

**Done on this branch:** a full versioned paper, a frozen-source numerical consistency auditor and negative-path regression tests. The original manuscript, registered experiment source/analysis, SI, figures and source SHA are untouched. The original papers' register and null outcomes are not altered.

**Still HOLD before journal submission:** exact-head CI/scientific-gate for this branch; re-render the anonymous reviewer ZIP for the new manuscript version and recheck the exact title/abstract/main-text word counts; visually inspect the current source-locked Figures 1–4 and S1–S3; author/reviewer approval of scientific English; independently downloadable external raw-data DOI deposit and version/license approval under [Issue #436](https://github.com/zuizui0223/izu-core/issues/436). A new numerical trial to rescue the inconclusive 384-case result is neither proposed nor authorized by this branch.
