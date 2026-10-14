# Chapter 2 — Colonisation genetic access: claim-admission and next-experiment decision

**2026-10-14 | TECHNICAL RESULT, NOT EVOLUTIONARY CONFIRMATION.** This memo is a reviewable scientific decision record for [PR #512](https://github.com/zuizui0223/izu-core/pull/512). It does **not** authorize new Model3 biological trajectories, alter the 1,536-case pilot or merge the PR.

## Accepted facts, each with its own estimand

| Layer | Grounded source result | What it cannot establish |
|---|---|---|
| Original t0 source identity | Two original 48-adult founder genomes were admitted by original typed-array hashes; six original full-N48 return summaries and 192 genotype-intervention *static* native return comparisons passed | Field mainland allele distribution, independent origin of copied genomes |
| New synthetic founders | 16 artificial phenotype-balanced sources, 48 adults each, four identical-phenotype adults per stratum; 12 A and 12 I heterozygous carriers across m=0/3/6/12 | Sixteen observed natural island systems, survival advantage |
| Conditional **single offspring** F1 marginals | Within a fixed artificial source × visitor context, changing m keeps individual trait F1 expected mean and variance unchanged to numerical tolerance | Identical full multivariate offspring distribution or later trajectory |
| Conditional **signed parental-pair midpoint** | m=12 vs m=0 raises the probability of both A-up and I-down gametic departures from the selected parental-pair midpoint for all 16 artificial inputs across the three original visitor settings | Preferentially beneficial segregation: all four A/I sign combinations are equally likely |
| Conditional **individual founder-mean threshold** | The **same child** can cross founder A+0.05/I−0.05 thresholds even at m=0 because the founding parents already differ in I. At zero visitors, m12−m0 is positive in **5/16** artificial sources and negative in **11/16** | Sustained 20-occupied-census *population-mean* response, causal influence of m on order |
| Existing separate prospective genotype-width pilot | Source/mirror-audited 1,536 histories yield A allele-width manipulation ΔD ≈ +0.669 and A-event-incidence difference ≈ +0.034, under matched adult phenotypes | Not a causal co-carriage intervention; cannot use this result as an estimated m effect or its power |

**Core interpretation:** there are three genuinely different outcomes: (1) whether existing A/I alleles can be inherited, (2) whether the first offspring's phenotype moves relative to its particular parent pair and/or founder reference, and (3) whether a population's mean trait changes **persistently** in the predeclared A-first / I-first six-class system. An increase at (2) does not imply an increase at (3).

Runnable source-locked audit for the old Model3 genotype inputs: scripts/audit_chapter2_colonisation_claim_gate_20261014.py. It recomputes all three t0 source reports and **refuses** to label its output as a biological history or Q4 persistence.

## What should actually be tested next

**Primary scientific question:** when adult expression, immediate reproductive returns, *each trait's marginal F1 access*, founder census and visitor context are held equal, does **joint A/I carriage** change the later six-class evolutionary response *distribution*?

The balanced-source engineering fixes the exact t0 control needed for that comparison; the original historical cohort and the existing unbalanced synthetic source distributions are **not** independent tests of this question.

**Candidate paired contrast (proposal, NOT preregistered, NOT approved):**

- For each independent **synthetic source genotype realization**, compare m=0 versus m=12 at N=48, with the same 12 four-adult phenotype strata and the same original Model3 visitor context. Keep contexts 0 / 3 / 4 separate rather than pooling their proportions.
- Preserve the original response definition verbatim: A mean +0.05, I mean −0.05, first occupied onset of 20 consecutive occupied censuses, ±5 periods near-simultaneous; all six categories **including single-side and neither** retained. Extinction is a separate recorded endpoint, not an exclusion.
- **Proposed primary outcome:** the complete six-class outcome distribution within each ecology. A paired source-level contrast of D = P(assurance_first) − P(investment_first) is a **directional secondary contrast**; do not assert D increases in advance because initial Mendelian signs have no beneficial directional bias. Onset-time comparisons must handle nondetection/censoring, not restrict to successful event trajectories.
- The correct sampling hierarchy is **independent synthetic source pool → matched co-carriage intervention → common stochastic future histories**. Future histories are not additional independent source pools. Confidence intervals and uncertainty must reflect source-pool clustering. A biological future-seed list, independent number of pools/history replicates, analysis family/error rate, minimal scientifically meaningful effect and computational cost remain unspecified.
- A founder-N=2/8/24/48 arm changes demographic recruitment as well as access; the N48 projected homolog control removes the adult census change by construction but inserts artificial repeated donors. Neither arm by itself identifies a *natural* founding history.
- Do **not** infer a co-carriage-specific treatment effect by changing the identities of I carriers among **unequal I phenotypes** without source-phenotype stratification; that also alters the effective reproductive-weighted I variance.

## Launch and interpretation gates

Before any *new biological simulation* can be presented as a prospective experiment:

1. **Source family:** prospectively fix the independently drawn source genotype distribution (and justify its ecological interpretation), exact source IDs, allele-origin conventions and hashes. The 16 artificial t0 examples alone do not supply external validity.
2. **Counterfactual protocol:** lock all genotype modifications, matched founder IDs, phenotype/return/F1 marginal tests, visitor environments and no-repacking rules to the original Model3 frozen biological operators.
3. **Prospective inference:** freeze the 6-class and persistence outcome denominators, estimand, source-cluster-aware uncertainty, power/sensitivity, correction across ecological settings, failure/STOP rules and a feasible independent source/history budget. The 1,536 original pilot's A-width SE is **not** a power estimate for co-carriage.
4. **Execution provenance:** prepare full raw-genome archival and independent replay/readback of every approved prospective result. A prior technical t0 source gate and historical pilot approval **cannot substitute** for new authorization.
5. **Human review:** obtain an independent scientific review and the author's explicit approval for this **new** biological experiment. The present PR remains a Draft and no biological dispatch is performed.

### Predefined falsification cases

The hypothesis of *universal monotone* founder-relative favorable offspring assembly is already **not compatible with these synthetic inputs** (5 positive, 11 negative at no visitors). Whether the **long-term six-class population response** changes remains completely open.

If the future m contrast only alters first-offspring joint segregation but not the sustained six-class response with adequate independent source-level precision, the proposed genetic co-carriage explanation of evolutionary **order** is **not supported by that test**. If order shifts but survival remains at the N48 ceiling, Q4 persistence benefit is **not supported**; assess survival separately with a justified non-ceiling biological design.

**Status at this document:** native t0 mathematical and reproducibility claims admitted only within the explicit synthetic source scope; new F1 biological births **0**, new Model3 future histories **0**, new natural mainland/island allele datasets **0**.


## Full one-child F1 marginal versus joint distribution (supplement)

The balanced four-adult-phenotype-stratum construction makes a stronger, directly testable claim than matched univariate moments: **for a given synthetic source and visitor ecology, the entire separate A and I offspring phenotype distributions agree across m=0/3/6/12, although the two-locus joint distribution changes**. This works because permuting an I carrier within a quartet of adults with identical expressed M/I/A does not alter its trait-specific original parental-return lottery. It does alter which parental identities jointly carry standing A and I homologs. Model3 segregation still draws A and I homolog copies independently **conditional on the chosen parent pair**; nothing implies physical linkage or a covariance in signed segregation deviations.

A new source-pinned analytic auditor, [scripts/audit_chapter2_full_F1_joint_distribution_20261014.py](../scripts/audit_chapter2_full_F1_joint_distribution_20261014.py), computes the **complete conditional one-offspring A/I phenotype probability mass** on the exact 1/32 grid by integrating all original-model parent-pair weights and all 16 independent A/I maternal/paternal copy combinations. A separate [test implementation](../tests/test_chapter2_full_F1_joint_distribution_20261014.py) uses `numpy.bincount` rather than the primary `numpy.add.at` implementation. It evaluates 16 artificial source inputs × three original visitor contexts × four co-carrier treatments = **192 analytically integrated distributions**, with zero births and zero future updates.

**2026-10-14 exact-range correction (post hoc descriptive, NOT preregistered):** The earlier table understated ranges for contexts 3 and 4 and a test incorrectly demanded that every TV maximum be below 0.10. Recomputing each of the 16 artificial source profiles from the original Model3 reproductive equations and all 16 A/I homolog-copy combinations gives the corrected ranges below (context 3 max **0.10463431991308235**, source pool 8). The lower and upper values are retained as source-locked regression snapshots, not meaningful biological thresholds, significance cutoffs or estimates of natural island effects.

Independent calculation across those source inputs obtained the following m12-vs-m0 **joint-distribution total variation** ranges (0 = identical, 1 = disjoint), while the largest full *single-trait* marginal bin discrepancy across all artificial treatments was only ~2.5×10⁻¹⁴ (floating-point accumulation, acceptance tolerance 10⁻¹²):

| Original Model3 visitor context | Joint A/I F1 total-variation range, 16 artificial source inputs |
|---|---:|
| 0, no visitors | **0.030801659–0.083655115** |
| 3, matched visitor optima | **0.026796927–0.104634320** |
| 4, separated visitor optima | **0.030697584–0.089248021** |

The **joint law can differ while both univariate laws stay constant**. Thus founder genetic co-carriage may change the multivariate combinations available to selection without changing the t0 individual-trait distribution. But changing the *joint probability distribution* is neither selecting a beneficial A-up/I-down genotype over equally likely unfavorable sign combinations nor establishing sustained evolutionary-order reversal. Joint total variation also need not increase monotonically for every intermediate m=3 and m=6 synthetic input.

This is still an artificially quartet-matched Model3 t0 source law. It does not demonstrate a natural founder bottleneck effect, a full F1 *population* outcome, a 20-occupied-census adaptation history, or Q4 persistence. The exact-head native tests and scientific gate must pass before this supplement is treated as a reproducibly admitted technical result.
