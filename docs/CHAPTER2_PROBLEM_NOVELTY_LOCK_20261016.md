# Model 3: problem statement and defensible novelty (2026-10-16)

**Scope.** This is an evidence-only editorial decision for the **single active, unsubmitted** Ecology Letters-format manuscript, `CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md`, stacked on [PR #565](https://github.com/zuizui0223/izu-core/pull/565). The introductory framing and three bibliography entries were updated; biological rules, runs, thresholds, figures, the original SI/source manifests and outcomes are not modified.

## Central question

**To what extent do finite diploid plant populations reproduce the predicted relative responses of floral investment and reproductive assurance under pollinator limitation, and when does genetic accessibility constrain a specified further response?**

An advantageous reproductive return, temporal first crossing, allelic accessibility, and population occupancy are separate estimands. The paper tests those distinctions in one explicitly specified Model 3, **not** a universal historical causal sequence for islands.

**Causal-identification status:** We observed a discrepancy between conditional genotype-density and original finite trajectories, and independently verified a genotype-support exclusion route in a different cohort. We did **not** identify why the two focal founder conditions produced 3/32 and 2/32 A-first histories. The density calculation is not the finite stochastic expectation; genetic-access exclusion from the other cohort cannot be assigned as its mediator. Therefore the paper's answer concerns **extent of predictability and a separately demonstrated boundary on attainability**, not a full causal decomposition of forecast failure.

## Closest primary literature and negative priority claims

| Precedent | Already established | Defensible difference in Model 3 |
| --- | --- | --- |
| [Sakai 1995](https://doi.org/10.1111/j.1558-5646.1995.tb02287.x); [Morgan & Wilson 2005](https://doi.org/10.1111/j.0014-3820.2005.tb01050.x) | Joint floral attraction/selfing allocation and pollination-dependent mating evolution | Prospectively fixed-versus-evolvable A-capacity intervention with independently inherited I; **not** first coupled allocation theory |
| [Bodbyl Roels & Kelly 2011](https://doi.org/10.1111/j.1558-5646.2011.01326.x); [Teixido & Aizen 2019](https://doi.org/10.1093/aob/mcz014) | Experimental pollinator-loss autogamy, sequential interpretation, and reduced floral-size selection under reproductive assurance | A model-specific test separating observed A-first **precedence** from the **necessity** of A evolution for I decline |
| [Lepers, Dufay & Billiard 2014](https://doi.org/10.1111/evo.12533) | Deterministic and stochastic individual-based selfing/pollinator models **already existed**; original studied settings reported similar outcomes | Independently inherited diploid I/A genotype support, named response-order classes and conditions for predictive disagreement. Not a claim to invent stochastic mating models |
| [Peterson & Kay 2015](https://doi.org/10.1086/679107); [Sachdeva 2019](https://doi.org/10.1111/evo.13812) | Individual-based founding, persistence, adaptation, selfing and genetic constraints | Explicit threshold-defined **order of two floral/reproductive responses** under matched model contexts, distinguished from persistence |
| [Barrett & Schluter 2008](https://doi.org/10.1016/j.tree.2007.09.008); [Busch et al. 2022](https://doi.org/10.1111/evo.14572); [Hartfield & Glémin 2024](https://doi.org/10.1371/journal.pgen.1011312) | Standing variation, genomic variation loss, segregation and polygenic adaptation under selfing | Specific allele sets necessary for a **further founder-relative I change** are followed through finite parental contribution and Mendelian inheritance. Not first evidence of genetic variation depletion |

This is a **targeted nearest-precedent review** (building on [the full-text Lepers audit](CHAPTER2_LEPERS_FULLTEXT_PRIORITY_CORRECTION_20261015.md) and [critical prior-art audit](CHAPTER2_CORE_PRIOR_ART_CRITICAL_AUDIT_20261015.md)), not a comprehensive review or worldwide priority certificate.

## Claims ranked by verification and biological novelty

### N1 — Primary bounded contribution: predicted order is not assured by survival

In the original birth-mutation ten-context comparison, deterministic genotype-density propagation predicted assurance-first (A-first) in **two** matched low-visitor-supply founder contexts. Among **32 native finite diploid histories per founder**, only **3/32** and **2/32** met the prospectively registered 0.05-change, 20-consecutive-census response-order definition. **All 64 original histories remained occupied at t200.** The additional **15/32 and 7/32 A-only** responses are not A-first. Source: [verified source and main-figure gate](CHAPTER2_Q3_ATOM_MAIN_FIGURE_20261016.md), [320 native original diploid-genome admission](CHAPTER2_Q3_ORIGINAL320_NATIVE_GENOME_ADMISSION_20261016.md).

This is **conditional predictive disagreement**, not a mathematical expectation mismatch test: the density closure is not the exact ABM stochastic expectation. The event labels vary with threshold (notably 0.025 and 0.1); two founder states are not 64 independent islands; the observed discrepancy is not a pure-drift effect size.

### N2 — Mechanistic source cohort: genetic reachability can close before fixation

In a *separate* 2,304-history fixed-access original cohort (**no new I mutation and no seed immigration**), **703** histories first lost access to a **future new** founder-relative investment decline of at least 0.05 **before fixation**, with positive expressed I variance still present. **One** of those 703 had already attained an earlier I event; 702 had not. In the **same original 2,304 histories**, 1,238 first-exclusion transitions were observed; in **315/1,238**, the needed low-I alleles had positive *conditional expected* parental-weighted frequency change immediately before finite offspring inherited zero copies. These **outcome-selected** 315 transitions are not an unconditional loss probability under positive selection, and do not identify the cause of N1. Sources: [separated source-unit map](CHAPTER2_Q3_SELECTION_REALIZATION_SOURCE_MAP_20261015.md), [genetic-access boundaries](CHAPTER2_Q3_FINITE_GENETIC_ACCESS_AND_REALIZATION_20261015.md).

### N3 — Registered reproductive baseline: precedence is not necessity

In the original four-setting, 64-independent-visitor-history experiment, investment declined under lower visitor replenishment even with assurance **capacity fixed at 0.5** (4/4 reproductive settings). Letting A-capacity evolve compressed the near/far investment divergence with an interaction of **+0.1007 to +0.2200** (4/4). Fixed capacity did **not** disable actual selfing; this is a counterfactual evolutionary effect within Model 3, not a theorem about all natural plant systems. Source: [frozen result](../data/results/chapter2_assurance_generality_20261006.json).

### Independent Q4 rather than a proven mediator

The separate **32-history** occupancy stress experiment reported a conditional A-evolvability × historical visitor-environment interaction of **+10.84 percentage points** (95% interval +6.54 to +15.14). A separately controlled fixed-B K comparison yielded a **+0.775-point** effect. Neither establishes that Q2's spontaneously evolved A-first sequence rescues populations, nor decomposes N1 into genetic and demographic mechanisms. Source: [Chapter 2 core synthesis](CHAPTER2_CORE_CLAIMS_SYNTHESIS_20261015.md).

## Claims the one-paper Introduction/Discussion must not make

- No first stochastic/individual-based model of plant mating-system evolution, or first discovery of standing-variation loss.
- No general “A must evolve before I can decline”: the four-setting intervention explicitly tests and rejects that *necessity* in this model, while allowing selfing.
- No statement that **all** flower-investment decrease stops after threshold-specific allele loss; the conclusion concerns a specified **new further ≥0.05 response**, with no I mutation/immigration.
- No causal claim that 315/1,238 favorable expected changes quantify selection against drift, or that the 703-path mechanism *explains* the distinct 320-path contrast.
- No conflation of time-200 occupancy with indefinite persistence, or of near/far visitor replenishment with real mainland/island geography.
- No natural A-first-induced rescue, universal threshold, observed island history, deposited DOI or submitted paper.

## Manuscript logic locked for review

1. **Introduction:** separate expected reproductive return, order, genetic attainability and occupancy; concede known selfing/flower-allocation and stochastic model antecedents.
2. **Results/Figs 1–2:** Q1 mechanisms and independently registered fixed/evolvable A test; Q2 threshold-dependent ordering.
3. **Results/Fig 3:** the original 320-path mutation-aware finite/density comparison as the **main visual Q3 result**; N2 pedigree accounting is distinct supporting evidence.
4. **Fig 4/Discussion:** independent demographic scope, strong nulls and the absence of order-mediated rescue identification.
5. **Ecological message:** persistent populations can still be missing a predicted evolutionary pathway under specified pollination and genetic conditions; no direct reconstruction of island floral evolution.

**Submission status:** still working-draft only. Original Figure 3/source quality review is under PR #565. An independent DOI-backed external source deposit and author/license/version/access approval remain blocked by [Issue #436](https://github.com/zuizui0223/izu-core/issues/436).
