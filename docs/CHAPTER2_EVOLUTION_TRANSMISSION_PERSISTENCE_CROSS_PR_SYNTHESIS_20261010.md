# Chapter 2: evidence-ranked synthesis across floral evolution, finite-genetic transmission, and persistence

**2026-10-10; cross-PR research synthesis, not a new outcome analysis.**
**Source scope:** merged [#411](https://github.com/zuizui0223/izu-core/pull/411), [#418](https://github.com/zuizui0223/izu-core/pull/418), [#442](https://github.com/zuizui0223/izu-core/pull/442), [#448](https://github.com/zuizui0223/izu-core/pull/448), [#450](https://github.com/zuizui0223/izu-core/pull/450); open [#420](https://github.com/zuizui0223/izu-core/pull/420) and [#451](https://github.com/zuizui0223/izu-core/pull/451). The latter two branches are **not merged**. This document records the evidence at their 2026-10-10 heads and does not itself validate or merge those branches.

## Bottom line: three distinct questions, not one established causal chain

1. **Evolutionary response:** Can low visitor replenishment reduce inherited floral investment without evolution of reproductive-assurance capacity, and how does assurance evolution modify the between-environment contrast? **YES within the frozen four-setting model experiment (#411).**
2. **Genetic transmission:** How do evolved parental genotype/census states and visitor conditions change the *expected next-generation direction* of a matching allele, through viable self versus outcross parental transmission? **An exact conditional accounting exists, with non-universal sign changes across eight post-discovery simulator histories (#420).**
3. **Demographic persistence:** Does finite carrying capacity, at fixed pollen background, modify the response of experimentally imposed A-first versus I-first expression-schedule occupancy to a selfed-viable-seed intervention? **YES, a small model-conditional registered K effect is supported (#442 and #451); the early-versus-late timing difference is inconclusive (#448).**

**No experiment currently identifies a joint causal path from the inherited allele-frequency direction of #420, through the expression-order intervention of #451, to natural persistence.** In particular, high-allele matching direction is not floral-investment reduction, an assigned *phenotypic expression* schedule is not mutation order, and terminal occupancy is not lifetime fitness.

## Evidence ledger (keep original inference units)

| Source | Exact result | Evidence rank / inference unit | Allowed conclusion |
|---|---|---|---|
| #411 four-setting assurance-evolution intervention | Fixed-assurance far-minus-near investment −0.302 to −0.441; assurance-evolving minus fixed interaction +0.101 to +0.220, all four frozen settings passed | Prospectively frozen, 64 independent synthetic visitor histories, 8 demographic repeats **nested per history** | Assurance-capacity evolution is **not necessary** for investment decline under visitor limitation; allowing it compresses between-environment divergence. |
| #411 post-confirmation mechanism | 78.1–90.2% of attenuation algebraically localized to **additional near-side investment decline**; corrected local rare-mutant maternal+paternal returns account for much of selection-gradient asymmetry | Mechanistic post-confirmation diagnostic, *not* dynamic mediation | Divergence can be masked because the more effectively pollinated population loses investment when assurance evolves. |
| #418 assigned order | Near/far A-first/I-first DID −0.0135891; 95% [−0.0228119,−0.0043024] entirely within preregistered ROPE ±0.05 | Prospectively frozen, 64 visitor histories | Practically equivalent near/far DID on declared scale; no strong environment-specific expression-order rescue. CI excluding zero does not negate practical equivalence. |
| #420 original finite genetics | Matching high-allele expected direction negative→positive in 4/8 histories at budget8, 5/8 at budget3; two-order original parent-state contribution **positive 8/8** in each budget, mean +0.030485/+0.028837; visitor-time mean −0.005291/−0.005138 | **Post-discovery exploratory**, 8 simulated visitor RNG histories, 128 demographic trajectories nested within each; K32, zero mutation, 8 generations | The conditional parent-state effect can be positive without a universal late allele-direction reversal. Crossed visitor cells are one-step transplants, not independently evolved populations. |
| #420 self versus outcross ledger | Parent-state matching-high expected direction: viable-self transmission +0.040252/+0.038802 (8/8 positive); outcross father+mother −0.009767/−0.009965 (6/8 negative) at budget8/3 | Exact source transmission decomposition *within the exploratory eight histories* | Self and outcross transmissions make opposing **signed genetic contributions**. This does *not* isolate natural selection for physiological selfing or identify fitness. |
| #420 neutral control, matched original census | Assurance-high terminal mean approx 0.977 vs neutral 0.501 at budget8 in the old source history | Exploratory single original visitor-history contrast, biology deliberately altered in control | A neutral finite-genetic martingale with matched census does not explain the large mean directional assurance change under this source condition. Not proof of a general adaptation mechanism. |
| #420 mean-matched variance holdout | Budget3 held-out source-minus-comparator variance gap changes sign (+0.001219 vs −0.001253) on train/holdout reversal | Exploratory same source visitor history; model-dependent retrospective mean matching | **No robust adaptive variance stabilization/canalization claim.** Strong negative covariance can also arise near allele-frequency boundaries. |
| #442 preregistered fixed-B test | `tau(K8,B48)−tau(K48,B48)=+0.0077457`, paired 64-history bootstrap95 [+0.0024972,+0.0130155]; 43/64 positive clusters | **One independently generated preregistered supported primary**, 64 new visitor histories | In this model, fixed-background smaller K increases the selfed-seed-viability sensitivity of the **assigned expression-schedule occupancy difference** by ~0.775 probability percentage points; not the total occupancy effect of K. |
| #450 unpooled cohort comparison | Same fixed-B48 full-period contrast +0.0134300 (previous K×B cohort), +0.0077457 (registered #442), +0.0085803 (timed cohort) | **One supported primary + two descriptive secondaries**, distinct 64-history cohorts, all from one model family | Directionally concordant synthetic cohorts, **not three confirmations**. Descriptive mean +0.0099187 is not a pooled estimate or a confidence interval. |
| #448 independent timing primary | Late-minus-early K moderator −0.0029649, bootstrap95 [−0.0072632,+0.0013173] | Independently preregistered **inconclusive** primary, 64 histories | Preferential early or late viability mechanism unresolved; nominally different marginal interval labels are not an interaction test. |
| #451 manuscript | Read-only narrative and Figure 1 of the previously frozen capacity results | Draft narrative, **no new inferential analysis** | Separate theoretical demographic companion, not an ecological validation or reason to change the #411 main manuscript. |

Underlying sources: `docs/CHAPTER2_MANUSCRIPT_ECOLOGY_LETTERS_20261006.md`, `docs/CHAPTER2_K_B48_THREE_COHORT_EVIDENCE_COMPARISON_20261010.md`, `docs/CHAPTER2_CAPACITY_PERSISTENCE_COMPANION_MANUSCRIPT_20261010.md` (#451 head), `docs/MODEL3_K32_MULTIHISTORY_STATE_VISITOR_CROSS_20261010.md` and `docs/MODEL3_K32_MULTIHISTORY_CHANNEL_COMPETITION_20261010.md` (#420 head), and their source-locked machine JSONs.

## Why the mechanisms are related but not directly poolable

The results are consistent with an **eco-evolutionary process with separable selection, inheritance and demographic survival bottlenecks**:

```text
Visitor supply / functional pollen environment
    |                              |
    v                              v
Maternal + paternal returns     Selfed viable seed production
    |                              |
    v                              v
Floral investment selection     Reproductive transmission
    |                              |
    +-- (joint genotype state, stochastic drift) --+
                                                    |
                                          Finite recruitment, K, extinction
```

This diagram is a **candidate mechanism**, not an estimated directed acyclic graph. Neither the #420 conditional one-generation self-transmission component nor the #451 assigned expression-schedule survival sensitivity establishes the dotted or implicit causal connections across rows. Visitors, viable selfed seed output, and genetic-state feedback are correlated because each is generated within the same model.

- **Different traits:** #420 matching-high allele expectation is not the #411 inherited **investment** phenotype. #420 also measures assurance allele frequency in a separate exploratory control. Collapsing them into a single selfing-syndrome score would be incorrect.
- **Different temporal and genetic conditions:** #420 K32, prior-selfing, zero mutation, eight updates, a selected late-survivor cohort; #411 mutation-enabled 1,000-update evolutionary comparisons with 48 founders; #451 inherited t400 sources, up-to-eight founders, imposed phenotype-expression schedules, K8 versus K48 at fixed B48 and 80 follow-up updates.
- **Different estimands:** #420 source `D(C,V)=q_high(C,V)−p_high(C)` and its signed one-step self/father/mother components; #451 `tau(K,B)=D_occupied(K,B,baseline)−D_occupied(K,B,half_selfed)`, where `D_occupied=P(occupied|A-first)−P(occupied|I-first)`. Sharing the symbol D across analyses does not make their effects numerically comparable.
- **Different independent units:** eight post-outcome original-generator visitor histories versus 64 new independent histories in the registered capacity experiment. Demographic trajectories and future branches are nested; no combined effective N or pooled P value is valid.
- **Different interventions and limits:** #420 source-state cross changes a parent-state/visitor snapshot in one-step reproductive expectation, without autonomous counterfactual evolution; #451 changes experimentally assigned transient expression schedule or viable selfed-seed retention. Neither is an intervention on spontaneous mutation order or an actual island environment.
- **Outcomes after extinction:** genetic trait values are undefined for extinct populations; occupancy must retain extinct histories. Do not re-code extinct traits to zero or condition population viability on a post-treatment survivor stratum.

## Strongest unified insight and competing interpretations

**Established, separately:** low visitor replenishment can lower floral investment *without assurance evolution* (#411), while an independently preregistered controlled viable-selfed-seed manipulation detects a small capacity-dependent assigned-history occupancy interaction (#442/#451).

**Exploratory mechanism, not established bridge:** parental genetic-state changes can promote matching-high expected gene transmission through the successful selfing ledger even while source outcross contributions oppose it (#420). Therefore a *trait's positive expected transmission component* cannot be equated with a universally favorable pollinator environment or enhanced population persistence.

**Most informative new joint question:** **Under exactly the same evolving genotype histories, does a reproductive channel that favors an allele's transmission also improve the causal probability of lineage persistence, and how does its answer change with capacity independently of pollen dilution?** An incompatibility is biologically possible, but these PRs **have not observed or proven this discordance**. The literature-facing claim should remain one of experimentally separable processes, not evolutionary rescue or a real-island maladaptation result.

Competing explanations for apparent cross-layer patterns include genotype correlations and composition, survivor conditioning, environmental-history stochasticity, near-fixation frequency ceilings, founder effects, and the original K-dependent pollen normalizer. Existing negative controls specifically rule out *some* simple accounts; they do not eliminate all of these alternatives.

## One bounded follow-up that could genuinely connect the levels (not yet executed)

**Pre-register a joint state × viability × K/B experiment** before generating a fresh outcome cohort. This is a design proposal, not a completed experiment.

1. Choose **one frozen biological source setting** first (e.g., prior selfing), an explicit mutation/survival/immigration regime, matching founder genotype/census and *the same* independently generated prospective visitor histories. Preserve fully diploid joint genotype support and a named time horizon. Do not mix #420 old histories with #442/#448 confirmation histories.
2. Hold pollen-recipient background **B** fixed while independently randomizing demographic capacity **K**. Within the same source state and visitor history randomize postzygotic selfed-seed viability. Retain an explicit viable-outcross-seed control. Verify that the manipulation leaves the intended pre-gate pollen and source reproduction ledgers unchanged.
3. Record at each generation (a) source-expected inherited gene directions at **all three loci** and their exact self/father/mother ledger, (b) *realized* genetic change among extant paths with extinction separately identified, (c) birth/census/seed-route transitions, and (d) 80-update **unconditional occupancy**. Do not treat selected surviving paths as the persistence denominator.
4. Set two distinct registered estimands: **genetic-direction intervention contrast** (within-parent/visitor-state expected allele-direction difference under a randomized route viability gate) and **occupancy intervention contrast** (difference in absolute survival probability under that gate at fixed K and B), plus the K interaction. Report both even if signs oppose; do not label a correlation across trajectories a mediated effect. Require matched histories, whole-visitor-history bootstrap and predeclared meaningful-effect thresholds.
5. Test competing mechanisms with neutral matched-census inheritance, independent-pollen-background intervention, and genotype/parent-state replacement controls while tracking where comparator biology differs. Diagnose horizon sensitivity and underpowered model scenarios before using the results to claim an evolutionary–demographic link.

**Interpretation if verified:** agreement in genetic and occupancy signs would support a particular model-conditional coupling; disagreement would be an explicit *within-model* transmission–persistence mismatch, not yet a general evolutionary paradox in island plants. Either outcome is publishable only with appropriately limited ecological transport claims.

## Publication and repository decisions

- **Keep #411 separate as the main Ecology Letters letter**: an independently frozen four-setting intervention establishes non-necessity of assurance evolution and masking/compression of divergent floral investment. Its original four-arm occupancy equals one, so persistence is not its inferred mechanism.
- **Keep #451 a separate, bounded demographic companion**: the single registered fixed-B48 K finding is its main positive; preserve #418 practical equivalence, previous inconclusives and #448 timing inconclusive. The three cohorts are not a pooled meta-analysis.
- **Keep #420 exploratory and Draft** as a stochastic genetic operator / inference-limit mechanism laboratory. The exact algebra, finite-state failure of continuum approximations, counterfactual failures and non-universal direction reversal can contribute to methods or a standalone mechanistic paper, but should not be written as external ecological confirmation.
- **No merge, model-code modification, biological simulation or retroactive preregistration** is performed by this synthesis. A future joint test must first freeze its own estimand and controls.
- **Reproducibility:** #451 still needs DOI-backed independent external raw deposit (Issue #436). #420's direct CI source receipts do not constitute a field-data fit.

**One-sentence shared program (hypothesis, not yet a combined result):**
> Ecological pollination limitation, inheritance through selfed and outcrossed offspring, and demographic persistence are mechanistically linked but can respond on different scales; testing when allele-transmission advantage becomes population-level survival benefit requires a common randomized, source-matched experiment.

## Upgraded unifying hypothesis (added 2026-10-10; planned, not a result)

**This is the main research question above, not subordinate to, the time20 state transplant:**

> Predict in advance the boundary between individual-level reproductive selection and population-level persistence agreement or discordance using maternal-outcross (F), paternal-outcross (P) and viable-self (S) genetic contributions; falsify those predictions by source-matched finite-population evolutionary trajectories.

The defined measurements are the rare-mutant local invasion gradient `beta`, the entire-population viable-reproduction response `Gamma_seed`, and the controlled **unconditional** finite-horizon survival response `Gamma_persist`. `beta` is not a surrogate for either `Gamma`. Cross signs classify alignment/mismatch only when all relevant estimates exclude prespecified near-zero regions; candidate evolutionary suicide additionally requires lower survival under **evolution enabled versus a properly matched trait-evolution freeze**, not merely a static survival gradient or a post-treatment genetic correlation.

- **Full design, F/P/S predictions, falsifiers, numerical and biological limits:** `docs/CHAPTER2_INDIVIDUAL_SELECTION_POPULATION_PERSISTENCE_DISCORDANCE_PROTOCOL_20261010.md`.
- **Machine-readable, explicitly NOT-registered design state and incomplete future gates:** `data/design/chapter2_beta_gamma_discordance_proposed_20261010.json`.
- **t20 transplant is a mechanistic subtest** of the larger problem, not a substitute for a beta × Gamma map. Equal 21/24 marginal survivors under K8/K48 do *not* remove post-survival selection bias; genotype source, recipient census N and capacity K require independent control. A stochastic genotype redraw clamp is not a drift-free control. Balanced two-order/Shapley factor contrasts must not double-count their interaction.
- **Model limitation:** with fixed depression and zero new mutation, this experiment cannot address mutation-load accumulation, purging or mutation-driven mutational meltdown in real islands. Any genetic effect is confined to the three inherited modeled trait axes and their segregation/finite sampling.

No new independent visitor histories have been generated for the proposed primary question, and no outcomes are promoted retroactively to confirm the prediction.

## Source-executed next layer: finite beta versus Gamma_seed (2026-10-10)

The larger proposed beta × Gamma_persist question is still **NOT TESTED**, but the first complete, pre-execution-declared **synthetic engineering** layer has now been run on the identical original finite Model3 reproductive ledger: `scripts/audit_chapter2_beta_gamma_seed_map.py`, source-locked results in `data/results/chapter2_beta_gamma_seed_engineering_receipt_20261010.json`, full [executed original JSON artifact #11654822692](https://github.com/zuizui0223/izu-core/actions/runs/38013728388/artifacts/11654822692), details in `docs/CHAPTER2_BETA_GAMMA_SEED_ENGINEERING_RESULTS_20261010.md`.

The 384-case fixed synthetic survey yields **362 aligned local signs, 14 beta-negative/Gamma_seed-positive discordances, 0 beta-positive/Gamma_seed-negative discordances, and 8 inconclusives**. Every resolved discordance is for **floral investment**, not the reproductive-assurance trait. One representative finite K8/B48 delayed-selfing case has beta_N = −0.063174 versus group viable seed Gamma_seed = +0.158229; exact additive maternal F/paternal P/self S components of beta are +0.134346/+0.156951/−0.354470. Thus positive maternal+paternal components can be outweighed by loss in viable-self returns to investment; the aggregate seed-production response can still be positive. Father/recipient mass conservation holds, but pollen competition is not assumed zero-sum when total outcross output changes.

These numbers are **model-conditional fixed-population one-individual derivatives** (one mutant equals 1/8 of K8 parents), **not** genuine infinite-population rare-mutant beta, multi-generation genetic change, group persistence Gamma_persist, or evolutionary suicide. The sign quadrant and next-stage decision must preserve the explicit **zero** positive-beta/negative-gamma cases and the eight unresolved cases. In particular, do not infer `Gamma_persist` from `Gamma_seed` in capacity-saturated regimes, and do not upgrade this source-grid exploration to independent ecological confirmation.
