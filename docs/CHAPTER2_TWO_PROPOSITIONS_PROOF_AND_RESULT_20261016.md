# Model 3 — Two propositions: evolutionary non-necessity and finite genetic accessibility (2026-10-16)

**Status:** source-verified and archive-reread scientific argument. This is a *retrospective synthesis*, not a newly randomized test, independent ecological model, empirical island confirmation, causal mediation result, or general theorem about natural mating systems. Original Q1/Q2/Q3/Q4 producers, frozen designs, original results, and original S1–S33 are unchanged.

**Machine-readable result:** [evidence receipt](CHAPTER2_TWO_PROPOSITION_EVIDENCE_RECEIPT_20261016.json). **Reproduction:** [read-only source and full original-Q1 archive admission](../scripts/audit_chapter2_two_propositions_20261016.py). No biological mutation or demography is simulated by this audit, except a *separate technical unit test* of the native Mendelian mutation-zero `inherit` operator.

## Proposition 1 — Assurance can change first, yet evolution of assurance is not necessary for an investment decline

Two **different original registered visitor-history cohorts in the same delayed-selfing + direct A cost 0.5 + mutation 0.01 biological setting** establish distinct logical components:

1. **Observed precedence:** among 64 independent synthetic visitor histories, A increased across the prespecified founder-relative 0.05 threshold before I decreased in **51/64** histories; visitor-history bootstrap95 **[0.687500,0.890625]**. At `0.025 / 0.05 / 0.10`, the assurance-first counts were **48 / 51 / 59**, according to [original independent confirmation](../data/results/chapter2_1005_confirmatory_replication_20261006.json). The cutoff also uses **20 consecutive censuses** and a **5-update near-simultaneous window**. This reports a *threshold-defined order*, not that the trait literally first mutated or that every individual experienced assurance first.
2. **Intervention-based non-necessity counterexample:** in the separately registered source-confirmation fixed-A intervention, setting A capacity at 0.5 still produced I(far) − I(near) **−0.43538938 [−0.45333049,−0.41719065]** across all 64 visitor histories. The larger four-setting 64-history experiment similarly reported A-fixed far−near differences **−0.441282, −0.301768, −0.330535, −0.433700**, with each historical interval fully below zero. Fixed A still **performs autonomous selfing at A=0.5**; this is an intervention on A *evolution*, not on the presence of selfing or pollinators.

These are **the same biological condition in (1)-(2), but not the same source histories, genotypes or paired realized genetic paths**. The logical conclusion is a counterexample to the claim that *A must evolve for lower visitor replenishment to generate lower investment*. It does not establish a universal ecological theorem that no species needs to change assurance before floral display can decline.

### Direct original-archive test of the founder-background gap

Original 2026-10-16 PR #569 source-run [#38853989138](https://github.com/zuizui0223/izu-core/actions/runs/38853989138) used **eight independently redrawn founder-genome populations × eight new synthetic visitor histories**, crossed within each of four mating rules. An independent reader re-extracted **32 original shard archives, validated all 1,088 original SHA-256 case receipts, and recomputed all 64 fixed-A near/far cells in each rule without running new biology**. Founder variation and visitor variation were resampled separately (9,999 resamples, the original bootstrap seed); 64 paired cells are not 64 independently sampled island populations. These **fixed-A bootstrap intervals are retrospective descriptive secondary readouts**, not the preregistered primary interaction confidence intervals.

| Original mating setting | **A fixed**: I(far)−I(near) at update 1000 (crossed 95%) | **A fixed**: I(far)−I(actual founder) (crossed 95%) | Negative far-vs-founder cells /64 |
| --- | --- | --- | ---: |
| Delayed, no direct A cost | −0.341988 [−0.395293,−0.288496] | **−0.217478** [−0.276050,−0.164674] | 63 |
| Prior selfing | −0.251546 [−0.314810,−0.186132] | **−0.277802** [−0.326139,−0.228902] | 64 |
| Pollen discount | −0.285850 [−0.358230,−0.206804] | **−0.286866** [−0.337550,−0.236655] | 64 |
| Direct A cost | −0.354941 [−0.415831,−0.298325] | **−0.219047** [−0.277394,−0.162133] | 62 |

