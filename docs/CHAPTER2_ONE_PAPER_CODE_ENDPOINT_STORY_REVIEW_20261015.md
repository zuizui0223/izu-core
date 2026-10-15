# Chapter 2 — Single-paper code and endpoint review (2026-10-15)

**Decision: ONE unified manuscript.** Q1–Q4 are distinct pieces of a single ecological-evolutionary argument, not four manuscripts, not separate companion papers, and not a proven continuous natural causal mediation path. This source-code and frozen-readout review produces no new independent ecological histories or scientific endpoints.

## Single scientific question

**When do changes in pollination-dependent reproductive returns become inherited floral evolution, and what are the conditional consequences for population persistence?**

In one genetically explicit plant–pollinator model, altered visitor replenishment reduces the maternal/paternal return to floral investment I; this can produce inherited I decline without evolution of reproductive assurance A. Allowing A evolution then compresses environmental investment divergence, rather than necessarily amplifying it. A response favourable under conditional reproductive weighting may still be blocked by finite transmission of the alleles needed for a prespecified future response. Population survival is a further distinct outcome sensitive to historical treatment, seed viability and demographic carrying capacity.

The one-paper center is **Q1 (strongest prospective evolutionary intervention) + Q3 (specific genetic realization filter)**; Q2 explains why apparent temporal order does not prove necessity, and **Q4 MUST REMAIN in Results as the distinct demographic endpoint**, with both supported conditional trials but no claimed Q1→Q4 natural mediation.

## Evidence-ranked endpoint map for the ONE paper

| Section | Existing estimand and origin | Source-confirmed result | Inferential ceiling |
|---|---|---|---|
| **Q1 — selection and evolutionary investment** | Original frozen 64 independent visitor histories × 8 nested demographic repeats × 4 reproductive rules × 2 replenishment arms × fixed/evolvable A: 8,192 evolutionary paths plus 256 zero-mutation controls; mean I at update1000 | With A evolution frozen, far−near I **−0.3018 to −0.4413**. Permitting A to evolve narrows far−near I difference **+0.1007 to +0.2200** across four mating rules, all registered 95% visitor-history bootstrap intervals exclude zero appropriately; occupancy=1 in every original arm; 128/128 matched zero-mutation traces pass | In fixed A selfing STILL occurs at constant A=0.5. Near remains pollen-limited, not mainland or pollen-saturated. Near accounts for 78–90% of arithmetic interaction, not 78–90% causal mediation. No observed extinction in this cohort |
| **Q2 — order, conditional rather than compulsory** | Independent 64-history sequence confirmation, +0.05 change sustained 20 censuses, founder relative; separate fixed-access ecological order grid | A-first **51/64** delayed costly histories, **30/64** prior selfing; fixed-access ecology test 18 simultaneous intervals all included 0, no identified replicated ecological reversal | Sequence changes with mating rule, trait genetic access and event threshold; being first does not establish that A caused I decline or that naturally A-first improves survival |
| **Q3 — genetic realization** | Separate original 2,304 finite no-I-mutation/no-immigration histories; defined *future new* I decrease by 0.05; subset of 1,238 selected first exclusion transitions | **703** histories lose specified future I response access before I fixation (535 at fixation). Of **1,238 observed first-loss transitions**, conditional expected needed-low-I allele frequency increases in **315** but next offspring contain no copies (923 conditional expected decline); other I variation may still segregate. Different 128-history density/ABM bridge gives −0.4510 vs −0.1446 inherited contrast, with separate source-matched A-first density/finite comparison achieving only 3/32 and 2/32 actual A-first histories | The 315 are retrospectively conditioned on observed loss, NOT 315/2304 independent probability; no isolated drift coefficient or universal no-mutation-free inaccessibility. Density is not a mathematical stochastic ABM ensemble mean; different cohorts cannot be declared a causal Q1 mediator |
| **Q4A — historical treatment × stressed persistence** | Frozen 32 *new* visitor histories (stress range pilot-informed), 400 updates prehistory plus 80 future; N reduced to 8, ovule budgets2–5 crossed with two future visitor conditions; original 4,096 futures nested within 32 histories | Original preregistered pooled evolving-A-mode × past near/far replenishment integrated terminal occupancy interaction **+0.108398** (95% history CI **[+0.065430,+0.151367]**); all eight biological replay shards revalidated, one demographic replicate per visitor history | **Code finding:** evolving/fixed A MODE remains active throughout both the 400-update prehistory and 80-update future; cannot call +10.84 percentage points the isolated legacy effect of earlier A allele evolution. Postshock K, ovule budget and pollen receipt all change. Prior-selfing setting individual interval includes 0 |
| **Q4B — fixed pollen-background demographic moderation** | Separate preregistered 64-new-history K8 versus K48 experiment, background pollen denominator fixed B=48, assigned A-first vs I-first phenotype-expression schedules and baseline/halved selfed viable seeds | **+0.0077457** occupancy-probability-unit interaction (95% **[+0.0024972,+0.0130155]**), approx +0.775 percentage points. Two other independent cohort estimates same-direction but post-outcome descriptive | Distinct from Q4A; expression schedule is *imposed*, NOT spontaneous genetically evolved order, and the natural near/far assigned-order effect was practically equivalent. Timing-specific primary inconclusive. Do not pool Q4A/Q4B or infer real-island extinction rescue |

