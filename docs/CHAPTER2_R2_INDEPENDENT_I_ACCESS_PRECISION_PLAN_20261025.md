# Chapter 2 R2 — independent I-access × pollinator-service confirmation: design precision only

**Date: 2026-10-25. Status: DESIGN ONLY / NOT AUTHORIZED / NOT PREREGISTERED.** This note is a proposed extension to `docs/protocols/CHAPTER2_R2_HISTORY_POLLEN_STATE_NEXT_STUDY_PROPOSAL_20261023.json`; it neither changes the canonical proposal nor schedules biological GitHub Actions. The previous R2 four-setting independently crossed overall outcome remains **INCONCLUSIVE**. The registered R1–R5 evidence ranks and R4 G/S remain intact.

## Current source-backed conclusion vs unanswered question

The [original 384-path experiment](https://github.com/zuizui0223/izu-core/actions/runs/39233450099), 12 founder IDs with nested repeats, has been independently source-audited through merged PRs #630–#637. In the *retrospectively selected* A/M-fixed and I-polymorphic **22 matched strong-prior-pollen source states (11 unique founder IDs)**, pollen decline caused positive expected **lowest numerical I allele** next-generation transmission in **22/22**, but the minimum originally available I allele ultimately fixed in **20/22**. Two populations with initial **4/96 and 6/96** minimum-I copies instead lost those alleles. Detailed original ancestry/genotype paths show positive expected lowest-I parental transmission during each segregating year, despite eventual stochastic loss. These are original Model 3 case observations **not** 22 independent or newly registered tests.

The nontrivial new question is therefore *not* simply whether a less effective pollinator environment can select for reduced floral investment. It is:

> When Model 3 favors transmission of a low-I allele, how does **independently specified genetic availability at the shock** change the probability and timing of losing that allele, under matched visitor activity, founder genomes, pollen transfer and demographic randomness?

The original observed 4/96, 6/96, and ≥16/96 copy gap must **not** be reverse-engineered into a universal 10% cutoff. It is a discovery from an already exposed subset, not preregistered effect-size or eligibility input.

## Proposed experiment, not yet frozen

Each **independent founder genome** is crossed with each **independently generated visitor history**, and an independent demographic replicate is nested within a founder×visitor cell. One original t30 state is built for each founder×visitor×demographic triplet, then branched into two **genetic-access interventions** and, within each access intervention, two *current visitor-activity* futures. Control and decline share the identical full t30 source genotype *within an access treatment*, and reproducible paired random streams. Neither founder nor visitor history may reuse the exposed R2 12-founder source axis, or the historical 8×8 source axes used in the earlier Q1/R2 registrations.

The number of new founder sources `F`, new visitor histories `V`, demographic continuations `R`, exact new source seed namespaces, and the lower/higher initial genetic-access states are **not decided**. The proposed conceptual factorial uses **2 access × 2 activity futures**, 30 original-style pre-shock updates, and 50 subsequent updates, but even these details remain conditional on author review, feasibility and registration.

**Critical confounding guard:** changing the number of minimum-I allele copies generally also changes mean I, heterozygosity and genetic covariance with A/M. Even adding a third I allele to compensate the starting mean changes the allele composition/variance. It is scientifically invalid to call a founder genome modified in this way a **pure low-I access intervention** while assuming all other genetic dimensions are unchanged. An implementation must report manipulated mean/variance/I–A/M covariance, allele origins and per-mother pollen receipt; if these cannot be matched or adjusted appropriately, the claimed causal quantity must be renamed as the **compound access/genetic-background treatment**.

The visitor-activity contrast must be interpreted through the **actual native per-mother pollen-delivery quantity q**, not activity scalar, global pollen export, or presumed equal pollen receipt. The native reproduction operator includes both paternal and maternal outcross contributions and viable selfing.

## Exactly defined first-event outcomes (proposed, not registered)

A population can lose the minimum numerical I allele, become fixed for it, go extinct, or remain segregating at the horizon. **Treat these as distinct states**. Inspect first post-fork census with (i) `low_I_copy_count = 0`, (ii) `low_I_copy_count = 2N(t)`, or (iii) `N(t)=0`; extinct trait means are **undefined**, never zero.

Maintain **all assigned** founder×visitor×demographic sources in the allocation table. Report whether a low allele was initially accessible (`0 < low_I_copy_count(t30) < 2N(t30)`), and show noneligible genetic access/failed intervention and extinction separately without removing such starts silently. A cause-specific cumulative incidence of low-I loss before extinction is one proposed endpoint; there must also be an all-start occupancy and genetic-access summary.

One possible primary interaction **only for genuinely predeclared, genetically at-risk matched sources** is

[
D(a)=L(a,mathrm{decline})-L(a,mathrm{maintained}), quad
H=D(mathrm{higher access})-D(mathrm{lower access}),
]

where `L = 1` if the minimum-I allele is lost by t80 before extinction, else 0, with extinction separately labelled as a competing event. `D(a)` lies in `[-1,1]`, and `H` lies in `[-2,2]`. The prospective primary estimand, causal interpretation, initial I-access feasibility, multiplicity rule, threshold for a meaningful H, and exact source-level analysis remain **unapproved**.

A separate discriminating experiment would hold the *entire genotype, activity, visitor history and shock-time copy counts* fixed while sampling independent demographic continuations. Diversity of endpoints in that experiment would establish realized stochastic dependence; it would **not** assign a unique proportion to neutral drift, selection, or genotype correlations.

## Source-crossed precision illustration — not achieved power

Under explicitly hypothesized **independent fresh founder sources**, **independent fresh visitor-history sources**, and **conditionally independent source-cell demographic stream primitives**, changing one founder, visitor source or nested demographic stream changes the average `H` by at most `4/F`, `4/V` or `4/(FVR)`. McDiarmid’s inequality gives an illustrative, distribution-free **two-sided 95% radius**

[
h_H=4sqrt{rac{ln(40)}{2}
left(rac{1}{F}+rac{1}{V}+rac{1}{FVR}ight)}.
]

For a within-access paired loss-risk difference, replace 4 with 2. These are **uncapped and very conservative** radii. They do not claim random-effect variance estimates, statistical power, exact confidence-interval coverage for correlated/pseudorandom sources, or known biological effects. In particular, `F×V×R` is **not** the count of independent source systems.

| Purely illustrative F×V, nested R | Uncapped radius for paired D | Uncapped radius for interaction H | Nominal Model 3 update-equivalents |
|---|---:|---:|---:|
| 16×16, R=1 | ±0.975 | ±1.950 | 58,880 |
| 32×32, R=2 | ±0.682 | ±1.363 | 471,040 |
| 64×64, R=4 | ±0.481 | ±0.961 | 3,768,320 |
| 128×128, R=4 | ±0.340 | ±0.679 | 15,073,280 |
| 256×256, R=4 | ±0.240 | ±0.480 | 60,293,120 |
| 512×512, R=4 | ±0.170 | ±0.340 | 241,172,480 |

*Nominal update-equivalents* assume `F×V×R×(30 + 2 access × 2 activity × 50 updates)`. This counts work in an illustrative allocation, **not** a measured CPU time or approved dispatch budget. The table is **not a recommendation to launch any row**. More demographic repeats barely improve the upper bound if the independent founder and visitor axes remain small. Achieving useful precision or power requires a predeclared effect size, independent-axis variance or appropriate pilot information from **fresh** sources, and a realistic computational budget. The exposed old 384 paths are unsuitable for independent replication power guarantees.

## Explicit no-dispatch gates and next actionable deliverable

The machine-readable extension is `docs/protocols/CHAPTER2_R2_INDEPENDENT_I_ACCESS_PRECISION_DESIGN_20261025.json`. The read-only numerical verifier is `scripts/audit_chapter2_r2_independent_i_access_precision_20261025.py`, and fail-closed tests are `tests/test_chapter2_r2_independent_i_access_precision_20261025.py`. Its checks require **all canonical proposal and extension run-gate values to remain false**, old 384-path sources to remain exploratory, and sample-size/meaningful-effect/source-SHA/author approval entries to remain unresolved.

The **next design work** is a deterministic, source-free I-access *feasibility specification* (what properties can simultaneously be matched at t30); then two-source-axis variance/precision design that states an intended meaningful interaction effect and an author-approved computational budget. Both can be prepared without dispatching biological futures. Only after these decisions, protocol freeze and explicit author signoff may a separate authorized execution workflow be considered.

**Current verdict:** no independent new data; no natural-island experiment; no preregistered fixation threshold; no author approval; **no new biological population updates**.