All **eight founder-specific A-fixed far−near means** were negative in all four settings. This supports a **non-necessity** mechanism across these eight new founder/visitor backgrounds and independently verifies *absolute* investment decline from actual founder states, not just a negative environmental contrast. Since founder **and visitor histories** both changed, the successful transfer cannot isolate the effect of founder genetics from visitor effects.

**Distinct estimand warning:** in PR #569, the **A-evolvable minus fixed-A effect on the near/far contrast** passed for **three of four** settings and was **inconclusive under direct A cost** (+0.044271, interval [−0.044065,+0.130837]). Fixed-A non-necessity succeeding 4/4 **does not rescue** the four-setting generality of this separate A-evolution-mediated compression. The new far-arm E−F was **negative** in delayed control and direct A cost, so a universal relative preservation of far investment is not supported.

**Process evidence, not dynamic mediation:** a held-resident fixed-state local rare-mutant assay at visitor snapshot 400 reported an I return gradient +0.579 near versus −0.700 far under one delayed-selfing context, and the no-visitor/no-male-return limit has local `d log W/dI = −2 c_I I` when viable selfing is positive and (W propto exp(-c_I I^2)). This illustrates attraction benefits disappearing without evolving A. It is **not** an identification of the historical 1000-update E−F pathway; the finite and fixed-resident states differ.

## Proposition 2 — Initial allele support bounds, loss and segregating finite paths

### 2a. An exact theorem — but only without allele mutation and immigration

For a locus (L), write (S_t(L)) for the set of **allele values** carried by the **occupied** parental population at time (t). If every recruited child receives its locus copies exclusively from parents, and **that locus has no mutation and no seed immigration**, then

\[
S_{t+1}(L)\subseteq S_t(L)\subseteq S_0(L).
\]

Any inherited diploid phenotype (Z=(a_m+a_p)/2) and every positive-population average therefore remain in ([​\min S_0(L),\max S_0(L)]). In the particular original symmetric assurance-founder design (S_0(A)=\{0.5-h,0.5+h\}), a positive **mean** A-change exceeding (h) from the original 0.5 is **impossible without new alleles**. If the population goes extinct, there is no future occupied mean. The theorem does not assert that an event (d\le h) must occur, nor that all trajectories share the same initial allele set.

The source operator [`population.inherit`](../scripts/model3_island/population.py) directly transmits two sampled parental homologs before the optional mutation step. Parent retention/survival cannot add alleles. A unit regression test uses this exact native operator with `mutation_rate=0` and no immigrants to verify monotonic support for ten generations. This engineering test supports correct implementation of the theorem's premise; the theorem itself is not a numerical discovery.

### 2b. Irrecoverable support loss under the *same* no-I-mutation law, and its measured frequency

The separate 2,304-history original ecological-order/source-locked cohort prohibits **I-locus birth mutation and seed immigration**. In [directional access](../data/results/directional_access_20261013/READOUT.json), a **new future** founder-relative decrease of 0.05 in investment became unreachable **before single-allele fixation in 703 original histories**, and all those exclusions occurred with positive expressed variance. Of those **703**, one had **previously achieved an I event**; the meaningful count of pre-fixation excluded histories *without a prior event* is therefore **702**. This is not evidence that all lower-investment alleles or all small responses disappeared.

In **the same original 2,304 histories**, [the first-exclusion analysis](../data/results/low_allele_loss_20261014/extracted/READOUT.json) screened 1,238 observed **first-loss transitions**, and the needed lower-I allele's **conditional expected parental-weighted frequency increase was positive for 315/1,238** (negative for 923/1,238). The resulting child census inherited **zero** copies in all selected transitions. Finite parental sampling/Mendelian inheritance can fail to retain an allele *despite favourable source-state expected frequency response*. The 315 are **conditioned on actually losing the allele**, not the probability of loss when an allele is selected or a pure-drift share. They are not 315 extra independent populations.

Under locus mutation or immigrant I alleles the structural absorption is **not** permanent; the correct claim becomes a model-conditional **delay/failure within the finite horizon** unless the relevant no-mutation/no-arrival intervention persists.