### Q1–Q3 concrete source/genetic bridge

The native reproduction kernel uses female outcross, male outcross and viable selfing. Under a fixed-population, no-new-mutation, no-adult-survival, no-immigration, conditionally occupied one-generation assay, the exact parent genetic contribution is:

- W_i = 0.5 F_i + 0.5 P_i + S_i.
- Expected mean I of offspring minus current adult mean I = Cov_N(I_i, W_i) / mean_N(W_i).

This is an exact **one-generation full-parent Price accounting identity**, not proof that static rare-mutant selection gradients determine 1,000-update evolutionary effects. The original evolved genome checkpoint audit from the *first of eight* historical demographic repeats finds far E−F I positive already at t200 yet far E−F expected one-step Price change negative at t400 in all four rules. This restricts simple static-selection explanations; not a unique genetic correlation mechanism.

## Source-code review: major model and inference assumptions

1. **scripts/model3_island/reproduction.py**: donor/recipient pollen transfer, matching, attraction investment, ovule resource cost, pollen discount, delayed/prior selfing and inbreeding depression are explicit; visitor arrival is imposed **exogenously**. A decline in I does not generate pollinator extinction in this model.
2. **scripts/model3_island/population.py**: parent lottery respects father-row/mother-column outcross and selfed diagonal, Mendelian diploid inheritance, allele mutation masks and K-limited recruitment. **Baseline adult survival=0, immigrant seed supply=0** in the frozen original Model3 config; no perennial plant dynamics or immigrant rescue can be inferred.
3. **scripts/run_chapter2_assurance_generality.py**: A fixed means A *capacity evolution* disabled, not selfing disabled. Both A modes begin with two A alleles=0.5. Matching X and investment I mutate/inherit in both modes. Q1 inference uses independent visitor-history clusters; repeats, years and plants are NOT independent archipelagos.
4. **scripts/model3_island/reproduction.py** uses K also in the recipient pollen background denominator. Changes to K therefore modify both density regulation and pollination unless B is separately fixed as in **scripts/chapter2_kb_reproduction.py**. Do not call ordinary K contrast a pure demographic manipulation.
5. **scripts/run_chapter2_island_demographic_independent32.py** constructs postshock config by changing K and ovule_budget only, keeping A mode and positive A mutation unchanged during future80. The protocol contains both pre_mutation_rate and post_mutation_rate but the runner uses pre rate for future as well; both original numbers are .01, so this is a **latent future-design configuration bug**, not a demonstrated error in archived original outcomes. Version source and add an explicit pre/post guard before any different-rate future experiment, without rewriting the original source.
6. **docs/CHAPTER2_HIGH_REPLENISHMENT_POLLEN_LIMITATION_FEASIBILITY_20261010.md**: in original fixed-state model snapshot400, near outcross ovule fertilization is ~0.2197 and far ~0.0103; exploratory pollen budget ×16 still failed the declared near saturation gate. near/far are **both pollen limited** and are not equivalent to measured mainland/island distance.
7. **docs/CHAPTER2_EVOLVED_GENOME_POLLEN_SERVICE_GATE_20261010.md**: in authentic t400 evolved genomes, higher individual I frequently boosts other mothers' viable seed returns, but lower aggregate pollen can coincide with higher total viable maternal offspring because of resource allocation and heterogeneity. This source-only one-repeat result does NOT prove public-goods extinction or pollinator collapse.

