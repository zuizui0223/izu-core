# Chapter 2 — Can trait-expression order change the realization and survival of island adaptation?

**2026-10-08 — prospectively specified, DESIGN ONLY.** This branch contains a testable experimental contract and a non-peeking cohort compiler. There are **no new biological simulations**, no new visitor histories, no estimated effects, and no approval to launch the production workflow. This is separate from, and does not modify, Draft PR #414.

## Decision from the existing results

1. **Established (merged #411):** Pollinator-replenishment limitation reduces floral investment even when assurance evolution is blocked. Allowing assurance evolution reduces the near–far investment gap in all four reproductive settings, mostly through extra investment decline in the near/high-replenishment treatment.
2. **Established only within a bounded synthetic stress envelope (Draft #413):** the independent 32-history relative-persistence interaction for past assurance-evolution opportunity is positive, +0.108398 [history-bootstrap95 +0.065430, +0.151367]. The stress envelope and eight-founder bottleneck are not measured natural-island risks.
3. **Failed priority confirmation (Draft #413):** the independent 16-history test that originally predicted a prior-selfing versus pollen-discount mutational-priority interaction **FAILED**. A separate balanced-mutation-duration four-history screen averaged zero across four mating settings. These outcomes cannot be reinterpreted as support for a general “selfing first rescues the island” mechanism.

The central unanswered mechanism is not merely which response is favoured or which allele is first detected. It is whether **experimentally ordered changes in the reproductive phenotype**, with equal prescribed cumulative expression exposure and a common future, causally change (i) inherited evolution and (ii) finite population persistence.



### Joint investment and assurance threshold diagnostics

The unforced t300/t400 snapshot function now records **both** investment and assurance local gradients and the analytic investment-cost and assurance-cost sign-change thresholds from the original fixed-monomorphic-resident rare-mutant formulation. The investment decomposition is checked against its total; these are local counterfactual benefits at a resident mean, not direct estimates of selection across the segregating finite population. At trait boundaries or nonpositive monomorphic invasion fitness, the interior threshold values are **null with an explicit reason**, never automatically set to zero. These records do not gate or retune the preregistered primary assigned-order survival contrast. Synthetic old-history tests are in `tests/test_chapter2_order_local_thresholds.py` and have not sampled the new independent visitor cohort.

## The four connected stages

| Stage | Observable quantity | What a positive result would — and would not — mean |
|---|---|---|
| **Threshold / 閾値** | Corrected fixed-resident rare-mutant marginal investment **and assurance** gradients, investment/assurance cost thresholds and decomposed maternal/paternal/selfing returns across synthetic visitor environments | Local selection-benefit sign change; **not** an automatic population change point, an observed finite-population selection coefficient or a calibrated Izu threshold |
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

## Annual inherited realization audit (production runner authored; not executed)

The independent recorder in `scripts/chapter2_order_genetic_realization.py` now takes a **real diploid `PlantState` at every annual census t0–400** and detects each locus's first absolute departure of at least 0.05 from its actual founder mean. It records six descriptive categories: A before I, I before A, A only, I only, tie and neither. After extinction, genetic trait values are **missing**, not zero; the first extinction census is separately retained. Offset phenotypes never enter the genetic crossing calculation. A skipped, duplicated or out-of-order annual observation is rejected. See `tests/test_chapter2_order_genetic_realization.py` for constructed edge cases.

The recorder is a **measurement component**, not a new inferential treatment or confirmation. In particular, the randomized primary intention-to-treat persistence contrast must include all 64 histories whether A or I ever crosses the genetic threshold, and regardless of extinction. Actual historical order is a post-treatment variable and may not be used to select or reweight the primary survival sample.

The old-history smoke and annual-crossing tests are non-prospective engineering tests. The prospective prehistory runner now **has code paths** to write this information for all 3,072 source groups, but those branches are unexecuted, and the CI results for the latest head have not been admitted.

## The identification line that must not be crossed

Randomized phase assignment makes the **effect of the expression-order protocol** identifiable within this model under successful pairing. Separately, record the inherited diploid A and I population means **at every update t0–400** and classify the first absolute 0.05 departure from each arm's actual t0 founder means, distinguishing A first, I first, one only, ties and neither. No transient imposed phenotype shift is permitted to count as a genetic crossing. The five coarse checkpoints alone are insufficient to recover first-crossing order. It does not identify the causal effect of an *observed naturally evolved trait order*. The latter is a post-treatment realized property of mutation, standing variation, selection and demographic noise. Conditioning on “A actually crossed first” would select survivors and favorable histories.

The first-order mechanistic question is whether the two schedules produce different future outcomes. Only *after* a successful independently confirmed schedule effect would it make sense to test genotype/variance mediation with separately declared full-diploid state swaps or matched expression histories. A genotype transplant alters joint state distributions and potential pedigree covariance, and cannot be called pure natural mediation without added identification assumptions.

The old independent16 FAILED result retains its original evidential rank. A new assigned-expression protocol is a **different intervention**, not a post-hoc rescue of that failure.

## PDE and field-evidence limits

Finite ABM extinction is required to answer whether response realization can lose the race to demographic stochasticity. A deterministic density / PDE comparator is **optional and inadmissible until its numerical representation of positive-mutation, full-genotype inheritance is independently validated**. It should not be a condition for declaring the ABM experiment operational, and disagreement must not be automatically framed as biological drift without checking discretization and operator parity.

The natural-island tests need pollination effectiveness, mating-system assays, inherited genetic transitions, and actual demographic recruitment linked at compatible population × time units. Neither Chapter 1 cross-sectional island trait summaries nor Chapter 3 Campanula morphology measures independently establish the A/I longitudinal order or this model's stress distribution.

## Next executable gate

The complete **production runner code is authored but NOT EXECUTED**:

- `scripts/chapter2_order_prehistory_runner.py` saves full t400 diploid `PlantState` archives (alleles, origin, mutation flags, ids, birth years), **each recruited child's generation/ID plus its two parental IDs**, 401 inherited annual censuses, extinction time, payoff checkpoints, and SHA-256 case/source receipts. The fork reader independently authenticates the original 48 founder IDs **and their deterministic original diploid alleles against the frozen biological source**, verifies the chronological parentage graph, rejects same-generation parental assignments, and requires all terminal individuals to be traceable to recorded founders. Terminal genotypes and file checksums alone are not treated as substitutes for these biological provenance checks.
- `scripts/chapter2_order_postshock_runner.py` restores only those hash-verified states and forks 28 zero-expression, same-future-evolution poststress cases per source, keeping common random-number identifiers across historical expression orders.
- `scripts/chapter2_order_confirmatory_readout.py` requires ALL 3,072 source populations and ALL 86,016 postshock cases, recomputes genetic-order events from the annual traces, checks the t400 genotype mean against the archived alleles, checks bottleneck founders, future regime occupancy, and applies the preregistered **64 visitor-history-level two-sided ITT** with full 7-budget ×2 future-visitor sensitivity.
- `tests/test_chapter2_order_full_archive_smoke.py` tests old history 26110601 only, full t400 →28 forks → audit and corrupted-summary rejection. `tests/test_chapter2_order_itt_synthetic.py` tests purely algebraic success/equivalence gates; neither is evidence from the new cohort.
- `.github/workflows/chapter2-order-expression-cohort.yml` is **manual workflow_dispatch only**, with 64 prehistory shards, 64 corresponding future shards and a fail-closed whole-cohort readout. Before any fresh histories, preflight runs `scripts/audit_chapter2_order_engineering_cost.py` on the archived history 26110601 and retains a standalone runtime/size/provenance receipt; extrapolation from one historical case is only an engineering diagnostic, not a production-time guarantee. It cannot be started from this Draft PR as a default-branch workflow. Even after a later merge, full execution is restricted to `main`, requires a true `full_cohort_launch_approved` manual input, and requires the user-entered reviewed `source_commit_sha` to exactly match the checked-out GitHub commit. The source approval is an operational launch guard, not a biological outcome.

**Operational and scientific stop gate:** no new cohort data are available and none should be promoted until the latest Python 3.10/3.11/3.12 CI plus Chapter 2 scientific gate pass, the frozen biological/source SHA audit is approved, engineering cost and raw-artifact retention are checked, and the design-only runner PR is reviewed/merged. A manual production launch is a separate step. The historical independent16 sequence test remains FAILED; a new assigned-expression experiment cannot retrospectively change its evidential rank.

The canonical `scripts/model3_island/` tree is **unchanged**. PR #414 is merged with its different, prospectively frozen unexecuted 64-history cohort; no production source for #414 is altered here. Numerical PDE equivalence and a natural island rescue mechanism are not established.