### 2c. Allele half-width affects response order even when both widths make the threshold accessible

The [original 36-row `boundary_access_diagnosis`](../data/results/four_question_resolution_20261011/boundary_access_diagnosis.json) reuses **6,144 unique biological trajectories**, each retrospectively classified at three thresholds. At the smaller (d=0.025) event threshold, both initial symmetric A half-widths satisfy (d\le h) under a hypothetical **no-mutation** bound. Yet the observed all-start order scores change:

| Founder A half-width | Total starts | A-first | I-first | Score `(A-first − I-first) / starts` |
| --- | ---: | ---: | ---: | ---: |
| 0.046875 | 3,072 | 566 | 1,003 | **−0.142253** |
| 0.078125 | 3,072 | 944 | 268 | **+0.220052** |

The two fixed founder blocks × three synthetic visitor contexts contribute **six** paired cells per half-width; the sign contrast held across all six descriptive cells. The actual experiment has **active A mutation**, so this is **not** a mutation-free evolutionary theorem. Changing half-width changes **initial support and standing genetic variation simultaneously**, potentially also subsequent selection-genotype associations. This shows that **binary standing-allele reachability is not sufficient to describe observed event order**. It does **not** show that segregation variance alone uniquely mediates the sign flip, or establish a continuous ecological supply threshold.

At the original primary (d=0.05), the narrow (h=0.046875) initial support is **insufficient in the mutation-zero counterfactual**; nevertheless **2,944/3,072** original mutation-active trajectories achieved an A event. Confusing an allele-support theorem with the active-mutation simulation would be demonstrably incorrect.

### 2d. Prediction versus finite realization is a **separate** result, not identified mediation

In the original 320-history birth-mutation genotype-density/finite comparison, two low-supply, functionally matched contexts predicted A-first under conditional deterministic density, yet the finite histories realized A-first in only **3/32 and 2/32**, respectively; **all 64** focal finite histories remained occupied at update200. The additional A-only categories are **15/32 and 7/32** and must not be silently counted as A-first. Importantly, genotype-density closure is **not an exact stochastic finite-ABM expectation**: individual self-pollen exclusion and recruitment differ. The separate 703/315 access-loss cohort is **a possible biological route**, not a demonstrated unique explanation for these precise two 32-history discrepancies.

The tempting rounded tuple `selection −0.050 + parental sampling +0.022 + segregation/transmission +0.008 = realized −0.020` was **not source-matched here to the two specific 3/32,2/32 contexts with identical definitions**. It is **excluded** from the proof and from manuscript promotion pending that identification. Signed within-update retrospective identity components do not become a unique multi-generation causal-drift allocation.

## Editorial decision for the one-paper Letter

- **Strongest conditional claim:** observed A-first **precedence is not the evolutionary necessity** of A for reduced investment (historical registered evidence plus new 8-founder archive readback).
- **Exact genetic theorem:** standing **locus-specific allele support cannot enlarge** under no mutation/no immigration. Loss may close *future new* target responses before fixation.
- **Positive but bounded finite evidence:** initial A half-width changes threshold-defined ordering even at a target both standing ranges could support; original finite-genotype inheritance can lose favourable needed allele copies despite positive conditional expected frequency responses.
- **Open scientific mechanism:** selection/segregation/genotype dynamics may jointly explain order, but 2c has not uniquely isolated genetic variance and 2d's density–finite discrepancy has no individually identified genetic-loss mediator.
- **Never pool inference units:** historical Q1 64 histories, new 8×8 founders/visitors, original 6,144 half-width paths, source 2,304 allele-loss histories/1,238 selected transitions, and separate 320 finite-density comparisons are **distinct experiments or denominators**, not five independent confirmations of the same causal chain.

**Suggested manuscript placement:** Q1 Results adds a concise original-founder + eight-founder A-fixed non-necessity sentence. Q2 Results explicitly distinguishes half-width and threshold reachability. Q3 Results/SI includes theorem and loss-selected numerators without adding a causal explanation of 3/32. Preserve existing numerical figures, original SI bytes and the Q4 independent occupancy experiment. Keep the one manuscript unsubmitted until external data/DOI readiness and submitted metadata are solved.
