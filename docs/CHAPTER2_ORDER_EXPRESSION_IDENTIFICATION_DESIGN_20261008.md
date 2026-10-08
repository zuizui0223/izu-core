# Chapter 2 — Can trait-expression order change the realization and survival of island adaptation?

**2026-10-08 — prospectively specified, DESIGN ONLY.** This branch contains a testable experimental contract and a non-peeking cohort compiler. There are **no new biological simulations**, no new visitor histories, no estimated effects, and no approval to launch the production workflow. This is separate from, and does not modify, Draft PR #414.

## Decision from the existing results

1. **Established (merged #411):** Pollinator-replenishment limitation reduces floral investment even when assurance evolution is blocked. Allowing assurance evolution reduces the near–far investment gap in all four reproductive settings, mostly through extra investment decline in the near/high-replenishment treatment.
2. **Established only within a bounded synthetic stress envelope (Draft #413):** the independent 32-history relative-persistence interaction for past assurance-evolution opportunity is positive, +0.108398 [history-bootstrap95 +0.065430, +0.151367]. The stress envelope and eight-founder bottleneck are not measured natural-island risks.
3. **Failed priority confirmation (Draft #413):** the independent 16-history test that originally predicted a prior-selfing versus pollen-discount mutational-priority interaction **FAILED**. A separate balanced-mutation-duration four-history screen averaged zero across four mating settings. These outcomes cannot be reinterpreted as support for a general “selfing first rescues the island” mechanism.

The central unanswered mechanism is not merely which response is favoured or which allele is first detected. It is whether **experimentally ordered changes in the reproductive phenotype**, with equal prescribed cumulative expression exposure and a common future, causally change (i) inherited evolution and (ii) finite population persistence.

## The four connected stages

| Stage | Observable quantity | What a positive result would — and would not — mean |
|---|---|---|
| **Threshold / 閾値** | Corrected local rare-mutant marginal investment gradient, separated into maternal outcross, paternal export, selfing displacement and cost, across synthetic visitor environments | Selection-benefit sign change; **not** an automatic population change point or calibrated Izu threshold |
| **Order / 順序** | Randomly assigned transient expression schedule for A and I, plus separately recorded spontaneous genotype-change order | Identification of the *assigned schedule* effect; **not** manipulation of naturally realized genetic order |
| **Realization / 実現** | Diploid allele means, variances, threshold-crossing time after release, and extinction before the future stress test | Whether evolution actually occurred within surviving finite histories; avoid survivor-only bias |
| **Consequence / 帰結** | 80-update occupancy, first extinction, viable maternal outcross, viable selfed contribution, paternal export and retained genetic variance | Bounded model-specific consequences of expression-order assignment; not proof of a general natural-island rescue law |

## New experimental intervention

Do **not** reuse the previously failed mutation-access order as if it directly controlled phenotypic order. In the previous experiments, early mutation access also conferred a longer allele age under selection; equal mutation supply did not force equal evolutionary histories.

Instead, explicitly intervene on **transient expressed phenotype**, while allowing the *underlying inherited A and I loci to mutate and segregate identically in all arms*. At each reproductive update, the payoff operator must use

```text
expressed_z = inherited_mean EXACTLY if assigned_logit_offset == 0\nexpressed_z = logistic(logit(clip(inherited_mean, 1e-8, 1-1e-8)) + assigned_logit_offset) otherwise
```

for each target axis, with no mutation, inheritance, overwriting, replacing or resetting of actual diploid allele states by the assigned offset. Matching X is not directly perturbed. The clamped endpoint numerics must be tested independently before any biological run. All arms share the source founders, visitor sequences and nested demographic random-number identifiers.

The schedule is four consecutive 100-update phases:

| Assigned arm | t0–100 | t100–200 | t200–300 | t300–400 |
|---|---|---|---|---|
| Assurance first | A +0.45 | A +0.45, I −0.45 | I −0.45 | No offset |
| Investment first | I −0.45 | A +0.45, I −0.45 | A +0.45 | No offset |
| Synchronous timing control | Both offsets | No offset | Both offsets | No offset |

**Overlap distinction:** A-first and I-first both have exactly 100 A-only, 100 I-only and 100 joint A×I updates; the only scheduled difference in the primary pair is which single-trait block comes first. The synchronous comparator has 200 *joint* A×I updates and no single-trait-only block, despite matching each individual trait's total exposure. It is a secondary schedule-profile control, not a pure order-matched negative control. Any synchronous-versus-sequential survival difference confounds order with co-expression duration.

These numbers are dimensionless **logit shifts**, not changes in the measured natural phenotype of an island plant. Every arm has **200 assigned updates** of the same A perturbation and **200** of the same I perturbation. This equalizes scheduled offset duration and magnitude, **not** realized mean phenotype, time of selection, accumulated fitness or achieved inherited states. That difference is the mechanistic object we intend to study, not a defect to “correct” after looking at outcomes.

The final 100 updates have no imposed offset. Thereafter, every source population enters exactly the same 80-update future visitor, mutation and expression rules. A visitor-history-matched eight-founder, capacity-eight stress is the prespecified primary scenario. A no-founder-bottleneck, capacity-48 scenario is a compulsory secondary comparator. Both cover ovule budgets 0.5, 1, 2, 3, 4, 5, 8 and two future visitor regimes. Zero immigration. Source populations already extinct at transfer contribute 0 occupancy; they are not discarded.

## Independent unit and fixed scope

The **64 new visitor histories 37110801–37110864** are independent environmental replicates and are distinct from PR #411, PR #413 and PR #414 seeds. Two demographic replicates are nested *within* each history. Four mating settings, near/far pre-environment and three assigned order arms are paired.

- Prehistory populations: 4 mating rules × 2 pre-environments × 3 schedules × 64 visitor histories × 2 nested demographic repeats = **3,072**.
- Future branches: 2 stress regimes × 7 ovule budgets × 2 visitor environments = **28** per actual inherited prehistory.
- Declared posthistory trajectories: **86,016**; these are **not** 86,016 independent ecological units.

The protocol compiler lives in `scripts/plan_chapter2_order_expression_identification.py`, the frozen contract in `data/design/chapter2_order_expression_identification_20261008.json`, and negative/positive logic tests in `tests/test_chapter2_order_expression_identification.py`. The plan compiler computes case identities and log-budget integration weights only. No new biological outcome is produced.

## Prospective primary estimand and decision

Define `S` as the binary terminal occupancy after 80 future updates, integrated over **all seven** ovule budgets on their natural-log grid, averaged over both future visitor environments and the two nested demographic repeats. For every independent visitor history `h` and mating rule `s`, compute

```text
Delta[h,s] = (S[A_first, far] - S[I_first, far])
           - (S[A_first, near] - S[I_first, near])
```

with all four mating rules pooled **equally within each visitor history**. Bootstrap the **64 visitor histories**, 9,999 draws, seed 3711082026; share resampling indices across all settings and contrasts. Do not bootstrap 86,016 branches as independent.

The preregistered test is **two-sided**. We do not choose a favourable A-first direction based on the failed #413 test. Count the pooled schedule effect as supported only when the percentile 95% history-bootstrap interval excludes zero **and** absolute mean effect is at least 0.05 on the occupancy scale. A full interval inside (−0.05,+0.05) permits **equivalence within this declared region**; all other cases are inconclusive. Setting-specific effects are mandatory regardless of the pooled sign. Report the far and near *absolute* survival contrasts too, so a difference-in-differences sign is not mistaken for survival rescue.

**No redefinition of the 0.05 effect threshold, stress budgets, comparison arms or independent-history denominator after new outcomes.** Secondary post-outcome threshold-crossing categories do not enter the primary randomized intention-to-treat analysis.

## Annual inherited realization audit (implemented; not yet production-wired)

The independent recorder in `scripts/chapter2_order_genetic_realization.py` now takes a **real diploid `PlantState` at every annual census t0–400** and detects each locus's first absolute departure of at least 0.05 from its actual founder mean. It records six descriptive categories: A before I, I before A, A only, I only, tie and neither. After extinction, genetic trait values are **missing**, not zero; the first extinction census is separately retained. Offset phenotypes never enter the genetic crossing calculation. A skipped, duplicated or out-of-order annual observation is rejected. See `tests/test_chapter2_order_genetic_realization.py` for constructed edge cases.

The recorder is a **measurement component**, not a new inferential treatment or confirmation. In particular, the randomized primary intention-to-treat persistence contrast must include all 64 histories whether A or I ever crosses the genetic threshold, and regardless of extinction. Actual historical order is a post-treatment variable and may not be used to select or reweight the primary survival sample.

The existing two-year legacy smoke and all annual-crossing tests are non-prospective engineering tests; there is still **no production runner** writing this information for the new 3,072 ancestry groups.

## The identification line that must not be crossed

Randomized phase assignment makes the **effect of the expression-order protocol** identifiable within this model under successful pairing. Separately, record the inherited diploid A and I population means **at every update t0–400** and classify the first absolute 0.05 departure from each arm's actual t0 founder means, distinguishing A first, I first, one only, ties and neither. No transient imposed phenotype shift is permitted to count as a genetic crossing. The five coarse checkpoints alone are insufficient to recover first-crossing order. It does not identify the causal effect of an *observed naturally evolved trait order*. The latter is a post-treatment realized property of mutation, standing variation, selection and demographic noise. Conditioning on “A actually crossed first” would select survivors and favorable histories.

The first-order mechanistic question is whether the two schedules produce different future outcomes. Only *after* a successful independently confirmed schedule effect would it make sense to test genotype/variance mediation with separately declared full-diploid state swaps or matched expression histories. A genotype transplant alters joint state distributions and potential pedigree covariance, and cannot be called pure natural mediation without added identification assumptions.

The old independent16 FAILED result retains its original evidential rank. A new assigned-expression protocol is a **different intervention**, not a post-hoc rescue of that failure.

## PDE and field-evidence limits

Finite ABM extinction is required to answer whether response realization can lose the race to demographic stochasticity. A deterministic density / PDE comparator is **optional and inadmissible until its numerical representation of positive-mutation, full-genotype inheritance is independently validated**. It should not be a condition for declaring the ABM experiment operational, and disagreement must not be automatically framed as biological drift without checking discretization and operator parity.

The natural-island tests need pollination effectiveness, mating-system assays, inherited genetic transitions, and actual demographic recruitment linked at compatible population × time units. Neither Chapter 1 cross-sectional island trait summaries nor Chapter 3 Campanula morphology measures independently establish the A/I longitudinal order or this model's stress distribution.

## Next executable gate

**Do not run the 86,016-case prospective cohort yet.** The canonical Model 3 reproduction operator still reads directly from diploid alleles. A versioned **opt-in** experimental payoff operator and its genotype-safe phenotype transformation are now maintained outside `scripts/model3_island/`, with exact zero-offset parity and dedicated unit tests (`scripts/chapter2_order_expression_phenotype.py`; `tests/test_model3_expression_override.py`). The isolated payoff adapter (`scripts/chapter2_order_expression_payoff.py`) and pure expression adapter (`scripts/chapter2_order_expression_phenotype.py`) are implemented **outside** the canonical `scripts/model3_island/` source tree. Source-parity, conservation and immutable-genotype tests are authored in `tests/test_model3_order_expression_reproduction.py` and `tests/test_model3_expression_override.py`. A pure schedule resolver (`scripts/chapter2_order_expression_schedule.py`) and OLD-HISTORY-only two-update Mendelian-recruitment smoke (`tests/test_chapter2_order_expression_engineering_smoke.py`) exercise the complete expression→reproductive ledger→inheritance call chain on visitor history 26110601. GitHub CI must still verify them. A production case runner and audited 3,072 source states/86,016 descendants **do not yet exist**, and no new cohort outcomes have been generated. Before launch, a distinct engineering PR must (1) wire an opt-in expression override into the reproductive payoff operator without modifying allele inheritance, (2) show that zero offsets reproduce existing biology exactly, (3) verify paired random histories and equal assigned doses, (4) benchmark cost and raw-data retention, and (5) freeze the code SHA and artifact plan. **Do not patch the shared `scripts/model3_island/reproduction.py` in this design PR:** merged PR #414 freezes a separate pending biological cohort against its existing Model 3 source. The expression-order experiment must use a versioned opt-in implementation with independent provenance rather than silently changing PR #414's source biology. PR #414 has now been **merged** following green CI/scientific checks; its distinct 64-history unified payoff–evolution–persistence biological campaign is still unexecuted. This order-expression design must not reuse its visitor histories or infer results from its merge.