No direct parent-index/sign bug was established by inspecting these source operators. Identified issues are primarily **causal scope**, **K/pollen confounding**, **Q4 continued evolvability**, and **latent post-rate configuration usage**. Source inspection is not an independently performed full-year replay of all campaigns.

## One-paper figure sequence and discussion

**Fig. 1 (Q1):** donor/recipient reproductive-return components at fixed resident plants, distinguish female, male, viable selfing and investment allocation.

**Fig. 2 (Q1 primary):** four registered fixed-versus-evolving A by near/far terminal I contrasts, cluster bootstrap CIs, one arm decomposition subplot. Strongest figure and predeclared evolutionary result.

**Fig. 3 (Q2+Q3):** conditional order counts as inset; visually contrast expected maternal/paternal/self parent weighting with finite actual required allele transmission and fixation-before-loss timing. Density/ABM discrepancy can be secondary/SI; no pooled test of cross-source mechanisms.

**Fig. 4 (Q4):** A) independent 32-history pre/post mode-by-history occupancy contrast with full 4-setting results; B) separate fixed-B48 64-history demographic capacity moderator. Exact cohorts/estimands labelled; no combined occupancy headline.

**Results subsections:** (1) Q1 source returns and independently confirmed A evolution interaction; (2) Q2 nonnecessary and conditional chronology; (3) Q3 genomic support and realized transmission; (4) Q4 controlled conditional occupancy endpoints. **All belong to ONE active Ecology Letters-format manuscript**, with negative/inconclusive variants and all unpooled samples disclosed in SI.

**Single discussion conclusion:** A pollination regime can change the return to floral attraction and thereby alter inherited investment even when reproductive assurance capacity cannot evolve. Insurance evolution changes the **magnitude of between-regime investment difference** without being the necessary precursor. Genetic access and finite offspring transmission further filter the response; distinct demographic experiments show that the resulting/prepared reproductive states have conditional occupancy consequences. The study separates selected directions, genetically possible changes, realized finite evolution, and persistence rather than claiming a single observed natural mediation chain.

### Which story not to write

- “Reproductive assurance always precedes and causes floral reduction.”
- “Assurance is absent when A is held fixed.”
- “All near regimes are pollen-saturated mainland controls, all far regimes are real islands.”
- “A evolution destroys pollination networks and causes population extinction.”
- “703/2304 or 315/1238 represents a natural island allele-loss rate or a direct mediator of Q1.”
- “Q4 +10.84pp proves prior A *alleles alone* rescued population persistence.”
- “Three independent K cohorts were three equivalent confirmatory primaries.”
- “A naturally evolved A-first sequence has a demonstrated occupancy benefit.”

## Provenance and action boundary

Q1 original: data/design/chapter2_assurance_generality_20261006.json; data/results/chapter2_assurance_generality_20261006.json; data/results/chapter2_assurance_attenuation_decomposition_20261006.json.

Q2: data/results/chapter2_1005_confirmatory_replication_20261006.json; docs/CHAPTER2_ECOLOGICAL_ORDER_BOUNDARY_RESULTS_20261013.md.

Q3: data/results/directional_access_20261013/READOUT.json; data/results/low_allele_loss_20261014/extracted/READOUT.json; data/results/model3_ch2_bridge_prospective_frozen_20260927.json; scripts/audit_chapter2_q1q3_genetic_price_identity_20261011.py.

Q4: data/results/chapter2_island_demographic_independent32_20261008.json; data/results/chapter2_island_demographic_independent32_replay_receipt_20261013.json; results/chapter2/k_fixedB48_independent_primary_20261009.json; docs/CHAPTER2_K_B48_THREE_COHORT_EVIDENCE_COMPARISON_20261010.md.

**Scientific/authoring boundary:** This document reviews already existing source and outcomes. No new source model run, no frozen primary reclassification, no manuscript submitted, no DOI deposited. Submission claims require exact-head figure, word-count and raw-data/source-provenance checks.
